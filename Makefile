.PHONY: up down seed test alembic-init alembic-rev alembic-upgrade

up:
	docker compose up --build -d

down:
	docker compose down

seed:
	docker compose exec web python -m app.seed

test:
	docker compose exec web pytest -q

alembic-init:
	@echo "Run inside container or install alembic locally. Example: alembic revision --autogenerate -m \"init\""

alembic-upgrade:
	@echo "Run inside container: alembic upgrade head"
