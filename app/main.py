import os
from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi import Header
import logging
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional

from . import models, schemas, crud
from .auth import create_access_token, verify_token
from .database import engine, Base, get_db


# Create DB tables (simple local startup migration)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PT2 - Employees & Tasks API",
    description="API to manage employees and tasks. Includes CRUD and basic filters.",
)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pt2")

# CORS (allow local dev / demo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/employees", response_model=schemas.EmployeeRead, status_code=status.HTTP_201_CREATED)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db), auth: str = Depends(verify_token)):
    # Check unique email
    existing = db.query(models.Employee).filter(models.Employee.email == employee.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_employee(db, employee)


@app.get("/employees", response_model=List[schemas.EmployeeRead])
def list_employees(skip: int = 0, limit: int = Query(100, le=1000), db: Session = Depends(get_db)):
    return crud.get_employees(db, skip=skip, limit=limit)


@app.get("/employees/{employee_id}", response_model=schemas.EmployeeRead)
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    db_emp = crud.get_employee(db, employee_id)
    if not db_emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_emp


@app.put("/employees/{employee_id}", response_model=schemas.EmployeeRead)
def update_employee(employee_id: int, updates: schemas.EmployeeUpdate, db: Session = Depends(get_db), auth: str = Depends(verify_token)):
    db_emp = crud.get_employee(db, employee_id)
    if not db_emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    # If email update requested, ensure uniqueness
    if updates.email and updates.email != db_emp.email:
        exists = db.query(models.Employee).filter(models.Employee.email == updates.email).first()
        if exists:
            raise HTTPException(status_code=400, detail="Email already registered")
    return crud.update_employee(db, db_emp, updates)


@app.delete("/employees/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: int, db: Session = Depends(get_db), auth: str = Depends(verify_token)):
    db_emp = crud.get_employee(db, employee_id)
    if not db_emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    crud.delete_employee(db, db_emp)
    return None


@app.post("/tasks", response_model=schemas.TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db), auth: str = Depends(verify_token)):
    # If assigned to an employee, ensure the employee exists
    if task.employee_id is not None:
        if not crud.get_employee(db, task.employee_id):
            raise HTTPException(status_code=400, detail="Assigned employee not found")
    return crud.create_task(db, task)


@app.get("/tasks", response_model=List[schemas.TaskRead])
def list_tasks(skip: int = 0, limit: int = Query(100, le=1000), employee_id: Optional[int] = None, db: Session = Depends(get_db)):
    return crud.get_tasks(db, skip=skip, limit=limit, employee_id=employee_id)


@app.get("/tasks/{task_id}", response_model=schemas.TaskRead)
def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@app.put("/tasks/{task_id}", response_model=schemas.TaskRead)
def update_task(task_id: int, updates: schemas.TaskUpdate, db: Session = Depends(get_db), auth: str = Depends(verify_token)):
    db_task = crud.get_task(db, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    # If assigning to an employee, ensure that employee exists
    if updates.employee_id is not None:
        if not crud.get_employee(db, updates.employee_id):
            raise HTTPException(status_code=400, detail="Assigned employee not found")
    return crud.update_task(db, db_task, updates)


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db), auth: str = Depends(verify_token)):
    db_task = crud.get_task(db, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    crud.delete_task(db, db_task)
    return None


@app.post("/token")
def login_for_access_token(credentials: dict):
    """Simple token endpoint: POST {"username":"admin", "password":"secret"} returns a JWT.
    The expected credentials can be set via env `API_USER`/`API_PASS` (defaults: admin/secret).
    """
    api_user = os.getenv("API_USER", "admin")
    api_pass = os.getenv("API_PASS", "secret")
    if not credentials or credentials.get("username") != api_user or credentials.get("password") != api_pass:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = create_access_token(api_user)
    return {"access_token": token, "token_type": "bearer"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/favicon.ico")
def favicon():
    # Return 204 to avoid 404 log spam from browsers requesting favicon
    from fastapi import Response
    return Response(status_code=204)
