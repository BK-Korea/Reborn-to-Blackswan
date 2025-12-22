#!/usr/bin/env python3
"""
🍎 Apple 주식에 대한 거장들의 멀티버그 파티!
Apple Stock: When the Hell Should We Buy This Thing?
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from investor_insight_processor import InvestorInsightProcessor
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

class AppleStockAnalyst:
    """Apple 주식 전문 분석가 (거장들의 머리를 합친 놈)"""

    def __init__(self):
        self.processor = InvestorInsightProcessor(data_dir="../data/investors")
        self.aapl = yf.Ticker("AAPL")

    def get_aapl_insights(self):
        """Apple에 대한 거장들의 인사이트만 추출"""
        all_insights = []

        # 모든 거장의 인사이트에서 Apple 관련 것만 찾기
        for investor_slug in self.processor.investors_data.keys():
            insights = self.processor.get_investor_insights(investor_slug)

            for insight in insights:
                if any(keyword in insight.content.lower() for keyword in ['apple', 'iphone', 'ios', 'tim cook']):
                    insight.investor = investor_slug
                    all_insights.append(insight)

                # 태그에도 Apple 관련 키워드가 있는지 확인
                elif any('apple' in tag.lower() for tag in insight.tags):
                    insight.investor = investor_slug
                    all_insights.append(insight)

        return all_insights

    def analyze_apple_fundamentals(self):
        """Apple의 펀더멘털 분석 (버핏 스타일)"""
        print("💰 Apple 펀더멘털 분석 (워런 버핏 관점)")
        print("=" * 50)

        # 최근 재무 정보 가져오기
        info = self.aapl.info

        metrics = {
            'Market Cap': f"${info.get('marketCap', 0) / 1e12:.1f}T",
            'P/E Ratio': f"{info.get('trailingPE', 'N/A')}",
            'P/B Ratio': f"{info.get('priceToBook', 'N/A')}",
            'Revenue Growth': f"{info.get('revenueGrowth', 0) * 100:.1f}%",
            'Profit Margin': f"{info.get('profitMargins', 0) * 100:.1f}%",
            'ROE': f"{info.get('returnOnEquity', 0) * 100:.1f}%",
            'Debt to Equity': f"{info.get('debtToEquity', 'N/A')}"
        }

        for metric, value in metrics.items():
            print(f"📊 {metric}: {value}")

        # 버핏의 투자 기준과 비교
        print(f"\n🎯 워런 버핏의 평가:")
        pe_ratio = info.get('trailingPE', 0)
        pb_ratio = info.get('priceToBook', 0)
        roe = info.get('returnOnEquity', 0)

        if pe_ratio < 20:
            print(f"✅ P/E Ratio {pe_ratio:.1f} - 합리적인 가격!")
        else:
            print(f"⚠️  P/E Ratio {pe_ratio:.1f} - 좀 비싸지만 그럴 만 해...")

        if roe > 20:
            print(f"🚀 ROE {roe*100:.1f}% - 엄청난 수익률!")
        else:
            print(f"😐 ROE {roe*100:.1f}% - 그냥 그래...")

    def analyze_appel_technicals(self):
        """Apple 기술적 분석 (린치 스타일)"""
        print(f"\n📈 Apple 기술적 분석 (피터 린치 관점)")
        print("=" * 50)

        # 1년간 주가 데이터
        hist = self.aapl.history(period="1y")

        current_price = hist['Close'].iloc[-1]
        ma_50 = hist['Close'].rolling(50).mean().iloc[-1]
        ma_200 = hist['Close'].rolling(200).mean().iloc[-1]

        # 52주 high/low
        week_52_high = hist['Close'].max()
        week_52_low = hist['Close'].min()

        print(f"🏷️  현재 가격: ${current_price:.2f}")
        print(f"📊 52주 최고: ${week_52_high:.2f}")
        print(f"📊 52주 최저: ${week_52_low:.2f}")
        print(f"📈 50일 이평선: ${ma_50:.2f}")
        print(f"📈 200일 이평선: ${ma_200:.2f}")

        # 현재 가격 위치 분석
        if current_price < ma_50 < ma_200:
            print(f"⚠️  하락 추세 - 린치라면 조심스럽겠지만...")
        elif current_price > ma_50 > ma_200:
            print(f"🚀 상승 추세 - 린치가 좋아할 만해!")
        else:
            print(f"🔄 조정 중 - 기회일 수도 있어!")

        # 52주 대비 현재 위치
        position_52w = (current_price - week_52_low) / (week_52_high - week_52_low)
        print(f"📍 52주 대비 위치: {position_52w*100:.1f}% (0% = 최저, 100% = 최고)")

        if position_52w < 0.3:
            print(f"💰 52주 하단권 - 린치 스타일 기회!")
        elif position_52w > 0.8:
            print(f"🚨 52주 상단권 - 조심해야 해...")
        else:
            print(f"😐 중간 - 판단은 알아서 해!")

    def backtest_insights(self):
        """거장들의 Apple 인사이트 백테스팅"""
        print(f"\n🕰️  거장들의 Apple 인사이트 백테스팅")
        print("=" * 50)

        insights = self.get_aapl_insights()

        if not insights:
            print("❌ Apple 관련 인사이트가 없어...")
            return

        print(f"📚 총 {len(insights)}개의 Apple 관련 인사이트 발견!")

        # 각 인사이트별 백테스팅
        for insight in insights:
            investor_profile = self.processor.get_investor_profile(insight.investor)
            investor_name = investor_profile['name']

            print(f"\n🎤 {investor_name}의 인사이트:")
            print(f"📅 날짜: {insight.date_said}")
            print(f"📖 내용: {insight.content}")
            print(f"🎯 감성: {insight.sentiment}")

            # 해당 날짜 이후의 수익률 계산 (가상)
            print(f"💸 백테스팅 결과: '이때 샀다면...' (상상 속에서)")

            if insight.sentiment == 'strongly_bullish':
                print("🚀 강력 매수 추천 - 아마 엄청났을 거야!")
            elif insight.sentiment == 'bullish':
                print("📈 매수 추천 - 꽤 잘됐을 거야!")
            elif insight.sentiment == 'cautiously_bullish':
                print("🤔 조심스러운 매수 - 그래도 났을 거야!")
            else:
                print("😐 중립 - 그냥 그랬을 거야...")

    def generate_buy_signal(self):
        """Apple 매수 신호 생성 (거장들의 합체 의견)"""
        print(f"\n🤖 거장들의 최종 Apple 매수 신호")
        print("=" * 50)

        # 기술적 지표
        hist = self.aapl.history(period="6mo")
        current_price = hist['Close'].iloc[-1]
        ma_50 = hist['Close'].rolling(50).mean().iloc[-1]

        # 변동성 계산
        returns = hist['Close'].pct_change().dropna()
        volatility = returns.std() * np.sqrt(252) * 100  # 연율화 변동성

        # 펀더멘털
        info = self.aapl.info
        pe_ratio = info.get('trailingPE', 0)
        roe = info.get('returnOnEquity', 0)

        # 인사이트 점수
        insights = self.get_aapl_insights()
        sentiment_score = 0
        for insight in insights:
            if insight.sentiment == 'strongly_bullish':
                sentiment_score += 3
            elif insight.sentiment == 'bullish':
                sentiment_score += 2
            elif insight.sentiment == 'cautiously_bullish':
                sentiment_score += 1

        # 종합 점수 계산
        tech_score = 0
        if current_price < ma_50:
            tech_score += 2
        elif current_price < ma_50 * 1.05:
            tech_score += 1

        fund_score = 0
        if pe_ratio < 25:
            fund_score += 2
        elif pe_ratio < 35:
            fund_score += 1
        if roe > 0.25:
            fund_score += 2
        elif roe > 0.20:
            fund_score += 1

        total_score = tech_score + fund_score + sentiment_score
        max_score = 10

        print(f"📊 기술적 점수: {tech_score}/4")
        print(f"💰 펀더멘털 점수: {fund_score}/4")
        print(f"🧠 거장 인사이트 점수: {sentiment_score}/3")
        print(f"🎯 총점: {total_score}/{max_score}")

        # 최종 의견
        print(f"\n🚀 최종 의견:")
        if total_score >= 8:
            print("🔥🔥🔥 지금 당장 사라! 이건 완전 기회야!")
            print("💡 전체 자금의 20-30%를 투자해도 돼!")
        elif total_score >= 6:
            print("🚀 괜찮아! 점진적으로 사볼 만 해!")
            print("💡 분할 매수로 접근해봐!")
        elif total_score >= 4:
            print("🤔 음... 기다려보는 게 좋을 거야!")
            print("💡 더 좋은 타이밍을 기다려!")
        else:
            print("🚨 살 생각 절대 마! 위험해!")
            print("💡 돈 지킬 때야!")

        print(f"\n📈 변동성: {volatility:.1f}% (이정도는 감수해야 돼!)")

        return total_score, max_score

    def warren_buffett_verdict(self):
        """워런 버핏이 Apple을 어떻게 볼까?"""
        print(f"\n👨‍🦳 워런 버핏의 Apple 최종 평가")
        print("=" * 50)

        print("🍎 '애플은 우리에게 소비재 기업이야'")
        print("📱 '아이폰은 사람들이 버리지 않는 제품'")
        print("🏪 '애플스토어는 현대적인 소매점'")
        print("💰 '막대한 현금 흐름과 자본 효율성'")

        info = self.aapl.info

        verdict_points = [
            ("🏢 강력한 브랜드와 경쟁 우위", True),
            (f"💸 ROE {info.get('returnOnEquity', 0)*100:.1f}%", info.get('returnOnEquity', 0) > 0.20),
            (f"📊 수익성 {info.get('profitMargins', 0)*100:.1f}%", info.get('profitMargins', 0) > 0.20),
            (f"💵 현금의 바다 ${info.get('totalCash', 0)/1e9:.0f}B", info.get('totalCash', 0) > 50e9)
        ]

        print(f"\n🎯 버핏의 체크리스트:")
        for point, check in verdict_points:
            status = "✅" if check else "❌"
            print(f"   {status} {point}")

        print(f"\n🗣️  버핏의 말:")
        print("   '애플은 우리 포트폴리오의 핵심이야'")
        print("   '단순한 테크놀로지 회사가 아니라 소비재 왕이야'")
        print("   '티머 쿡은 경영의 천재야!'")

def main():
    """메인 함수 - Apple 종합 분석"""
    print("🍎🍎🍎 Apple 주식: 지금 사야 할까 말아야 할까? 🍎🍎🍎")
    print("=" * 60)

    analyst = AppleStockAnalyst()

    # 1. 거장들의 Apple 인사이트 분석
    insights = analyst.get_aapl_insights()
    print(f"🧠 거장들의 Apple 인사이트 ({len(insights)}개)")

    for insight in insights:
        investor_profile = analyst.processor.get_investor_profile(insight.investor)
        print(f"   👤 {investor_profile['name']}: {insight.sentiment}")

    # 2. 펀더멘털 분석
    analyst.analyze_apple_fundamentals()

    # 3. 기술적 분석
    analyst.analyze_appel_technicals()

    # 4. 백테스팅
    analyst.backtest_insights()

    # 5. 버핏의 평가
    analyst.warren_buffett_verdict()

    # 6. 최종 매수 신호
    analyst.generate_buy_signal()

    print(f"\n🎭 한마디로 요약하자면...")
    print("🍎 Apple은 그냥... 사라! (단, 돈 잃어도 책임 안 져! 😈)")

if __name__ == "__main__":
    main()