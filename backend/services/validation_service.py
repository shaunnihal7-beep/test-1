from typing import Dict, Any, List, Tuple
import re
import time
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class ValidationService:
    def __init__(self):
        self.required_fields = {
            'idea': [
                'team-size', 'founder-experience', 'technical-expertise', 'domain-expertise', 
                'commitment-level', 'market-size-tam', 'market-size-som', 'market-growth', 
                'market-timing', 'customer-segment', 'problem-severity', 'problem-frequency', 
                'current-solution', 'solution-uniqueness', 'value-proposition', 'defensibility', 
                'ip-protection', 'competitive-timeline', 'revenue-model', 'pricing-strategy', 
                'unit-economics-visibility', 'scalability', 'validation-type', 'customer-count'
            ],
            'launched': [
                'team-size', 'founder-experience', 'technical-expertise', 'domain-expertise', 
                'commitment-level', 'market-size-tam', 'market-size-som', 'market-growth', 
                'market-timing', 'customer-segment', 'problem-severity', 'problem-frequency', 
                'current-solution', 'solution-uniqueness', 'value-proposition', 'defensibility', 
                'ip-protection', 'competitive-timeline', 'revenue-model', 'pricing-strategy', 
                'unit-economics-visibility', 'scalability', 'validation-type', 'customer-count',
                'cac', 'ltv', 'payback-period', 'gross-margin', 'churn-rate', 'mrr', 
                'growth-rate', 'runway', 'funding-amount', 'use-of-funds'
            ]
        }
        
        self.min_completion_time_ms = 180000  # 3 minutes
        self.max_submissions_per_day = 2
    
    def validate_submission(self, form_data: Dict[str, Any], session_metadata: Dict[str, Any], 
                          startup_type: str) -> Tuple[bool, List[str], List[str]]:
        """Comprehensive validation of form submission."""
        validation_errors = []
        anti_gaming_flags = []
        
        try:
            # Basic field validation
            field_errors = self._validate_required_fields(form_data, startup_type)
            validation_errors.extend(field_errors)
            
            # Data type and format validation
            format_errors = self._validate_data_formats(form_data)
            validation_errors.extend(format_errors)
            
            # Cross-field validation
            logic_errors = self._validate_business_logic(form_data)
            validation_errors.extend(logic_errors)
            
            # Anti-gaming checks
            gaming_flags = self._check_anti_gaming(form_data, session_metadata)
            anti_gaming_flags.extend(gaming_flags)
            
            is_valid = len(validation_errors) == 0 and len(anti_gaming_flags) == 0
            
            return is_valid, validation_errors, anti_gaming_flags
            
        except Exception as e:
            logger.error(f"Validation error: {str(e)}")
            return False, ["Validation system error"], ["System error detected"]
    
    def _validate_required_fields(self, form_data: Dict[str, Any], startup_type: str) -> List[str]:
        """Validate that all required fields are present and not empty."""
        errors = []
        required = self.required_fields.get(startup_type, [])
        
        for field in required:
            value = form_data.get(field)
            if value is None or value == '' or (isinstance(value, list) and len(value) == 0):
                errors.append(f"Field '{field}' is required")
        
        return errors
    
    def _validate_data_formats(self, form_data: Dict[str, Any]) -> List[str]:
        """Validate data formats and types."""
        errors = []
        
        # Email validation
        email_fields = ['founder-email', 'contact-email']
        email_regex = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]+$')
        
        for field in email_fields:
            if field in form_data and form_data[field]:
                if not email_regex.match(str(form_data[field])):
                    errors.append(f"Invalid email format in '{field}'")
        
        # Numeric validation
        numeric_fields = {
            'cac': (0, 10000),
            'ltv': (0, 50000),
            'payback-period': (0, 60),
            'gross-margin': (0, 100),
            'churn-rate': (0, 100),
            'growth-rate': (-50, 150),
            'runway': (0, 120)
        }
        
        for field, (min_val, max_val) in numeric_fields.items():
            if field in form_data and form_data[field] is not None:
                try:
                    value = float(form_data[field])
                    if not (min_val <= value <= max_val):
                        errors.append(f"Value for '{field}' must be between {min_val} and {max_val}")
                except (ValueError, TypeError):
                    errors.append(f"Invalid numeric value for '{field}'")
        
        # Text length validation
        text_fields = {
            'customer-segment': (20, 1000),
            'value-proposition': (20, 1000),
            'pricing-strategy': (20, 1000),
            'use-of-funds': (20, 1000)
        }
        
        for field, (min_len, max_len) in text_fields.items():
            if field in form_data and form_data[field]:
                length = len(str(form_data[field]))
                if not (min_len <= length <= max_len):
                    errors.append(f"Text for '{field}' must be between {min_len} and {max_len} characters")
        
        return errors
    
    def _validate_business_logic(self, form_data: Dict[str, Any]) -> List[str]:
        """Validate business logic and cross-field consistency."""
        errors = []
        
        # LTV should be greater than CAC
        cac = form_data.get('cac')
        ltv = form_data.get('ltv')
        if cac and ltv:
            try:
                if float(ltv) <= float(cac):
                    errors.append("Lifetime Value (LTV) should be greater than Customer Acquisition Cost (CAC)")
            except (ValueError, TypeError):
                pass
        
        # Market size logic: SOM should be reasonable relative to TAM
        tam = form_data.get('market-size-tam')
        som = form_data.get('market-size-som')
        if tam == 'under-100m' and som in ['100m-500m', 'over-500m']:
            errors.append("Serviceable market cannot be larger than total addressable market")
        
        # Growth rate reasonableness
        growth_rate = form_data.get('growth-rate')
        if growth_rate:
            try:
                if float(growth_rate) > 150:
                    errors.append("Growth rate above 150% seems unrealistic")
            except (ValueError, TypeError):
                pass
        
        # Churn rate logic
        churn_rate = form_data.get('churn-rate')
        if churn_rate:
            try:
                if float(churn_rate) > 100:
                    errors.append("Churn rate cannot exceed 100%")
            except (ValueError, TypeError):
                pass
        
        return errors
    
    def _check_anti_gaming(self, form_data: Dict[str, Any], session_metadata: Dict[str, Any]) -> List[str]:
        """Check for anti-gaming violations."""
        flags = []
        
        # Check honeypot field
        if form_data.get('_bot_field'):
            flags.append("Bot detection triggered")
        
        # Check completion time (minimum 3 minutes)
        start_time = session_metadata.get('start_time')
        if start_time:
            try:
                completion_time = time.time() * 1000 - int(start_time)
                if completion_time < self.min_completion_time_ms:
                    flags.append(f"Form completed too quickly ({completion_time/1000:.1f}s minimum is {self.min_completion_time_ms/1000}s)")
            except (ValueError, TypeError):
                pass
        
        # Check for suspicious patterns in text responses
        text_fields = ['customer-segment', 'value-proposition', 'pricing-strategy', 'use-of-funds']
        for field in text_fields:
            if field in form_data and form_data[field]:
                text = str(form_data[field]).lower()
                if self._detect_suspicious_text(text):
                    flags.append(f"Suspicious content detected in '{field}'")
        
        # Check for repeated identical values
        if self._check_repeated_values(form_data):
            flags.append("Suspicious pattern of identical responses detected")
        
        return flags
    
    def _detect_suspicious_text(self, text: str) -> bool:
        """Detect suspicious text patterns."""
        suspicious_patterns = [
            r'test\s*test\s*test',
            r'lorem\s*ipsum',
            r'asdf+',
            r'^(.)\1{10,}',  # Repeated characters
            r'^\s*$',  # Empty or whitespace only
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        # Check for very short responses
        words = text.strip().split()
        if len(words) < 3:
            return True
        
        return False
    
    def _check_repeated_values(self, form_data: Dict[str, Any]) -> bool:
        """Check for suspiciously repeated identical values."""
        select_values = []
        radio_values = []
        
        for key, value in form_data.items():
            if key.startswith('_') or value is None:
                continue
                
            if isinstance(value, str) and not key.endswith(('textarea', 'segment', 'proposition', 'strategy', 'funds')):
                if 'select' in key or 'radio' in key or key in ['team-size', 'market-size-tam', 'market-size-som']:
                    select_values.append(value)
                else:
                    radio_values.append(value)
        
        # Check if too many identical selections (suspicious)
        if select_values and len(set(select_values)) / len(select_values) < 0.3:
            return True
        
        return False
    
    def sanitize_input(self, value: Any) -> Any:
        """Sanitize input to prevent XSS and injection attacks."""
        if isinstance(value, str):
            # Basic XSS prevention
            value = re.sub(r'<[^>]*>', '', value)  # Remove HTML tags
            value = value.replace('&', '&amp;')
            value = value.replace('<', '&lt;')
            value = value.replace('>', '&gt;')
            value = value.replace('"', '&quot;')
            value = value.replace("'", '&#x27;')
        
        return value
    
    def sanitize_form_data(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize entire form data dictionary."""
        sanitized = {}
        for key, value in form_data.items():
            if isinstance(value, list):
                sanitized[key] = [self.sanitize_input(item) for item in value]
            else:
                sanitized[key] = self.sanitize_input(value)
        
        return sanitized