# PT2 Backend — Employees & Tasks API

Simple, production-minded FastAPI backend demonstrating RESTful CRUD for Employees and Tasks. This repo is designed to be shown to recruiters: it runs in Docker, includes tests, seed data, OpenAPI docs, and a short developer quickstart.

![tests](https://img.shields.io/badge/tests-pytest-blue)
![docker](https://img.shields.io/badge/docker-ready-lightgrey)

## Tech stack
- Python 3.10 (container)
- FastAPI + Pydantic v2
- SQLAlchemy (SQLite for demo)
- Uvicorn (ASGI server)

## Highlights
- Complete CRUD for `Employee` and `Task` with proper DB relationships
- JWT token endpoint for lightweight auth (demo credentials: `admin` / `secret`)
- Docker + docker-compose with named volume persistence
- Seed script that populates demo data for immediate exploration
- Tests with `pytest` and a CI workflow
- Interactive OpenAPI docs (`/docs`) with examples

## Quickstart (Docker — recommended)

Run everything (build image, create volume, start container):

```powershell
docker compose up --build -d
```

Open the interactive docs at `http://127.0.0.1:9000/docs` (host `9000` → container `8080`).

Seed the database (if not seeded automatically):

```powershell
docker compose exec web python -m app.seed
```

Run tests inside the container:

```powershell
docker compose exec web pytest -q
```

## Live examples (from running instance)

I ran the API locally in Docker and captured real responses to include here. You can reproduce these steps or open the saved OpenAPI HTML at `artifacts/openapi_docs.html` and take a screenshot for your portfolio.

1) Request a token (demo credentials `admin` / `secret`):

```json
{
	"access_token": "<REDACTED_JWT_TOKEN>",
	"token_type": "bearer"
}
```

2) Create an employee (response):

```json
{
	"first_name": "Portfolio",
	"last_name": "User",
	"email": "portfolio.user@example.com",
	"position": "Engineer",
	"id": 3,
	"tasks": []
}
```

3) Create a task assigned to that employee (response):

```json
{
	"title": "Demo task",
	"description": "Demo task created for README",
	"status": "pending",
	"employee_id": 3,
	"id": 3,
	"created_at": "2025-11-27T15:16:04.144620"
}
```

Files created for demo artifacts:
- `artifacts/openapi_docs.html` — saved OpenAPI docs HTML (open in browser and screenshot for your portfolio).


## API usage examples (curl)

1) Get a demo token:

```powershell
curl -s -X POST "http://127.0.0.1:9000/token" -H "Content-Type: application/json" -d '{"username":"admin","password":"secret"}'
```

Response:

```json
{"access_token":"<JWT_TOKEN>","token_type":"bearer"}
```

2) Create an employee (use the token):

```powershell
curl -s -X POST "http://127.0.0.1:9000/employees" -H "Content-Type: application/json" -H "Authorization: Bearer <JWT_TOKEN>" -d '{"first_name":"Jane","last_name":"Doe","email":"jane.doe@example.com","position":"Engineer"}'
```

3) Create a task assigned to that employee:

```powershell
curl -s -X POST "http://127.0.0.1:9000/tasks" -H "Content-Type: application/json" -H "Authorization: Bearer <JWT_TOKEN>" -d '{"title":"Interview prep","description":"Prepare coding assignment","employee_id":1}'
```

## Project structure

- `app/main.py` — FastAPI application and routes
- `app/models.py` — SQLAlchemy models
- `app/schemas.py` — Pydantic v2 schemas (request/response models)
- `app/database.py` — DB engine, Session and dependency
- `app/crud.py` — Database CRUD helpers
- `tests/` — `pytest` test suite
- `docker-compose.yml` — development launch (host `9000` → container `8080`)

## Notes for  reviewers

- Demonstrates practical API design, DB modeling, validation, and basic auth.
- The JWT `SECRET_KEY` is set to a demo value in the project; for production replace via env var.
- Alembic scaffolding is included for starting migrations: run `alembic revision --autogenerate -m "init"` then `alembic upgrade head`.

## Tests & CI

Run tests locally (inside container recommended):

```powershell
docker compose exec web pytest -q
```

I can run the test suite now and paste the output here if you'd like — tell me to `run tests` and I'll run them inside the container and report results for inclusion in the README and your recruiter notes.

