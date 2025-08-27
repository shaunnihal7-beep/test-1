import { mockData } from '../data/mockData';

export const calculateScore = (formData, startupType, sections) => {
  let totalScore = 0;
  let totalWeight = 0;

  // Get all applicable sections for the startup type
  const applicableSections = sections.filter(section => 
    section.stages.includes('both') || section.stages.includes(startupType)
  );

  // Add launched-specific sections if applicable
  if (startupType === 'launched') {
    applicableSections.push(...mockData.launchedSections);
  }

  applicableSections.forEach(section => {
    let sectionScore = 0;
    let sectionFields = 0;

    section.fields.forEach(field => {
      const value = formData[field.id];
      if (value !== undefined && value !== '' && value !== null) {
        sectionFields++;
        
        // Get score from scoring matrix or use default scoring
        let fieldScore = 5; // Default score
        
        if (mockData.scoringMatrix[field.id] && mockData.scoringMatrix[field.id][value]) {
          fieldScore = mockData.scoringMatrix[field.id][value];
        } else {
          // Dynamic scoring based on field type and value
          fieldScore = getDynamicScore(field, value);
        }
        
        sectionScore += fieldScore;
      }
    });

    if (sectionFields > 0) {
      const averageScore = (sectionScore / sectionFields) * (section.weight / 10);
      totalScore += averageScore;
      totalWeight += section.weight;
    }
  });

  // Normalize to 0-100 scale
  const finalScore = totalWeight > 0 ? (totalScore / totalWeight) * 100 : 0;
  return Math.min(100, Math.max(0, finalScore));
};

const getDynamicScore = (field, value) => {
  switch (field.type) {
    case 'number':
      // Score based on reasonable ranges for financial metrics
      if (field.id === 'cac') {
        return value <= 50 ? 10 : value <= 100 ? 8 : value <= 200 ? 6 : 4;
      }
      if (field.id === 'ltv') {
        return value >= 500 ? 10 : value >= 300 ? 8 : value >= 150 ? 6 : 4;
      }
      if (field.id === 'growth-rate') {
        return value >= 15 ? 10 : value >= 10 ? 8 : value >= 5 ? 6 : 4;
      }
      if (field.id === 'gross-margin') {
        return value >= 80 ? 10 : value >= 60 ? 8 : value >= 40 ? 6 : 4;
      }
      if (field.id === 'churn-rate') {
        return value <= 2 ? 10 : value <= 5 ? 8 : value <= 10 ? 6 : 4;
      }
      return 7; // Default for other numbers

    case 'textarea':
      // Score based on text length and quality indicators
      const wordCount = value.split(' ').length;
      if (wordCount >= 50) return 9;
      if (wordCount >= 25) return 7;
      if (wordCount >= 10) return 5;
      return 3;

    case 'checkbox':
      // Score based on number of selected options
      const selections = Array.isArray(value) ? value.length : 0;
      if (selections >= 3) return 9;
      if (selections >= 2) return 7;
      if (selections >= 1) return 5;
      return 2;

    case 'email':
      // Simple email validation scoring
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return emailRegex.test(value) ? 8 : 3;

    default:
      return 6; // Default score for other field types
  }
};

export const validateFormData = (formData, startupType, sections) => {
  const missingFields = [];
  
  // Get all applicable sections for the startup type
  const applicableSections = sections.filter(section => 
    section.stages.includes('both') || section.stages.includes(startupType)
  );

  // Add launched-specific sections if applicable
  if (startupType === 'launched') {
    applicableSections.push(...mockData.launchedSections);
  }

  applicableSections.forEach(section => {
    section.fields.forEach(field => {
      if (field.required) {
        const value = formData[field.id];
        if (value === undefined || value === '' || value === null || 
            (Array.isArray(value) && value.length === 0)) {
          missingFields.push(field.label);
        }
      }
    });
  });

  return {
    isValid: missingFields.length === 0,
    missingFields
  };
};

export const checkAntiGaming = (formData, timeSpent) => {
  const errors = [];

  // Check minimum time spent (3 minutes)
  if (timeSpent < 180000) {
    errors.push("Form completed too quickly. Please take time to provide thoughtful responses.");
  }

  // Check for honeypot field
  if (formData._bot_field && formData._bot_field !== '') {
    errors.push("Bot detection triggered.");
  }

  // Check for unrealistic financial data
  const cac = formData.cac;
  const ltv = formData.ltv;
  if (cac && ltv && ltv <= cac) {
    errors.push("LTV should be higher than CAC for a sustainable business model.");
  }

  const growthRate = formData['growth-rate'];
  if (growthRate && growthRate > 150) {
    errors.push("Growth rate seems unrealistic. Please provide accurate data.");
  }

  const churnRate = formData['churn-rate'];
  if (churnRate && churnRate > 100) {
    errors.push("Churn rate cannot exceed 100%.");
  }

  // Check TAM vs SOM logic
  const tam = formData['market-size-tam'];
  const som = formData['market-size-som'];
  if (tam === 'under-100m' && som === 'over-500m') {
    errors.push("Serviceable market cannot be larger than total addressable market.");
  }

  // Check for localStorage submission limits (simplified mock)
  const submissionCount = localStorage.getItem('vc-test-submissions') || 0;
  const lastSubmission = localStorage.getItem('vc-test-last-submission');
  const now = new Date().getTime();
  
  if (lastSubmission && now - parseInt(lastSubmission) < 86400000 && submissionCount >= 2) {
    errors.push("Maximum 2 submissions per 24 hours allowed.");
  }

  if (errors.length === 0) {
    // Update submission tracking
    localStorage.setItem('vc-test-submissions', parseInt(submissionCount) + 1);
    localStorage.setItem('vc-test-last-submission', now.toString());
  }

  return {
    isValid: errors.length === 0,
    message: errors.join(' ')
  };
};

export const generateCSRFToken = () => {
  return Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
};

export const sanitizeInput = (input) => {
  if (typeof input !== 'string') return input;
  
  // Basic XSS prevention
  return input
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;')
    .replace(/\//g, '&#x2F;');
};

export const generateUUID = () => {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0;
    const v = c === 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
};