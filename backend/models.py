from sqlalchemy import Column, Integer, String, Float, Date
from .database import Base


class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    category = Column(String, index=True, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    price = Column(Float, nullable=False, default=0.0)
    reorder_level = Column(Integer, nullable=False, default=0)
    supplier = Column(String, nullable=True)
    last_restock = Column(Date, nullable=True)
