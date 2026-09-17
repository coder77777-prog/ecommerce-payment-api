# Architecture

## Request flow

1. Client authenticates and receives a JWT.
2. Client creates an order.
3. Client sends `POST /payments` with an `Idempotency-Key`.
4. Payment service checks whether that key has already produced a payment.
5. New requests are passed to the provider adapter.
6. The provider result is persisted in PostgreSQL.
7. Retries with the same idempotency key return the existing payment.

## Production evolution

For high scale, the payment creation operation should use a transactional idempotency record, database uniqueness constraints, explicit payment state transitions, provider request IDs, durable outbox/event processing, webhook reconciliation, and observability.
