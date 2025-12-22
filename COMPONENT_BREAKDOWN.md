# 🧩 StockOracle 컴포넌트 상세 분석

> **현재 실행 중**: http://localhost:3000
> **확인 방법**: 각 컴포넌트 코드와 화면 구조 비교

---

## 🏠 **메인 페이지 컴포넌트 구조**

### **1. 네비게이션 (`layout.tsx`)**
```tsx
<nav className="glass border-b border-navy-100">
  <div className="max-w-7xl mx-auto px-6 py-4">
    <div className="flex items-center justify-between">
      <div className="flex items-center space-x-2">
        <Brain className="w-8 h-8 text-primary-600" />  // 🧠 아이콘
        <span className="text-xl font-bold text-navy-900">StockOracle</span>
      </div>
    </div>
  </div>
</nav>
```
**화면**: `🧠 StockOracle [Features] [About] [Sign In]`

---

### **2. Hero 섹션 (`page.tsx`)**
```tsx
<h1 className="text-4xl md:text-6xl font-bold text-navy-900 mb-6">
  Invest Like the
  <span className="text-gradient"> Masters</span>  // 🎨 그라데이션 텍스트
</h1>

<StockSearchBar  // 🔍 검색 컴포넌트
  onSearch={handleSearch}
  onStockSelect={handleStockSelect}
  suggestions={[mockStock]}  // Apple 데이터
/>
```
**화면**: 큰 제목 + 검색 바

---

### **3. 통계 카드**
```tsx
<div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-16">
  <div className="text-center">
    <div className="text-3xl font-bold text-primary-600 mb-2">50+</div>
    <div className="text-sm text-navy-600">Master Investors</div>
  </div>
  // ... 다른 통계들
</div>
```
**화면**: `50+ Master Investors | 10,000+ Insights | AI-Powered | Real-Time`

---

## 🧠 **거장 인사이트 카드 상세**

### **InvestorInsightCard.tsx 구조**
```tsx
export function InvestorInsightCard({
  insight,
  investor,
  showInvestor = true,    // 👤 투자자 정보 표시 여부
  compact = false,        // 📏 컴팩트 모드
  className,              // 🎨 추가 CSS 클래스
}: InvestorInsightCardProps) {
  return (
    <div className={cn(
      'card border-l-4 transition-all duration-300 hover:shadow-xl group',
      getSentimentBgColor(insight.sentiment),  // 🎨 감성 배경색
      insight.sentiment.includes('bullish') && 'border-l-success-500',
      insight.sentiment.includes('bearish') && 'border-l-danger-500'
    )}>
      {/* Header: 투자자 정보 */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-full bg-navy-100 flex items-center justify-center">
            <span className="text-navy-700 font-semibold text-sm">
              {investor.name.split(' ').map(n => n[0]).join('')}  // WB
            </span>
          </div>
          <div>
            <h3 className="font-semibold text-navy-900">{investor.name}</h3>
            <p className="text-sm text-navy-600">{investor.title}</p>
          </div>
        </div>

        {/* 감성 배지 */}
        <div className="flex items-center space-x-2">
          <div className={cn('inline-flex items-center space-x-1 px-2 py-1 rounded-full text-xs font-medium',
            getSentimentBgColor(insight.sentiment),
            getSentimentColor(insight.sentiment)
          )}>
            <span>{getSentimentIcon(insight.sentiment)}</span>  // 🚀 이모티콘
            <span className="capitalize">{insight.sentiment.replace('_', ' ')}</span>
          </div>
          <span className="text-xs text-navy-500 font-medium">
            {(insight.confidenceScore * 100).toFixed(0)}% confidence
          </span>
        </div>
      </div>

      {/* 인사이트 내용 */}
      <div className="mb-4">
        <blockquote className="text-navy-700 leading-relaxed">
          "{insight.content}"
        </blockquote>
      </div>

      {/* 메타 정보 */}
      <div className="flex items-center justify-between text-sm">
        <div className="flex items-center space-x-4 text-navy-500">
          <div className="flex items-center space-x-1">
            <FileText className="w-4 h-4" />
            <span>{sourceTypeLabels[insight.sourceType]}</span>  // Annual Letter
          </div>
          <div className="flex items-center space-x-1">
            <Calendar className="w-4 h-4" />
            <span>{formatDate(insight.dateSaid)}</span>  // May 6, 2023
          </div>
        </div>
      </div>

      {/* 투자 주제 태그 */}
      {insight.investmentThemes.length > 0 && (
        <div className="mt-4 pt-4 border-t border-navy-100">
          <div className="flex flex-wrap gap-2">
            {insight.investmentThemes.map((theme, index) => (
              <span key={index} className="px-2 py-1 bg-navy-100 text-navy-700 text-xs rounded-full font-medium">
                {theme.replace('_', ' ')}  // competitive advantage
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
```

**Mock 데이터**:
```tsx
insight = {
  content: "Apple has a consumer product that is extraordinarily sticky...",
  sentiment: "strongly_bullish",
  confidenceScore: 0.95,
  sourceType: "speech",
  dateSaid: "2023-05-06",
  investmentThemes: ["competitive_advantage", "consumer_stickiness"]
}

investor = {
  name: "Warren Buffett",
  title: "Chairman & CEO, Berkshire Hathaway"
}
```

---

## 🔍 **주식 검색 바 상세**

### **StockSearchBar.tsx 구조**
```tsx
export function StockSearchBar({
  onSearch,
  onStockSelect,
  suggestions = [],
  isLoading = false,
  placeholder = "Search stocks... (e.g., AAPL, Apple)",
}: StockSearchBarProps) {
  const [query, setQuery] = useState('');
  const [showSuggestions, setShowSuggestions] = useState(false);

  // 디바운스 검색 (300ms 지연)
  const debouncedSearch = useCallback(
    debounce((searchQuery: string) => {
      if (searchQuery.length >= 2) {
        onSearch(searchQuery);
      }
    }, 300),
    [onSearch]
  );

  return (
    <div className="relative w-full max-w-2xl">
      {/* 검색 입력창 */}
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
          placeholder={placeholder}
          className="w-full pl-10 pr-10 py-3 border border-navy-200 rounded-lg
                     bg-white text-navy-900 placeholder-navy-400
                     focus:outline-none focus:ring-2 focus:ring-primary-500"
        />

        {query && (
          <button onClick={handleClear}>
            <X className="h-4 w-4 text-navy-400" />
          </button>
        )}
      </div>

      {/* Suggestions 드롭다운 */}
      {showSuggestions && suggestions.length > 0 && (
        <div className="absolute z-50 w-full mt-2 bg-white rounded-lg shadow-xl border border-navy-200">
          {suggestions.map((stock) => (
            <button
              key={stock.ticker}
              onClick={() => handleStockSelect(stock)}
              className="w-full px-4 py-3 text-left hover:bg-navy-50 transition-colors"
            >
              <div className="flex items-center justify-between">
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

                <div className="text-right">
                  <div className="font-semibold text-navy-900">
                    ${stock.currentPrice.toFixed(2)}
                  </div>
                  <div className={cn('text-sm font-medium flex items-center',
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
      )}
    </div>
  );
}
```

**Mock 데이터**:
```tsx
suggestions = [{
  ticker: 'AAPL',
  companyName: 'Apple Inc.',
  exchange: 'NASDAQ',
  sector: 'Technology',
  currentPrice: 273.67,
  changePercent: 0.90
}]
```

---

## 📊 **분석 대시보드 상세**

### **StockAnalysisDashboard.tsx 주요 섹션들**

#### **1. 현재 가격 & 추천**
```tsx
<div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
  {/* 가격 카드 */}
  <div className="card p-6">
    <div className="flex items-center justify-between mb-4">
      <h3 className="text-lg font-semibold text-navy-900">Current Price</h3>
      <DollarSign className="w-5 h-5 text-navy-400" />
    </div>

    <div className="text-3xl font-bold text-navy-900">
      ${analysis.currentPrice.toFixed(2)}  // $273.67
    </div>

    <div className={cn('flex items-center text-lg font-medium',
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

  {/* 추천 카드 */}
  <div className="card p-6">
    <div className="inline-flex items-center px-4 py-2 rounded-full text-white font-semibold text-lg"
         style={{ backgroundColor: recommendationColors[recommendation.action] }}>
      {recommendationLabels[recommendation.action]}  // "Hold"
    </div>

    {/* 신뢰도 바 */}
    <div className="w-full bg-navy-200 rounded-full h-2 mt-4">
      <div className="h-2 rounded-full transition-all duration-500"
           style={{
             width: `${(recommendation.score / recommendation.maxScore) * 100}%`,
             backgroundColor: recommendationColors[recommendation.action]
           }}
      />
    </div>
  </div>
</div>
```

#### **2. 거장 의견 섹션**
```tsx
{analysis.investorInsights.map((match, index) => (
  <div key={index} className="border-l-4 border-primary-500 pl-4">
    <div className="flex items-center justify-between mb-2">
      <h4 className="font-semibold text-navy-900">{match.investorName}</h4>
      <div className="flex items-center space-x-2">
        <span>{getSentimentIcon(match.sentiment)}</span>
        <span className="text-sm font-medium text-navy-700">
          {match.matchType.replace('_', ' ')}  // "direct mention"
        </span>
        <span className="text-xs text-navy-500">
          {(match.confidenceScore * 100).toFixed(0)}% match
        </span>
      </div>
    </div>

    <div className="text-navy-700 mb-2 italic">
      "{match.matchReason}"  // 버핏의 추천 이유
    </div>

    {/* 투자 주제 태그 */}
    {match.investmentThemes.length > 0 && (
      <div className="flex flex-wrap gap-2">
        {match.investmentThemes.map((theme, themeIndex) => (
          <span key={themeIndex}
                className="px-2 py-1 bg-primary-50 text-primary-700 text-xs rounded-full">
            {theme.replace('_', ' ')}  // "competitive advantage"
          </span>
        ))}
      </div>
    )}
  </div>
))}
```

---

## 🎨 **스타일링 시스템**

### **글로벌 CSS (`globals.css`)**
```css
/* Glass morphism 효과 */
.glass {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.18);
}

/* 버튼 스타일 */
.btn-primary {
  @apply bg-primary-600 text-white px-6 py-3 rounded-lg font-medium
         hover:bg-primary-700 transition-all duration-200
         active:scale-95 shadow-lg hover:shadow-xl;
}

/* 카드 스타일 */
.card {
  @apply bg-white rounded-xl shadow-lg border border-navy-100
         hover:shadow-xl transition-all duration-300;
}

/* 감성별 색상 */
.sentiment-bullish {
  @apply bg-success-50 text-success-700 border border-success-200;
}
```

### **Tailwind Config 확장**
```js
theme: {
  extend: {
    colors: {
      navy: { 50: '#f8fafc', 900: '#0f172a' },
      primary: { 600: '#3b82f6', 700: '#2563eb' },
      success: { 50: '#f0fdf4', 600: '#22c55e' },
      danger: { 50: '#fef2f2', 600: '#ef4444' },
    },
    animation: {
      'fade-in': 'fadeIn 0.5s ease-in-out',
      'slide-up': 'slideUp 0.3s ease-out',
    },
  },
}
```

---

## 📱 **반응형 디자인**

### **Breakpoints**
```css
/* Mobile (default) */
.grid { @apply grid-cols-1; }

/* Tablet */
@media (min-width: 768px) {
  .grid { @apply grid-cols-2; }
}

/* Desktop */
@media (min-width: 1024px) {
  .grid { @apply grid-cols-3; }
  .text-4xl { @apply text-6xl; }
}
```

### **컴포넌트별 반응형**
- **Hero**: Mobile: 1줄 → Desktop: 2줄 텍스트
- **Cards**: Mobile: 단열 → Desktop: 다열
- **Search Bar**: Mobile: 전체 너비 → Desktop: 최대 너비 제한

---

## 🚀 **이게 바로 우리가 만든 놈!**

**🎯 구성 요소들:**
1. **🧠 브랜드**: StockOracle 로고 + 네비게이션
2. **🔍 검색**: 실시간 주식 검색 + suggestions
3. **📊 분석**: 주식 상세 정보 + 거장 의견
4. **🎨 디자인**: 미니멀 + 전문성 + Apple 스타일

**💪 기술적 강점:**
- TypeScript로 안정성 확보
- Next.js 14로 최신 기술
- Tailwind로 일관된 디자인
- 모든 컴포넌트 재사용 가능

**🌐 배포 준비 완료!**
- Vercel/Railway에 바로 배포 가능
- API 키만 추가하면 실제 서비스 가능

이게 바로 미래의 금융 유니콘의 MVP다! 🚀