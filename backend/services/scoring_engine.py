from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class ScoringEngine:
    def __init__(self):
        self.scoring_matrix = {
            # Founding Team Scoring (30% weight)
            'team-size': {
                '1': 5,
                '2-3': 10,
                '4-5': 8,
                '6+': 6
            },
            'founder-experience': {
                'first-time': 4,
                'some-experience': 7,
                'serial-entrepreneurs': 9,
                'industry-veterans': 10
            },
            'technical-expertise': {
                'no-tech': 3,
                'outsourced': 5,
                'tech-cofounder': 9,
                'tech-team': 10
            },
            'domain-expertise': {
                'limited': 3,
                'some-knowledge': 6,
                'deep-expertise': 9,
                'industry-insider': 10
            },
            'commitment-level': {
                'part-time': 3,
                'mostly-full': 6,
                'full-time': 9,
                'bootstrapped': 10
            },
            
            # Market Opportunity Scoring (25% weight)
            'market-size-tam': {
                'under-100m': 3,
                '100m-1b': 6,
                '1b-10b': 9,
                'over-10b': 10
            },
            'market-size-som': {
                'under-10m': 4,
                '10m-100m': 7,
                '100m-500m': 9,
                'over-500m': 10
            },
            'market-growth': {
                'declining': 2,
                'stable': 5,
                'growing': 8,
                'exploding': 10
            },
            'market-timing': {
                'too-early': 4,
                'emerging': 8,
                'perfect-timing': 10,
                'mature': 6
            },
            
            # Problem/Solution Fit Scoring (20% weight)
            'problem-severity': {
                'nice-to-have': 3,
                'moderate-pain': 6,
                'significant-pain': 8,
                'critical-pain': 10
            },
            'problem-frequency': {
                'rare': 3,
                'occasional': 5,
                'frequent': 8,
                'daily': 10
            },
            'current-solution': {
                'no-solution': 8,
                'poor-alternatives': 9,
                'decent-competitors': 6,
                'strong-incumbents': 4
            },
            'solution-uniqueness': {
                'incremental': 4,
                'significant-better': 7,
                'breakthrough': 9,
                'paradigm-shift': 10
            },
            
            # Competitive Advantage Scoring (10% weight)
            'ip-protection': {
                'none': 3,
                'trade-secrets': 6,
                'pending-patents': 8,
                'granted-ip': 10
            },
            'competitive-timeline': {
                'immediate': 3,
                'months': 5,
                'year-plus': 8,
                'very-difficult': 10
            },
            
            # Business Model Scoring (15% weight)
            'revenue-model': {
                'subscription': 9,
                'transaction': 8,
                'marketplace': 8,
                'advertising': 6,
                'enterprise': 9,
                'product-sales': 7,
                'freemium': 6,
                'other': 5
            },
            'unit-economics-visibility': {
                'unclear': 3,
                'rough-estimates': 5,
                'solid-projections': 8,
                'proven-metrics': 10
            },
            'scalability': {
                'linear': 4,
                'moderate': 6,
                'high-leverage': 9,
                'viral-network': 10
            },
            
            # Validation & Traction Scoring (25% weight for idea, adjusted for launched)
            'customer-count': {
                'none': 2,
                '1-10': 4,
                '11-50': 6,
                '51-100': 7,
                '101-500': 9,
                '500+': 10
            },
            
            # Launched-specific scoring
            'mrr': {
                'under-1k': 3,
                '1k-10k': 5,
                '10k-50k': 7,
                '50k-100k': 8,
                '100k-500k': 9,
                'over-500k': 10
            },
            'funding-amount': {
                'under-500k': 6,
                '500k-1m': 7,
                '1m-2m': 8,
                '2m-5m': 9,
                'over-5m': 10
            }
        }
        
        self.section_weights = {
            'founding-team': 30,
            'market-opportunity': 25,
            'problem-solution-fit': 20,
            'competitive-advantage': 10,
            'business-model': 15,
            'validation-traction': 25,  # For idea stage
            'unit-economics': 20,       # For launched stage
            'financials-capital': 15    # For launched stage
        }
    
    def calculate_score(self, form_data: Dict[str, Any], startup_type: str) -> Dict[str, Any]:
        """Calculate comprehensive startup score based on form data."""
        try:
            section_scores = {}
            total_weighted_score = 0
            total_weight = 0
            
            # Calculate section scores
            section_scores['founding-team'] = self._calculate_team_score(form_data)
            section_scores['market-opportunity'] = self._calculate_market_score(form_data)
            section_scores['problem-solution-fit'] = self._calculate_problem_solution_score(form_data)
            section_scores['competitive-advantage'] = self._calculate_competitive_score(form_data)
            section_scores['business-model'] = self._calculate_business_model_score(form_data)
            section_scores['validation-traction'] = self._calculate_traction_score(form_data, startup_type)
            
            # Add launched-specific sections
            if startup_type == 'launched':
                section_scores['unit-economics'] = self._calculate_unit_economics_score(form_data)
                section_scores['financials-capital'] = self._calculate_financials_score(form_data)
            
            # Calculate weighted total
            for section, score in section_scores.items():
                if section in self.section_weights and score is not None:
                    weight = self.section_weights[section]
                    total_weighted_score += score * weight
                    total_weight += weight
            
            # Normalize to 0-100 scale
            final_score = (total_weighted_score / total_weight) if total_weight > 0 else 0
            final_score = min(100, max(0, final_score))
            
            # Generate verdict
            verdict = self._generate_verdict(final_score)
            
            return {
                'total_score': round(final_score, 1),
                'section_scores': {k: round(v, 1) if v is not None else 0 for k, v in section_scores.items()},
                'verdict': verdict
            }
            
        except Exception as e:
            logger.error(f"Error calculating score: {str(e)}")
            return {
                'total_score': 0,
                'section_scores': {},
                'verdict': {'emoji': '⚠️', 'text': 'Error in calculation', 'category': 'error'}
            }
    
    def _get_field_score(self, field_id: str, value: Any) -> float:
        """Get score for a specific field value."""
        if field_id in self.scoring_matrix and value in self.scoring_matrix[field_id]:
            return self.scoring_matrix[field_id][value]
        return self._get_dynamic_score(field_id, value)
    
    def _get_dynamic_score(self, field_id: str, value: Any) -> float:
        """Calculate dynamic score for fields not in scoring matrix."""
        if isinstance(value, str):
            if field_id.endswith('-textarea') or 'description' in field_id or 'proposition' in field_id:
                word_count = len(value.split())
                if word_count >= 50: return 9
                elif word_count >= 25: return 7
                elif word_count >= 10: return 5
                else: return 3
        
        if isinstance(value, list):  # For checkbox fields
            selections = len(value)
            if selections >= 3: return 9
            elif selections >= 2: return 7
            elif selections >= 1: return 5
            else: return 2
        
        if isinstance(value, (int, float)):
            return self._score_numeric_field(field_id, value)
        
        return 5  # Default score
    
    def _score_numeric_field(self, field_id: str, value: float) -> float:
        """Score numeric fields based on business logic."""
        if field_id == 'cac':
            if value <= 50: return 10
            elif value <= 100: return 8
            elif value <= 200: return 6
            else: return 4
        
        elif field_id == 'ltv':
            if value >= 500: return 10
            elif value >= 300: return 8
            elif value >= 150: return 6
            else: return 4
        
        elif field_id == 'growth-rate':
            if value >= 15: return 10
            elif value >= 10: return 8
            elif value >= 5: return 6
            else: return 4
        
        elif field_id == 'gross-margin':
            if value >= 80: return 10
            elif value >= 60: return 8
            elif value >= 40: return 6
            else: return 4
        
        elif field_id == 'churn-rate':
            if value <= 2: return 10
            elif value <= 5: return 8
            elif value <= 10: return 6
            else: return 4
        
        return 5
    
    def _calculate_team_score(self, form_data: Dict[str, Any]) -> float:
        """Calculate founding team score."""
        team_fields = ['team-size', 'founder-experience', 'technical-expertise', 
                      'domain-expertise', 'commitment-level']
        return self._calculate_section_average(form_data, team_fields)
    
    def _calculate_market_score(self, form_data: Dict[str, Any]) -> float:
        """Calculate market opportunity score."""
        market_fields = ['market-size-tam', 'market-size-som', 'market-growth', 
                        'market-timing', 'customer-segment']
        return self._calculate_section_average(form_data, market_fields)
    
    def _calculate_problem_solution_score(self, form_data: Dict[str, Any]) -> float:
        """Calculate problem/solution fit score."""
        problem_fields = ['problem-severity', 'problem-frequency', 'current-solution', 
                         'solution-uniqueness', 'value-proposition']
        return self._calculate_section_average(form_data, problem_fields)
    
    def _calculate_competitive_score(self, form_data: Dict[str, Any]) -> float:
        """Calculate competitive advantage score."""
        competitive_fields = ['defensibility', 'ip-protection', 'competitive-timeline']
        return self._calculate_section_average(form_data, competitive_fields)
    
    def _calculate_business_model_score(self, form_data: Dict[str, Any]) -> float:
        """Calculate business model score."""
        business_fields = ['revenue-model', 'pricing-strategy', 'unit-economics-visibility', 'scalability']
        return self._calculate_section_average(form_data, business_fields)
    
    def _calculate_traction_score(self, form_data: Dict[str, Any], startup_type: str) -> float:
        """Calculate validation & traction score."""
        traction_fields = ['validation-type', 'customer-count']
        return self._calculate_section_average(form_data, traction_fields)
    
    def _calculate_unit_economics_score(self, form_data: Dict[str, Any]) -> float:
        """Calculate unit economics score for launched startups."""
        unit_fields = ['cac', 'ltv', 'payback-period', 'gross-margin', 'churn-rate']
        return self._calculate_section_average(form_data, unit_fields)
    
    def _calculate_financials_score(self, form_data: Dict[str, Any]) -> float:
        """Calculate financials & capital score for launched startups."""
        financial_fields = ['mrr', 'growth-rate', 'runway', 'funding-amount', 'use-of-funds']
        return self._calculate_section_average(form_data, financial_fields)
    
    def _calculate_section_average(self, form_data: Dict[str, Any], fields: List[str]) -> float:
        """Calculate average score for a section's fields."""
        scores = []
        for field in fields:
            if field in form_data and form_data[field] is not None:
                score = self._get_field_score(field, form_data[field])
                scores.append(score)
        
        return sum(scores) / len(scores) if scores else 0
    
    def _generate_verdict(self, score: float) -> Dict[str, str]:
        """Generate verdict based on score."""
        if score >= 90:
            return {'emoji': '🦄', 'text': 'Unicorn Potential', 'category': 'unicorn'}
        elif score >= 80:
            return {'emoji': '🚀', 'text': 'Strong Candidate', 'category': 'strong'}
        elif score >= 70:
            return {'emoji': '📈', 'text': 'Promising but Needs Work', 'category': 'promising'}
        elif score >= 60:
            return {'emoji': '🔧', 'text': 'Early Potential', 'category': 'early'}
        else:
            return {'emoji': '⚠️', 'text': 'Not Investment-Ready', 'category': 'not-ready'}