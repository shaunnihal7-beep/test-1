import os
import stripe
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class PaymentService:
    def __init__(self):
        # Use test keys for development
        stripe.api_key = os.getenv('STRIPE_SECRET_KEY', 'sk_test_mock_key')
        self.publishable_key = os.getenv('STRIPE_PUBLISHABLE_KEY', 'pk_test_mock_key')
        self.webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET', 'whsec_mock_secret')
        
        # For demo purposes, we'll mock Stripe functionality if no real keys are provided
        self.is_mock_mode = stripe.api_key == 'sk_test_mock_key'
        
        if self.is_mock_mode:
            logger.info("Payment service running in MOCK mode - no real payments will be processed")
    
    def create_payment_intent(self, evaluation_id: str, amount: int = 999, currency: str = 'usd') -> Dict[str, Any]:
        """Create a Stripe payment intent for premium unlock."""
        try:
            if self.is_mock_mode:
                return self._create_mock_payment_intent(evaluation_id, amount, currency)
            
            # Real Stripe integration
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                metadata={
                    'evaluation_id': evaluation_id,
                    'product': 'vc_test_premium_analysis'
                },
                description=f'VC Test Premium Analysis - Evaluation {evaluation_id[:8]}'
            )
            
            return {
                'success': True,
                'client_secret': intent.client_secret,
                'payment_intent_id': intent.id,
                'amount': amount,
                'currency': currency
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error creating payment intent: {str(e)}")
            return {
                'success': False,
                'error': 'Payment processing error',
                'details': str(e)
            }
        except Exception as e:
            logger.error(f"Unexpected error creating payment intent: {str(e)}")
            return {
                'success': False,
                'error': 'Internal server error'
            }
    
    def _create_mock_payment_intent(self, evaluation_id: str, amount: int, currency: str) -> Dict[str, Any]:
        """Create a mock payment intent for testing."""
        mock_intent_id = f"pi_mock_{evaluation_id[:8]}_{int(datetime.now().timestamp())}"
        mock_client_secret = f"{mock_intent_id}_secret_mock"
        
        return {
            'success': True,
            'client_secret': mock_client_secret,
            'payment_intent_id': mock_intent_id,
            'amount': amount,
            'currency': currency,
            'mock_mode': True
        }
    
    def verify_payment(self, payment_intent_id: str) -> Dict[str, Any]:
        """Verify that a payment was successful."""
        try:
            if self.is_mock_mode:
                return self._verify_mock_payment(payment_intent_id)
            
            # Real Stripe verification
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            return {
                'success': True,
                'status': intent.status,
                'amount': intent.amount,
                'currency': intent.currency,
                'metadata': intent.metadata
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error verifying payment: {str(e)}")
            return {
                'success': False,
                'error': 'Payment verification error',
                'details': str(e)
            }
        except Exception as e:
            logger.error(f"Unexpected error verifying payment: {str(e)}")
            return {
                'success': False,
                'error': 'Internal server error'
            }
    
    def _verify_mock_payment(self, payment_intent_id: str) -> Dict[str, Any]:
        """Mock payment verification - always returns success for demo."""
        return {
            'success': True,
            'status': 'succeeded',
            'amount': 999,
            'currency': 'usd',
            'metadata': {
                'product': 'vc_test_premium_analysis'
            },
            'mock_mode': True
        }
    
    def handle_webhook(self, payload: str, signature: str) -> Dict[str, Any]:
        """Handle Stripe webhook events."""
        try:
            if self.is_mock_mode:
                return {'success': True, 'mock_mode': True}
            
            event = stripe.Webhook.construct_event(
                payload, signature, self.webhook_secret
            )
            
            if event['type'] == 'payment_intent.succeeded':
                payment_intent = event['data']['object']
                evaluation_id = payment_intent['metadata'].get('evaluation_id')
                
                # Here you would update the database to mark the evaluation as premium unlocked
                logger.info(f"Payment succeeded for evaluation {evaluation_id}")
                
                return {
                    'success': True,
                    'event_type': event['type'],
                    'evaluation_id': evaluation_id
                }
            
            return {'success': True, 'event_type': event['type']}
            
        except ValueError as e:
            logger.error(f"Invalid payload in webhook: {str(e)}")
            return {'success': False, 'error': 'Invalid payload'}
        except stripe.error.SignatureVerificationError as e:
            logger.error(f"Invalid signature in webhook: {str(e)}")
            return {'success': False, 'error': 'Invalid signature'}
        except Exception as e:
            logger.error(f"Unexpected webhook error: {str(e)}")
            return {'success': False, 'error': 'Internal server error'}
    
    def get_publishable_key(self) -> str:
        """Get the Stripe publishable key for frontend."""
        return self.publishable_key
    
    def is_payment_successful(self, payment_intent_id: str) -> bool:
        """Check if a payment was successful."""
        verification = self.verify_payment(payment_intent_id)
        return verification.get('success', False) and verification.get('status') == 'succeeded'