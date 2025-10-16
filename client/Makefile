# FastAPI endpoint configuration
FASTAPI_HOST ?= localhost
FASTAPI_PORT ?= 5001

# Python interpreter - automatically detect venv
PYTHON := $(shell if [ -f .venv/bin/python ]; then echo .venv/bin/python; elif [ -f venv/bin/python ]; then echo venv/bin/python; else echo python; fi)

# Default target - show available commands
.PHONY: help
help:
	@echo "📋 Available commands:"
	@echo ""
	@echo "  Setup:"
	@echo "    make setup          - Create virtual environment and install dependencies (using uv)"
	@echo "    make setup-pip      - Create virtual environment and install dependencies (using pip)"
	@echo ""
	@echo "  Run Test Scripts:"
	@echo "    make low            - Run low transaction volume test"
	@echo "    make errors         - Run error cases test (wrong vendor IDs)"
	@echo "    make high           - Run high transaction volume test"
	@echo "    make resupply       - Run product resupply test"
	@echo "    make all-tests      - Run all tests in parallel (Ctrl+C to stop)"
	@echo "    make all-tests-seq  - Run all tests sequentially"
	@echo ""
	@echo "  Configuration:"
	@echo "    FASTAPI_HOST=$(FASTAPI_HOST)"
	@echo "    FASTAPI_PORT=$(FASTAPI_PORT)"
	@echo ""
	@echo "  Example with custom host/port:"
	@echo "    make low FASTAPI_HOST=192.168.1.100 FASTAPI_PORT=8000"

# Setup virtual environment using uv (modern, fast)
.PHONY: setup
setup:
	@echo "🔧 Setting up environment with uv..."
	uv venv
	@echo "📦 Installing dependencies..."
	uv sync
	@echo "✅ Setup complete! Activate with: source .venv/bin/activate"

# Setup virtual environment using pip (traditional)
.PHONY: setup-pip
setup-pip:
	@echo "🔧 Setting up environment with pip..."
	python -m venv venv
	@echo "📦 Installing dependencies..."
	./venv/bin/pip install -r requirements.txt
	@echo "✅ Setup complete! Activate with: source venv/bin/activate"

# Run low transaction volume test
.PHONY: low
low:
	@echo "🔄 Running low transaction volume test..."
	FASTAPI_PORT=$(FASTAPI_PORT) $(PYTHON) 00-post_transactions_low.py $(FASTAPI_HOST)

# Run error cases test
.PHONY: errors
errors:
	@echo "⚠️  Running error cases test (wrong vendor IDs)..."
	FASTAPI_PORT=$(FASTAPI_PORT) $(PYTHON) 01-wrong_vendor_id.py $(FASTAPI_HOST)

# Run high transaction volume test
.PHONY: high
high:
	@echo "🚀 Running high transaction volume test..."
	FASTAPI_PORT=$(FASTAPI_PORT) $(PYTHON) 02-post_transactions_high.py $(FASTAPI_HOST)

# Run product resupply test
.PHONY: resupply
resupply:
	@echo "📦 Running product resupply test..."
	FASTAPI_PORT=$(FASTAPI_PORT) $(PYTHON) 03-resupply_products.py $(FASTAPI_HOST)

# Run all tests sequentially
.PHONY: all-tests-seq
all-tests-seq:
	@echo "🎯 Running all tests sequentially..."
	@echo ""
	$(MAKE) low
	@echo ""
	@echo "⏳ Waiting 5 seconds before next test..."
	@sleep 5
	@echo ""
	$(MAKE) errors
	@echo ""
	@echo "⏳ Waiting 5 seconds before next test..."
	@sleep 5
	@echo ""
	$(MAKE) high
	@echo ""
	@echo "⏳ Waiting 5 seconds before next test..."
	@sleep 5
	@echo ""
	$(MAKE) resupply
	@echo ""
	@echo "✅ All tests completed!"

# Run all tests in parallel (use Ctrl+C to stop all)
.PHONY: all-tests
all-tests:
	@echo "🎯 Running all tests in parallel..."
	@echo "Press Ctrl+C to stop all tests"
	@echo ""
	@trap 'echo ""; echo "🛑 Stopping all tests..."; kill 0; exit' INT TERM; \
	( \
		echo "🔄 Starting low transaction volume test..."; \
		FASTAPI_PORT=$(FASTAPI_PORT) $(PYTHON) 00-post_transactions_low.py $(FASTAPI_HOST) & \
		PID1=$$!; \
		echo "⚠️  Starting error cases test..."; \
		FASTAPI_PORT=$(FASTAPI_PORT) $(PYTHON) 01-wrong_vendor_id.py $(FASTAPI_HOST) & \
		PID2=$$!; \
		echo "🚀 Starting high transaction volume test..."; \
		FASTAPI_PORT=$(FASTAPI_PORT) $(PYTHON) 02-post_transactions_high.py $(FASTAPI_HOST) & \
		PID3=$$!; \
		echo "📦 Starting product resupply test..."; \
		FASTAPI_PORT=$(FASTAPI_PORT) $(PYTHON) 03-resupply_products.py $(FASTAPI_HOST) & \
		PID4=$$!; \
		echo ""; \
		echo "✅ All tests started (PIDs: $$PID1 $$PID2 $$PID3 $$PID4)"; \
		echo "📊 Monitor in Grafana: http://localhost:3001"; \
		echo ""; \
		wait $$PID1 $$PID2 $$PID3 $$PID4; \
		echo ""; \
		echo "✅ All tests completed!"; \
	)

# Clean up generated files and cache
.PHONY: clean
clean:
	@echo "🧹 Cleaning up..."
	rm -rf .venv venv __pycache__ *.pyc .pytest_cache
	@echo "✅ Cleanup complete!"
