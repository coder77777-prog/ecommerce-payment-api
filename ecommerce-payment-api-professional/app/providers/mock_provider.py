import uuid

class MockPaymentProvider:
    def charge(self, amount, currency):
        return {"status": "SUCCEEDED", "reference": f"mock_{uuid.uuid4().hex}"}
