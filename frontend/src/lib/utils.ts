// Simple utility function to combine class names
export function cn(...classes: string[]): string {
  return classes.filter(Boolean).join(' ');
}

export function formatCurrency(amount: number, currency: string = 'USD'): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
  }).format(amount);
}

export function formatPercent(value: number, decimals: number = 2): string {
  return `${value.toFixed(decimals)}%`;
}

export function formatMarketCap(marketCap: number): string {
  if (marketCap >= 1e12) {
    return `$${(marketCap / 1e12).toFixed(1)}T`;
  } else if (marketCap >= 1e9) {
    return `$${(marketCap / 1e9).toFixed(1)}B`;
  } else if (marketCap >= 1e6) {
    return `$${(marketCap / 1e6).toFixed(1)}M`;
  } else {
    return `$${marketCap.toLocaleString()}`;
  }
}

export function formatVolume(volume: number): string {
  if (volume >= 1e9) {
    return `${(volume / 1e9).toFixed(1)}B`;
  } else if (volume >= 1e6) {
    return `${(volume / 1e6).toFixed(1)}M`;
  } else if (volume >= 1e3) {
    return `${(volume / 1e3).toFixed(1)}K`;
  } else {
    return volume.toLocaleString();
  }
}

export function formatDate(date: string | Date): string {
  const dateObj = typeof date === 'string' ? new Date(date) : date;
  return dateObj.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
}

export function getSentimentColor(sentiment: string): string {
  switch (sentiment) {
    case 'strongly_bullish':
      return 'text-success-600';
    case 'bullish':
      return 'text-success-500';
    case 'cautiously_bullish':
      return 'text-success-400';
    case 'neutral':
      return 'text-gray-500';
    case 'cautiously_bearish':
      return 'text-danger-400';
    case 'bearish':
      return 'text-danger-500';
    case 'strongly_bearish':
      return 'text-danger-600';
    default:
      return 'text-gray-500';
  }
}

export function getSentimentBgColor(sentiment: string): string {
  switch (sentiment) {
    case 'strongly_bullish':
      return 'bg-success-50 border-success-200';
    case 'bullish':
      return 'bg-success-50 border-success-200';
    case 'cautiously_bullish':
      return 'bg-success-25 border-success-200';
    case 'neutral':
      return 'bg-gray-50 border-gray-200';
    case 'cautiously_bearish':
      return 'bg-danger-25 border-danger-200';
    case 'bearish':
      return 'bg-danger-50 border-danger-200';
    case 'strongly_bearish':
      return 'bg-danger-50 border-danger-200';
    default:
      return 'bg-gray-50 border-gray-200';
  }
}

export function getSentimentIcon(sentiment: string): string {
  switch (sentiment) {
    case 'strongly_bullish':
      return '🚀';
    case 'bullish':
      return '📈';
    case 'cautiously_bullish':
      return '📊';
    case 'neutral':
      return '➡️';
    case 'cautiously_bearish':
      return '📉';
    case 'bearish':
      return '📊';
    case 'strongly_bearish':
      return '🚨';
    default:
      return '📊';
  }
}

export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout;
  return (...args: Parameters<T>) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
}

export function getRecommendationColor(recommendation: string): string {
  switch (recommendation.toLowerCase()) {
    case 'strong_buy':
    case 'buy':
      return 'text-success-600';
    case 'hold':
      return 'text-yellow-600';
    case 'sell':
    case 'strong_sell':
      return 'text-danger-600';
    default:
      return 'text-gray-600';
  }
}

export function extractTickerFromText(text: string): string[] {
  // Simple regex to find tickers (1-5 uppercase letters)
  const tickerRegex = /\b[A-Z]{1,5}\b/g;
  return Array.from(new Set(text.match(tickerRegex) || []));
}