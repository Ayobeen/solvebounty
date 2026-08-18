.PHONY: help install migrate seed test dev-api dev-web dev-ai docker-up docker-down

help:
	@echo "SolveBounty Engineering Commands:"
	@echo "  make install     - Install Python & Node dependencies"
	@echo "  make migrate     - Run Django database migrations"
	@echo "  make seed        - Seed the skills database"
	@echo "  make test        - Run backend pytest test suite"
	@echo "  make dev-api     - Start Django local development server"
	@echo "  make dev-web     - Start Next.js frontend development server"
	@echo "  make dev-ai      - Start FastAPI AI microservice"
	@echo "  make docker-up   - Start full docker-compose stack"
	@echo "  make docker-down - Stop docker-compose stack"

install:
	pip install -r apps/api/requirements.txt
	pip install -r apps/ai/requirements.txt
	cd apps/web && npm install

migrate:
	python apps/api/manage.py migrate

seed:
	python apps/api/manage.py seed_skills

test:
	cd apps/api && pytest

dev-api:
	python apps/api/manage.py runserver 0.0.0.0:8000

dev-web:
	cd apps/web && npm run dev

dev-ai:
	cd apps/ai && uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload

docker-up:
	docker compose up -d

docker-down:
	docker compose down
