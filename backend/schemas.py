from datetime import date
from pydantic import BaseModel, Field
from typing import Optional


# ---------------- CREATE (REQUEST BODY) ----------------
class InventoryCreate(BaseModel):
    sku: str = Field(..., example="ZEP001")
    name: str = Field(..., example="Milk")
    category: str = Field(..., example="Dairy")
    quantity: int = Field(..., ge=0)
    price: float = Field(..., ge=0.0)
    reorder_level: int = Field(..., ge=0)
    supplier: Optional[str] = None
    last_restock: Optional[date] = None


# ---------------- UPDATE (PATCH BODY) ----------------
class InventoryUpdate(BaseModel):
    sku: Optional[str] = None
    name: Optional[str] = None
    category: Optional[str] = None
    quantity: Optional[int] = None
    price: Optional[float] = None
    reorder_level: Optional[int] = None
    supplier: Optional[str] = None
    last_restock: Optional[date] = None


# ---------------- RESPONSE MODEL ----------------
class InventoryItem(InventoryCreate):
    id: int

    class Config:
        from_attributes = True   # ✅ FIX for Pydantic v2


# ---------------- STATS ----------------
class InventoryStats(BaseModel):
    total_products: int
    total_quantity: int
    inventory_value: float
    low_stock_count: int
    out_of_stock_count: int
    categories: int


# ---------------- CATEGORY ----------------
class CategoryDistribution(BaseModel):
    category: str
    count: int
    share: float
    value: float