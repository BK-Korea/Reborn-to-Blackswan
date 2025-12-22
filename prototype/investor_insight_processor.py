#!/usr/bin/env python3
"""
거장 인사이트 처리 및 종목 매칭 프로토타입
Investor Insight Processing and Stock Matching Prototype
"""

import json
import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import requests
import yfinance as yf
import pandas as pd
from collections import defaultdict

@dataclass
class InvestorInsight:
    """거장 인사이트 데이터 클래스"""
    id: str
    content: str
    source: str
    source_type: str
    date_said: str
    context: str
    companies_mentioned: List[str]
    sentiment: str
    investment_themes: List[str]
    confidence_score: float
    tags: List[str]

@dataclass
class StockMatch:
    """종목 매칭 결과 클래스"""
    ticker: str
    company_name: str
    match_type: str  # 'direct_mention', 'semantic', 'theme_based'
    confidence_score: float
    match_reason: str
    sentiment: str
    investor_themes: List[str]

class InvestorInsightProcessor:
    """거장 인사이트 처리기"""

    def __init__(self, data_dir: str = "data/investors"):
        self.data_dir = data_dir
        self.investors_data = {}
        self.load_investor_data()

        # 종목명-티커 매핑 사전
        self.stock_name_to_ticker = self.build_stock_mapping()

        # 투자 주제별 관련 키워드
        self.theme_keywords = {
            'value_investing': ['intrinsic value', 'undervalued', 'cheap', 'bargain', 'margin of safety'],
            'growth_investing': ['growth', 'expanding', 'innovation', 'future', 'disruption'],
            'competitive_advantage': ['moat', 'competitive advantage', 'market share', 'barrier to entry'],
            'brand_power': ['brand', 'loyalty', 'pricing power', 'consumer preference'],
            'financial_metrics': ['return on capital', 'roe', 'cash flow', 'profitability'],
            'market_cycles': ['cycle', 'timing', 'entry point', 'market sentiment'],
            'risk_management': ['risk', 'downside', 'safety', 'capital preservation']
        }

    def load_investor_data(self):
        """거장 데이터 로드"""
        import os

        for filename in os.listdir(self.data_dir):
            if filename.endswith('.json'):
                investor_slug = filename.replace('.json', '')
                file_path = os.path.join(self.data_dir, filename)

                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.investors_data[investor_slug] = data

        print(f"✅ {len(self.investors_data)}명의 거장 데이터 로드 완료")

    def build_stock_mapping(self) -> Dict[str, str]:
        """주요 기업명-티커 매핑 사전 구축"""
        mapping = {
            # 기술주
            'Apple': 'AAPL', 'Microsoft': 'MSFT', 'Amazon': 'AMZN', 'Google': 'GOOGL',
            'Alphabet': 'GOOGL', 'Tesla': 'TSLA', 'Meta': 'META', 'Facebook': 'META',
            'NVIDIA': 'NVDA', 'Intel': 'INTC', 'AMD': 'AMD', 'Adobe': 'ADBE',

            # 금융주
            'Berkshire Hathaway': 'BRK-A', 'Bank of America': 'BAC', 'Wells Fargo': 'WFC',
            'JPMorgan': 'JPM', 'Goldman Sachs': 'GS',

            # 소비재
            'Coca-Cola': 'KO', 'Pepsi': 'PEP', 'Nike': 'NKE', 'Procter & Gamble': 'PG',
            'Walmart': 'WMT', 'Costco': 'COST', 'Home Depot': 'HD',

            # 자동차
            'Ford': 'F', 'General Motors': 'GM',

            # 항공사
            'American Airlines': 'AAL', 'Delta': 'DAL', 'United': 'UAL',

            # 에너지
            'Exxon': 'XOM', 'Chevron': 'CVX',

            # 헬스케어
            'Johnson & Johnson': 'JNJ', 'Pfizer': 'PFE',

            # 기타
            'See\'s Candies': 'PRIVATE',  # 비상장
            'Dunkin\' Donuts': 'DNKN', 'Dunkin\' Brands': 'DNKN'
        }

        return mapping

    def get_investor_insights(self, investor_slug: str) -> List[InvestorInsight]:
        """특정 거장의 모든 인사이트 가져오기"""
        if investor_slug not in self.investors_data:
            return []

        investor_data = self.investors_data[investor_slug]
        insights = []

        for insight_data in investor_data.get('insights', []):
            insight = InvestorInsight(
                id=insight_data['id'],
                content=insight_data['content'],
                source=insight_data['source'],
                source_type=insight_data['source_type'],
                date_said=insight_data['date_said'],
                context=insight_data['context'],
                companies_mentioned=insight_data.get('companies_mentioned', []),
                sentiment=insight_data.get('sentiment', 'neutral'),
                investment_themes=insight_data.get('investment_themes', []),
                confidence_score=insight_data.get('confidence_score', 0.5),
                tags=insight_data.get('tags', [])
            )
            insights.append(insight)

        return insights

    def extract_stock_mentions(self, text: str) -> List[str]:
        """텍스트에서 언급된 종목 추출"""
        mentioned_stocks = []

        # 1. 직접 회사명 매칭
        for company_name, ticker in self.stock_name_to_ticker.items():
            if company_name.lower() in text.lower():
                mentioned_stocks.append(ticker)

        # 2. 티커 패턴 찾기 (대문자 1-5자)
        ticker_pattern = r'\b[A-Z]{1,5}\b'
        potential_tickers = re.findall(ticker_pattern, text)
        mentioned_stocks.extend(potential_tickers)

        # 중복 제거 및 PRIVATE 제외
        return list(set([ticker for ticker in mentioned_stocks if ticker != 'PRIVATE']))

    def calculate_theme_match(self, text: str, themes: List[str]) -> float:
        """텍스트와 투자 주제의 유사도 계산"""
        if not themes:
            return 0.0

        text_lower = text.lower()
        total_score = 0.0

        for theme in themes:
            if theme in self.theme_keywords:
                keywords = self.theme_keywords[theme]
                keyword_matches = sum(1 for keyword in keywords if keyword in text_lower)
                theme_score = keyword_matches / len(keywords)
                total_score += theme_score

        return min(1.0, total_score / len(themes))

    def find_semantic_matches(self, insight: InvestorInsight) -> List[StockMatch]:
        """의미적 분석으로 관련 종목 찾기 (간단 버전)"""
        matches = []

        # 투자 주제 기반 매칭
        theme_matches = []

        if 'technology' in insight.tags or 'Apple' in insight.tags:
            theme_matches.extend([
                StockMatch('AAPL', 'Apple Inc.', 'theme_based', 0.8, 'Technology sector interest', insight.sentiment, insight.investment_themes),
                StockMatch('MSFT', 'Microsoft Corp.', 'theme_based', 0.7, 'Technology sector interest', insight.sentiment, insight.investment_themes),
                StockMatch('GOOGL', 'Alphabet Inc.', 'theme_based', 0.7, 'Technology sector interest', insight.sentiment, insight.investment_themes)
            ])

        if 'banking' in insight.tags or 'Wells_Fargo' in insight.tags:
            theme_matches.extend([
                StockMatch('BAC', 'Bank of America', 'theme_based', 0.8, 'Banking sector focus', insight.sentiment, insight.investment_themes),
                StockMatch('WFC', 'Wells Fargo', 'theme_based', 0.7, 'Banking sector focus', insight.sentiment, insight.investment_themes),
                StockMatch('JPM', 'JPMorgan Chase', 'theme_based', 0.8, 'Banking sector focus', insight.sentiment, insight.investment_themes)
            ])

        if 'consumer_products' in insight.tags or 'Coca-Cola' in insight.tags:
            theme_matches.extend([
                StockMatch('KO', 'Coca-Cola', 'theme_based', 0.9, 'Consumer products focus', insight.sentiment, insight.investment_themes),
                StockMatch('PEP', 'PepsiCo', 'theme_based', 0.8, 'Consumer products focus', insight.sentiment, insight.investment_themes),
                StockMatch('PG', 'Procter & Gamble', 'theme_based', 0.7, 'Consumer products focus', insight.sentiment, insight.investment_themes)
            ])

        return theme_matches

    def analyze_insight(self, insight: InvestorInsight) -> List[StockMatch]:
        """단일 인사이트 분석 및 관련 종목 매칭"""
        all_matches = []

        # 1. 직접 언급된 종목
        direct_mentions = self.extract_stock_mentions(insight.content)
        for ticker in direct_mentions:
            # 회사명 찾기 (티커 -> 회사명)
            company_name = None
            for name, t in self.stock_name_to_ticker.items():
                if t == ticker:
                    company_name = name
                    break

            if not company_name:
                company_name = ticker  # 티커만 있는 경우

            match = StockMatch(
                ticker=ticker,
                company_name=company_name,
                match_type='direct_mention',
                confidence_score=0.95,  # 직접 언급은 높은 신뢰도
                match_reason=f"Direct mention in insight: {insight.content[:100]}...",
                sentiment=insight.sentiment,
                investor_themes=insight.investment_themes
            )
            all_matches.append(match)

        # 2. 의미적 매칭
        semantic_matches = self.find_semantic_matches(insight)
        all_matches.extend(semantic_matches)

        # 3. 중복 제거 및 정렬
        seen_tickers = set()
        unique_matches = []

        for match in sorted(all_matches, key=lambda x: x.confidence_score, reverse=True):
            if match.ticker not in seen_tickers:
                unique_matches.append(match)
                seen_tickers.add(match.ticker)

        return unique_matches[:10]  # 상위 10개만 반환

    def get_investor_profile(self, investor_slug: str) -> Dict[str, Any]:
        """거장 프로필 정보 가져오기"""
        if investor_slug not in self.investors_data:
            return {}

        data = self.investors_data[investor_slug]
        return {
            'name': data['investor_info']['name'],
            'title': data['investor_info']['title'],
            'investment_philosophy': data['investor_info']['investment_philosophy'],
            'famous_quotes': data['investor_info']['famous_quotes'],
            'investment_criteria': data.get('investment_criteria', {}),
            'historical_performance': data.get('historical_performance', {})
        }

def main():
    """메인 함수 - 프로토타입 데모"""
    print("🎯 StockOracle 거장 인사이트 분석 프로토타입")
    print("=" * 50)

    # 프로세서 초기화
    processor = InvestorInsightProcessor()

    # 사용 가능한 거장 목록
    print("\n📊 분석 가능한 거장 목록:")
    for investor_slug in processor.investors_data.keys():
        profile = processor.get_investor_profile(investor_slug)
        print(f"  - {profile['name']} ({investor_slug})")

    while True:
        print("\n" + "=" * 50)
        print("분석할 거장을 선택하세요:")
        print("1. Warren Buffett (warren_buffett)")
        print("2. Peter Lynch (peter_ynch)")
        print("3. Howard Marks (howard_marks)")
        print("q. 종료")

        choice = input("\n선택 (1-3, q): ").strip()

        if choice == 'q':
            break

        investor_map = {
            '1': 'warren_buffett',
            '2': 'peter_ynch',
            '3': 'howard_marks'
        }

        if choice not in investor_map:
            print("❌ 잘못된 선택입니다.")
            continue

        investor_slug = investor_map[choice]

        # 거장 프로필 출력
        profile = processor.get_investor_profile(investor_slug)
        print(f"\n👤 {profile['name']}")
        print(f"📝 {profile['title']}")
        print(f"💡 투자 철학: {profile['investment_philosophy']}")

        # 인사이트 분석
        insights = processor.get_investor_insights(investor_slug)
        print(f"\n📚 총 {len(insights)}개의 인사이트 분석 중...")

        for i, insight in enumerate(insights[:3], 1):  # 상위 3개만 표시
            print(f"\n--- 인사이트 {i} ---")
            print(f"📖 내용: {insight.content[:100]}...")
            print(f"📅 날짜: {insight.date_said}")
            print(f"🎯 감성: {insight.sentiment}")
            print(f"🏷️  테마: {', '.join(insight.investment_themes)}")

            # 관련 종목 분석
            matches = processor.analyze_insight(insight)
            print(f"\n🔗 관련 종목 ({len(matches)}개):")

            for match in matches:
                print(f"  • {match.company_name} ({match.ticker})")
                print(f"    - 매칭 유형: {match.match_type}")
                print(f"    - 신뢰도: {match.confidence_score:.2f}")
                print(f"    - 감성: {match.sentiment}")
                print(f"    - 이유: {match.match_reason}")
                print()

if __name__ == "__main__":
    main()