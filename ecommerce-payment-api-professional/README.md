# E-Commerce Payment API

A production-style payment backend built with Python and Flask. The project demonstrates reliable payment processing patterns including JWT authentication, PostgreSQL persistence, Redis-backed idempotency, retry-safe workflows, validation, error handling, automated tests, and Docker support.

## Problem

E-commerce platforms need a payment service that can safely process requests despite duplicate client submissions, network failures, retries, and downstream payment-provider failures.

## Architecture

Client → Flask REST API → Service Layer → PostgreSQL
                         ↘ Redis (idempotency / short-lived state)
                         ↘ Payment Provider Adapter

The application separates HTTP handling, business logic, persistence, and infrastructure concerns.

## Core Features

- User registration and JWT login
- Product and order APIs
- Payment creation and status tracking
- Idempotency keys to prevent duplicate payment creation
- Retry-safe payment-provider interaction
- PostgreSQL persistence with SQLAlchemy
- Redis integration
- Centralized API error handling
- Request validation
- Unit and API tests
- Docker / Docker Compose
- Environment-based configuration
- Health endpoint
- OpenAPI-friendly REST design
- CI workflow with GitHub Actions

## Important production note

This repository implements a payment-service architecture and a mock payment provider adapter. It does **not** process real money or store card numbers, CVVs, or other sensitive payment credentials. A real provider such as Stripe/Adyen/PayPal should be integrated through the provider adapter and tokenized payment methods.

## Project Structure

```text
app/
  __init__.py
  config.py
  extensions.py
  models/
    __init__.py
    user.py
    product.py
    order.py
    payment.py
  routes/
    __init__.py
    auth.py
    products.py
    orders.py
    payments.py
    health.py
  services/
    __init__.py
    payment_service.py
  providers/
    __init__.py
    mock_provider.py
  utils/
    __init__.py
    errors.py
tests/
  test_health.py
  test_payments.py
.env.example
docker-compose.yml
Dockerfile
requirements.txt
.github/workflows/ci.yml
```

## Run locally

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
# source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env
python -m flask --app app run --debug
```

API base URL: `http://127.0.0.1:5000`

Health check:

```http
GET /health
```

## Docker

```bash
docker compose up --build
```

## Example payment request

```http
POST /payments
Authorization: Bearer <JWT>
Idempotency-Key: order-123-payment-001
Content-Type: application/json

{
  "order_id": 1,
  "amount": 4999,
  "currency": "USD"
}
```

The amount is represented in the smallest currency unit (for example, cents) to avoid floating-point money calculations.

## Reliability design

### Idempotency

Clients send an `Idempotency-Key`. The service stores the result associated with that key so a retried request does not create another payment.

A production implementation should enforce uniqueness at the database level and use transactional locking/atomic operations where needed.

### Retries

Only retry transient provider failures. Do not blindly retry every error. A retry strategy should use bounded attempts and exponential backoff.

### Failure modes considered

- Duplicate client request
- Client timeout followed by retry
- Payment-provider timeout
- Provider temporary failure
- Invalid order
- Invalid amount/currency
- Database failure
- Redis unavailable
- Authentication failure

## Testing

```bash
pytest -q
```

## CI/CD

GitHub Actions runs the automated test suite on pushes and pull requests. The workflow is intentionally simple so it can be extended later with image builds, security scanning, staging deployment, and production deployment.

## Security

- Passwords are hashed; plaintext passwords are never persisted.
- JWT protects authenticated endpoints.
- Secrets are provided through environment variables.
- Sensitive card data is intentionally not stored.
- Input validation and consistent error responses are included.
- In a real deployment, HTTPS, secret management, rate limiting, audit logging, and provider webhooks should also be enabled.

## Production roadmap

- Add Alembic migrations
- Add real payment-provider adapter
- Add signed webhook verification
- Add distributed locking / stronger idempotency storage
- Add structured JSON logging
- Add metrics and tracing
- Add rate limiting
- Add Kubernetes deployment manifests
- Add security and dependency scanning
- Add load testing

## License

MIT
