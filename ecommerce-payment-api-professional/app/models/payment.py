from ..extensions import db

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, nullable=False, index=True)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    amount = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    status = db.Column(db.String(32), nullable=False, default="CREATED")
    idempotency_key = db.Column(db.String(255), unique=True, nullable=False, index=True)
    provider_reference = db.Column(db.String(255), nullable=True)
