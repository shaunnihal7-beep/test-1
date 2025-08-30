from fastapi import APIRouter, HTTPException, Request
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Dict, Any
import os
import logging

from models.vc_models import PaymentIntentCreate
from services.payment_service import PaymentService

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/payments", tags=["payments"])

# Initialize services
payment_service = PaymentService()

# Database connection
mongo_url = os.environ.get('MONGO_URL')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'app_db')]

@router.post("/create-intent", response_model=Dict[str, Any])
async def create_payment_intent(request: PaymentIntentCreate):
    """Create a Stripe payment intent for premium analysis unlock."""
    try:
        # Verify evaluation exists
        evaluation = await db.vc_evaluations.find_one({"id": request.evaluation_id})
        if not evaluation:
            raise HTTPException(status_code=404, detail="Evaluation not found")
        
        # Check if already unlocked
        if evaluation.get('premium_unlocked'):
            raise HTTPException(status_code=400, detail="Premium analysis already unlocked for this evaluation")
        
        # Create payment intent
        result = payment_service.create_payment_intent(
            evaluation_id=request.evaluation_id,
            amount=request.amount,
            currency=request.currency
        )
        
        if not result.get('success'):
            raise HTTPException(status_code=500, detail=result.get('error', 'Payment processing error'))
        
        return {
            "success": True,
            "data": {
                "client_secret": result['client_secret'],
                "payment_intent_id": result['payment_intent_id'],
                "amount": result['amount'],
                "currency": result['currency'],
                "publishable_key": payment_service.get_publishable_key()
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Create payment intent error: {str(e)}")
        raise HTTPException(status_code=500, detail="Payment system error")

@router.post("/webhook")
async def stripe_webhook(request: Request):
    """Handle Stripe webhook events."""
    try:
        payload = await request.body()
        signature = request.headers.get('stripe-signature')
        
        if not signature:
            raise HTTPException(status_code=400, detail="Missing stripe-signature header")
        
        result = payment_service.handle_webhook(payload.decode(), signature)
        
        if not result.get('success'):
            raise HTTPException(status_code=400, detail=result.get('error', 'Webhook processing error'))
        
        return {"received": True}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Webhook error: {str(e)}")
        raise HTTPException(status_code=500, detail="Webhook processing error")

@router.get("/config")
async def get_stripe_config():
    """Get Stripe configuration for frontend."""
    try:
        return {
            "success": True,
            "data": {
                "publishable_key": payment_service.get_publishable_key(),
                "currency": "usd",
                "amount": 999  # $9.99 in cents
            }
        }
        
    except Exception as e:
        logger.error(f"Get config error: {str(e)}")
        raise HTTPException(status_code=500, detail="Configuration error")