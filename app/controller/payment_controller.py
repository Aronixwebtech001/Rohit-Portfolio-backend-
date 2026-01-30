from app.schema.payment_schema import *
from app.services.payment_service import PaymentService


async def CreatePaymentOrderController(
        request: PaymentOrderRequestSchema
) -> PaymentOrderResponseSchema:
    
    # Calling payment service for razorpay order creation
    amount: str = request.amount
    currency: str = request.currency
    return await PaymentService.create_razorpay_order_service(amount=amount, currency=currency)


async def PaymentVerificationController(request: PaymentVerificationRequestSchema) -> PaymentVerificationResponseSchema:
    return PaymentService.verify_payment_service(request)
