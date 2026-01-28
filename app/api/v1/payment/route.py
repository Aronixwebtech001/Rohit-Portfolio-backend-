from fastapi import APIRouter, HTTPException
from app.schema.payment_schema import *
from app.controller.payment_controller import *



router = APIRouter()


@router.post("/create-order", response_model=PaymentOrderResponseSchema)
async def create_payment_order(request: PaymentOrderRequestSchema):

    # Calling Controller for razorpay order creation
    try:
        result = await CreatePaymentOrderController(request=request)

        return PaymentOrderResponseSchema(
            order_id=result["id"],
            amount=result["amount"]
        )
        
    except Exception as e:
        print(f"[ERROR] - [{e}]")
        raise HTTPException(
            status_code=502,
            detail={
                "code": "RAZORPAY_ORDER_CREATION_FAILED",
                "message": "Payment service unavailable. Please try again later."
            }
        )
        

@router.post("/verify-payment")
async def verify_payment(request: PaymentVerificationRequestSchema) -> PaymentVerificationResponseSchema:
    try:
        result = await PaymentVerificationController(request=request)
        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "code": "PAYMENT_VERIFICATION_FAILED",
                "message": str(e),
            },
        )

