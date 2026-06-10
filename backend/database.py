import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


BASE_DIR = os.path.dirname(__file__)
DB_FILE = os.path.join(BASE_DIR, "inventory.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_FILE}"

# SQLite specific: disable same-thread check for multithreaded servers
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency that provides a SQLAlchemy session and ensures it is closed."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
