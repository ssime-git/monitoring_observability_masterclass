# Default target - complete setup from scratch with one command
all: setup-env setup-dirs build setup-data
	@echo "✅ Complete setup finished! Services are running."
	@echo "📊 Grafana: http://localhost:3001 (admin/admin_password123)"
	@echo "📈 Prometheus: http://localhost:9091"
	@echo "🚀 FastAPI: http://localhost:5001/docs"
	@echo "🗄️  PostgreSQL: localhost:5433"
	@echo "🔴 Redis: localhost:6380"

# Just start services (no setup)
start:
	docker compose up -d
	$(MAKE) exec_redis
	$(MAKE) exec_postgres

# Build and start all services
build:
	docker compose up -d --build
	$(MAKE) exec_postgres
	$(MAKE) exec_redis


down:
	docker compose down -v

re: down build

postgres:
	docker compose up -d --build postgres
	$(MAKE) exec_postgres

redis:
	docker compose up -d --build redis
	$(MAKE) exec_redis

exec_redis:
	docker exec -d redis /prometheus/redis_exporter

exec_postgres:
	docker exec -d postgres /prometheus/postgres_exporter

# Setup environment file
setup-env:
	@echo "Setting up environment..."
	@/bin/bash -c 'echo "USER_ID=$$(id -u)" > .env'
	@echo "✅ .env file created"

# Setup required directories with permissions
setup-dirs:
	@echo "Creating required directories..."
	@mkdir -p requirements/prometheus/data
	@chmod 777 requirements/prometheus/data
	@echo "✅ Directories created with proper permissions"

# Copy data and initialize database
setup-data:
	@echo "Waiting for PostgreSQL to be ready..."
	@until docker exec postgres pg_isready -U suppliers > /dev/null 2>&1; do sleep 1; done
	@echo "✅ PostgreSQL is ready"
	@echo "Importing data..."
	@docker exec postgres mkdir -p /data
	@docker cp ../client/data/vendors.csv postgres:/data/
	@docker cp ../client/data/products.csv postgres:/data/
	@docker cp ../client/import.sql postgres:/
	@docker exec postgres psql -U suppliers -d suppliers -f import.sql
	@echo "✅ Data imported successfully"
	@echo "Verifying data..."
	@docker exec postgres psql -U suppliers -d suppliers -c "SELECT COUNT(*) FROM vendors;"
	@docker exec postgres psql -U suppliers -d suppliers -c "SELECT COUNT(*) FROM products;"