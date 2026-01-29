from fastapi import HTTPException
from app.schema.payment_schema import PaymentVerificationRequestSchema, PaymentVerificationResponseSchema
from app.core.razorpay_client import RazorpayClient
from razorpay.errors import SignatureVerificationError

class PaymentService:

    @staticmethod
    async def create_razorpay_order_service(
        amount: float,
        currency: str
    ) -> dict:
        client = RazorpayClient.get_client()

        order_data = {
            "amount": int(amount * 100),  # Razorpay expects paise
            "currency": currency
        }

        razorpay_order = client.order.create(data=order_data)

        return razorpay_order
    
    @staticmethod
    def verify_payment_service(
        payload: PaymentVerificationRequestSchema
    ) -> PaymentVerificationResponseSchema:

        try:
            client = RazorpayClient.get_client()  # ✅ instance

            client.utility.verify_payment_signature({
                "razorpay_order_id": payload.razorpay_order_id,
                "razorpay_payment_id": payload.razorpay_payment_id,
                "razorpay_signature": payload.razorpay_signature,
            })

            # ✅ Signature valid → payment verified
            return PaymentVerificationResponseSchema(
                success=True,
                message="Payment verified successfully",
                order_id=payload.razorpay_order_id,
                payment_id=payload.razorpay_payment_id,
            )

        except SignatureVerificationError:
            return PaymentVerificationResponseSchema(
                success=False,
                message="Invalid payment signature",
            )

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail={
                    "code": "PAYMENT_VERIFICATION_FAILED",
                    "message": str(e),
                },
            )
