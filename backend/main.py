from datetime import date
from typing import Dict, List, Optional
import os
import logging

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field


class InventoryItem(BaseModel):
    id: int
    sku: str = Field(..., example="ZEP001")
    name: str = Field(..., example="Milk")
    category: str = Field(..., example="Dairy")
    quantity: int = Field(..., ge=0)
    price: float = Field(..., ge=0.0)
    reorder_level: int = Field(..., ge=0)
    supplier: str = Field(..., example="Zepto Foods")
    last_restock: date


class InventoryStats(BaseModel):
    total_products: int
    total_quantity: int
    inventory_value: float
    low_stock_count: int
    out_of_stock_count: int
    categories: int


class CategoryDistribution(BaseModel):
    category: str
    count: int
    share: float
    value: float


DEFAULT_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# Allow overriding allowed origins via environment variable for debugging or CI.
# Comma-separated list, e.g. ALLOW_ORIGINS="http://localhost:5173,http://127.0.0.1:5173"
env_origins = os.environ.get("ALLOW_ORIGINS")
if env_origins:
    origins = [o.strip() for o in env_origins.split(",") if o.strip()]
else:
    origins = DEFAULT_ORIGINS

# If running with DEV_ALLOW_ALL_CORS=true then allow all origins (development only)
if os.environ.get("DEV_ALLOW_ALL_CORS", "true").lower() in ("1", "true", "yes"):
    origins = ["*"]

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("zepto-backend")

app = FastAPI(
    title="Xepto Inventory Analysis",
    description="Production-ready inventory analytics API for a Zepto-inspired dashboard.",
    version="1.0.0",
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info("Incoming request %s %s", request.method, request.url.path)
    try:
        response = await call_next(request)
        logger.info("Completed %s %s -> %s", request.method, request.url.path, response.status_code)
        return response
    except Exception as exc:
        logger.exception("Unhandled exception while handling request %s %s", request.method, request.url.path)
        return JSONResponse(status_code=500, content={"detail": "Internal server error"})

# When allow_origins contains '*' do not allow credentials (browsers reject '*' with credentials)
allow_credentials = False if origins == ["*"] else True

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)


SUPPLIERS = [
    "Zepto Fresh",
    "Green Valley",
    "Bright Harvest",
    "Daily Essentials",
    "Pure Pantry",
    "Household Hub",
    "Fresh & Frozen",
    "Snack Street",
    "Sip Source",
    "Care Plus",
]

CATEGORY_ITEMS = {
    "Fruits": [
        "Green Apple",
        "Banana Bunch",
        "Mandarin Orange",
        "Seedless Grapes",
        "Blueberry Pack",
    ],
    "Vegetables": [
        "Baby Carrots",
        "Organic Spinach",
        "Cherry Tomatoes",
        "Broccoli Florets",
        "Cucumber Mix",
    ],
    "Dairy": [
        "Whole Milk",
        "Greek Yogurt",
        "Cheddar Cheese",
        "Butter Block",
        "Cottage Cheese",
    ],
    "Bakery": [
        "Sourdough Loaf",
        "Seeded Bagels",
        "Croissant Pack",
        "Muffin Bundle",
        "Burger Buns",
    ],
    "Snacks": [
        "Potato Chips",
        "Trail Mix",
        "Granola Bars",
        "Roasted Nuts",
        "Fruit Snacks",
    ],
    "Beverages": [
        "Sparkling Water",
        "Cold Brew",
        "Orange Juice",
        "Herbal Tea",
        "Energy Drink",
    ],
    "Personal Care": [
        "Hand Soap",
        "Shampoo",
        "Toothpaste",
        "Moisturizer",
        "Lip Balm",
    ],
    "Household": [
        "Laundry Detergent",
        "Dishwasher Tabs",
        "Paper Towels",
        "Floor Cleaner",
        "Garbage Bags",
    ],
    "Frozen Foods": [
        "Veggie Patties",
        "Frozen Pizza",
        "Ice Cream Tub",
        "Fish Fillets",
        "Frozen Berries",
    ],
    "Pantry": [
        "Olive Oil",
        "Rice Bag",
        "Pasta Pack",
        "Tomato Sauce",
        "Salt & Pepper",
    ],
}

PRICE_RANGES = {
    "Fruits": (18, 45),
    "Vegetables": (12, 40),
    "Dairy": (20, 120),
    "Bakery": (15, 70),
    "Snacks": (10, 55),
    "Beverages": (15, 90),
    "Personal Care": (45, 160),
    "Household": (60, 220),
    "Frozen Foods": (48, 180),
    "Pantry": (30, 140),
}


def generate_inventory() -> List[InventoryItem]:
    inventory: List[InventoryItem] = []
    item_id = 1

    for category, names in CATEGORY_ITEMS.items():
        low, high = PRICE_RANGES[category]

        for name in names:
            price = round(low + (high - low) * ((item_id % 5) / 5) + (item_id % 4) * 0.95, 2)
            quantity = ((item_id * 7) % 78) + 5
            reorder_level = 8 + (item_id % 4) * 3
            supplier = SUPPLIERS[(item_id - 1) % len(SUPPLIERS)]
            sku = f"ZEP{item_id:03d}"

            inventory.append(
                InventoryItem(
                    id=item_id,
                    sku=sku,
                    name=name,
                    category=category,
                    quantity=quantity,
                    price=price,
                    reorder_level=reorder_level,
                    supplier=supplier,
                    last_restock=date(2026, 6, (item_id % 28) + 1),
                )
            )
            item_id += 1

    return inventory


inventory_data = generate_inventory()


def build_stats(items: List[InventoryItem]) -> InventoryStats:
    total_products = len(items)
    total_quantity = sum(item.quantity for item in items)
    inventory_value = round(sum(item.quantity * item.price for item in items), 2)
    low_stock_count = sum(1 for item in items if 0 < item.quantity <= item.reorder_level)
    out_of_stock_count = sum(1 for item in items if item.quantity == 0)
    categories = len({item.category for item in items})

    return InventoryStats(
        total_products=total_products,
        total_quantity=total_quantity,
        inventory_value=inventory_value,
        low_stock_count=low_stock_count,
        out_of_stock_count=out_of_stock_count,
        categories=categories,
    )


def build_category_distribution(items: List[InventoryItem]) -> List[CategoryDistribution]:
    counts: Dict[str, int] = {}
    values: Dict[str, float] = {}

    for item in items:
        counts[item.category] = counts.get(item.category, 0) + 1
        values[item.category] = round(values.get(item.category, 0.0) + item.quantity * item.price, 2)

    return [
        CategoryDistribution(
            category=category,
            count=count,
            share=round((count / len(items)) * 100, 1),
            value=values[category],
        )
        for category, count in sorted(counts.items(), key=lambda pair: pair[1], reverse=True)
    ]


@app.get("/inventory", response_model=List[InventoryItem])
async def get_inventory(
    search: Optional[str] = Query(None, description="Filter inventory by SKU, name, or category"),
    category: Optional[str] = Query(None, description="Filter inventory by category"),
):
    print("Inventory endpoint called", {"search": search, "category": category})
    results = inventory_data

    if search:
        query = search.strip().lower()
        results = [
            item
            for item in results
            if query in item.sku.lower()
            or query in item.name.lower()
            or query in item.category.lower()
        ]

    if category and category.lower() != "all":
        results = [item for item in results if item.category.lower() == category.lower()]

    return results


@app.get("/inventory/stats", response_model=InventoryStats)
async def get_inventory_stats():
    print("Inventory stats endpoint called")
    return build_stats(inventory_data)


@app.get("/inventory/categories", response_model=List[CategoryDistribution])
async def get_inventory_categories():
    print("Inventory categories endpoint called")
    return build_category_distribution(inventory_data)


@app.get("/inventory/low-stock", response_model=List[InventoryItem])
async def get_inventory_low_stock():
    print("Inventory low-stock endpoint called")
    return [item for item in inventory_data if 0 < item.quantity <= item.reorder_level]


@app.post("/inventory", response_model=InventoryItem, status_code=201)
async def create_inventory_item(item: InventoryItem):
    print("Create inventory item called", item.dict())
    if any(existing.sku == item.sku for existing in inventory_data):
        raise HTTPException(status_code=400, detail="Item SKU already exists")

    item.id = max((existing.id for existing in inventory_data), default=0) + 1
    inventory_data.append(item)
    return item


@app.put("/inventory/{item_id}", response_model=InventoryItem)
async def update_inventory_item(item_id: int, patch: InventoryItem):
    print("Update inventory item called", {"item_id": item_id})
    for index, existing in enumerate(inventory_data):
        if existing.id == item_id:
            inventory_data[index] = patch
            return patch

    raise HTTPException(status_code=404, detail="Item not found")
