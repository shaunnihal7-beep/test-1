export const mockData = {
  sections: [
    {
      id: 'founding-team',
      number: 'A',
      title: 'Founding Team',
      description: 'Tell us about the people behind your startup. VCs invest in teams first, ideas second.',
      weight: 30,
      stages: ['both'],
      fields: [
        {
          id: 'team-size',
          type: 'select',
          label: 'Team Size',
          required: true,
          options: [
            { value: '1', label: 'Solo Founder' },
            { value: '2-3', label: '2-3 Founders' },
            { value: '4-5', label: '4-5 Founders' },
            { value: '6+', label: '6+ Founders' }
          ],
          tooltip: 'Optimal team size is typically 2-3 founders with complementary skills'
        },
        {
          id: 'founder-experience',
          type: 'radio',
          label: 'Combined Founder Experience',
          required: true,
          options: [
            { value: 'first-time', label: 'First-time entrepreneurs' },
            { value: 'some-experience', label: 'Some startup/industry experience' },
            { value: 'serial-entrepreneurs', label: 'Serial entrepreneurs' },
            { value: 'industry-veterans', label: 'Industry veterans (10+ years)' }
          ]
        },
        {
          id: 'technical-expertise',
          type: 'radio',
          label: 'Technical Expertise',
          required: true,
          options: [
            { value: 'no-tech', label: 'No technical co-founder' },
            { value: 'outsourced', label: 'Technical work outsourced' },
            { value: 'tech-cofounder', label: 'Strong technical co-founder' },
            { value: 'tech-team', label: 'Multiple technical experts' }
          ]
        },
        {
          id: 'domain-expertise',
          type: 'radio',
          label: 'Domain Expertise',
          required: true,
          options: [
            { value: 'limited', label: 'Limited industry knowledge' },
            { value: 'some-knowledge', label: 'Some industry experience' },
            { value: 'deep-expertise', label: 'Deep domain expertise' },
            { value: 'industry-insider', label: 'Industry insider/thought leader' }
          ]
        },
        {
          id: 'commitment-level',
          type: 'radio',
          label: 'Team Commitment',
          required: true,
          options: [
            { value: 'part-time', label: 'Part-time commitment' },
            { value: 'mostly-full', label: 'Mostly full-time' },
            { value: 'full-time', label: 'All founders full-time' },
            { value: 'bootstrapped', label: 'Full-time + bootstrapped runway' }
          ]
        }
      ]
    },
    {
      id: 'market-opportunity',
      number: 'B',
      title: 'Market Opportunity',
      description: 'Size matters. Help us understand the market you\'re addressing and its potential.',
      weight: 25,
      stages: ['both'],
      fields: [
        {
          id: 'market-size-tam',
          type: 'select',
          label: 'Total Addressable Market (TAM)',
          required: true,
          options: [
            { value: 'under-100m', label: 'Under $100M' },
            { value: '100m-1b', label: '$100M - $1B' },
            { value: '1b-10b', label: '$1B - $10B' },
            { value: 'over-10b', label: 'Over $10B' }
          ],
          tooltip: 'VCs typically look for markets of $1B+ for scalable returns'
        },
        {
          id: 'market-size-som',
          type: 'select',
          label: 'Serviceable Obtainable Market (SOM)',
          required: true,
          options: [
            { value: 'under-10m', label: 'Under $10M' },
            { value: '10m-100m', label: '$10M - $100M' },
            { value: '100m-500m', label: '$100M - $500M' },
            { value: 'over-500m', label: 'Over $500M' }
          ]
        },
        {
          id: 'market-growth',
          type: 'radio',
          label: 'Market Growth Rate',
          required: true,
          options: [
            { value: 'declining', label: 'Declining market' },
            { value: 'stable', label: 'Stable (0-5% growth)' },
            { value: 'growing', label: 'Growing (5-15% growth)' },
            { value: 'exploding', label: 'Exploding (15%+ growth)' }
          ]
        },
        {
          id: 'market-timing',
          type: 'radio',
          label: 'Market Timing',
          required: true,
          options: [
            { value: 'too-early', label: 'Market not ready (too early)' },
            { value: 'emerging', label: 'Emerging market' },
            { value: 'perfect-timing', label: 'Perfect timing' },
            { value: 'mature', label: 'Mature/saturated market' }
          ]
        },
        {
          id: 'customer-segment',
          type: 'textarea',
          label: 'Target Customer Segment',
          required: true,
          placeholder: 'Describe your ideal customer profile, pain points, and buying behavior...',
          tooltip: 'Be specific about demographics, company size, industry, and decision-making process'
        }
      ]
    },
    {
      id: 'problem-solution-fit',
      number: 'C',
      title: 'Problem / Solution Fit',
      description: 'The foundation of any great startup: a real problem with a compelling solution.',
      weight: 20,
      stages: ['both'],
      fields: [
        {
          id: 'problem-severity',
          type: 'radio',
          label: 'Problem Severity',
          required: true,
          options: [
            { value: 'nice-to-have', label: 'Nice-to-have solution' },
            { value: 'moderate-pain', label: 'Moderate pain point' },
            { value: 'significant-pain', label: 'Significant pain point' },
            { value: 'critical-pain', label: 'Critical/urgent pain point' }
          ]
        },
        {
          id: 'problem-frequency',
          type: 'radio',
          label: 'Problem Frequency',
          required: true,
          options: [
            { value: 'rare', label: 'Rare occurrence' },
            { value: 'occasional', label: 'Occasional problem' },
            { value: 'frequent', label: 'Frequent issue' },
            { value: 'daily', label: 'Daily struggle' }
          ]
        },
        {
          id: 'current-solution',
          type: 'radio',
          label: 'Current Solution Landscape',
          required: true,
          options: [
            { value: 'no-solution', label: 'No existing solutions' },
            { value: 'poor-alternatives', label: 'Poor alternatives exist' },
            { value: 'decent-competitors', label: 'Decent competitors exist' },
            { value: 'strong-incumbents', label: 'Strong incumbents dominate' }
          ]
        },
        {
          id: 'solution-uniqueness',
          type: 'radio',
          label: 'Solution Uniqueness',
          required: true,
          options: [
            { value: 'incremental', label: 'Incremental improvement' },
            { value: 'significant-better', label: 'Significantly better' },
            { value: 'breakthrough', label: 'Breakthrough innovation' },
            { value: 'paradigm-shift', label: 'Paradigm shift/new category' }
          ]
        },
        {
          id: 'value-proposition',
          type: 'textarea',
          label: 'Value Proposition',
          required: true,
          placeholder: 'Clearly articulate your unique value proposition and key benefits...',
          tooltip: 'Focus on quantifiable benefits and ROI for customers'
        }
      ]
    },
    {
      id: 'competitive-advantage',
      number: 'D',
      title: 'Competitive Advantage',
      description: 'What makes you defensible? Identify your moats and sustainable competitive advantages.',
      weight: 10,
      stages: ['both'],
      fields: [
        {
          id: 'defensibility',
          type: 'checkbox',
          label: 'Competitive Moats (select all that apply)',
          required: true,
          options: [
            { value: 'network-effects', label: 'Network effects' },
            { value: 'data-moat', label: 'Data advantage' },
            { value: 'technology-ip', label: 'Technology/IP protection' },
            { value: 'brand-loyalty', label: 'Brand & customer loyalty' },
            { value: 'switching-costs', label: 'High switching costs' },
            { value: 'economies-scale', label: 'Economies of scale' },
            { value: 'regulatory', label: 'Regulatory barriers' },
            { value: 'partnerships', label: 'Strategic partnerships' }
          ]
        },
        {
          id: 'ip-protection',
          type: 'radio',
          label: 'Intellectual Property Protection',
          required: true,
          options: [
            { value: 'none', label: 'No IP protection' },
            { value: 'trade-secrets', label: 'Trade secrets/know-how' },
            { value: 'pending-patents', label: 'Pending patents/trademarks' },
            { value: 'granted-ip', label: 'Granted patents/strong IP' }
          ]
        },
        {
          id: 'competitive-timeline',
          type: 'radio',
          label: 'Time to Competitive Response',
          required: true,
          options: [
            { value: 'immediate', label: 'Competitors can copy immediately' },
            { value: 'months', label: '3-6 months to replicate' },
            { value: 'year-plus', label: '1+ years to replicate' },
            { value: 'very-difficult', label: 'Very difficult to replicate' }
          ]
        }
      ]
    },
    {
      id: 'business-model',
      number: 'E',
      title: 'Business Model',
      description: 'Show us how you plan to make money and scale your revenue streams.',
      weight: 15,
      stages: ['both'],
      fields: [
        {
          id: 'revenue-model',
          type: 'radio',
          label: 'Primary Revenue Model',
          required: true,
          options: [
            { value: 'subscription', label: 'Subscription/SaaS' },
            { value: 'transaction', label: 'Transaction fees' },
            { value: 'marketplace', label: 'Marketplace commission' },
            { value: 'advertising', label: 'Advertising/sponsored content' },
            { value: 'enterprise', label: 'Enterprise licensing' },
            { value: 'product-sales', label: 'Product sales' },
            { value: 'freemium', label: 'Freemium model' },
            { value: 'other', label: 'Other/hybrid model' }
          ]
        },
        {
          id: 'pricing-strategy',
          type: 'textarea',
          label: 'Pricing Strategy',
          required: true,
          placeholder: 'Describe your pricing model, tiers, and rationale...',
          tooltip: 'Include pricing research, customer willingness to pay, and competitive positioning'
        },
        {
          id: 'unit-economics-visibility',
          type: 'radio',
          label: 'Unit Economics Understanding',
          required: true,
          options: [
            { value: 'unclear', label: 'Unit economics unclear' },
            { value: 'rough-estimates', label: 'Rough estimates available' },
            { value: 'solid-projections', label: 'Solid projections with data' },
            { value: 'proven-metrics', label: 'Proven metrics from operations' }
          ]
        },
        {
          id: 'scalability',
          type: 'radio',
          label: 'Business Model Scalability',
          required: true,
          options: [
            { value: 'linear', label: 'Linear scaling (1:1 with resources)' },
            { value: 'moderate', label: 'Moderate leverage' },
            { value: 'high-leverage', label: 'High leverage/scalability' },
            { value: 'viral-network', label: 'Viral/network effects' }
          ]
        }
      ]
    },
    {
      id: 'validation-traction',
      number: 'F',
      title: 'Validation & Traction',
      description: 'Evidence that customers want what you\'re building. Show us the traction.',
      weight: 25,
      stages: ['both'],
      fields: [
        {
          id: 'validation-type',
          type: 'checkbox',
          label: 'Validation Evidence (select all that apply)',
          required: true,
          options: [
            { value: 'customer-interviews', label: 'Customer interviews (20+)' },
            { value: 'surveys', label: 'Market surveys' },
            { value: 'loi', label: 'Letters of intent (LOI)' },
            { value: 'pre-orders', label: 'Pre-orders/deposits' },
            { value: 'beta-users', label: 'Beta users/testers' },
            { value: 'pilot-customers', label: 'Pilot customers' },
            { value: 'paying-customers', label: 'Paying customers' },
            { value: 'partnerships', label: 'Strategic partnerships' }
          ]
        },
        {
          id: 'customer-count',
          type: 'select',
          label: 'Customer Base Size',
          required: true,
          options: [
            { value: 'none', label: 'No customers yet' },
            { value: '1-10', label: '1-10 customers' },
            { value: '11-50', label: '11-50 customers' },
            { value: '51-100', label: '51-100 customers' },
            { value: '101-500', label: '101-500 customers' },
            { value: '500+', label: '500+ customers' }
          ]
        }
      ]
    }
  ],
  
  // Additional sections for launched startups
  launchedSections: [
    {
      id: 'unit-economics',
      number: 'G',
      title: 'Unit Economics',
      description: 'The financial foundation of your business. Show us your path to profitability.',
      weight: 20,
      stages: ['launched'],
      fields: [
        {
          id: 'cac',
          type: 'number',
          label: 'Customer Acquisition Cost (CAC)',
          required: true,
          placeholder: '150',
          tooltip: 'Average cost to acquire one paying customer across all channels'
        },
        {
          id: 'ltv',
          type: 'number',
          label: 'Lifetime Value (LTV)',
          required: true,
          placeholder: '500',
          tooltip: 'Total revenue expected from a customer over their lifetime'
        },
        {
          id: 'payback-period',
          type: 'number',
          label: 'Payback Period (months)',
          required: true,
          placeholder: '12',
          tooltip: 'Time to recover customer acquisition costs'
        },
        {
          id: 'gross-margin',
          type: 'number',
          label: 'Gross Margin (%)',
          required: true,
          min: 0,
          max: 100,
          placeholder: '80',
          tooltip: 'Revenue minus cost of goods sold, as percentage'
        },
        {
          id: 'churn-rate',
          type: 'number',
          label: 'Monthly Churn Rate (%)',
          required: true,
          min: 0,
          max: 100,
          placeholder: '5',
          tooltip: 'Percentage of customers lost each month'
        }
      ]
    },
    {
      id: 'financials-capital',
      number: 'H',
      title: 'Financials & Capital Plan',
      description: 'Your financial position and growth funding requirements.',
      weight: 15,
      stages: ['launched'],
      fields: [
        {
          id: 'mrr',
          type: 'select',
          label: 'Monthly Recurring Revenue (MRR)',
          required: true,
          options: [
            { value: 'under-1k', label: 'Under $1K' },
            { value: '1k-10k', label: '$1K - $10K' },
            { value: '10k-50k', label: '$10K - $50K' },
            { value: '50k-100k', label: '$50K - $100K' },
            { value: '100k-500k', label: '$100K - $500K' },
            { value: 'over-500k', label: 'Over $500K' }
          ]
        },
        {
          id: 'growth-rate',
          type: 'number',
          label: 'Month-over-Month Growth Rate (%)',
          required: true,
          min: -50,
          max: 150,
          placeholder: '15',
          tooltip: 'Average monthly revenue growth rate'
        },
        {
          id: 'runway',
          type: 'number',
          label: 'Current Runway (months)',
          required: true,
          placeholder: '18',
          tooltip: 'How long current cash will last at current burn rate'
        },
        {
          id: 'funding-amount',
          type: 'select',
          label: 'Funding Amount Sought',
          required: true,
          options: [
            { value: 'under-500k', label: 'Under $500K' },
            { value: '500k-1m', label: '$500K - $1M' },
            { value: '1m-2m', label: '$1M - $2M' },
            { value: '2m-5m', label: '$2M - $5M' },
            { value: 'over-5m', label: 'Over $5M' }
          ]
        },
        {
          id: 'use-of-funds',
          type: 'textarea',
          label: 'Use of Funds',
          required: true,
          placeholder: 'Describe how you plan to use the investment capital...',
          tooltip: 'Break down spending priorities: team, marketing, product, operations, etc.'
        }
      ]
    }
  ],

  // Scoring matrix for calculating startup scores
  scoringMatrix: {
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
    'market-size-tam': {
      'under-100m': 3,
      '100m-1b': 6,
      '1b-10b': 9,
      'over-10b': 10
    },
    'market-growth': {
      'declining': 2,
      'stable': 5,
      'growing': 8,
      'exploding': 10
    },
    'problem-severity': {
      'nice-to-have': 3,
      'moderate-pain': 6,
      'significant-pain': 8,
      'critical-pain': 10
    },
    'solution-uniqueness': {
      'incremental': 4,
      'significant-better': 7,
      'breakthrough': 9,
      'paradigm-shift': 10
    }
    // Additional scoring rules can be added here
  },

  // Mock AI responses for analysis
  mockAnalyses: {
    executiveSummary: "Based on the comprehensive evaluation, this startup demonstrates strong potential in several key areas. The founding team shows solid domain expertise and technical capabilities, positioned in a growing market with clear customer pain points. However, there are opportunities for improvement in market validation and competitive differentiation strategies.",
    
    deepDiveAnalysis: `**FOUNDING TEAM ANALYSIS (8.5/10)**
The team composition shows promise with complementary skills and industry experience. The combination of technical and domain expertise provides a solid foundation for execution. However, consider strengthening the business development capabilities and ensuring full-time commitment across all key roles.

**MARKET OPPORTUNITY ASSESSMENT (7.8/10)**  
The target market size is substantial with favorable growth trends. Market timing appears optimal given recent technological shifts and changing customer behaviors. The serviceable market segment is well-defined, though competitive dynamics require careful navigation.

**PRODUCT-MARKET FIT EVALUATION (7.2/10)**
Customer pain points are validated through research, with early traction indicators showing promise. The solution approach addresses core problems, but differentiation from existing alternatives needs strengthening. Consider focusing on a more specific niche initially.

**COMPETITIVE POSITIONING (6.9/10)**
While the startup has identified several potential moats, the competitive landscape is evolving rapidly. Intellectual property protection is minimal, requiring accelerated development of network effects and data advantages.

**BUSINESS MODEL VIABILITY (8.1/10)**
The revenue model is well-suited to the target market with clear monetization pathways. Unit economics projections appear reasonable, though validation through real customer data is needed. Scalability potential is strong with proper execution.

**INVESTMENT RECOMMENDATION**
This startup merits serious consideration for seed-stage investment, with the potential for Series A readiness within 18-24 months given proper execution of growth strategies.`
  }
};