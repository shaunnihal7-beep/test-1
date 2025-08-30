from typing import Dict, Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class AnalysisGenerator:
    def __init__(self):
        self.executive_summaries = {
            'unicorn': "This startup demonstrates exceptional potential across all key metrics. The founding team combines deep domain expertise with proven execution capabilities, addressing a massive market opportunity with breakthrough innovation. Strong competitive moats and validated traction indicate unicorn-scale potential.",
            
            'strong': "A compelling investment opportunity with strong fundamentals. The team shows solid experience and technical capabilities, targeting a substantial market with clear customer pain points. Well-defined business model with promising early validation metrics.",
            
            'promising': "Shows meaningful potential but requires focused execution improvements. Core concept is sound with identifiable market opportunity, though competitive positioning and go-to-market strategy need strengthening. Good foundation for seed-stage investment.",
            
            'early': "Early-stage potential with foundational elements in place. Market opportunity exists but validation is limited. Team capabilities are developing and business model requires refinement. Suitable for pre-seed or accelerator programs.",
            
            'not-ready': "Significant foundational work needed before investment readiness. Core assumptions require validation, team composition needs strengthening, and market approach requires substantial refinement. Focus on customer development and product-market fit validation."
        }
    
    def generate_executive_summary(self, score: float, verdict: Dict[str, str], form_data: Dict[str, Any]) -> str:
        """Generate executive summary based on evaluation results."""
        try:
            category = verdict.get('category', 'not-ready')
            base_summary = self.executive_summaries.get(category, self.executive_summaries['not-ready'])
            
            # Customize based on specific strengths/weaknesses
            customizations = self._analyze_strengths_weaknesses(form_data, score)
            
            if customizations:
                base_summary += f" {customizations}"
            
            return base_summary
            
        except Exception as e:
            logger.error(f"Error generating executive summary: {str(e)}")
            return "Analysis completed. Please review individual section scores for detailed insights."
    
    def generate_deep_analysis(self, score: float, section_scores: Dict[str, float], 
                             form_data: Dict[str, Any], startup_type: str) -> str:
        """Generate comprehensive deep-dive analysis."""
        try:
            analysis_parts = []
            
            # Header with overall assessment
            analysis_parts.append(f"**COMPREHENSIVE VC ANALYSIS - SCORE: {score}/100**\n")
            analysis_parts.append(f"*Evaluation Date: {datetime.now().strftime('%B %d, %Y')}*\n")
            
            # Founding Team Analysis
            team_analysis = self._analyze_founding_team(form_data, section_scores.get('founding-team', 0))
            analysis_parts.append(f"**FOUNDING TEAM ASSESSMENT ({section_scores.get('founding-team', 0):.1f}/10)**")
            analysis_parts.append(team_analysis)
            
            # Market Opportunity Analysis
            market_analysis = self._analyze_market_opportunity(form_data, section_scores.get('market-opportunity', 0))
            analysis_parts.append(f"\n**MARKET OPPORTUNITY ANALYSIS ({section_scores.get('market-opportunity', 0):.1f}/10)**")
            analysis_parts.append(market_analysis)
            
            # Product-Market Fit Analysis
            pmf_analysis = self._analyze_product_market_fit(form_data, section_scores.get('problem-solution-fit', 0))
            analysis_parts.append(f"\n**PRODUCT-MARKET FIT EVALUATION ({section_scores.get('problem-solution-fit', 0):.1f}/10)**")
            analysis_parts.append(pmf_analysis)
            
            # Competitive Positioning
            competitive_analysis = self._analyze_competitive_position(form_data, section_scores.get('competitive-advantage', 0))
            analysis_parts.append(f"\n**COMPETITIVE POSITIONING ({section_scores.get('competitive-advantage', 0):.1f}/10)**")
            analysis_parts.append(competitive_analysis)
            
            # Business Model Analysis
            business_analysis = self._analyze_business_model(form_data, section_scores.get('business-model', 0))
            analysis_parts.append(f"\n**BUSINESS MODEL VIABILITY ({section_scores.get('business-model', 0):.1f}/10)**")
            analysis_parts.append(business_analysis)
            
            # Stage-specific analysis
            if startup_type == 'launched':
                unit_economics_analysis = self._analyze_unit_economics(form_data, section_scores.get('unit-economics', 0))
                analysis_parts.append(f"\n**UNIT ECONOMICS ANALYSIS ({section_scores.get('unit-economics', 0):.1f}/10)**")
                analysis_parts.append(unit_economics_analysis)
            
            # Investment Recommendation
            investment_rec = self._generate_investment_recommendation(score, startup_type, section_scores)
            analysis_parts.append(f"\n**INVESTMENT RECOMMENDATION**")
            analysis_parts.append(investment_rec)
            
            return "\n\n".join(analysis_parts)
            
        except Exception as e:
            logger.error(f"Error generating deep analysis: {str(e)}")
            return "Deep analysis generation encountered an error. Please contact support for assistance."
    
    def _analyze_strengths_weaknesses(self, form_data: Dict[str, Any], score: float) -> str:
        """Analyze key strengths and weaknesses."""
        observations = []
        
        # Team experience check
        founder_exp = form_data.get('founder-experience')
        if founder_exp in ['serial-entrepreneurs', 'industry-veterans']:
            observations.append("Strong founding team with proven track record")
        elif founder_exp == 'first-time':
            observations.append("First-time entrepreneurs may benefit from experienced advisors")
        
        # Market size check
        market_size = form_data.get('market-size-tam')
        if market_size in ['1b-10b', 'over-10b']:
            observations.append("addresses substantial market opportunity")
        elif market_size == 'under-100m':
            observations.append("limited market size may constrain scalability")
        
        # Traction check
        customer_count = form_data.get('customer-count')
        if customer_count in ['101-500', '500+']:
            observations.append("demonstrates meaningful customer traction")
        
        return ". ".join(observations) + "." if observations else ""
    
    def _analyze_founding_team(self, form_data: Dict[str, Any], score: float) -> str:
        """Analyze founding team strengths and areas for improvement."""
        team_size = form_data.get('team-size', 'Unknown')
        founder_exp = form_data.get('founder-experience', 'Unknown')
        tech_expertise = form_data.get('technical-expertise', 'Unknown')
        domain_expertise = form_data.get('domain-expertise', 'Unknown')
        
        analysis = f"Team composition shows {team_size} founders with {founder_exp.replace('-', ' ')} experience. "
        
        if score >= 8:
            analysis += "The founding team demonstrates strong complementary skills and deep market understanding. "
            analysis += "Technical capabilities are well-established and domain expertise provides significant competitive advantages."
        elif score >= 6:
            analysis += "Solid team foundation with room for strategic strengthening. "
            analysis += "Consider adding advisors or team members to fill capability gaps, particularly in areas of limited experience."
        else:
            analysis += "Team composition requires significant strengthening before investment readiness. "
            analysis += "Focus on recruiting co-founders with complementary skills and proven industry experience."
        
        return analysis
    
    def _analyze_market_opportunity(self, form_data: Dict[str, Any], score: float) -> str:
        """Analyze market opportunity and timing."""
        tam = form_data.get('market-size-tam', 'Unknown')
        growth = form_data.get('market-growth', 'Unknown')
        timing = form_data.get('market-timing', 'Unknown')
        
        analysis = f"Target market size ({tam.replace('-', ' to $')}) with {growth.replace('-', ' ')} growth trends. "
        
        if score >= 8:
            analysis += "Excellent market positioning with substantial addressable opportunity and favorable timing. "
            analysis += "Market dynamics support aggressive growth strategies and venture-scale returns."
        elif score >= 6:
            analysis += "Reasonable market opportunity with moderate growth potential. "
            analysis += "Market timing appears favorable, though competitive dynamics require careful navigation."
        else:
            analysis += "Limited market opportunity may constrain venture scalability. "
            analysis += "Consider pivoting to larger adjacent markets or developing strategies to expand addressable market size."
        
        return analysis
    
    def _analyze_product_market_fit(self, form_data: Dict[str, Any], score: float) -> str:
        """Analyze product-market fit and customer validation."""
        problem_severity = form_data.get('problem-severity', 'Unknown')
        solution_uniqueness = form_data.get('solution-uniqueness', 'Unknown')
        
        analysis = f"Addresses {problem_severity.replace('-', ' ')} customer pain points with {solution_uniqueness.replace('-', ' ')} solution approach. "
        
        if score >= 8:
            analysis += "Strong product-market fit indicators with clear customer value proposition. "
            analysis += "Solution differentiation provides sustainable competitive advantages."
        elif score >= 6:
            analysis += "Promising product-market alignment with validation evidence. "
            analysis += "Continue iterating based on customer feedback to strengthen value proposition."
        else:
            analysis += "Product-market fit requires validation and refinement. "
            analysis += "Focus on customer development and rapid experimentation to achieve stronger alignment."
        
        return analysis
    
    def _analyze_competitive_position(self, form_data: Dict[str, Any], score: float) -> str:
        """Analyze competitive advantages and market positioning."""
        defensibility = form_data.get('defensibility', [])
        ip_protection = form_data.get('ip-protection', 'Unknown')
        
        moats = len(defensibility) if isinstance(defensibility, list) else 0
        
        analysis = f"Competitive positioning with {moats} identified moats and {ip_protection.replace('-', ' ')} intellectual property protection. "
        
        if score >= 8:
            analysis += "Strong competitive differentiation with multiple defensible advantages. "
            analysis += "Market position should be sustainable against competitive threats."
        elif score >= 6:
            analysis += "Moderate competitive advantages requiring continued development. "
            analysis += "Focus on strengthening network effects and customer switching costs."
        else:
            analysis += "Limited competitive differentiation increases vulnerability to competition. "
            analysis += "Urgent need to develop sustainable moats and unique positioning."
        
        return analysis
    
    def _analyze_business_model(self, form_data: Dict[str, Any], score: float) -> str:
        """Analyze business model viability and scalability."""
        revenue_model = form_data.get('revenue-model', 'Unknown')
        scalability = form_data.get('scalability', 'Unknown')
        
        analysis = f"Business model based on {revenue_model.replace('-', ' ')} with {scalability.replace('-', ' ')} scalability characteristics. "
        
        if score >= 8:
            analysis += "Highly scalable business model with clear path to profitability. "
            analysis += "Revenue streams are diversified and unit economics support venture-scale growth."
        elif score >= 6:
            analysis += "Viable business model with good scalability potential. "
            analysis += "Unit economics projections are reasonable though require real-world validation."
        else:
            analysis += "Business model requires fundamental refinement for venture viability. "
            analysis += "Focus on improving unit economics and developing scalable revenue streams."
        
        return analysis
    
    def _analyze_unit_economics(self, form_data: Dict[str, Any], score: float) -> str:
        """Analyze unit economics for launched startups."""
        cac = form_data.get('cac')
        ltv = form_data.get('ltv')
        churn = form_data.get('churn-rate')
        
        ltv_cac_ratio = ltv / cac if cac and ltv and cac > 0 else 0
        
        analysis = f"Unit economics show ${cac} CAC, ${ltv} LTV (ratio: {ltv_cac_ratio:.1f}:1), and {churn}% monthly churn. "
        
        if score >= 8:
            analysis += "Excellent unit economics with strong LTV:CAC ratio and low churn rates. "
            analysis += "Financial metrics support aggressive growth investment and scaling strategies."
        elif score >= 6:
            analysis += "Solid unit economics foundation with room for optimization. "
            analysis += "Focus on improving customer retention and reducing acquisition costs."
        else:
            analysis += "Unit economics require significant improvement for sustainable growth. "
            analysis += "Critical to optimize CAC and LTV before scaling marketing investments."
        
        return analysis
    
    def _generate_investment_recommendation(self, score: float, startup_type: str, section_scores: Dict[str, float]) -> str:
        """Generate investment recommendation based on overall assessment."""
        if score >= 85:
            rec = "**STRONG BUY RECOMMENDATION** - This startup merits immediate consideration for lead or co-lead investment. "
            rec += "All key metrics indicate venture-scale potential with experienced team and validated market opportunity."
        elif score >= 75:
            rec = "**QUALIFIED RECOMMENDATION** - Suitable for investment consideration with standard due diligence. "
            rec += "Strong fundamentals with minor areas for improvement during growth phase."
        elif score >= 65:
            rec = "**CONDITIONAL RECOMMENDATION** - Consider for seed investment with active engagement and milestone tracking. "
            rec += "Good potential but requires hands-on support to achieve venture-scale outcomes."
        elif score >= 55:
            rec = "**WATCH LIST** - Monitor progress over 6-12 months before investment consideration. "
            rec += "Foundational elements present but significant execution risk remains."
        else:
            rec = "**PASS RECOMMENDATION** - Not suitable for venture investment in current form. "
            rec += "Fundamental issues require resolution before considering any investment."
        
        # Add stage-specific recommendations
        if startup_type == 'idea':
            rec += "\n\n**Next Steps**: Focus on customer validation, MVP development, and early traction metrics before Series A readiness."
        else:
            rec += "\n\n**Next Steps**: Optimize unit economics, scale customer acquisition, and prepare for growth stage metrics tracking."
        
        return rec