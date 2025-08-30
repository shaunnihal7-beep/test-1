import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Lock, Unlock, CreditCard, CheckCircle, Star } from 'lucide-react';
import { toast } from '../hooks/use-toast';
import { createPaymentIntent, unlockPremiumAnalysis } from '../services/vcTestApi';

const PremiumUnlock = ({ isUnlocked, onUnlock, evaluationId, score }) => {
  const [isProcessing, setIsProcessing] = useState(false);
  const [premiumData, setPremiumData] = useState(null);

  const handleUnlockPremium = async () => {
    setIsProcessing(true);
    
    try {
      // Create payment intent (in mock mode, this will simulate success)
      const paymentResult = await createPaymentIntent(evaluationId);
      
      if (!paymentResult.success) {
        throw new Error(paymentResult.error);
      }

      // Simulate payment processing delay
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Unlock premium analysis (in mock mode, this will return mock data)
      const unlockResult = await unlockPremiumAnalysis(evaluationId, paymentResult.data.payment_intent_id);
      
      if (!unlockResult.success) {
        throw new Error(unlockResult.error);
      }

      setPremiumData(unlockResult.data);
      onUnlock(true);
      
      toast({
        title: "Premium Unlocked! 🎉",
        description: "Your detailed analysis is now available.",
        duration: 5000
      });
    } catch (error) {
      console.error('Payment error:', error);
      toast({
        title: "Payment Failed",
        description: error.message || "Please try again or contact support.",
        variant: "destructive"
      });
    } finally {
      setIsProcessing(false);
    }
  };

  if (isUnlocked) {
    return (
      <Card className="bg-gradient-to-br from-green-900/20 to-green-800/10 border-green-700">
        <CardHeader className="text-center">
          <div className="flex items-center justify-center gap-2 mb-2">
            <Unlock className="h-6 w-6 text-green-400" />
            <CardTitle className="text-xl text-white">Premium Analysis Unlocked</CardTitle>
          </div>
          <Badge variant="outline" className="text-green-400 border-green-400 w-fit mx-auto">
            <CheckCircle className="h-3 w-3 mr-1" />
            Premium Access
          </Badge>
        </CardHeader>
        <CardContent>
          <div className="bg-slate-800/50 rounded-lg p-6">
            <h4 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
              <Star className="h-5 w-5 text-yellow-400" />
              Detailed VC Analysis Report
            </h4>
            <div className="prose prose-slate prose-invert max-w-none">
              <div className="text-slate-300 leading-relaxed whitespace-pre-line">
                {mockData.mockAnalyses.deepDiveAnalysis}
              </div>
            </div>
          </div>
          
          <div className="mt-6 grid md:grid-cols-3 gap-4">
            <div className="bg-slate-800/30 rounded-lg p-4 text-center">
              <h5 className="font-semibold text-white mb-2">Investment Readiness</h5>
              <div className="text-2xl font-bold text-cyan-400">
                {score >= 80 ? 'Ready' : score >= 60 ? 'Near Ready' : 'Early Stage'}
              </div>
            </div>
            <div className="bg-slate-800/30 rounded-lg p-4 text-center">
              <h5 className="font-semibold text-white mb-2">Recommended Round</h5>
              <div className="text-2xl font-bold text-cyan-400">
                {score >= 80 ? 'Series A' : score >= 60 ? 'Seed' : 'Pre-Seed'}
              </div>
            </div>
            <div className="bg-slate-800/30 rounded-lg p-4 text-center">
              <h5 className="font-semibold text-white mb-2">Valuation Range</h5>
              <div className="text-2xl font-bold text-cyan-400">
                {score >= 80 ? '$10M+' : score >= 60 ? '$3-10M' : '$0.5-3M'}
              </div>
            </div>
          </div>

          <div className="mt-6 bg-blue-900/20 border border-blue-700 rounded-lg p-4">
            <h5 className="font-semibold text-blue-300 mb-2">Next Steps Recommendation</h5>
            <ul className="text-blue-200 text-sm space-y-1">
              <li>• Focus on customer validation and early traction metrics</li>
              <li>• Strengthen competitive moats and IP protection</li>
              <li>• Prepare detailed financial projections and unit economics</li>
              <li>• Build strategic advisor network in target industry</li>
              <li>• Develop comprehensive go-to-market strategy</li>
            </ul>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="bg-gradient-to-br from-blue-900/20 to-purple-800/10 border-slate-700">
      <CardHeader className="text-center">
        <div className="flex items-center justify-center gap-2 mb-2">
          <Lock className="h-6 w-6 text-slate-400" />
          <CardTitle className="text-xl text-white">Unlock Deep-Dive Analysis</CardTitle>
        </div>
        <p className="text-slate-300">
          Get a comprehensive 600-word analysis from legendary VC perspectives
        </p>
      </CardHeader>
      <CardContent>
        {/* Blurred Preview */}
        <div className="relative mb-6">
          <div className="bg-slate-800/50 rounded-lg p-6 overflow-hidden">
            <h4 className="text-lg font-semibold text-white mb-4">Premium Analysis Preview</h4>
            <div className="filter blur-sm pointer-events-none select-none">
              <div className="text-slate-300 leading-relaxed">
                <p className="mb-4">
                  <strong>FOUNDING TEAM DEEP ANALYSIS</strong><br />
                  The team composition reveals sophisticated understanding of market dynamics with complementary skill sets that position the startup for rapid execution...
                </p>
                <p className="mb-4">
                  <strong>MARKET PENETRATION STRATEGY</strong><br />
                  Based on TAM/SAM analysis and competitive landscape mapping, the startup has identified a clear path to capturing significant market share through...
                </p>
                <p>
                  <strong>FINANCIAL PROJECTIONS & SCENARIOS</strong><br />
                  Conservative, base, and optimistic scenarios project revenue trajectories that align with successful unicorn companies at similar stages...
                </p>
              </div>
            </div>
          </div>
          <div className="absolute inset-0 bg-gradient-to-t from-slate-900 via-transparent to-transparent flex items-end justify-center pb-4">
            <Badge className="bg-slate-700 text-white">
              <Lock className="h-3 w-3 mr-1" />
              Premium Content
            </Badge>
          </div>
        </div>

        {/* Premium Features */}
        <div className="grid md:grid-cols-2 gap-6 mb-6">
          <div className="space-y-4">
            <h5 className="font-semibold text-white">What You'll Get:</h5>
            <ul className="space-y-2 text-slate-300">
              <li className="flex items-center gap-2">
                <CheckCircle className="h-4 w-4 text-green-400 flex-shrink-0" />
                Detailed team assessment & recommendations
              </li>
              <li className="flex items-center gap-2">
                <CheckCircle className="h-4 w-4 text-green-400 flex-shrink-0" />
                Market strategy & competitive analysis
              </li>
              <li className="flex items-center gap-2">
                <CheckCircle className="h-4 w-4 text-green-400 flex-shrink-0" />
                Investment readiness scorecard
              </li>
              <li className="flex items-center gap-2">
                <CheckCircle className="h-4 w-4 text-green-400 flex-shrink-0" />
                Valuation range & funding recommendations
              </li>
              <li className="flex items-center gap-2">
                <CheckCircle className="h-4 w-4 text-green-400 flex-shrink-0" />
                Actionable next steps roadmap
              </li>
            </ul>
          </div>
          
          <div className="bg-slate-800/30 rounded-lg p-4 text-center">
            <div className="text-3xl font-bold text-cyan-400 mb-2">$9.99</div>
            <div className="text-slate-400 text-sm mb-4">One-time payment</div>
            <div className="text-xs text-slate-500">
              ✓ Instant access<br />
              ✓ No subscription<br />
              ✓ 30-day money-back guarantee
            </div>
          </div>
        </div>

        {/* CTA Button */}
        <Button 
          onClick={handleUnlockPremium}
          disabled={isProcessing}
          className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white py-3 text-lg font-semibold"
        >
          {isProcessing ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent mr-2"></div>
              Processing Payment...
            </>
          ) : (
            <>
              <CreditCard className="h-5 w-5 mr-2" />
              Unlock Premium Analysis - $9.99
            </>
          )}
        </Button>

        <p className="text-xs text-slate-500 text-center mt-4">
          Secure payment powered by Stripe • 256-bit SSL encryption
        </p>
      </CardContent>
    </Card>
  );
};

export default PremiumUnlock;