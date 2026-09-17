from ..extensions import db
from ..models.payment import Payment
from ..providers.mock_provider import MockPaymentProvider

class PaymentService:
    def __init__(self, provider=None):
        self.provider = provider or MockPaymentProvider()

    def create_payment(self, *, order_id, user_id, amount, currency, idempotency_key):
        existing = Payment.query.filter_by(idempotency_key=idempotency_key).first()
        if existing:
            return existing, False

        provider_result = self.provider.charge(amount, currency)
        payment = Payment(
            order_id=order_id,
            user_id=user_id,
            amount=amount,
            currency=currency,
            status=provider_result["status"],
            idempotency_key=idempotency_key,
            provider_reference=provider_result["reference"],
        )
        db.session.add(payment)
        db.session.commit()
        return payment, True
