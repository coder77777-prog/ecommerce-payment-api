import pytest
from app import create_app
from app.extensions import db
from app.models.user import User

@pytest.fixture()
def client(tmp_path):
    app = create_app()
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{tmp_path / 'test.db'}",
        JWT_SECRET_KEY="test",
    )
    with app.app_context():
        db.drop_all()
        db.create_all()
    return app.test_client()

def test_register_login_and_idempotent_payment(client):
    r = client.post("/auth/register", json={"email": "dev@example.com", "password": "secret123"})
    assert r.status_code == 201

    r = client.post("/auth/login", json={"email": "dev@example.com", "password": "secret123"})
    token = r.json["access_token"]

    headers = {"Authorization": f"Bearer {token}", "Idempotency-Key": "payment-001"}
    payload = {"order_id": 10, "amount": 4999, "currency": "USD"}

    first = client.post("/payments", json=payload, headers=headers)
    second = client.post("/payments", json=payload, headers=headers)

    assert first.status_code == 201
    assert second.status_code == 200
    assert first.json["id"] == second.json["id"]
    assert second.json["replayed"] is True
