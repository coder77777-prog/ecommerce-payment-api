from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models.product import Product

products_bp = Blueprint("products", __name__)

@products_bp.post("")
def create_product():
    data = request.get_json(silent=True) or {}
    required = ["name", "price"]
    if any(k not in data for k in required):
        return jsonify({"error": "name and price are required"}), 400
    product = Product(
        name=data["name"],
        price=int(data["price"]),
        currency=data.get("currency", "USD"),
        stock=int(data.get("stock", 0)),
    )
    db.session.add(product)
    db.session.commit()
    return jsonify({"id": product.id, "name": product.name}), 201

@products_bp.get("")
def list_products():
    return jsonify([
        {"id": p.id, "name": p.name, "price": p.price, "currency": p.currency, "stock": p.stock}
        for p in Product.query.all()
    ])
