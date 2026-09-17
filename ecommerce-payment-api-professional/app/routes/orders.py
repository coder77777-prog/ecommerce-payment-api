from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models.order import Order

orders_bp = Blueprint("orders", __name__)

@orders_bp.post("")
@jwt_required()
def create_order():
    data = request.get_json(silent=True) or {}
    amount = data.get("total_amount")
    currency = data.get("currency", "USD")
    if amount is None or int(amount) <= 0:
        return jsonify({"error": "total_amount must be positive"}), 400
    order = Order(user_id=int(get_jwt_identity()), total_amount=int(amount), currency=currency)
    db.session.add(order)
    db.session.commit()
    return jsonify({"id": order.id, "status": order.status}), 201
