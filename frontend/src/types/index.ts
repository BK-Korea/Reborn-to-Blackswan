// Investor Types
export interface Investor {
  id: string;
  name: string;
  slug: string;
  title: string;
  birthYear: number;
  nationality: string;
  netWorth: string;
  investmentPhilosophy: string;
  famousQuotes: string[];
  photoUrl: string;
}

export interface InvestorInsight {
  id: string;
  investorId: string;
  content: string;
  source: string;
  sourceType: 'annual_letter' | 'interview' | 'speech' | 'book' | 'memo' | 'tweet';
  dateSaid: string;
  context: string;
  companiesMentioned: string[];
  sentiment: 'strongly_bullish' | 'bullish' | 'cautiously_bullish' | 'neutral' | 'cautiously_bearish' | 'bearish' | 'strongly_bearish';
  investmentThemes: string[];
  confidenceScore: number;
  tags: string[];
}

export interface InvestorWithInsights extends Investor {
  insights: InvestorInsight[];
}

// Stock Types
export interface Stock {
  ticker: string;
  companyName: string;
  exchange: string;
  sector: string;
  industry: string;
  marketCap: number;
  currentPrice: number;
  change: number;
  changePercent: number;
}

export interface FinancialMetrics {
  peRatio: number;
  pbRatio: number;
  dividend: number;
  dividendYield: number;
  eps: number;
  revenue: number;
  netIncome: number;
  roe: number;
  debtToEquity: number;
  currentRatio: number;
  grossMargin: number;
}

export interface StockAnalysis extends Stock {
  financialMetrics: FinancialMetrics;
  investorInsights: InsightMatch[];
  technicalIndicators: TechnicalIndicators;
  recommendation: Recommendation;
}

export interface InsightMatch {
  insightId: string;
  investorId: string;
  investorName: string;
  matchType: 'direct_mention' | 'semantic' | 'theme_based';
  confidenceScore: number;
  matchReason: string;
  sentiment: string;
  investmentThemes: string[];
}

export interface TechnicalIndicators {
  ma50: number;
  ma200: number;
  rsi: number;
  week52High: number;
  week52Low: number;
  averageVolume: number;
  volatility: number;
}

export interface Recommendation {
  action: 'strong_buy' | 'buy' | 'hold' | 'sell' | 'strong_sell';
  score: number;
  maxScore: number;
  reasoning: string;
  riskLevel: 'low' | 'medium' | 'high';
  targetPrice?: number;
}

// Market Types
export interface MarketOverview {
  indices: {
    sp500: IndexData;
    nasdaq: IndexData;
    dow: IndexData;
    vix: IndexData;
  };
  sentiment: MarketSentiment;
  topGainers: Stock[];
  topLosers: Stock[];
  marketTrends: MarketTrend[];
}

export interface IndexData {
  name: string;
  symbol: string;
  price: number;
  change: number;
  changePercent: number;
  volume: number;
}

export interface MarketSentiment {
  overall: 'bullish' | 'bearish' | 'neutral';
  fearGreedIndex: number;
  putCallRatio: number;
  marketBreadth: number;
}

export interface MarketTrend {
  sector: string;
  performance: number;
  momentum: string;
  keyStocks: string[];
}

// API Types
export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
  error?: string;
}

export interface SearchRequest {
  query: string;
  type: 'stock' | 'investor' | 'insight';
  limit?: number;
}

export interface SearchResponse {
  stocks: Stock[];
  investors: Investor[];
  insights: InvestorInsight[];
}

// UI Types
export interface ChartDataPoint {
  date: string;
  value: number;
  volume?: number;
}

export interface TimeRange {
  label: string;
  value: '1D' | '5D' | '1M' | '3M' | '6M' | '1Y' | '5Y' | 'ALL';
}

export type SortOption = 'relevance' | 'date' | 'confidence' | 'sentiment';
export type FilterOption = 'all' | 'bullish' | 'bearish' | 'recent';