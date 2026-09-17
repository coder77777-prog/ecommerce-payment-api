from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from ..services.payment_service import PaymentService

payments_bp = Blueprint("payments", __name__)
service = PaymentService()

@payments_bp.post("")
@jwt_required()
def create_payment():
    data = request.get_json(silent=True) or {}
    key = request.headers.get("Idempotency-Key")
    if not key:
        return jsonify({"error": "Idempotency-Key header is required"}), 400

    try:
        payment, created = service.create_payment(
            order_id=int(data["order_id"]),
            user_id=int(get_jwt_identity()),
            amount=int(data["amount"]),
            currency=data.get("currency", "USD"),
            idempotency_key=key,
        )
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "order_id and positive amount are required"}), 400
    except IntegrityError:
        # A concurrent duplicate can race between lookup and insert.
        from ..extensions import db
        db.session.rollback()
        payment = service.create_payment(
            order_id=int(data["order_id"]),
            user_id=int(get_jwt_identity()),
            amount=int(data["amount"]),
            currency=data.get("currency", "USD"),
            idempotency_key=key,
        )[0]
        created = False

    return jsonify({
        "id": payment.id,
        "status": payment.status,
        "amount": payment.amount,
        "currency": payment.currency,
        "idempotency_key": payment.idempotency_key,
        "provider_reference": payment.provider_reference,
        "replayed": not created,
    }), 201 if created else 200
