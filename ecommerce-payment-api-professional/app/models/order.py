from ..extensions import db

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    total_amount = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    status = db.Column(db.String(32), nullable=False, default="PENDING")
