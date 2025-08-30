import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Generate CSRF token
export const generateCSRFToken = () => {
  return Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
};

// Generate UUID for user session
export const generateUUID = () => {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0;
    const v = c === 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
};

// Validate form data before submission
export const validateSubmission = async (formData, sessionMetadata, startupType) => {
  try {
    const response = await axios.post(`${API}/vc-test/validate`, {
      form_data: formData,
      session_metadata: sessionMetadata,
      startup_type: startupType
    });
    return response.data;
  } catch (error) {
    console.error('Validation API error:', error);
    return {
      success: false,
      validation_errors: ['Network error during validation'],
      anti_gaming_flags: []
    };
  }
};

// Submit evaluation and get scoring results
export const submitEvaluation = async (formData, sessionMetadata, startupType) => {
  try {
    const response = await axios.post(`${API}/vc-test/evaluate`, {
      startup_type: startupType,
      form_data: formData,
      session_metadata: sessionMetadata
    });
    return response.data;
  } catch (error) {
    console.error('Evaluation API error:', error);
    if (error.response?.status === 400) {
      return {
        success: false,
        error: error.response.data.detail || 'Validation failed',
        details: error.response.data.detail
      };
    }
    return {
      success: false,
      error: 'Network error during evaluation'
    };
  }
};

// Create payment intent for premium unlock
export const createPaymentIntent = async (evaluationId) => {
  try {
    const response = await axios.post(`${API}/payments/create-intent`, {
      evaluation_id: evaluationId,
      amount: 999,
      currency: 'usd'
    });
    return response.data;
  } catch (error) {
    console.error('Payment intent API error:', error);
    return {
      success: false,
      error: error.response?.data?.detail || 'Payment processing error'
    };
  }
};

// Unlock premium analysis after successful payment
export const unlockPremiumAnalysis = async (evaluationId, paymentIntentId) => {
  try {
    const response = await axios.post(`${API}/vc-test/unlock-premium`, {
      evaluation_id: evaluationId,
      stripe_payment_intent_id: paymentIntentId
    });
    return response.data;
  } catch (error) {
    console.error('Premium unlock API error:', error);
    return {
      success: false,
      error: error.response?.data?.detail || 'Premium unlock failed'
    };
  }
};

// Get Stripe configuration
export const getStripeConfig = async () => {
  try {
    const response = await axios.get(`${API}/payments/config`);
    return response.data;
  } catch (error) {
    console.error('Stripe config API error:', error);
    return {
      success: false,
      error: 'Failed to load payment configuration'
    };
  }
};

// Get evaluation by ID
export const getEvaluation = async (evaluationId) => {
  try {
    const response = await axios.get(`${API}/vc-test/evaluation/${evaluationId}`);
    return response.data;
  } catch (error) {
    console.error('Get evaluation API error:', error);
    return {
      success: false,
      error: 'Failed to load evaluation'
    };
  }
};