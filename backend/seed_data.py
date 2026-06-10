from datetime import date
from sqlalchemy.orm import Session
from . import models

# Seed constants copied from previous implementation
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


def seed_db(db: Session):
    """Seed the inventory table if it's empty."""
    count = db.query(models.Inventory).count()
    if count > 0:
        return

    item_id = 1
    for category, names in CATEGORY_ITEMS.items():
        low, high = PRICE_RANGES[category]

        for name in names:
            price = round(low + (high - low) * ((item_id % 5) / 5) + (item_id % 4) * 0.95, 2)
            quantity = ((item_id * 7) % 78) + 5
            reorder_level = 8 + (item_id % 4) * 3
            supplier = SUPPLIERS[(item_id - 1) % len(SUPPLIERS)]
            sku = f"ZEP{item_id:03d}"

            db_item = models.Inventory(
                sku=sku,
                name=name,
                category=category,
                quantity=quantity,
                price=price,
                reorder_level=reorder_level,
                supplier=supplier,
                last_restock=date(2026, 6, (item_id % 28) + 1),
            )

            db.add(db_item)
            item_id += 1

    db.commit()
