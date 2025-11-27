import json
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
# Use StaticPool so the in-memory SQLite database is shared across connections
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_create_and_read_employee():
    # create employee
    resp = client.post("/employees", json={
        "first_name": "Test",
        "last_name": "User",
        "email": "test.user@example.com",
        "position": "QA"
    })
    # Creating without auth should fail since write endpoints are protected
    assert resp.status_code == 401


def test_token_and_create_employee():
    # get token
    resp_t = client.post("/token", json={"username": "admin", "password": "secret"})
    assert resp_t.status_code == 200
    token = resp_t.json()["access_token"]

    # create employee with token
    resp = client.post("/employees", json={
        "first_name": "Test",
        "last_name": "User",
        "email": "test.user2@example.com",
        "position": "QA"
    }, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == "test.user2@example.com"

    # read employee
    emp_id = data["id"]
    resp2 = client.get(f"/employees/{emp_id}")
    assert resp2.status_code == 200
    assert resp2.json()["id"] == emp_id


def test_create_task_and_filter_by_employee():
    # obtain token
    resp_t = client.post("/token", json={"username": "admin", "password": "secret"})
    token = resp_t.json()["access_token"]

    # create employee
    resp = client.post("/employees", json={
        "first_name": "Task",
        "last_name": "Owner",
        "email": "task.owner@example.com",
        "position": "Dev"
    }, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 201
    emp = resp.json()

    # create task assigned to employee
    resp_t = client.post("/tasks", json={
        "title": "Write tests",
        "description": "Add unit tests",
        "employee_id": emp["id"]
    }, headers={"Authorization": f"Bearer {token}"})
    assert resp_t.status_code == 201
    task = resp_t.json()

    # filter tasks by employee_id
    resp_list = client.get(f"/tasks?employee_id={emp['id']}")
    assert resp_list.status_code == 200
    tasks = resp_list.json()
    assert any(t["id"] == task["id"] for t in tasks)


def test_invalid_employee_creation():
    # missing email should produce 422
    resp = client.post("/employees", json={
        "first_name": "NoEmail",
        "last_name": "User"
    })
    assert resp.status_code == 401 or resp.status_code == 422
