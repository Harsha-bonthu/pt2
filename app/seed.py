"""Seed script to populate the local SQLite DB with sample data."""
from .database import SessionLocal, engine
from . import models


def seed():
    models.Base = getattr(models, 'Base', None)
    # Create tables (no-op if exist)
    from .database import Base
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Only seed if no employees exist
        if db.query(models.Employee).count() == 0:
            e1 = models.Employee(first_name="Alice", last_name="Anderson", email="alice@example.com", position="Engineer")
            e2 = models.Employee(first_name="Bob", last_name="Brown", email="bob@example.com", position="Manager")
            db.add_all([e1, e2])
            db.commit()

            t1 = models.Task(title="Setup project", description="Initial project setup and scaffolding", status="done", employee_id=e1.id)
            t2 = models.Task(title="Plan sprint", description="Define stories for next sprint", status="pending", employee_id=e2.id)
            db.add_all([t1, t2])
            db.commit()
            print("Seeded sample employees and tasks.")
        else:
            print("DB already seeded.")
    finally:
        db.close()


if __name__ == '__main__':
    seed()
