from fastapi import APIRouter, HTTPException, Request
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Dict, Any
import os
import logging
import time
from datetime import datetime

from models.vc_models import (
    VCEvaluationCreate, VCEvaluation, PaymentIntentCreate, PaymentRecord,
    PremiumUnlockRequest, ValidationRequest, ValidationResponse
)
from services.scoring_engine import ScoringEngine
from services.validation_service import ValidationService
from services.payment_service import PaymentService
from services.analysis_generator import AnalysisGenerator

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/vc-test", tags=["vc-test"])

# Initialize services
scoring_engine = ScoringEngine()
validation_service = ValidationService()
payment_service = PaymentService()
analysis_generator = AnalysisGenerator()

# Database connection
mongo_url = os.environ.get('MONGO_URL')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'app_db')]

@router.post("/validate", response_model=ValidationResponse)
async def validate_submission(request: ValidationRequest):
    """Validate form data and check anti-gaming measures."""
    try:
        # Sanitize form data
        sanitized_data = validation_service.sanitize_form_data(request.form_data)
        
        # Perform validation
        is_valid, validation_errors, anti_gaming_flags = validation_service.validate_submission(
            sanitized_data, request.session_metadata, request.startup_type
        )
        
        return ValidationResponse(
            success=is_valid,
            validation_errors=validation_errors,
            anti_gaming_flags=anti_gaming_flags
        )
        
    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Validation system error")

@router.post("/evaluate", response_model=Dict[str, Any])
async def evaluate_startup(request: VCEvaluationCreate):
    """Evaluate startup and generate score with executive summary."""
    try:
        # Validate the submission first
        sanitized_data = validation_service.sanitize_form_data(request.form_data)
        
        is_valid, validation_errors, anti_gaming_flags = validation_service.validate_submission(
            sanitized_data, request.session_metadata, request.startup_type
        )
        
        if not is_valid:
            raise HTTPException(
                status_code=400, 
                detail={
                    "message": "Validation failed",
                    "validation_errors": validation_errors,
                    "anti_gaming_flags": anti_gaming_flags
                }
            )
        
        # Calculate scoring
        scoring_result = scoring_engine.calculate_score(sanitized_data, request.startup_type)
        
        # Generate executive summary
        executive_summary = analysis_generator.generate_executive_summary(
            scoring_result['total_score'],
            scoring_result['verdict'],
            sanitized_data
        )
        
        # Create evaluation record
        evaluation = VCEvaluation(
            startup_type=request.startup_type,
            form_data=sanitized_data,
            total_score=scoring_result['total_score'],
            section_scores=scoring_result['section_scores'],
            verdict=scoring_result['verdict'],
            executive_summary=executive_summary,
            user_uuid=request.session_metadata.get('user_uuid', 'anonymous'),
            csrf_token=request.session_metadata.get('csrf_token', ''),
            submission_time_ms=int(time.time() * 1000)
        )
        
        # Save to database
        result = await db.vc_evaluations.insert_one(evaluation.dict())
        
        return {
            "success": True,
            "data": {
                "evaluation_id": evaluation.id,
                "total_score": scoring_result['total_score'],
                "section_scores": scoring_result['section_scores'],
                "verdict": scoring_result['verdict'],
                "executive_summary": executive_summary,
                "premium_locked": True
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Evaluation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Evaluation system error")

@router.post("/unlock-premium", response_model=Dict[str, Any])
async def unlock_premium_analysis(request: PremiumUnlockRequest):
    """Unlock premium deep-dive analysis after payment verification."""
    try:
        # Verify payment
        payment_verification = payment_service.verify_payment(request.stripe_payment_intent_id)
        
        if not payment_verification.get('success') or payment_verification.get('status') != 'succeeded':
            raise HTTPException(status_code=400, detail="Payment verification failed")
        
        # Get evaluation record
        evaluation_record = await db.vc_evaluations.find_one({"id": request.evaluation_id})
        if not evaluation_record:
            raise HTTPException(status_code=404, detail="Evaluation not found")
        
        # Check if already unlocked
        if evaluation_record.get('premium_unlocked'):
            raise HTTPException(status_code=400, detail="Premium analysis already unlocked")
        
        # Generate deep analysis
        deep_analysis = analysis_generator.generate_deep_analysis(
            evaluation_record['total_score'],
            evaluation_record['section_scores'],
            evaluation_record['form_data'],
            evaluation_record['startup_type']
        )
        
        # Update evaluation record
        await db.vc_evaluations.update_one(
            {"id": request.evaluation_id},
            {
                "$set": {
                    "deep_analysis": deep_analysis,
                    "premium_unlocked": True,
                    "premium_unlocked_at": datetime.utcnow()
                }
            }
        )
        
        # Record payment
        payment_record = PaymentRecord(
            evaluation_id=request.evaluation_id,
            stripe_payment_intent_id=request.stripe_payment_intent_id,
            amount=payment_verification.get('amount', 999),
            status='succeeded'
        )
        await db.payment_records.insert_one(payment_record.dict())
        
        # Generate recommendations
        score = evaluation_record['total_score']
        recommendations = _generate_recommendations(score, evaluation_record['startup_type'])
        
        return {
            "success": True,
            "data": {
                "deep_analysis": deep_analysis,
                "recommendations": recommendations['next_steps'],
                "investment_readiness": recommendations['investment_readiness'],
                "valuation_range": recommendations['valuation_range'],
                "recommended_round": recommendations['recommended_round']
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Premium unlock error: {str(e)}")
        raise HTTPException(status_code=500, detail="Premium unlock system error")

@router.get("/evaluation/{evaluation_id}", response_model=Dict[str, Any])
async def get_evaluation(evaluation_id: str):
    """Get evaluation results by ID."""
    try:
        evaluation = await db.vc_evaluations.find_one({"id": evaluation_id})
        if not evaluation:
            raise HTTPException(status_code=404, detail="Evaluation not found")
        
        # Convert ObjectId to string for serialization
        if '_id' in evaluation:
            evaluation['_id'] = str(evaluation['_id'])
        
        # Remove sensitive data
        evaluation.pop('form_data', None)
        evaluation.pop('csrf_token', None)
        
        return {
            "success": True,
            "data": evaluation
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get evaluation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error")

def _generate_recommendations(score: float, startup_type: str) -> Dict[str, Any]:
    """Generate investment recommendations based on score."""
    if score >= 80:
        return {
            "investment_readiness": "Series A Ready" if startup_type == 'launched' else "Seed Ready",
            "valuation_range": "$10M+" if startup_type == 'launched' else "$3-10M",
            "recommended_round": "Series A" if startup_type == 'launched' else "Seed",
            "next_steps": [
                "Prepare comprehensive due diligence materials",
                "Develop 18-month growth projections",
                "Build strategic advisor network",
                "Establish key performance metrics dashboard"
            ]
        }
    elif score >= 60:
        return {
            "investment_readiness": "Seed Ready" if startup_type == 'launched' else "Pre-Seed Ready",
            "valuation_range": "$3-10M" if startup_type == 'launched' else "$0.5-3M",
            "recommended_round": "Seed" if startup_type == 'launched' else "Pre-Seed",
            "next_steps": [
                "Focus on customer validation and early traction",
                "Strengthen competitive moats and IP protection",
                "Prepare detailed financial projections",
                "Build strategic partnerships in target industry"
            ]
        }
    else:
        return {
            "investment_readiness": "Pre-Seed" if startup_type == 'launched' else "Bootstrap/Accelerator",
            "valuation_range": "$0.5-3M" if startup_type == 'launched' else "$0.1-1M",
            "recommended_round": "Pre-Seed" if startup_type == 'launched' else "Bootstrap",
            "next_steps": [
                "Validate product-market fit with target customers",
                "Develop minimum viable product (MVP)",
                "Establish clear value proposition and pricing",
                "Build founding team and advisory board"
            ]
        }

@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "vc-test", "timestamp": datetime.utcnow()}