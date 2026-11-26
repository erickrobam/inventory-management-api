# Inventory Management API

A production-minded REST API for multi-warehouse inventory operations. Built with FastAPI, SQLAlchemy 2, Pydantic v2 and PostgreSQL.

## Capabilities
- Create and retrieve products and warehouses.
- Record stock movements (receipts, issues and adjustments).
- Prevent negative stock and preserve an auditable movement history.
- Versioned API, structured validation errors and OpenAPI docs.
- Repository/service separation and deterministic tests.

## Architecture
`HTTP → FastAPI router → service/use-case → SQLAlchemy repository → PostgreSQL`

The service owns business invariants; persistence details stay in the repository layer. The in-memory store keeps the starter runnable without a database; replace it with the SQLAlchemy adapter for deployment.

## Quick start
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000/docs.

## Configuration
Copy `.env.example` to `.env`. Set `DATABASE_URL` when wiring the PostgreSQL adapter. Never commit real credentials.

## Quality
```bash
pytest
ruff check .
ruff format --check .
mypy app
```

## API example
```bash
curl -X POST http://127.0.0.1:8000/api/v1/products \
  -H 'content-type: application/json' \
  -d '{"sku":"KB-001","name":"Mechanical keyboard"}'
```

## Roadmap
- [ ] SQLAlchemy/PostgreSQL adapter and Alembic migrations
- [ ] OAuth2/JWT authentication and role-based access control
- [ ] Idempotency keys for stock movement writes
- [ ] OpenTelemetry traces and metrics

## Design decisions
Stock changes are represented as immutable movements rather than silently overwriting quantities. This provides a traceable audit trail and makes reconciliation possible.
