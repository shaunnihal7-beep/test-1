import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Progress } from './ui/progress';
import { ChevronDown, ChevronUp, Lock, TrendingUp, Star, Award, AlertTriangle } from 'lucide-react';
import { toast } from '../hooks/use-toast';
import QuestionnaireSection from './QuestionnaireSection';
import ScoreDisplay from './ScoreDisplay';
import PremiumUnlock from './PremiumUnlock';
import { mockData } from '../data/mockData';
import { 
  generateCSRFToken, 
  generateUUID, 
  validateSubmission, 
  submitEvaluation 
} from '../services/vcTestApi';

const VCTest = () => {
  const [startupType, setStartupType] = useState('');
  const [formData, setFormData] = useState({});
  const [expandedSections, setExpandedSections] = useState({});
  const [completionPercentages, setCompletionPercentages] = useState({});
  const [evaluationResult, setEvaluationResult] = useState(null);
  const [showResults, setShowResults] = useState(false);
  const [isPremiumUnlocked, setIsPremiumUnlocked] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [startTime] = useState(Date.now());
  const [sessionMetadata] = useState({
    start_time: Date.now(),
    csrf_token: generateCSRFToken(),
    user_uuid: generateUUID()
  });

  // Add honeypot field (hidden from users)
  useEffect(() => {
    setFormData(prev => ({ ...prev, _bot_field: '' }));
  }, []);

  const sections = mockData.sections;

  useEffect(() => {
    // Calculate completion percentages
    const percentages = {};
    sections.forEach(section => {
      if (startupType && (section.stages.includes('both') || section.stages.includes(startupType))) {
        const sectionFields = section.fields;
        const completedFields = sectionFields.filter(field => {
          const value = formData[field.id];
          return value !== undefined && value !== '' && value !== null && 
                 (!Array.isArray(value) || value.length > 0);
        }).length;
        percentages[section.id] = Math.round((completedFields / sectionFields.length) * 100);
      }
    });

    // Add launched-specific sections
    if (startupType === 'launched') {
      mockData.launchedSections.forEach(section => {
        const sectionFields = section.fields;
        const completedFields = sectionFields.filter(field => {
          const value = formData[field.id];
          return value !== undefined && value !== '' && value !== null;
        }).length;
        percentages[section.id] = Math.round((completedFields / sectionFields.length) * 100);
      });
    }

    setCompletionPercentages(percentages);
  }, [formData, startupType, sections]);

  const handleStartupTypeSelect = (type) => {
    setStartupType(type);
    setFormData({ _bot_field: '' }); // Reset with honeypot
    setExpandedSections({});
    setShowResults(false);
    setEvaluationResult(null);
    setIsPremiumUnlocked(false);
  };

  const toggleSection = (sectionId) => {
    setExpandedSections(prev => ({
      ...prev,
      [sectionId]: !prev[sectionId]
    }));
  };

  const updateFormData = (fieldId, value) => {
    setFormData(prev => ({
      ...prev,
      [fieldId]: value
    }));
  };

  const handleSubmit = async () => {
    setIsLoading(true);
    
    try {
      // First validate the submission
      const validation = await validateSubmission(formData, sessionMetadata, startupType);
      
      if (!validation.success) {
        const errorMessage = validation.validation_errors?.length > 0 
          ? `Validation errors: ${validation.validation_errors.join(', ')}`
          : validation.anti_gaming_flags?.length > 0 
            ? `Security check failed: ${validation.anti_gaming_flags.join(', ')}`
            : 'Validation failed';
        
        toast({
          title: "Submission Error",
          description: errorMessage,
          variant: "destructive"
        });
        return;
      }

      // Submit for evaluation
      const result = await submitEvaluation(formData, sessionMetadata, startupType);
      
      if (!result.success) {
        toast({
          title: "Evaluation Error",
          description: result.error || 'Failed to evaluate startup',
          variant: "destructive"
        });
        return;
      }

      setEvaluationResult(result.data);
      setShowResults(true);
      
      toast({
        title: "Analysis Complete! 🎉",
        description: "Your startup has been evaluated by our AI system.",
        duration: 5000
      });

    } catch (error) {
      console.error('Submission error:', error);
      toast({
        title: "System Error",
        description: "An unexpected error occurred. Please try again.",
        variant: "destructive"
      });
    } finally {
      setIsLoading(false);
    }
  };

  const getScoreIcon = (score) => {
    if (score >= 90) return <Award className="h-6 w-6 text-yellow-500" />;
    if (score >= 80) return <TrendingUp className="h-6 w-6 text-green-500" />;
    if (score >= 70) return <Star className="h-6 w-6 text-blue-500" />;
    if (score >= 60) return <ChevronUp className="h-6 w-6 text-orange-500" />;
    return <AlertTriangle className="h-6 w-6 text-red-500" />;
  };

  const getScoreVerdict = (score) => {
    if (score >= 90) return { emoji: "🦄", text: "Unicorn Potential" };
    if (score >= 80) return { emoji: "🚀", text: "Strong Candidate" };
    if (score >= 70) return { emoji: "📈", text: "Promising but Needs Work" };
    if (score >= 60) return { emoji: "🔧", text: "Early Potential" };
    return { emoji: "⚠️", text: "Not Investment-Ready" };
  };

  const overallCompletion = Object.keys(completionPercentages).length > 0 
    ? Math.round(Object.values(completionPercentages).reduce((a, b) => a + b, 0) / Object.keys(completionPercentages).length)
    : 0;

  const allSections = startupType === 'launched' 
    ? [...sections.filter(s => s.stages.includes('both') || s.stages.includes(startupType)), ...mockData.launchedSections]
    : sections.filter(s => s.stages.includes('both') || s.stages.includes(startupType));

  if (!startupType) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
        <div className="container mx-auto px-4 py-16">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-5xl font-bold text-white mb-6 bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
              VC Investor Test
            </h1>
            <p className="text-xl text-slate-300 mb-12 max-w-2xl mx-auto">
              Get your startup evaluated by legendary VCs. Receive a comprehensive analysis of your business potential and investment readiness.
            </p>
            
            <div className="grid md:grid-cols-2 gap-8 mt-16">
              <Card className="bg-slate-800/50 border-slate-700 hover:bg-slate-800/70 transition-all duration-300 cursor-pointer group" 
                    onClick={() => handleStartupTypeSelect('idea')}>
                <CardHeader className="text-center pb-4">
                  <div className="text-4xl mb-4 group-hover:scale-110 transition-transform">💡</div>
                  <CardTitle className="text-2xl text-white">I only have a startup idea</CardTitle>
                </CardHeader>
                <CardContent className="text-center">
                  <p className="text-slate-300 mb-6">
                    Perfect for early-stage entrepreneurs with a concept ready for validation and funding.
                  </p>
                  <ul className="text-sm text-slate-400 space-y-2">
                    <li>• Founding Team Assessment</li>
                    <li>• Market Opportunity Analysis</li>
                    <li>• Problem-Solution Fit</li>
                    <li>• Business Model Validation</li>
                    <li>• Pre-launch Traction</li>
                  </ul>
                </CardContent>
              </Card>

              <Card className="bg-slate-800/50 border-slate-700 hover:bg-slate-800/70 transition-all duration-300 cursor-pointer group" 
                    onClick={() => handleStartupTypeSelect('launched')}>
                <CardHeader className="text-center pb-4">
                  <div className="text-4xl mb-4 group-hover:scale-110 transition-transform">🏢</div>
                  <CardTitle className="text-2xl text-white">I already launched</CardTitle>
                </CardHeader>
                <CardContent className="text-center">
                  <p className="text-slate-300 mb-6">
                    For existing startups with products in market seeking growth capital and scaling strategies.
                  </p>
                  <ul className="text-sm text-slate-400 space-y-2">
                    <li>• Revenue & Growth Metrics</li>
                    <li>• Unit Economics Analysis</li>
                    <li>• Customer Acquisition</li>
                    <li>• Financial Projections</li>
                    <li>• Scaling Strategy</li>
                  </ul>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-white mb-4 bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
              VC Investor Test
            </h1>
            <div className="flex items-center justify-center gap-4 mb-6">
              <Badge variant="outline" className="text-cyan-400 border-cyan-400">
                {startupType === 'idea' ? '💡 Idea Stage' : '🏢 Launched Startup'}
              </Badge>
              <Button 
                variant="ghost" 
                size="sm" 
                onClick={() => handleStartupTypeSelect('')}
                className="text-slate-400 hover:text-white"
              >
                Change Type
              </Button>
            </div>
            
            {/* Overall Progress */}
            <div className="bg-slate-800/50 rounded-lg p-4 mb-8">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-slate-300">Overall Completion</span>
                <span className="text-sm font-medium text-cyan-400">{overallCompletion}%</span>
              </div>
              <Progress value={overallCompletion} className="h-2" />
            </div>
          </div>

          {/* Questionnaire Sections */}
          <div className="space-y-6 mb-8">
            {allSections.map((section) => (
              <QuestionnaireSection
                key={section.id}
                section={section}
                isExpanded={expandedSections[section.id]}
                onToggle={() => toggleSection(section.id)}
                completion={completionPercentages[section.id] || 0}
                formData={formData}
                updateFormData={updateFormData}
              />
            ))}
          </div>

          {/* Submit Button */}
          <div className="text-center mb-8">
            <Button 
              onClick={handleSubmit}
              disabled={overallCompletion < 100 || isLoading}
              className="bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 text-white px-8 py-3 text-lg font-semibold disabled:opacity-50"
            >
              {isLoading ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent mr-2"></div>
                  Analyzing...
                </>
              ) : overallCompletion < 100 ? 
                `Complete Form (${overallCompletion}%)` : 
                'Get My VC Analysis'
              }
            </Button>
          </div>

          {/* Results */}
          {showResults && evaluationResult && (
            <div className="space-y-8">
              <ScoreDisplay 
                score={evaluationResult.total_score}
                verdict={evaluationResult.verdict}
                icon={getScoreIcon(evaluationResult.total_score)}
                sectionScores={evaluationResult.section_scores}
                executiveSummary={evaluationResult.executive_summary}
              />
              
              <PremiumUnlock 
                isUnlocked={isPremiumUnlocked}
                onUnlock={setIsPremiumUnlocked}
                evaluationId={evaluationResult.evaluation_id}
                score={evaluationResult.total_score}
              />
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default VCTest;