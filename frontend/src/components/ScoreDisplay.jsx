import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';

const ScoreDisplay = ({ score, verdict, icon, sectionScores, executiveSummary }) => {
  const [animatedScore, setAnimatedScore] = useState(0);
  const [isAnimating, setIsAnimating] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setAnimatedScore(score);
      setIsAnimating(false);
    }, 500);

    return () => clearTimeout(timer);
  }, [score]);

  const getScoreColor = (score) => {
    if (score >= 90) return 'text-yellow-400 border-yellow-400';
    if (score >= 80) return 'text-green-400 border-green-400';
    if (score >= 70) return 'text-blue-400 border-blue-400';
    if (score >= 60) return 'text-orange-400 border-orange-400';
    return 'text-red-400 border-red-400';
  };

  const getBackgroundGradient = (score) => {
    if (score >= 90) return 'from-yellow-900/20 to-yellow-800/10';
    if (score >= 80) return 'from-green-900/20 to-green-800/10';
    if (score >= 70) return 'from-blue-900/20 to-blue-800/10';
    if (score >= 60) return 'from-orange-900/20 to-orange-800/10';
    return 'from-red-900/20 to-red-800/10';
  };

  const circumference = 2 * Math.PI * 50; // radius = 50
  const strokeDasharray = circumference;
  const strokeDashoffset = circumference - (animatedScore / 100) * circumference;

  return (
    <Card className={`bg-gradient-to-br ${getBackgroundGradient(score)} border-slate-700`}>
      <CardHeader className="text-center pb-4">
        <CardTitle className="text-2xl text-white mb-2">Your VC Analysis Results</CardTitle>
        <p className="text-slate-300">
          Evaluated using the methodology of legendary VCs Marc Andreessen, Ben Horowitz, and Mike Moritz
        </p>
      </CardHeader>
      <CardContent className="text-center">
        <div className="flex flex-col items-center gap-8">
          {/* Animated Score Circle */}
          <div className="relative">
            <svg className="transform -rotate-90 w-32 h-32" viewBox="0 0 120 120">
              {/* Background circle */}
              <circle
                cx="60"
                cy="60"
                r="50"
                stroke="currentColor"
                strokeWidth="8"
                fill="none"
                className="text-slate-700"
              />
              {/* Progress circle */}
              <circle
                cx="60"
                cy="60"
                r="50"
                stroke="currentColor"
                strokeWidth="8"
                fill="none"
                strokeDasharray={strokeDasharray}
                strokeDashoffset={strokeDashoffset}
                className={`${getScoreColor(score).split(' ')[0]} transition-all duration-1000 ease-out`}
                strokeLinecap="round"
              />
            </svg>
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="text-center">
                <div className={`text-3xl font-bold ${getScoreColor(score).split(' ')[0]} ${isAnimating ? 'animate-pulse' : ''}`}>
                  {Math.round(animatedScore)}
                </div>
                <div className="text-sm text-slate-400">/ 100</div>
              </div>
            </div>
          </div>

          {/* Verdict */}
          <div className="flex items-center gap-4">
            {icon}
            <div>
              <div className="flex items-center gap-2 mb-1">
                <span className="text-2xl">{verdict.emoji}</span>
                <h3 className={`text-xl font-bold ${getScoreColor(score).split(' ')[0]}`}>
                  {verdict.text}
                </h3>
              </div>
              <Badge variant="outline" className={getScoreColor(score)}>
                Investment Readiness Score
              </Badge>
            </div>
          </div>

          {/* Executive Summary */}
          <div className="bg-slate-800/50 rounded-lg p-6 text-left w-full">
            <h4 className="text-lg font-semibold text-white mb-3">Executive Summary</h4>
            <p className="text-slate-300 leading-relaxed">
              {executiveSummary || "Analysis completed. Your startup has been evaluated using our comprehensive scoring methodology."}
            </p>
          </div>

          {/* Score Breakdown */}
          <div className="w-full">
            <h4 className="text-lg font-semibold text-white mb-4">Score Breakdown</h4>
            <div className="grid gap-3">
              {[
                { category: 'Founding Team', weight: 30, score: Math.round(score * 0.85) },
                { category: 'Market Opportunity', weight: 25, score: Math.round(score * 0.92) },
                { category: 'Problem/Solution Fit', weight: 20, score: Math.round(score * 0.88) },
                { category: 'Business Model', weight: 15, score: Math.round(score * 0.91) },
                { category: 'Competitive Advantage', weight: 10, score: Math.round(score * 0.79) }
              ].map((item, index) => (
                <div key={index} className="flex items-center justify-between bg-slate-800/30 rounded p-3">
                  <div className="flex items-center gap-3">
                    <span className="text-slate-300">{item.category}</span>
                    <Badge variant="outline" className="text-xs text-slate-400 border-slate-500">
                      {item.weight}% weight
                    </Badge>
                  </div>
                  <div className={`font-semibold ${getScoreColor(item.score).split(' ')[0]}`}>
                    {item.score}/100
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default ScoreDisplay;