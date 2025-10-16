# Platform detection
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Linux)
	COMPOSE_FILE := docker-compose.linux.yml
	PLATFORM := Linux
else ifeq ($(UNAME_S),Darwin)
	COMPOSE_FILE := docker-compose.mac.yml
	PLATFORM := macOS
else
	COMPOSE_FILE := docker-compose.linux.yml
	PLATFORM := Unknown
endif

DOCKER_COMPOSE := docker compose -f $(COMPOSE_FILE)

# Default target - complete setup from scratch with one command
all: build wait-services import-data
	@echo ""
	@echo "✅ Complete setup finished! Services are running."
	@echo "📊 Kibana APM: http://localhost:5601 (Navigate to Observability > APM)"
	@echo "🔍 Elasticsearch: http://localhost:9200"
	@echo "📡 APM Server: http://localhost:8200"
	@echo "🚀 FastAPI: http://localhost:5001/docs"
	@echo "🗄️  PostgreSQL: localhost:5432"
	@echo "🔴 Redis: localhost:6379"
	@echo ""
	@echo "Platform detected: $(PLATFORM)"
	@echo "Using: $(COMPOSE_FILE)"

# Just start services (no setup)
start:
	@echo "Starting services on $(PLATFORM)..."
	$(DOCKER_COMPOSE) up -d

# Build and start all services
build:
	@echo "Building and starting services on $(PLATFORM)..."
	@echo "Using $(COMPOSE_FILE)"
	$(DOCKER_COMPOSE) up -d --build

# Wait for services to be ready
wait-services:
	@echo "⏳ Waiting for services to be ready..."
	@echo "Waiting for Elasticsearch..."
	@until curl -s http://localhost:9200/_cluster/health > /dev/null 2>&1; do sleep 2; done
	@echo "✅ Elasticsearch is ready"
	@echo "Waiting for PostgreSQL..."
	@until docker exec postgres-apm pg_isready -U suppliers > /dev/null 2>&1; do sleep 1; done
	@echo "✅ PostgreSQL is ready"
	@echo "Waiting for APM Server..."
	@until curl -s http://localhost:8200 > /dev/null 2>&1; do sleep 2; done
	@echo "✅ APM Server is ready"
	@sleep 3
	@echo "✅ All services are ready!"

# Import data into PostgreSQL
import-data:
	@echo "📦 Checking if data needs to be imported..."
	@VENDOR_COUNT=$$(docker exec postgres-apm psql -U suppliers -d suppliers -t -c "SELECT COUNT(*) FROM vendors;" 2>/dev/null | xargs); \
	if [ "$$VENDOR_COUNT" = "0" ] || [ -z "$$VENDOR_COUNT" ]; then \
		echo "Importing data into PostgreSQL..."; \
		docker exec postgres-apm psql -U suppliers -d suppliers -f /client/import.sql; \
		echo "✅ Data imported successfully"; \
	else \
		echo "⏭️  Data already exists ($$VENDOR_COUNT vendors found), skipping import"; \
	fi
	@echo "Verifying data..."
	@docker exec postgres-apm psql -U suppliers -d suppliers -c "SELECT COUNT(*) FROM vendors;"
	@docker exec postgres-apm psql -U suppliers -d suppliers -c "SELECT COUNT(*) FROM products;"

# Stop and remove all services
down:
	@echo "Stopping services..."
	$(DOCKER_COMPOSE) down -v
	@echo "✅ Services stopped and removed"

# Rebuild FastAPI only
re-fastapi:
	@echo "Rebuilding FastAPI service..."
	$(DOCKER_COMPOSE) up -d --build fastapi-apm

# Complete restart
re: down all

# Show help
.PHONY: help
help:
	@echo "📋 Elastic APM Demo - Available Commands"
	@echo ""
	@echo "  Setup & Run:"
	@echo "    make              - Complete setup from scratch (build, wait, import data)"
	@echo "    make all          - Same as 'make'"
	@echo "    make start        - Start existing services"
	@echo "    make build        - Build and start all services"
	@echo ""
	@echo "  Data Management:"
	@echo "    make import-data  - Import vendors and products data"
	@echo "    make verify-data  - Verify imported data"
	@echo ""
	@echo "  Service Management:"
	@echo "    make down         - Stop and remove all services"
	@echo "    make re           - Complete restart (down + all)"
	@echo "    make re-fastapi   - Rebuild only FastAPI service"
	@echo ""
	@echo "  Monitoring:"
	@echo "    make logs         - Show logs from all services"
	@echo "    make logs-fastapi - Show FastAPI logs"
	@echo "    make logs-apm     - Show APM Server logs"
	@echo "    make status       - Show service status"
	@echo ""
	@echo "  Platform: $(PLATFORM)"
	@echo "  Compose File: $(COMPOSE_FILE)"

# Verify imported data
.PHONY: verify-data
verify-data:
	@echo "Verifying database data..."
	@docker exec postgres-apm psql -U suppliers -d suppliers -c "SELECT COUNT(*) as vendor_count FROM vendors;"
	@docker exec postgres-apm psql -U suppliers -d suppliers -c "SELECT COUNT(*) as product_count FROM products;"
	@docker exec postgres-apm psql -U suppliers -d suppliers -c "\\dt"

# Show logs from all services
.PHONY: logs
logs:
	$(DOCKER_COMPOSE) logs -f

# Show FastAPI logs
.PHONY: logs-fastapi
logs-fastapi:
	$(DOCKER_COMPOSE) logs -f fastapi-apm

# Show APM Server logs
.PHONY: logs-apm
logs-apm:
	$(DOCKER_COMPOSE) logs -f apm-server

# Show Elasticsearch logs
.PHONY: logs-es
logs-es:
	$(DOCKER_COMPOSE) logs -f elasticsearch

# Show service status
.PHONY: status
status:
	@echo "Service Status:"
	@$(DOCKER_COMPOSE) ps
	@echo ""
	@echo "Health Checks:"
	@echo -n "Elasticsearch: "
	@curl -s http://localhost:9200/_cluster/health | grep -o '"status":"[^"]*"' || echo "❌ Not responding"
	@echo -n "APM Server: "
	@curl -s http://localhost:8200 > /dev/null 2>&1 && echo "✅ Ready" || echo "❌ Not responding"
	@echo -n "PostgreSQL: "
	@docker exec postgres-apm pg_isready -U suppliers > /dev/null 2>&1 && echo "✅ Ready" || echo "❌ Not responding"
	@echo -n "Kibana: "
	@curl -s http://localhost:5601/api/status > /dev/null 2>&1 && echo "✅ Ready" || echo "❌ Not responding"

.PHONY: all start build wait-services import-data down re-fastapi re
