from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas


### Employee CRUD ###

def create_employee(db: Session, employee: schemas.EmployeeCreate) -> models.Employee:
    db_employee = models.Employee(
        first_name=employee.first_name,
        last_name=employee.last_name,
        email=employee.email,
        position=employee.position,
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


def get_employee(db: Session, employee_id: int) -> Optional[models.Employee]:
    return db.query(models.Employee).filter(models.Employee.id == employee_id).first()


def get_employees(db: Session, skip: int = 0, limit: int = 100) -> List[models.Employee]:
    return db.query(models.Employee).offset(skip).limit(limit).all()


def update_employee(db: Session, db_employee: models.Employee, updates: schemas.EmployeeUpdate) -> models.Employee:
    for field, value in updates.dict(exclude_unset=True).items():
        setattr(db_employee, field, value)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


def delete_employee(db: Session, db_employee: models.Employee) -> None:
    db.delete(db_employee)
    db.commit()


### Task CRUD ###

def create_task(db: Session, task: schemas.TaskCreate) -> models.Task:
    db_task = models.Task(
        title=task.title,
        description=task.description,
        status=task.status or "pending",
        employee_id=task.employee_id,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_task(db: Session, task_id: int) -> Optional[models.Task]:
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def get_tasks(db: Session, skip: int = 0, limit: int = 100, employee_id: Optional[int] = None) -> List[models.Task]:
    q = db.query(models.Task)
    if employee_id is not None:
        q = q.filter(models.Task.employee_id == employee_id)
    return q.offset(skip).limit(limit).all()


def update_task(db: Session, db_task: models.Task, updates: schemas.TaskUpdate) -> models.Task:
    for field, value in updates.dict(exclude_unset=True).items():
        setattr(db_task, field, value)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, db_task: models.Task) -> None:
    db.delete(db_task)
    db.commit()
