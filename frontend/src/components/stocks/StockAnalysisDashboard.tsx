'use client';

import React from 'react';
import { StockAnalysis, InsightMatch } from '@/types';
import { TrendingUp, TrendingDown, DollarSign, BarChart3, Users, Target, AlertTriangle } from 'lucide-react';
import { formatCurrency, formatPercent, formatMarketCap, getRecommendationColor } from '@/lib/utils';
import { InvestorInsightCard } from '@/components/investors/InvestorInsightCard';

interface StockAnalysisDashboardProps {
  analysis: StockAnalysis;
}

const recommendationColors = {
  strong_buy: 'bg-success-500',
  buy: 'bg-success-400',
  hold: 'bg-warning-400',
  sell: 'bg-danger-400',
  strong_sell: 'bg-danger-500',
};

const recommendationLabels = {
  strong_buy: 'Strong Buy',
  buy: 'Buy',
  hold: 'Hold',
  sell: 'Sell',
  strong_sell: 'Strong Sell',
};

export const StockAnalysisDashboard: React.FC<StockAnalysisDashboardProps> = ({
  analysis,
}) => {
  const recommendationPercentage = (analysis.recommendation.score / analysis.recommendation.maxScore) * 100;

  return (
    <div className="max-w-7xl mx-auto p-6 space-y-8">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-navy-900 mb-2">
          {analysis.companyName}
        </h1>
        <p className="text-xl text-navy-600">{analysis.ticker}</p>
      </div>

      {/* Current Price & Recommendation */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Price Card */}
        <div className="card p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-navy-900">Current Price</h3>
            <DollarSign className="w-5 h-5 text-navy-400" />
          </div>

          <div className="space-y-2">
            <div className="text-3xl font-bold text-navy-900">
              ${analysis.currentPrice.toFixed(2)}
            </div>

            <div className={cn(
              'flex items-center text-lg font-medium',
              analysis.change >= 0 ? 'text-success-600' : 'text-danger-600'
            )}>
              {analysis.change >= 0 ? (
                <TrendingUp className="w-5 h-5 mr-1" />
              ) : (
                <TrendingDown className="w-5 h-5 mr-1" />
              )}
              {Math.abs(analysis.change).toFixed(2)} ({formatPercent(analysis.changePercent)})
            </div>
          </div>

          <div className="mt-4 pt-4 border-t border-navy-100">
            <div className="flex justify-between text-sm">
              <span className="text-navy-600">Market Cap</span>
              <span className="font-medium text-navy-900">
                {formatMarketCap(analysis.marketCap)}
              </span>
            </div>
            <div className="flex justify-between text-sm mt-1">
              <span className="text-navy-600">Volume</span>
              <span className="font-medium text-navy-900">
                {analysis.technicalIndicators.averageVolume.toLocaleString()}
              </span>
            </div>
          </div>
        </div>

        {/* Recommendation Card */}
        <div className="card p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-navy-900">Master Recommendation</h3>
            <Target className="w-5 h-5 text-navy-400" />
          </div>

          <div className="space-y-4">
            <div className="text-center">
              <div className={cn(
                'inline-flex items-center px-4 py-2 rounded-full text-white font-semibold text-lg',
                recommendationColors[analysis.recommendation.action]
              )}>
                {recommendationLabels[analysis.recommendation.action]}
              </div>
            </div>

            {/* Score Bar */}
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-navy-600">Confidence</span>
                <span className="font-medium text-navy-900">
                  {analysis.recommendation.score}/{analysis.recommendation.maxScore}
                </span>
              </div>
              <div className="w-full bg-navy-200 rounded-full h-2">
                <div
                  className={cn(
                    'h-2 rounded-full transition-all duration-500',
                    recommendationColors[analysis.recommendation.action]
                  )}
                  style={{ width: `${recommendationPercentage}%` }}
                />
              </div>
            </div>

            <div className="text-sm text-navy-700 leading-relaxed">
              {analysis.recommendation.reasoning}
            </div>

            {analysis.recommendation.targetPrice && (
              <div className="pt-2 border-t border-navy-100">
                <div className="flex justify-between text-sm">
                  <span className="text-navy-600">Target Price</span>
                  <span className="font-medium text-navy-900">
                    ${analysis.recommendation.targetPrice.toFixed(2)}
                  </span>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Financial Metrics */}
      <div className="card p-6">
        <div className="flex items-center mb-6">
          <BarChart3 className="w-5 h-5 mr-2 text-navy-600" />
          <h3 className="text-lg font-semibold text-navy-900">Financial Metrics</h3>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          <div className="text-center">
            <div className="text-2xl font-bold text-navy-900">
              {analysis.financialMetrics.peRatio.toFixed(1)}
            </div>
            <div className="text-sm text-navy-600">P/E Ratio</div>
          </div>

          <div className="text-center">
            <div className="text-2xl font-bold text-navy-900">
              {analysis.financialMetrics.pbRatio.toFixed(1)}
            </div>
            <div className="text-sm text-navy-600">P/B Ratio</div>
          </div>

          <div className="text-center">
            <div className="text-2xl font-bold text-navy-900">
              {formatPercent(analysis.financialMetrics.roe)}
            </div>
            <div className="text-sm text-navy-600">ROE</div>
          </div>

          <div className="text-center">
            <div className="text-2xl font-bold text-navy-900">
              {formatPercent(analysis.financialMetrics.dividendYield)}
            </div>
            <div className="text-sm text-navy-600">Dividend Yield</div>
          </div>
        </div>
      </div>

      {/* Master Investors' Insights */}
      <div className="card p-6">
        <div className="flex items-center mb-6">
          <Users className="w-5 h-5 mr-2 text-navy-600" />
          <h3 className="text-lg font-semibold text-navy-900">
            What the Masters Think About {analysis.companyName}
          </h3>
          {analysis.investorInsights.length > 0 && (
            <span className="ml-auto text-sm text-navy-600">
              {analysis.investorInsights.length} insights found
            </span>
          )}
        </div>

        {analysis.investorInsights.length > 0 ? (
          <div className="grid grid-cols-1 gap-6">
            {analysis.investorInsights.map((match, index) => (
              <div key={index} className="border-l-4 border-primary-500 pl-4">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="font-semibold text-navy-900">{match.investorName}</h4>
                  <div className="flex items-center space-x-2">
                    <span className="text-sm text-navy-600">
                      {getSentimentIcon(match.sentiment)}
                    </span>
                    <span className="text-sm font-medium text-navy-700">
                      {match.matchType.replace('_', ' ')}
                    </span>
                    <span className="text-xs text-navy-500">
                      {(match.confidenceScore * 100).toFixed(0)}% match
                    </span>
                  </div>
                </div>

                <div className="text-navy-700 mb-2 italic">
                  "{match.matchReason}"
                </div>

                {match.investmentThemes.length > 0 && (
                  <div className="flex flex-wrap gap-2">
                    {match.investmentThemes.map((theme, themeIndex) => (
                      <span
                        key={themeIndex}
                        className="px-2 py-1 bg-primary-50 text-primary-700 text-xs rounded-full"
                      >
                        {theme.replace('_', ' ')}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8">
            <AlertTriangle className="w-12 h-12 text-navy-300 mx-auto mb-4" />
            <p className="text-navy-600">
              No master investor insights available for {analysis.companyName}
            </p>
            <p className="text-sm text-navy-500 mt-1">
              Try searching for companies like Apple (AAPL), Coca-Cola (KO), or Bank of America (BAC)
            </p>
          </div>
        )}
      </div>

      {/* Risk Warning */}
      <div className="bg-warning-50 border border-warning-200 rounded-lg p-4">
        <div className="flex items-start">
          <AlertTriangle className="w-5 h-5 text-warning-600 mr-3 flex-shrink-0 mt-0.5" />
          <div>
            <h4 className="font-semibold text-warning-900 mb-1">Investment Disclaimer</h4>
            <p className="text-sm text-warning-800">
              This analysis is based on historical investor insights and should not be considered as financial advice.
              All investments carry risk. Past performance does not guarantee future results.
              Please consult with a qualified financial advisor before making investment decisions.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

function getSentimentIcon(sentiment: string): string {
  if (sentiment.includes('bullish')) return '📈';
  if (sentiment.includes('bearish')) return '📉';
  return '➡️';
}

