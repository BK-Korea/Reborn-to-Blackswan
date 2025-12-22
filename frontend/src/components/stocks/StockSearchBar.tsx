'use client';

import React, { useState, useCallback } from 'react';
import { Search, TrendingUp, X } from 'lucide-react';
import { debounce } from '@/lib/utils';
import { Stock } from '@/types';

interface StockSearchBarProps {
  onSearch: (query: string) => void;
  onStockSelect: (stock: Stock) => void;
  suggestions?: Stock[];
  isLoading?: boolean;
  placeholder?: string;
}

export function StockSearchBar({
  onSearch,
  onStockSelect,
  suggestions = [],
  isLoading = false,
  placeholder = "Search stocks... (e.g., AAPL, Apple)",
}: StockSearchBarProps) => {
  const [query, setQuery] = useState('');
  const [showSuggestions, setShowSuggestions] = useState(false);

  // Debounced search
  const debouncedSearch = useCallback(
    debounce((searchQuery: string) => {
      if (searchQuery.length >= 2) {
        onSearch(searchQuery);
      }
    }, 300),
    [onSearch]
  );

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setQuery(value);
    setShowSuggestions(value.length >= 2);
    debouncedSearch(value);
  };

  const handleStockSelect = (stock: Stock) => {
    onStockSelect(stock);
    setQuery(stock.companyName);
    setShowSuggestions(false);
  };

  const handleClear = () => {
    setQuery('');
    setShowSuggestions(false);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      setShowSuggestions(false);
    }
  };

  return (
    <div className="relative w-full max-w-2xl">
      {/* Search Input */}
      <div className="relative">
        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          {isLoading ? (
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-primary-600"></div>
          ) : (
            <Search className="h-4 w-4 text-navy-400" />
          )}
        </div>

        <input
          type="text"
          value={query}
          onChange={handleInputChange}
          onKeyPress={handleKeyPress}
          onFocus={() => setShowSuggestions(query.length >= 2)}
          onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
          placeholder={placeholder}
          className="w-full pl-10 pr-10 py-3 border border-navy-200 rounded-lg
                     bg-white text-navy-900 placeholder-navy-400
                     focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent
                     transition-all duration-200"
        />

        {query && (
          <button
            onClick={handleClear}
            className="absolute inset-y-0 right-0 pr-3 flex items-center"
          >
            <X className="h-4 w-4 text-navy-400 hover:text-navy-600 transition-colors" />
          </button>
        )}
      </div>

      {/* Suggestions Dropdown */}
      {showSuggestions && suggestions.length > 0 && (
        <div className="absolute z-50 w-full mt-2 bg-white rounded-lg shadow-xl border border-navy-200 max-h-96 overflow-hidden">
          <div className="max-h-96 overflow-y-auto">
            {suggestions.map((stock) => (
              <button
                key={stock.ticker}
                onClick={() => handleStockSelect(stock)}
                className="w-full px-4 py-3 text-left hover:bg-navy-50 transition-colors duration-150
                           border-b border-navy-100 last:border-b-0 group"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div>
                      <div className="flex items-center space-x-2">
                        <span className="font-semibold text-navy-900">
                          {stock.companyName}
                        </span>
                        <span className="text-navy-500 text-sm">
                          ({stock.ticker})
                        </span>
                      </div>
                      <div className="text-sm text-navy-600">
                        {stock.sector} • {stock.exchange}
                      </div>
                    </div>
                  </div>

                  <div className="text-right">
                    <div className="font-semibold text-navy-900">
                      ${stock.currentPrice.toFixed(2)}
                    </div>
                    <div className={cn(
                      'text-sm font-medium flex items-center',
                      stock.changePercent >= 0 ? 'text-success-600' : 'text-danger-600'
                    )}>
                      {stock.changePercent >= 0 ? (
                        <TrendingUp className="w-3 h-3 mr-1" />
                      ) : (
                        <TrendingUp className="w-3 h-3 mr-1 transform rotate-180" />
                      )}
                      {Math.abs(stock.changePercent).toFixed(2)}%
                    </div>
                  </div>
                </div>
              </button>
            ))}
          </div>

          {/* Footer */}
          <div className="px-4 py-2 bg-navy-50 border-t border-navy-100">
            <div className="text-xs text-navy-500">
              Showing {suggestions.length} results • Use ticker or company name
            </div>
          </div>
        </div>
      )}

      {/* No Results */}
      {showSuggestions && query.length >= 2 && suggestions.length === 0 && !isLoading && (
        <div className="absolute z-50 w-full mt-2 bg-white rounded-lg shadow-xl border border-navy-200 p-4">
          <div className="text-center text-navy-500">
            <Search className="h-8 w-8 mx-auto mb-2 text-navy-300" />
            <p className="text-sm">No stocks found for "{query}"</p>
            <p className="text-xs mt-1">Try a different ticker or company name</p>
          </div>
        </div>
      )}
    </div>
  );
};