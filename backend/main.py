from typing import List, Optional
import os
import logging

from fastapi import FastAPI, HTTPException, Query, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session
from sqlalchemy import func

from mangum import Mangum  # ✅ REQUIRED FOR VERCEL

from . import models, schemas, seed_data
from .database import engine, Base, get_db, SessionLocal


# ---------------- LOGGING ----------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("zepto-api")


# ---------------- FASTAPI APP ----------------
app = FastAPI(title="Zepto Inventory API (Vercel)", version="1.0.0")


# ---------------- CORS (IMPORTANT FOR FRONTEND) ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to your Vercel frontend domain in production
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------- HEALTH CHECK (VERY IMPORTANT FOR VERCEL) ----------------
@app.get("/")
def root():
    return {"status": "ok", "message": "Zepto API running on Vercel"}


# ---------------- DB INIT (SAFE FOR SERVERLESS) ----------------
def init_db():
    Base.metadata.create_all(bind=engine)


# run once per cold start
init_db()


# ---------------- DB SESSION DEPENDENCY ----------------
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- HELPERS ----------------
def build_stats(db: Session):
    return schemas.InventoryStats(
        total_products=db.query(func.count(models.Inventory.id)).scalar() or 0,
        total_quantity=db.query(func.sum(models.Inventory.quantity)).scalar() or 0,
        inventory_value=db.query(
            func.sum(models.Inventory.quantity * models.Inventory.price)
        ).scalar()
        or 0.0,
        low_stock_count=db.query(models.Inventory)
        .filter(models.Inventory.quantity > 0)
        .filter(models.Inventory.quantity <= models.Inventory.reorder_level)
        .count(),
        out_of_stock_count=db.query(models.Inventory)
        .filter(models.Inventory.quantity == 0)
        .count(),
        categories=db.query(func.count(func.distinct(models.Inventory.category))).scalar() or 0,
    )


# ---------------- ROUTES ----------------

@app.get("/inventory", response_model=List[schemas.InventoryItem])
def get_inventory(
    search: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db_session),
):
    query = db.query(models.Inventory)

    if search:
        s = f"%{search}%"
        query = query.filter(
            models.Inventory.sku.ilike(s)
            | models.Inventory.name.ilike(s)
            | models.Inventory.category.ilike(s)
        )

    if category and category.lower() != "all":
        query = query.filter(models.Inventory.category == category)

    return query.all()


@app.post("/inventory", response_model=schemas.InventoryItem)
def create_item(
    item: schemas.InventoryCreate,
    db: Session = Depends(get_db_session),
):
    existing = db.query(models.Inventory).filter(
        models.Inventory.sku == item.sku
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="SKU already exists")

    db_item = models.Inventory(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.put("/inventory/{item_id}", response_model=schemas.InventoryItem)
def update_item(
    item_id: int,
    patch: schemas.InventoryUpdate,
    db: Session = Depends(get_db_session),
):
    db_item = db.query(models.Inventory).filter(
        models.Inventory.id == item_id
    ).first()

    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    for k, v in patch.dict(exclude_unset=True).items():
        setattr(db_item, k, v)

    db.commit()
    db.refresh(db_item)
    return db_item


@app.get("/inventory/stats", response_model=schemas.InventoryStats)
def stats(db: Session = Depends(get_db_session)):
    return build_stats(db)


@app.get("/inventory/categories", response_model=list[schemas.CategoryDistribution])
def categories(db: Session = Depends(get_db_session)):
    rows = db.query(
        models.Inventory.category,
        func.count(models.Inventory.id),
        func.sum(models.Inventory.quantity * models.Inventory.price),
    ).group_by(models.Inventory.category).all()

    total = db.query(func.count(models.Inventory.id)).scalar() or 1

    return [
        schemas.CategoryDistribution(
            category=c,
            count=count,
            share=round((count / total) * 100, 1),
            value=float(value or 0),
        )
        for c, count, value in rows
    ]


@app.get("/inventory/low-stock", response_model=List[schemas.InventoryItem])
def low_stock(db: Session = Depends(get_db_session)):
    return db.query(models.Inventory).filter(
        models.Inventory.quantity > 0,
        models.Inventory.quantity <= models.Inventory.reorder_level
    ).all()


# ---------------- VERCEL HANDLER (CRITICAL) ----------------
handler = Mangum(app)