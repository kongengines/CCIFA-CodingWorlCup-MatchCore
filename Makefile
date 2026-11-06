.PHONY: help install migrate seed run test docker-up docker-down lint format clean simulate

PYTHON ?= python
PORT ?= 8000

help: ## Show this help
        @awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} \
        /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

install: ## Install Python deps
        $(PYTHON) -m pip install --upgrade pip
        $(PYTHON) -m pip install -r requirements.txt
        cd dashboard && pnpm install || npm install

migrate: ## Run SQL migrations
        bash scripts/run_migrations.sh

seed: ## Seed the database
        $(PYTHON) scripts/seed_db.py

run: ## Start MatchCore REST API
        uvicorn matchcore.engine.api.rest:app --host 0.0.0.0 --port $(PORT) --reload

run-cli: ## Start MatchCore CLI
        $(PYTHON) -m matchcore.engine.cli.matchcore --help

test: ## Run unit tests
        $(PYTHON) -m pytest matchcore/tests/unit -v

test-offline: ## Run offline simulations
        $(PYTHON) matchcore/tests/offline_simulation/simulate_match.py
        $(PYTHON) matchcore/tests/offline_simulation/simulate_season.py

lint: ## Lint Python + TypeScript
        $(PYTHON) -m ruff check matchcore scripts
        cd dashboard && pnpm run lint || npm run lint

format: ## Format code
        $(PYTHON) -m ruff format matchcore scripts
        cd dashboard && pnpm run format || true

docker-up: ## Boot the full stack
        docker compose up -d --build

docker-down: ## Stop the full stack
        docker compose down

docker-logs: ## Tail logs
        docker compose logs -f --tail=100

monitoring-up: ## Boot monitoring stack (Prometheus + Grafana + Loki)
        docker compose -f matchcore/infra/monitoring/docker-compose.monitoring.yml up -d

simulate: ## Simulate a full season + World Cup
        $(PYTHON) scripts/simulate_season.py

clean: ## Remove caches and build artefacts
        rm -rf .pytest_cache .ruff_cache __pycache__ */__pycache__ */*/__pycache__
        rm -rf dashboard/dist dashboard/node_modules
        find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

.PHONY: arena-seal arena-verify
arena-seal: ## Seal an offline match (demo)
        $(PYTHON) -m matchcore.engine.cli.matchcore match seal --match-id demo-001

arena-verify: ## Verify the sovereign ledger
        $(PYTHON) -m matchcore.engine.cli.matchcore ledger verify
