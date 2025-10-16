# Monitoring & Observability Masterclass

A comprehensive demonstration of modern monitoring and observability patterns with two complete setups using different tools and approaches.

## Overview

This repository contains hands-on demonstrations of monitoring and observability implementations using industry-standard tools. Each setup includes a complete stack with a FastAPI application, PostgreSQL database, and visualization/monitoring tools.

## Demonstrations

### 1. [Prometheus & Grafana](./prometheus_grafana/README.md)

A metrics-based monitoring approach using Prometheus for time-series data collection and Grafana for visualization.

**Key Components:**
- Prometheus for metrics scraping and storage
- Grafana for dashboard visualization
- Redis for caching and session management
- PostgreSQL for data persistence
- FastAPI application exposing metrics endpoints

[→ Start with Prometheus & Grafana Setup](./prometheus_grafana/README.md)

### 2. [Elastic APM](./elastic_apm/README.md)

A distributed tracing and application performance monitoring approach using Elastic APM stack.

**Key Components:**
- Elastic APM Server for trace collection
- Kibana for visualization and analysis
- Redis for caching and session management
- PostgreSQL for data persistence
- FastAPI application with APM instrumentation

[→ Start with Elastic APM Setup](./elastic_apm/README.md)

## Quick Start

### Prerequisites

Before running either demonstration, download the required SQL scripts from S3:

```bash
wget -P elastic_apm/requirements/postgres/initdb.d https://dst-masterclass.s3.eu-west-1.amazonaws.com/Monitoring_Observability/postgres/01-insert_into_vendors.sql
cp elastic_apm/requirements/postgres/initdb.d/01-insert_into_vendors.sql prometheus_grafana/requirements/postgres/initdb.d
wget -P elastic_apm/requirements/postgres/initdb.d https://dst-masterclass.s3.eu-west-1.amazonaws.com/Monitoring_Observability/postgres/02-insert_into_products.sql
cp elastic_apm/requirements/postgres/initdb.d/02-insert_into_products.sql prometheus_grafana/requirements/postgres/initdb.d
```

## Directory Structure

```
.
├── client/                    # Python test clients for generating transactions
├── prometheus_grafana/        # Prometheus & Grafana demonstration
│   └── README.md             # Detailed setup and configuration guide
├── elastic_apm/              # Elastic APM demonstration
│   └── README.md             # Detailed setup and configuration guide
└── README.md                 # This file
```

## Common Infrastructure

Both demonstrations share common components and patterns:

### Database Schema

Each setup creates a PostgreSQL database named `suppliers` with three tables:

- **vendors**: Vendor information with qualification levels
- **products**: Product catalog with pricing and qualification requirements
- **transactions**: Transaction history for inventory management

### FastAPI Application

Both setups feature a FastAPI application with endpoints for:

- **Authentication** (`/login`): User login with Redis-backed session management
- **Products** (`/products`): Product listing and inventory management
- **Transactions** (`/transaction`): Transaction creation and history

### Caching & Sessions

Redis is used in both setups for:
- User authentication token storage
- Session management with TTL support
- Performance optimization

## Next Steps

1. Choose your demonstration:
   - [Prometheus & Grafana](./prometheus_grafana/README.md) - Metrics-based monitoring
   - [Elastic APM](./elastic_apm/README.md) - Distributed tracing & APM

2. Follow the detailed setup instructions in the chosen directory

3. Use the `client/` directory to generate test transactions and observe monitoring in action

## Additional Resources

- [Client Documentation](./client/README.md) - How to generate test transactions
- [Prometheus & Grafana Guide](./prometheus_grafana/README.md) - Complete setup and architecture
- [Elastic APM Guide](./elastic_apm/README.md) - Complete setup and architecture
