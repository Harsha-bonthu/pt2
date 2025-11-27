import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Read database URL from env so containers can override where DB is stored
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./pt2.db")

# `check_same_thread` is required for SQLite + single-threaded SQLAlchemy sessions
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
