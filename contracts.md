# VC/Investor Test API Contracts & Integration Plan

## API Endpoints

### 1. Startup Evaluation & Scoring
```
POST /api/vc-test/evaluate
```
**Request Body:**
```json
{
  "startup_type": "idea|launched",
  "form_data": {
    "team-size": "2-3",
    "founder-experience": "serial-entrepreneurs",
    "market-size-tam": "1b-10b",
    "cac": 150,
    "ltv": 500,
    // ... all form fields
  },
  "session_metadata": {
    "start_time": 1640995200000,
    "csrf_token": "abc123",
    "user_uuid": "uuid-string"
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "evaluation_id": "eval_12345",
    "total_score": 78.5,
    "section_scores": {
      "founding-team": 8.2,
      "market-opportunity": 7.8,
      // ...
    },
    "verdict": {
      "emoji": "📈",
      "text": "Promising but Needs Work",
      "category": "promising"
    },
    "executive_summary": "Based on comprehensive evaluation...",
    "premium_locked": true
  }
}
```

### 2. Premium Analysis Unlock
```
POST /api/vc-test/unlock-premium
```
**Request Body:**
```json
{
  "evaluation_id": "eval_12345",
  "stripe_payment_intent_id": "pi_1234567890"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "deep_analysis": "Full detailed analysis text...",
    "recommendations": ["Focus on...", "Strengthen..."],
    "investment_readiness": "Series A ready",
    "valuation_range": "$3-10M",
    "next_steps": ["Build traction", "Hire team"]
  }
}
```

### 3. Payment Processing
```
POST /api/payments/create-intent
```
**Request Body:**
```json
{
  "evaluation_id": "eval_12345",
  "amount": 999,
  "currency": "usd"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "client_secret": "pi_1234567890_secret_abc",
    "payment_intent_id": "pi_1234567890"
  }
}
```

### 4. Anti-Gaming & Validation
```
POST /api/vc-test/validate
```
**Request Body:**
```json
{
  "form_data": {...},
  "session_metadata": {...}
}
```

**Response:**
```json
{
  "success": true,
  "validation_errors": [],
  "anti_gaming_flags": []
}
```

## Data Models

### VCEvaluation
```python
class VCEvaluation(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    startup_type: str  # "idea" or "launched"
    form_data: dict
    total_score: float
    section_scores: dict
    verdict: dict
    executive_summary: str
    deep_analysis: Optional[str] = None
    premium_unlocked: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_uuid: str
    csrf_token: str
    submission_time_ms: int
```

### PaymentRecord
```python
class PaymentRecord(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    evaluation_id: str
    stripe_payment_intent_id: str
    amount: int
    currency: str = "usd"
    status: str  # "succeeded", "failed", "pending"
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

## Mock Data Replacement Strategy

### Frontend Changes Needed:
1. **Replace mockData scoring** with API calls to `/api/vc-test/evaluate`
2. **Payment integration** using Stripe Elements for premium unlock
3. **Real-time validation** calls to `/api/vc-test/validate`
4. **Session tracking** with CSRF tokens and UUIDs

### Mock Data Mapping:
- `mockData.sections` → Backend scoring algorithm
- `mockData.scoringMatrix` → Database-driven scoring rules
- `mockData.mockAnalyses` → AI-generated responses (mock for now)
- Form validation → Backend validation with business logic

## Backend Implementation Plan

### 1. Core Features:
- **Scoring Engine**: Implement the weighted scoring algorithm
- **Validation System**: Anti-gaming measures and data validation
- **Payment Integration**: Stripe payment processing
- **Session Management**: CSRF protection and rate limiting

### 2. Database Schema:
- `vc_evaluations` collection for storing assessments
- `payment_records` collection for payment tracking
- `rate_limits` collection for anti-gaming

### 3. Security Measures:
- CSRF token validation
- Rate limiting (2 submissions per 24h per UUID)
- Input sanitization and validation
- Honeypot field detection
- Time-based submission validation (minimum 3 minutes)

## Frontend-Backend Integration Points

### 1. Form Submission Flow:
```
Frontend → POST /api/vc-test/validate → Validation Response
Frontend → POST /api/vc-test/evaluate → Scoring Response
Frontend → Display Results + Premium CTA
```

### 2. Premium Unlock Flow:
```
Frontend → POST /api/payments/create-intent → Stripe Client Secret
Frontend → Stripe Payment → Payment Success
Frontend → POST /api/vc-test/unlock-premium → Deep Analysis
```

### 3. Error Handling:
- Validation errors: Display field-specific messages
- Payment errors: Retry mechanism with user-friendly messages
- Rate limiting: Show cooldown period
- Server errors: Graceful fallback to basic functionality

## Environment Variables Needed:
```
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
VC_TEST_ENCRYPTION_KEY=random_key_for_data_encryption
```

## Testing Checklist:
- [ ] Scoring algorithm accuracy
- [ ] Anti-gaming validation
- [ ] Payment flow (test mode)
- [ ] Rate limiting
- [ ] CSRF protection
- [ ] Input sanitization
- [ ] Error handling
- [ ] Mobile responsiveness
- [ ] Performance under load