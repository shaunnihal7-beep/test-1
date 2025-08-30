from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
import uuid

class VCEvaluationCreate(BaseModel):
    startup_type: str  # "idea" or "launched"
    form_data: Dict[str, Any]
    session_metadata: Dict[str, Any]

class VCEvaluation(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    startup_type: str
    form_data: Dict[str, Any]
    total_score: float
    section_scores: Dict[str, float]
    verdict: Dict[str, str]
    executive_summary: str
    deep_analysis: Optional[str] = None
    premium_unlocked: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_uuid: str
    csrf_token: str
    submission_time_ms: int
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class PaymentIntentCreate(BaseModel):
    evaluation_id: str
    amount: int = 999  # $9.99 in cents
    currency: str = "usd"

class PaymentRecord(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    evaluation_id: str
    stripe_payment_intent_id: str
    amount: int
    currency: str = "usd"
    status: str  # "succeeded", "failed", "pending"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class PremiumUnlockRequest(BaseModel):
    evaluation_id: str
    stripe_payment_intent_id: str

class ValidationRequest(BaseModel):
    form_data: Dict[str, Any]
    session_metadata: Dict[str, Any]
    startup_type: str

class ValidationResponse(BaseModel):
    success: bool
    validation_errors: List[str] = []
    anti_gaming_flags: List[str] = []