.PHONY: help install install-dev setup clean test test-unit test-integration test-e2e test-cov lint format type-check security-check run run-dev run-prod db-migrate db-upgrade db-downgrade docker-build docker-up docker-down

# Default target
.DEFAULT_GOAL := help

# Variables
PYTHON := python3
PIP := $(PYTHON) -m pip
PYTEST := $(PYTHON) -m pytest
BLACK := $(PYTHON) -m black
ISORT := $(PYTHON) -m isort
MYPY := $(PYTHON) -m mypy
FLAKE8 := $(PYTHON) -m flake8
BANDIT := $(PYTHON) -m bandit
ALEMBIC := alembic

help: ## Show this help message
	@echo "AutoAgentHire - LinkedIn Job Automation System"
	@echo ""
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install production dependencies
	$(PIP) install -r requirements.txt

install-dev: ## Install development dependencies
	$(PIP) install -r requirements.txt
	$(PIP) install -e ".[dev]"

setup: ## Initial project setup (create directories, copy env file)
	mkdir -p data/logs data/uploads data/resumes data/job_listings data/templates data/vector_db
	cp -n .env.example .env || true
	@echo "Setup complete! Edit .env file with your configuration."

clean: ## Clean up cache and temporary files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ htmlcov/ .coverage

test: ## Run all tests
	$(PYTEST) tests/

test-unit: ## Run unit tests only
	$(PYTEST) tests/unit/ -v

test-integration: ## Run integration tests only
	$(PYTEST) tests/integration/ -v -m integration

test-e2e: ## Run end-to-end tests only
	$(PYTEST) tests/e2e/ -v -m e2e

test-cov: ## Run tests with coverage report
	$(PYTEST) --cov=backend --cov-report=html --cov-report=term tests/
	@echo "Coverage report generated in htmlcov/index.html"

lint: ## Run linters (flake8)
	$(FLAKE8) backend/ tests/

format: ## Format code with black and isort
	$(BLACK) backend/ tests/
	$(ISORT) backend/ tests/

format-check: ## Check code formatting without making changes
	$(BLACK) --check backend/ tests/
	$(ISORT) --check-only backend/ tests/

type-check: ## Run type checking with mypy
	$(MYPY) backend/

security-check: ## Run security checks with bandit
	$(BANDIT) -r backend/ -ll

quality: format-check lint type-check security-check ## Run all code quality checks

run: ## Run the application (development mode)
	uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

run-dev: ## Run development server with auto-reload
	uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000 --log-level debug

run-prod: ## Run production server
	uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4

streamlit: ## Run Streamlit frontend
	streamlit run frontend/streamlit/app.py

db-init: ## Initialize database with alembic
	$(ALEMBIC) init alembic

db-migrate: ## Create a new database migration
	$(ALEMBIC) revision --autogenerate -m "$(msg)"

db-upgrade: ## Apply database migrations (upgrade to latest)
	$(ALEMBIC) upgrade head

db-downgrade: ## Rollback database migration (downgrade by 1)
	$(ALEMBIC) downgrade -1

db-current: ## Show current database revision
	$(ALEMBIC) current

db-history: ## Show migration history
	$(ALEMBIC) history

docker-build: ## Build Docker images
	docker-compose build

docker-up: ## Start Docker containers
	docker-compose up -d

docker-down: ## Stop Docker containers
	docker-compose down

docker-logs: ## View Docker logs
	docker-compose logs -f

docker-clean: ## Remove Docker containers and volumes
	docker-compose down -v

shell: ## Open Python shell with app context
	$(PYTHON)

deps-update: ## Update dependencies
	$(PIP) install --upgrade pip
	$(PIP) list --outdated

deps-export: ## Export current dependencies
	$(PIP) freeze > requirements.txt

ci: quality test ## Run CI pipeline (quality checks + tests)
