import razorpay
from app.core.config import settings

class RazorpayClient:
    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            cls._client = razorpay.Client(
                auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
            )
        return cls._client
