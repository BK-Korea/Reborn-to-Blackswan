'use client';

import React, { useState } from 'react';
import { TrendingUp, Brain, Users, Target, Search, Star } from 'lucide-react';
import { Stock, StockAnalysis, Investor, InvestorWithInsights } from '@/types';
import { StockSearchBar } from '@/components/stocks/StockSearchBar';
import { StockAnalysisDashboard } from '@/components/stocks/StockAnalysisDashboard';
import { InvestorInsightCard } from '@/components/investors/InvestorInsightCard';
import { Button } from '@/components/ui/Button';

// Mock data for demo
const mockInvestors: InvestorWithInsights[] = [
  {
    id: 'warren_buffett',
    name: 'Warren Buffett',
    slug: 'warren_buffett',
    title: 'Chairman & CEO, Berkshire Hathaway',
    birthYear: 1930,
    nationality: 'American',
    netWorth: '120+ Billion USD',
    investmentPhilosophy: 'Value investing with focus on companies with strong competitive advantages',
    famousQuotes: [
      "It's far better to buy a wonderful company at a fair price than a fair company at a wonderful price.",
      "Rule No. 1: Never lose money. Rule No. 2: Never forget Rule No. 1."
    ],
    photoUrl: '/images/investors/warren_buffett.jpg',
    insights: [
      {
        id: 'buffett_001',
        investorId: 'warren_buffett',
        content: "Apple has a consumer product that is extraordinarily sticky. People love their iPhone. The whole ecosystem is incredible. And we own a good chunk of it.",
        source: '2023 Berkshire Hathaway Annual Meeting',
        sourceType: 'speech',
        dateSaid: '2023-05-06',
        context: 'Discussing Berkshire\'s investment in Apple and its consumer moat',
        companiesMentioned: ['Apple'],
        sentiment: 'strongly_bullish',
        investmentThemes: ['competitive_advantage', 'consumer_stickiness'],
        confidenceScore: 0.95,
        tags: ['Apple', 'iPhone', 'consumer_moat', 'competitive_advantage']
      }
    ]
  },
  {
    id: 'peter_ynch',
    name: 'Peter Lynch',
    slug: 'peter_ynch',
    title: 'Former Manager, Fidelity Magellan Fund',
    birthYear: 1944,
    nationality: 'American',
    netWorth: '350+ Million USD',
    investmentPhilosophy: 'Growth investing focused on buying what you know',
    famousQuotes: [
      "Invest in what you know.",
      "The key to making money in stocks is not to get scared out of them."
    ],
    photoUrl: '/images/investors/peter_ynch.jpg',
    insights: []
  }
];

const mockStockAnalysis: StockAnalysis = {
  ticker: 'AAPL',
  companyName: 'Apple Inc.',
  exchange: 'NASDAQ',
  sector: 'Technology',
  industry: 'Consumer Electronics',
  marketCap: 4100000000000,
  currentPrice: 273.67,
  change: 2.45,
  changePercent: 0.90,
  financialMetrics: {
    peRatio: 36.6,
    pbRatio: 54.8,
    dividend: 0.96,
    dividendYield: 0.35,
    eps: 7.48,
    revenue: 383285000000,
    netIncome: 99803000000,
    roe: 171.4,
    debtToEquity: 152.4,
    currentRatio: 1.04,
    grossMargin: 45.96
  },
  investorInsights: [
    {
      insightId: 'buffett_001',
      investorId: 'warren_buffett',
      investorName: 'Warren Buffett',
      matchType: 'direct_mention',
      confidenceScore: 0.95,
      matchReason: "Buffett has repeatedly praised Apple's sticky ecosystem and strong brand, calling it one of Berkshire's best investments",
      sentiment: 'strongly_bullish',
      investmentThemes: ['competitive_advantage', 'consumer_stickiness']
    }
  ],
  technicalIndicators: {
    ma50: 269.41,
    ma200: 229.54,
    rsi: 65.2,
    week52High: 286.19,
    week52Low: 171.83,
    averageVolume: 57234567,
    volatility: 21.5
  },
  recommendation: {
    action: 'hold',
    score: 7,
    maxScore: 10,
    reasoning: "While Apple remains a fundamentally strong company with Buffett's endorsement, current valuation (P/E 36.6) suggests waiting for a better entry point. Consider buying on 15-20% pullbacks.",
    riskLevel: 'medium',
    targetPrice: 295.00
  }
};

export default function HomePage() {
  const [selectedStock, setSelectedStock] = useState<Stock | null>(null);
  const [showAnalysis, setShowAnalysis] = useState(false);

  const handleStockSelect = (stock: Stock) => {
    setSelectedStock(stock);
    setShowAnalysis(true);
  };

  const handleSearch = (query: string) => {
    // Mock search - in real app, this would call API
    console.log('Searching for:', query);
  };

  if (showAnalysis && selectedStock) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-navy-50 via-white to-primary-50">
        {/* Navigation */}
        <nav className="glass border-b border-navy-100 sticky top-0 z-40">
          <div className="max-w-7xl mx-auto px-6 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <Brain className="w-8 h-8 text-primary-600" />
                <span className="text-xl font-bold text-navy-900">StockOracle</span>
              </div>
              <Button
                variant="ghost"
                onClick={() => setShowAnalysis(false)}
              >
                ← Back to Search
              </Button>
            </div>
          </div>
        </nav>

        {/* Analysis Dashboard */}
        <StockAnalysisDashboard analysis={mockStockAnalysis} />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-navy-50 via-white to-primary-50">
      {/* Navigation */}
      <nav className="glass border-b border-navy-100">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Brain className="w-8 h-8 text-primary-600" />
              <span className="text-xl font-bold text-navy-900">StockOracle</span>
            </div>
            <div className="flex items-center space-x-4">
              <Button variant="ghost">Features</Button>
              <Button variant="ghost">About</Button>
              <Button>Sign In</Button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="px-6 py-16 md:py-24">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-4xl md:text-6xl font-bold text-navy-900 mb-6">
            Invest Like the
            <span className="text-gradient"> Masters</span>
          </h1>
          <p className="text-xl md:text-2xl text-navy-600 mb-8 leading-relaxed">
            Get investment insights from Warren Buffett, Peter Lynch, Charlie Munger,
            and other legendary investors. Stop guessing. Start investing with wisdom.
          </p>

          {/* Search Bar */}
          <div className="mb-12">
            <StockSearchBar
              onSearch={handleSearch}
              onStockSelect={handleStockSelect}
              suggestions={[
                {
                  ticker: 'AAPL',
                  companyName: 'Apple Inc.',
                  exchange: 'NASDAQ',
                  sector: 'Technology',
                  industry: 'Consumer Electronics',
                  marketCap: 4100000000000,
                  currentPrice: 273.67,
                  change: 2.45,
                  changePercent: 0.90
                }
              ]}
            />
          </div>

          {/* Quick Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-16">
            <div className="text-center">
              <div className="text-3xl font-bold text-primary-600 mb-2">50+</div>
              <div className="text-sm text-navy-600">Master Investors</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-primary-600 mb-2">10,000+</div>
              <div className="text-sm text-navy-600">Verified Insights</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-primary-600 mb-2">AI-Powered</div>
              <div className="text-sm text-navy-600">Smart Matching</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-primary-600 mb-2">Real-Time</div>
              <div className="text-sm text-navy-600">Market Analysis</div>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Insights */}
      <section className="px-6 py-16 bg-white">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-navy-900 mb-4">
              Latest Master Insights
            </h2>
            <p className="text-lg text-navy-600">
              See what the world's greatest investors are saying right now
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {mockInvestors.map((investor) =>
              investor.insights.slice(0, 2).map((insight) => (
                <InvestorInsightCard
                  key={insight.id}
                  insight={insight}
                  investor={investor}
                />
              ))
            )}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="px-6 py-16">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-navy-900 mb-4">
              How StockOracle Works
            </h2>
            <p className="text-lg text-navy-600">
              Three simple steps to smarter investing
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Search className="w-8 h-8 text-primary-600" />
              </div>
              <h3 className="text-xl font-semibold text-navy-900 mb-2">
                1. Search Any Stock
              </h3>
              <p className="text-navy-600">
                Enter a ticker or company name to get comprehensive analysis
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Brain className="w-8 h-8 text-primary-600" />
              </div>
              <h3 className="text-xl font-semibold text-navy-900 mb-2">
                2. Get Master Wisdom
              </h3>
              <p className="text-navy-600">
                Our AI analyzes decades of insights from legendary investors
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Target className="w-8 h-8 text-primary-600" />
              </div>
              <h3 className="text-xl font-semibold text-navy-900 mb-2">
                3. Make Better Decisions
              </h3>
              <p className="text-navy-600">
                Invest with confidence using time-tested strategies
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="px-6 py-16 bg-gradient-to-r from-primary-600 to-emerald-600">
        <div className="max-w-4xl mx-auto text-center">
          <Star className="w-16 h-16 text-white mx-auto mb-6" />
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
            Ready to Invest Like a Master?
          </h2>
          <p className="text-xl text-white/90 mb-8">
            Join thousands of investors who are already making smarter decisions
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" className="bg-white text-primary-600 hover:bg-gray-100">
              Start Free Trial
            </Button>
            <Button size="lg" variant="secondary" className="border-white text-white hover:bg-white/10">
              Watch Demo
            </Button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-navy-900 text-white px-6 py-12">
        <div className="max-w-6xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <Brain className="w-6 h-6" />
                <span className="font-bold">StockOracle</span>
              </div>
              <p className="text-navy-400 text-sm">
                Invest with the wisdom of the world's greatest investors.
              </p>
            </div>

            <div>
              <h4 className="font-semibold mb-4">Product</h4>
              <ul className="space-y-2 text-sm text-navy-400">
                <li>Features</li>
                <li>Pricing</li>
                <li>API</li>
              </ul>
            </div>

            <div>
              <h4 className="font-semibold mb-4">Company</h4>
              <ul className="space-y-2 text-sm text-navy-400">
                <li>About</li>
                <li>Blog</li>
                <li>Careers</li>
              </ul>
            </div>

            <div>
              <h4 className="font-semibold mb-4">Legal</h4>
              <ul className="space-y-2 text-sm text-navy-400">
                <li>Privacy</li>
                <li>Terms</li>
                <li>Disclaimer</li>
              </ul>
            </div>
          </div>

          <div className="border-t border-navy-800 mt-8 pt-8 text-center text-sm text-navy-400">
            <p>&copy; 2025 StockOracle. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}