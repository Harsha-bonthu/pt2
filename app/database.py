import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Read database URL from env so containers can override where DB is stored
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./pt2.db")

# For SQLite we need the `check_same_thread` connect arg; PostgreSQL/others
# should not receive this option (psycopg2 will reject it).
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
