PT2 — Employees & Tasks API

One-page summary (for recruiters)

Purpose
- Small, production-minded backend demonstrating API design, data modeling, validation, and deployment readiness.

Tech stack
- FastAPI + Pydantic v2
- SQLAlchemy (SQLite for demo)
- Uvicorn for ASGI
- Docker + docker-compose for reproducible dev environment
- Pytest for automated tests

What to look for
- Clean separation: `models` (SQLAlchemy), `schemas` (Pydantic), `crud` helpers, and `main` for routes.
- JWT token endpoint and token-protected write endpoints provide basic API security demonstration.
- OpenAPI docs available at `/docs` and saved snapshot included in `artifacts/openapi_docs.html`.
- Tests are present and pass: `4 passed` (captured in CI runs and local container tests).

Architecture & Decisions
- SQLite chosen for demo portability; the project includes Alembic scaffolding to migrate to Postgres in production.
- Pydantic v2 with `from_attributes=True` ensures smooth conversion from ORM objects to response models.
- Named Docker volume `pt2_data` keeps demo data persistent between runs while avoiding host-file permission issues.
- Endpoints implement sensible validation (unique email checks, employee existence for task assignment) and pagination for lists.

How to run the demo (copy for your interview)
1. Build and start with Docker Compose:

```powershell
docker compose up --build -d
```

2. Open interactive docs:

`http://127.0.0.1:9000/docs`

3. Seed data (optional):

```powershell
docker compose exec web python -m app.seed
```

4. Run tests:

```powershell
docker compose exec web pytest -q
```

Talking points (what you can highlight in an interview)
- Explain the API design choices (resource modeling, relationships between employees and tasks).
- Discuss the use of Pydantic and SQLAlchemy together and why `from_attributes=True` is important.
- Describe how you'd swap SQLite for Postgres and run migrations via Alembic in CI/CD.
- Explain security considerations (JWT secret management, rotating secrets, role-based access).

Contact
- If you want, I can produce a short demo script and GIF that walks through the API in the browser that you can attach to your portfolio.
