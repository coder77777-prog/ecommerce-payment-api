from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from ..extensions import db
from ..models.user import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "email already registered"}), 409
    user = User(email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"id": user.id, "email": user.email}), 201

@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    user = User.query.filter_by(email=data.get("email")).first()
    if not user or not user.check_password(data.get("password", "")):
        return jsonify({"error": "invalid credentials"}), 401
    return jsonify({"access_token": create_access_token(identity=str(user.id))}), 200
