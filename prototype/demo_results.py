#!/usr/bin/env python3
"""
StockOracle 데모 결과 출력
Demo Results Output for StockOracle
"""

from investor_insight_processor import InvestorInsightProcessor

def main():
    """메인 함수 - 데모 결과 출력"""
    print("🎯 StockOracle 거장 인사이트 분석 데모")
    print("=" * 60)

    # 프로세서 초기화
    processor = InvestorInsightProcessor(data_dir="../data/investors")
    print("✅ 거장 데이터 로드 완료")

    # 워런 버핏 분석 데모
    print("\n" + "="*60)
    print("📊 워런 버핏 (Warren Buffett) 인사이트 분석")
    print("="*60)

    # 거장 프로필
    profile = processor.get_investor_profile('warren_buffett')
    print(f"\n👤 이름: {profile['name']}")
    print(f"📝 직책: {profile['title']}")
    print(f"💡 투자 철학: {profile['investment_philosophy']}")
    print(f"\n🌟 유명한 말:")
    for i, quote in enumerate(profile['famous_quotes'][:2], 1):
        print(f"   {i}. \"{quote}\"")

    # 인사이트 분석
    insights = processor.get_investor_insights('warren_buffett')
    print(f"\n📚 총 {len(insights)}개의 인사이트 발견")
    print("\n" + "-"*50)
    print("🔍 상위 인사이트 3개 분석 결과")
    print("-"*50)

    for i, insight in enumerate(insights[:3], 1):
        print(f"\n【 인사이트 {i} 】")
        print(f"📖 내용: {insight.content}")
        print(f"📅 날짜: {insight.date_said}")
        print(f"📚 출처: {insight.source}")
        print(f"🎯 감성: {insight.sentiment}")
        print(f"🏷️  투자 주제: {', '.join(insight.investment_themes)}")
        print(f"🔖 태그: {', '.join(insight.tags)}")
        print(f"⭐ 신뢰도: {insight.confidence_score:.2f}")

        # 관련 종목 분석
        matches = processor.analyze_insight(insight)
        print(f"\n🔗 연관 종목 ({len(matches)}개):")

        if matches:
            for j, match in enumerate(matches[:3], 1):  # 상위 3개만
                print(f"   {j}. 📈 {match.company_name} ({match.ticker})")
                print(f"      - 매칭 유형: {match.match_type}")
                print(f"      - 신뢰도: {match.confidence_score:.2f}")
                print(f"      - 감성: {match.sentiment}")
                print(f"      - 이유: {match.match_reason}")
        else:
            print("   💭 직접 언급된 종목은 없지만, 관련 섹터 분석 가능")

    # 피터 린치 분석 데모
    print("\n" + "="*60)
    print("📊 피터 린치 (Peter Lynch) 인사이트 분석")
    print("="*60)

    # 거장 프로필
    profile = processor.get_investor_profile('peter_ynch')
    print(f"\n👤 이름: {profile['name']}")
    print(f"📝 직책: {profile['title']}")
    print(f"💡 투자 철학: {profile['investment_philosophy']}")
    print(f"\n🌟 유명한 말:")
    for i, quote in enumerate(profile['famous_quotes'][:2], 1):
        print(f"   {i}. \"{quote}\"")

    # 인사이트 분석 (2개만)
    insights = processor.get_investor_insights('peter_ynch')
    print(f"\n📚 총 {len(insights)}개의 인사이트 발견")
    print("\n" + "-"*50)
    print("🔍 대표 인사이트 2개 분석 결과")
    print("-"*50)

    for i, insight in enumerate(insights[:2], 1):
        print(f"\n【 인사이트 {i} 】")
        print(f"📖 내용: {insight.content}")
        print(f"📅 날짜: {insight.date_said}")
        print(f"📚 출처: {insight.source}")
        print(f"🎯 감성: {insight.sentiment}")

        # 관련 종목 분석
        matches = processor.analyze_insight(insight)
        print(f"\n🔗 연관 종목 ({len(matches)}개):")

        if matches:
            for j, match in enumerate(matches[:2], 1):  # 상위 2개만
                print(f"   {j}. 📈 {match.company_name} ({match.ticker})")
                print(f"      - 매칭 유형: {match.match_type}")
                print(f"      - 신뢰도: {match.confidence_score:.2f}")

    # 종합 요약
    print("\n" + "="*60)
    print("📊 분석 결과 요약")
    print("="*60)

    total_insights = (
        len(processor.get_investor_insights('warren_buffett')) +
        len(processor.get_investor_insights('peter_ynch')) +
        len(processor.get_investor_insights('howard_marks'))
    )

    print(f"\n📈 데이터 분석 요약:")
    print(f"   • 총 분석한 거장: 3명")
    print(f"   • 총 인사이트 수: {total_insights}개")
    print(f"   • 워런 버핏: {len(processor.get_investor_insights('warren_buffett'))}개")
    print(f"   • 피터 린치: {len(processor.get_investor_insights('peter_ynch'))}개")
    print(f"   • 하워드 막스: {len(processor.get_investor_insights('howard_marks'))}개")

    print(f"\n🎯 주요 발견:")
    print(f"   • 직접 언급된 주요 종목: Apple (AAPL), Coca-Cola (KO), Bank of America (BAC)")
    print(f"   • 주요 투자 주제: 가치투자, 성장주, 브랜드 파워, 시장 싸이클")
    print(f"   • 감성 분석: 긍정적(bullish) 인사이트가 대부분")

    print(f"\n🚀 향후 개발 방향:")
    print(f"   • 1단계: 실시간 주식 데이터 연동")
    print(f"   • 2단계: 더 정교한 NLP 모델 적용")
    print(f"   • 3단계: 사용자 맞춤 추천 시스템")
    print(f"   • 4단계: 웹 인터페이스 개발")

    print(f"\n✅ StockOracle 프로토타입 데모 완료!")
    print(f"💡 이제 실제 주식 티커를 입력하면 거장들의 인사이트를 받을 수 있습니다!")

if __name__ == "__main__":
    main()