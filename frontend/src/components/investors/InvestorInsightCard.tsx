'use client';

import React from 'react';
import { InvestorInsight, Investor } from '@/types';
import { formatDate, getSentimentColor, getSentimentBgColor, getSentimentIcon, cn } from '@/lib/utils';
import { TrendingUp, TrendingDown, Minus, Calendar, FileText, MessageCircle, Twitter, Book } from 'lucide-react';

interface InvestorInsightCardProps {
  insight: InvestorInsight;
  investor: Investor;
  showInvestor?: boolean;
  compact?: boolean;
  className?: string;
}

const sourceTypeIcons = {
  annual_letter: FileText,
  interview: MessageCircle,
  speech: MessageCircle,
  book: Book,
  memo: FileText,
  tweet: Twitter,
};

const sourceTypeLabels = {
  annual_letter: 'Annual Letter',
  interview: 'Interview',
  speech: 'Speech',
  book: 'Book',
  memo: 'Memo',
  tweet: 'Tweet',
};

export function InvestorInsightCard({
  insight,
  investor,
  showInvestor = true,
  compact = false,
  className,
}: InvestorInsightCardProps) {
  const Icon = sourceTypeIcons[insight.sourceType] || MessageCircle;

  const sentimentStr = String(insight.sentiment);
  
  return (
    <div className={cn(
      'card border-l-4 transition-all duration-300 hover:shadow-xl group',
      getSentimentBgColor(insight.sentiment),
      sentimentStr.includes('bullish') && 'border-l-success-500',
      sentimentStr.includes('bearish') && 'border-l-danger-500',
      insight.sentiment === 'neutral' && 'border-l-gray-400',
      compact && 'p-4',
      !compact && 'p-6',
      className
    )}>
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        {showInvestor && (
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-full bg-navy-100 flex items-center justify-center">
              <span className="text-navy-700 font-semibold text-sm">
                {investor.name.split(' ').map(n => n[0]).join('')}
              </span>
            </div>
            <div>
              <h3 className="font-semibold text-navy-900">{investor.name}</h3>
              <p className="text-sm text-navy-600">{investor.title}</p>
            </div>
          </div>
        )}

        <div className="flex items-center space-x-2">
          {/* Sentiment Badge */}
          <div className={cn(
            'inline-flex items-center space-x-1 px-2 py-1 rounded-full text-xs font-medium',
            getSentimentBgColor(insight.sentiment),
            getSentimentColor(insight.sentiment)
          )}>
            <span>{getSentimentIcon(insight.sentiment)}</span>
            <span className="capitalize">
              {insight.sentiment.replace('_', ' ')}
            </span>
          </div>

          {/* Confidence Score */}
          <div className="text-xs text-navy-500 font-medium">
            {(insight.confidenceScore * 100).toFixed(0)}% confidence
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="mb-4">
        <blockquote className={cn(
          'text-navy-700 leading-relaxed',
          compact ? 'text-sm' : 'text-base'
        )}>
          "{insight.content}"
        </blockquote>
      </div>

      {/* Meta Information */}
      <div className="flex items-center justify-between text-sm">
        <div className="flex items-center space-x-4 text-navy-500">
          {/* Source Type */}
          <div className="flex items-center space-x-1">
            <Icon className="w-4 h-4" />
            <span>{sourceTypeLabels[insight.sourceType]}</span>
          </div>

          {/* Date */}
          <div className="flex items-center space-x-1">
            <Calendar className="w-4 h-4" />
            <span>{formatDate(insight.dateSaid)}</span>
          </div>
        </div>

        {/* Companies Mentioned */}
        {insight.companiesMentioned.length > 0 && (
          <div className="flex items-center space-x-1">
            <TrendingUp className="w-4 h-4 text-navy-400" />
            <span className="text-navy-600 font-medium">
              {insight.companiesMentioned.join(', ')}
            </span>
          </div>
        )}
      </div>

      {/* Investment Themes */}
      {insight.investmentThemes.length > 0 && !compact && (
        <div className="mt-4 pt-4 border-t border-navy-100">
          <div className="flex flex-wrap gap-2">
            {insight.investmentThemes.map((theme, index) => (
              <span
                key={index}
                className="px-2 py-1 bg-navy-100 text-navy-700 text-xs rounded-full font-medium"
              >
                {theme.replace('_', ' ')}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Tags */}
      {insight.tags.length > 0 && !compact && (
        <div className="mt-3">
          <div className="flex flex-wrap gap-1">
            {insight.tags.slice(0, 5).map((tag, index) => (
              <span
                key={index}
                className="text-xs text-navy-500 bg-navy-50 px-2 py-1 rounded"
              >
                #{tag}
              </span>
            ))}
            {insight.tags.length > 5 && (
              <span className="text-xs text-navy-500">
                +{insight.tags.length - 5} more
              </span>
            )}
          </div>
        </div>
      )}

      {/* Hover Effect */}
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none" />
    </div>
  );
};

