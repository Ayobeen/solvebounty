import hmac
import hashlib
import requests
from django.conf import settings
from .base import PaymentProvider

class PaystackProvider(PaymentProvider):
    BASE_URL = "https://api.paystack.co"

    def __init__(self, secret_key: str = None):
        self.secret_key = secret_key or getattr(settings, 'PAYSTACK_SECRET_KEY', 'sk_test_mock')
        self.headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json"
        }

    def verify_webhook_signature(self, payload_bytes: bytes, signature_header: str) -> bool:
        if not signature_header:
            return False
        # If mock key in development
        if self.secret_key.startswith('sk_test_mock') or settings.DEBUG:
            return True
        computed = hmac.new(self.secret_key.encode('utf-8'), payload_bytes, hashlib.sha512).hexdigest()
        return hmac.compare_digest(computed, signature_header)

    def initialize_payment(self, email: str, amount_kobo: int, reference: str, callback_url: str = None) -> dict:
        if self.secret_key.startswith('sk_test_mock'):
            return {
                "status": True,
                "message": "Authorization URL created (Sandbox Mock)",
                "data": {
                    "authorization_url": f"https://checkout.paystack.com/mock-{reference}",
                    "access_code": f"mock_access_{reference}",
                    "reference": reference
                }
            }
        try:
            url = f"{self.BASE_URL}/transaction/initialize"
            payload = {
                "email": email,
                "amount": amount_kobo,
                "reference": reference,
            }
            if callback_url:
                payload["callback_url"] = callback_url
            response = requests.post(url, json=payload, headers=self.headers, timeout=10)
            return response.json()
        except Exception as e:
            return {
                "status": False,
                "message": str(e),
                "data": {}
            }

    def verify_payment(self, reference: str) -> dict:
        if self.secret_key.startswith('sk_test_mock'):
            return {
                "status": True,
                "message": "Verification successful (Sandbox Mock)",
                "data": {
                    "status": "success",
                    "reference": reference,
                    "amount": 10000000,
                    "currency": "NGN"
                }
            }
        try:
            url = f"{self.BASE_URL}/transaction/verify/{reference}"
            response = requests.get(url, headers=self.headers, timeout=10)
            return response.json()
        except Exception as e:
            return {"status": False, "message": str(e), "data": {}}

    def create_recipient(self, name: str, account_number: str, bank_code: str) -> dict:
        if self.secret_key.startswith('sk_test_mock'):
            return {
                "status": True,
                "message": "Recipient created (Sandbox Mock)",
                "data": {
                    "recipient_code": f"RCP_mock_{account_number[-4:]}",
                    "active": True,
                    "name": name,
                    "details": {"account_number": account_number, "bank_code": bank_code}
                }
            }
        try:
            url = f"{self.BASE_URL}/transferrecipient"
            payload = {
                "type": "nuban",
                "name": name,
                "account_number": account_number,
                "bank_code": bank_code,
                "currency": "NGN"
            }
            response = requests.post(url, json=payload, headers=self.headers, timeout=10)
            return response.json()
        except Exception as e:
            return {"status": False, "message": str(e), "data": {}}

    def initiate_transfer(self, amount_kobo: int, recipient_code: str, reason: str, reference: str) -> dict:
        if self.secret_key.startswith('sk_test_mock'):
            return {
                "status": True,
                "message": "Transfer queued (Sandbox Mock)",
                "data": {
                    "reference": reference,
                    "transfer_code": f"TRF_mock_{reference}",
                    "status": "success"
                }
            }
        try:
            url = f"{self.BASE_URL}/transfer"
            payload = {
                "source": "balance",
                "amount": amount_kobo,
                "recipient": recipient_code,
                "reason": reason,
                "reference": reference
            }
            response = requests.post(url, json=payload, headers=self.headers, timeout=10)
            return response.json()
        except Exception as e:
            return {"status": False, "message": str(e), "data": {}}
