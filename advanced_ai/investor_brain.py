#!/usr/bin/env python3
"""
🧠 Investor Brain - 거장들의 뇌를 시뮬레이션하는 AI 시스템

"단순한 데이터 저장이 아니라, 거장들의 사고방식을 복제하는 것"
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import json
import re
from datetime import datetime, timedelta

class MarketPhase(Enum):
    BULL_MARKET = "bull_market"
    BEAR_MARKET = "bear_market"
    TRANSITION = "transition"
    UNCERTAIN = "uncertain"

@dataclass
class MarketContext:
    """시장 상황 정보"""
    phase: MarketPhase
    volatility: float  # 0-1
    sentiment_score: float  # -1 to 1
    valuation_level: float  # 0-1 (고가/저가)
    key_themes: List[str]
    risk_factors: List[str]

@dataclass
class Company:
    """기업 정보"""
    ticker: str
    name: str
    sector: str
    pe_ratio: float
    pb_ratio: float
    roe: float
    debt_equity: float
    revenue_growth: float
    business_complexity: float  # 0-1 (단순함-복잡함)
    moat_strength: float  # 0-1
    growth_stage: str  # early, growth, mature, declining

@dataclass
class InvestorDecision:
    """투자 결정"""
    action: str  # buy, sell, hold, avoid
    confidence: float  # 0-1
    reasoning: str
    emotional_state: str
    key_factors: List[str]
    time_horizon: str

class InvestorBrain:
    """거장 뇌 기반 클래스"""

    def __init__(self, name: str):
        self.name = name
        self.memory = []  # 과거 결정 기억
        self.confidence_calibration = 0.5  # 신뢰도 보정
        self.learning_rate = 0.1

        # 투자 성격 행렬
        self.personality = {
            'patience': 0.5,
            'risk_tolerance': 0.5,
            'complexity_tolerance': 0.5,
            'time_preference': 'medium',
            'emotional_volatility': 0.5
        }

    def analyze_company(self, company: Company, context: MarketContext) -> InvestorDecision:
        """기업 분석 - 각 거장 클래스에서 오버라이드"""
        raise NotImplementedError

    def learn_from_outcome(self, decision: InvestorDecision, actual_outcome: float) -> None:
        """결정 결과로부터 학습"""
        outcome_quality = self.evaluate_decision_quality(decision, actual_outcome)

        # 신뢰도 보정
        if outcome_quality > 0.7:
            self.confidence_calibration = min(1.0, self.confidence_calibration + 0.05)
        elif outcome_quality < 0.3:
            self.confidence_calibration = max(0.1, self.confidence_calibration - 0.05)

        # 기억에 추가
        self.memory.append({
            'decision': decision,
            'outcome': actual_outcome,
            'quality': outcome_quality,
            'timestamp': datetime.now()
        })

        # 기억 관리 (최근 100개만 유지)
        if len(self.memory) > 100:
            self.memory = self.memory[-100:]

class WarrenBuffettBrain(InvestorBrain):
    """워런 버핏 뇌 모델"""

    def __init__(self):
        super().__init__("Warren Buffett")

        # 버핏의 성격 특성 (많은 분석 기반)
        self.personality = {
            'patience': 0.95,           # 엄청난 인내심
            'risk_tolerance': 0.25,      # 낮은 위험 허용도
            'complexity_tolerance': 0.2, # 복잡한 것 싫어함
            'time_preference': 'long_term',
            'emotional_volatility': 0.1   # 감정 변동 거의 없음
        }

        # 버핏의 핵심 투자 원칙
        self.core_principles = {
            'business_understanding': 0.25,
            'moat_strength': 0.25,
            'management_quality': 0.2,
            'valuation_reasonableness': 0.15,
            'long_term_prospects': 0.15
        }

        # 버핏이 피하는 것들
        self.avoidance_factors = {
            'high_complexity': 0.8,
            'excessive_valuation': 0.7,
            'technological_disruption_risk': 0.6,
            'poor_management': 0.9,
            'cyclical_volatility': 0.5
        }

    def analyze_company(self, company: Company, context: MarketContext) -> InvestorDecision:
        """버핏 방식으로 기업 분석"""

        # 1. 사업 이해도 평가
        understandability = max(0, 1 - company.business_complexity)
        if understandability < 0.7:
            return InvestorDecision(
                action="avoid",
                confidence=0.9,
                reasoning=f"Business too complex for my understanding. Complexity score: {company.business_complexity:.2f}",
                emotional_state="cautious",
                key_factors=["business_complexity"],
                time_horizon="long_term"
            )

        # 2. 핵심 원칙 기반 점수 계산
        scores = {}

        # 사업 이해도
        scores['understanding'] = understandability * self.core_principles['business_understanding']

        # 경쟁 우위 (Moat)
        scores['moat'] = company.moat_strength * self.core_principles['moat_strength']

        # 수익성 (ROE)
        roe_score = min(1.0, company.roe / 20.0)  # 15%+ 좋음, 20%+ 최고
        scores['profitability'] = roe_score * 0.3  # ROE의 가중치

        # 재무 안정성 (부채)
        debt_penalty = min(0.5, company.debt_equity / 2.0)
        scores['financial_stability'] = (1 - debt_penalty) * 0.3

        # 성장성
        if company.growth_stage in ['mature', 'declining']:
            growth_score = company.revenue_growth / 20.0
        else:  # early, growth
            growth_score = min(0.5, company.revenue_growth / 30.0)
        scores['growth'] = growth_score * 0.2

        total_score = sum(scores.values())

        # 3. 회피 요소 확인
        avoidance_penalty = 0
        if company.pe_ratio > 30:
            avoidance_penalty += self.avoidance_factors['excessive_valuation'] * 0.5

        if company.business_complexity > 0.7:
            avoidance_penalty += self.avoidance_factors['high_complexity'] * 0.3

        # 4. 시장 상황 고려
        context_adjustment = 1.0
        if context.phase == MarketPhase.BEAR_MARKET:
            context_adjustment = 1.2  # 불황일 때 기회
        elif context.phase == MarketPhase.BULL_MARKET and context.valuation_level > 0.7:
            context_adjustment = 0.6  # 과열 상황에서는 조심

        final_score = max(0, (total_score - avoidance_penalty) * context_adjustment)

        # 5. 결정
        if final_score > 0.7:
            return InvestorDecision(
                action="buy",
                confidence=min(0.95, final_score) * self.confidence_calibration,
                reasoning=self.generate_buffett_reasoning(scores, company, context),
                emotional_state="confident",
                key_factors=list(scores.keys()),
                time_horizon="long_term"
            )
        elif final_score > 0.5:
            return InvestorDecision(
                action="hold",
                confidence=0.7 * self.confidence_calibration,
                reasoning="Reasonable company but not compelling at current valuation",
                emotional_state="patient",
                key_factors=["moderate_score"],
                time_horizon="long_term"
            )
        else:
            return InvestorDecision(
                action="avoid",
                confidence=0.8 * self.confidence_calibration,
                reasoning="Does not meet my investment criteria",
                emotional_state="uninterested",
                key_factors=["low_score"],
                time_horizon="long_term"
            )

    def generate_buffett_reasoning(self, scores: Dict[str, float], company: Company, context: MarketContext) -> str:
        """버핏 스타일의 추론 생성"""
        reasons = []

        if scores.get('moat', 0) > 0.6:
            reasons.append(f"Strong competitive moat with {company.moat_strength*100:.0f}% strength")

        if scores.get('understanding', 0) > 0.7:
            reasons.append("Business I can understand and predict")

        if company.roe > 15:
            reasons.append(f"Excellent returns on equity ({company.roe:.1f}%)")

        if company.debt_equity < 0.5:
            reasons.append("Conservative capital structure")

        if context.phase == MarketPhase.BEAR_MARKET:
            reasons.append("Market decline creates opportunity for patient investors")

        return ". ".join(reasons) + ". This aligns with my value investing philosophy."

class PeterLynchBrain(InvestorBrain):
    """피터 린치 뇌 모델"""

    def __init__(self):
        super().__init__("Peter Lynch")

        # 린치의 성격 특성
        self.personality = {
            'patience': 0.6,
            'risk_tolerance': 0.6,
            'complexity_tolerance': 0.7,
            'time_preference': 'medium',
            'emotional_volatility': 0.4
        }

        # 린치의 투자 카테고리
        self.categories = {
            'fast_growers': {
                'criteria': {'revenue_growth_min': 20, 'pe_max': 40},
                'weight': 0.3
            },
            'stalwarts': {
                'criteria': {'revenue_growth_min': 10, 'pe_max': 20},
                'weight': 0.25
            },
            'slow_growers': {
                'criteria': {'revenue_growth_min': 5, 'pe_max': 15},
                'weight': 0.2
            },
            'cyclicals': {
                'criteria': {'pe_min': 5, 'pe_max': 15},
                'weight': 0.15
            },
            'turnarounds': {
                'criteria': {'pe_range': 'any', 'improvement_potential': 0.3},
                'weight': 0.1
            }
        }

    def analyze_company(self, company: Company, context: MarketContext) -> InvestorDecision:
        """린치 방식으로 기업 분석"""

        # 1. 성장 카테고리 분류
        category = self.classify_growth_category(company)

        # 2. 일상 관찰 가능성 평가
        observability = self.assess_observability(company)

        # 3. 성장 스토리 평가
        growth_story_score = self.evaluate_growth_story(company)

        # 4. 재무 건전성
        financial_health = self.check_financial_health(company)

        # 5. 분석가 커버리지 (너무 많은 관심 = 좋은 신호)
        analyst_interest = 0.5  # 기본값

        # 점수 계산
        total_score = (
            category['score'] * 0.3 +
            observability * 0.2 +
            growth_story_score * 0.25 +
            financial_health * 0.15 +
            analyst_interest * 0.1
        )

        # 린치 특유의 시장 상황 고려
        if context.phase == MarketPhase.BEAR_MARKET:
            total_score += 0.2  # 하락장은 기회
        elif company.pe_ratio < 10:
            total_score += 0.15  # 저PER는 매력적

        # 결정
        if total_score > 0.75:
            return InvestorDecision(
                action="buy",
                confidence=0.85 * self.confidence_calibration,
                reasoning=self.generate_lynch_reasoning(category, company, total_score),
                emotional_state="excited",
                key_factors=["growth_story", "category"],
                time_horizon="medium_term"
            )
        elif total_score > 0.5:
            return InvestorDecision(
                action="hold",
                confidence=0.6 * self.confidence_calibration,
                reasoning="Interesting but waiting for better entry point",
                emotional_state="watching",
                key_factors=["potential"],
                time_horizon="medium_term"
            )
        else:
            return InvestorDecision(
                action="avoid",
                confidence=0.7 * self.confidence_calibration,
                reasoning="Doesn't meet my growth criteria or is too complex",
                emotional_state="bored",
                key_factors=["growth_criteria"],
                time_horizon="medium_term"
            )

    def classify_growth_category(self, company: Company) -> Dict:
        """린치의 성장 카테고리 분류"""

        if company.revenue_growth > 20 and company.pe_ratio < 40:
            return {
                'name': 'fast_grower',
                'score': 0.9,
                'fit': "Excellent growth with reasonable valuation"
            }
        elif company.revenue_growth > 10 and company.pe_ratio < 20:
            return {
                'name': 'stalwart',
                'score': 0.8,
                'fit': "Solid large company with steady growth"
            }
        elif company.revenue_growth > 5 and company.pe_ratio < 15:
            return {
                'name': 'slow_grower',
                'score': 0.7,
                'fit': "Stable company with modest growth"
            }
        else:
            return {
                'name': 'other',
                'score': 0.4,
                'fit': "Doesn't fit my standard categories"
            }

    def assess_observability(self, company: Company) -> float:
        """일상에서 관찰 가능성 평가 (린치 철학)"""

        # 관찰 용이한 섹터
        observable_sectors = {
            'consumer_staples': 0.9,
            'retail': 0.9,
            'restaurants': 0.95,
            'technology': 0.7,
            'healthcare': 0.6,
            'finance': 0.5,
            'industrial': 0.4,
            'energy': 0.3
        }

        sector_score = observable_sectors.get(company.sector.lower(), 0.5)

        # 복잡도 감점
        complexity_penalty = company.business_complexity * 0.3

        return max(0, sector_score - complexity_penalty)

    def evaluate_growth_story(self, company: Company) -> float:
        """성장 스토리 평가"""
        score = 0.0

        # 매출 성장성
        if company.revenue_growth > 20:
            score += 0.3
        elif company.revenue_growth > 10:
            score += 0.2
        elif company.revenue_growth > 5:
            score += 0.1

        # 이익 성장성
        if company.roe > 20:
            score += 0.2
        elif company.roe > 15:
            score += 0.1

        # 비즈니스 모델 단순성
        if company.business_complexity < 0.3:
            score += 0.3
        elif company.business_complexity < 0.5:
            score += 0.2

        return min(1.0, score)

    def check_financial_health(self, company: Company) -> float:
        """재무 건전성 확인"""
        score = 1.0

        # 부채 비율 패널티
        if company.debt_equity > 2.0:
            score -= 0.4
        elif company.debt_equity > 1.0:
            score -= 0.2

        # ROE
        if company.roe < 5:
            score -= 0.3
        elif company.roe < 10:
            score -= 0.1

        # 현금 흐름 (대리: P/B 비율)
        if company.pb_ratio > 10:
            score -= 0.2

        return max(0, score)

    def generate_lynch_reasoning(self, category: Dict, company: Company, score: float) -> str:
        """린치 스타일의 추론 생성"""

        reasons = [f"Excellent {category['name']} with {category['fit'].lower()}"]

        if company.revenue_growth > 15:
            reasons.append(f"Strong revenue growth of {company.revenue_growth:.1f}%")

        if company.pe_ratio < 15:
            reasons.append("Reasonable valuation for growth potential")

        if score > 0.8:
            reasons.append("This is exactly what I look for in a growth investment")

        return ". ".join(reasons) + "."

class HowardMarksBrain(InvestorBrain):
    """하워드 막스 뇌 모델"""

    def __init__(self):
        super().__init__("Howard Marks")

        # 막스의 성격 특성
        self.personality = {
            'patience': 0.85,
            'risk_tolerance': 0.4,
            'complexity_tolerance': 0.6,
            'time_preference': 'medium_term',
            'emotional_volatility': 0.3
        }

        # 막스의 핵심 투자 원칙
        self.core_principles = {
            'cycle_positioning': 0.25,
            'risk_control': 0.25,
            'contrarian_thinking': 0.2,
            'valuation_discipline': 0.2,
            'psychology_understanding': 0.1
        }

        # 막스가 중요하게 생각하는 것들
        self.key_factors = {
            'market_cycle_position': 0.8,
            'sentiment_extremes': 0.7,
            'valuation_reasonableness': 0.6,
            'risk_premium': 0.5,
            'downside_protection': 0.9
        }

    def analyze_company(self, company: Company, context: MarketContext) -> InvestorDecision:
        """막스 방식으로 기업 분석"""

        # 1. 시장 사이클 위치 평가
        cycle_score = self.assess_cycle_positioning(company, context)

        # 2. 감성 극단 평가
        sentiment_score = self.assess_sentiment_extremes(company, context)

        # 3. 가치 규율 평가
        valuation_score = self.assess_valuation_discipline(company)

        # 4. 하방 리스크 평가
        risk_score = self.assess_downside_protection(company)

        # 5. 종합 점수 계산
        total_score = (
            cycle_score * self.core_principles['cycle_positioning'] +
            sentiment_score * self.core_principles['contrarian_thinking'] +
            valuation_score * self.core_principles['valuation_discipline'] +
            risk_score * self.core_principles['risk_control']
        )

        # 막스 특유의 시장 상황 조정
        context_adjustment = 1.0
        if context.sentiment_score > 0.7:  # 과도한 낙관주의
            context_adjustment = 0.6  # 매우 보수적
        elif context.sentiment_score < -0.5:  # 과도한 비관주의
            context_adjustment = 1.4  # 공격적

        final_score = max(0, total_score * context_adjustment)

        # 결정
        if final_score > 0.7:
            return InvestorDecision(
                action="buy",
                confidence=0.75 * self.confidence_calibration,
                reasoning=self.generate_marks_reasoning(total_score, company, context),
                emotional_state="cautiously_optimistic",
                key_factors=["cycle_positioning", "risk_control"],
                time_horizon="medium_term"
            )
        elif final_score > 0.5:
            return InvestorDecision(
                action="hold",
                confidence=0.65 * self.confidence_calibration,
                reasoning="Interesting but waiting for better risk/reward balance",
                emotional_state="watchful",
                key_factors=["assessment_mode"],
                time_horizon="medium_term"
            )
        else:
            return InvestorDecision(
                action="avoid",
                confidence=0.85 * self.confidence_calibration,
                reasoning="Risk/reward not attractive at current levels",
                emotional_state="cautious",
                key_factors=["risk_management"],
                time_horizon="medium_term"
            )

    def assess_cycle_positioning(self, company: Company, context: MarketContext) -> float:
        """시장 사이클 위치 평가"""
        score = 0.5

        # 변동성이 높을 때 기회
        if context.volatility > 0.6:
            score += 0.3

        # 밸류에이션 수준 고려
        if context.valuation_level < 0.3:  # 저가
            score += 0.2
        elif context.valuation_level > 0.7:  # 고가
            score -= 0.2

        return max(0, min(1, score))

    def assess_sentiment_extremes(self, company: Company, context: MarketContext) -> float:
        """감성 극단 평가"""
        sentiment_abs = abs(context.sentiment_score)

        # 감성이 극단일 때 기회
        if sentiment_abs > 0.7:
            return 0.8
        elif sentiment_abs > 0.5:
            return 0.6
        else:
            return 0.3  # 중간 감성은 기회 부족

    def assess_valuation_discipline(self, company: Company) -> float:
        """가치 규율 평가"""
        score = 0.5

        # P/E 비율
        if company.pe_ratio < 15:
            score += 0.3
        elif company.pe_ratio > 30:
            score -= 0.3

        # P/B 비율
        if company.pb_ratio < 2:
            score += 0.2
        elif company.pb_ratio > 5:
            score -= 0.2

        return max(0, min(1, score))

    def assess_downside_protection(self, company: Company) -> float:
        """하방 리스크 보호 평가"""
        score = 1.0

        # 부채 비율
        if company.debt_equity > 2.0:
            score -= 0.4
        elif company.debt_equity > 1.0:
            score -= 0.2

        # 현금 흐름 대리: ROE
        if company.roe < 10:
            score -= 0.3

        return max(0, score)

    def generate_marks_reasoning(self, score: float, company: Company, context: MarketContext) -> str:
        """막스 스타일의 추론 생성"""
        reasons = []

        if abs(context.sentiment_score) > 0.7:
            if context.sentiment_score > 0:
                reasons.append("Market sentiment too optimistic - time for caution")
            else:
                reasons.append("Market pessimism creating opportunity")

        if context.volatility > 0.6:
            reasons.append("High volatility provides better risk/reward opportunities")

        if company.pe_ratio < 15:
            reasons.append("Reasonable valuation provides downside protection")

        if score > 0.7:
            reasons.append("Current conditions align with cycle positioning principles")

        return ". ".join(reasons) + ". This fits with my risk-controlled approach to market cycles."

class GeorgeSorosBrain(InvestorBrain):
    """조지 소로스 뇌 모델"""

    def __init__(self):
        super().__init__("George Soros")

        # 소로스의 성격 특성
        self.personality = {
            'patience': 0.4,
            'risk_tolerance': 0.8,
            'complexity_tolerance': 0.9,
            'time_preference': 'short_term',
            'emotional_volatility': 0.6
        }

        # 소로스의 핵심 투자 원칙 (반사성 이론)
        self.core_principles = {
            'reflexivity_identification': 0.3,
            'feedback_loop_monitoring': 0.25,
            'cognitive_bias_exploitation': 0.2,
            'macro_trend_anticipation': 0.15,
            'policy_impact_analysis': 0.1
        }

        # 반사성 패턴 감지기
        self.reflexivity_patterns = {
            'price_perception_loop': 0.9,
            'sentiment_fundamental_gap': 0.8,
            'policy_market_feedback': 0.7,
            'narrative_reality_divergence': 0.6
        }

    def analyze_company(self, company: Company, context: MarketContext) -> InvestorDecision:
        """소로스 방식으로 기업 분석"""

        # 1. 반사성 상황 식별
        reflexivity_score = self.identify_reflexivity(company, context)

        # 2. 피드백 루프 강도 평가
        feedback_score = self.assess_feedback_loops(company, context)

        # 3. 인지적 편향 기회 평가
        bias_score = self.assess_cognitive_biases(company, context)

        # 4. 거시 동향 예측
        macro_score = self.anticipate_macro_trends(company, context)

        # 5. 종합 점수 계산
        total_score = (
            reflexivity_score * self.core_principles['reflexivity_identification'] +
            feedback_score * self.core_principles['feedback_loop_monitoring'] +
            bias_score * self.core_principles['cognitive_bias_exploitation'] +
            macro_score * self.core_principles['macro_trend_anticipation']
        )

        # 소로스 특유의 시장 상황 조정
        context_adjustment = 1.0
        if context.volatility > 0.7:  # 높은 변동성 = 반사성 기회
            context_adjustment = 1.3
        elif len(context.key_themes) > 3:  # 복잡한 시장 = 반사성 증가
            context_adjustment = 1.2

        final_score = max(0, total_score * context_adjustment)

        # 결정 (더 공격적)
        if final_score > 0.6:
            action = "buy"
        elif final_score < 0.4:
            action = "sell"  # 소로스는 공매도도 자주 함
        else:
            action = "hold"

        confidence = min(0.95, final_score * 1.2) * self.confidence_calibration

        return InvestorDecision(
            action=action,
            confidence=confidence,
            reasoning=self.generate_soros_reasoning(final_score, company, context),
            emotional_state="opportunistic" if action == "buy" else "analytical",
            key_factors=["reflexivity", "feedback_loops"],
            time_horizon="short_term"
        )

    def identify_reflexivity(self, company: Company, context: MarketContext) -> float:
        """반사성 상황 식별"""
        score = 0.3

        # 높은 변동성은 반사성 신호
        if context.volatility > 0.6:
            score += 0.3

        # 강한 감성은 반사성 신호
        if abs(context.sentiment_score) > 0.6:
            score += 0.3

        # 복잡한 비즈니스 모델은 반사성 가능성
        if company.business_complexity > 0.6:
            score += 0.2

        # 극단적인 가치평가는 반사성 신호
        if company.pe_ratio > 40 or company.pe_ratio < 8:
            score += 0.2

        return max(0, min(1, score))

    def assess_feedback_loops(self, company: Company, context: MarketContext) -> float:
        """피드백 루프 강도 평가"""
        score = 0.5

        # 가격-감성 피드백
        if abs(context.sentiment_score) > 0.7 and context.volatility > 0.5:
            score += 0.3

        # 정책-시장 피드백
        policy_themes = ['inflation', 'rates', 'regulation', 'policy']
        if any(theme in ' '.join(context.key_themes).lower() for theme in policy_themes):
            score += 0.2

        return max(0, min(1, score))

    def assess_cognitive_biases(self, company: Company, context: MarketContext) -> float:
        """인지적 편향 기회 평가"""
        score = 0.3

        # 확증 편향 (강한 시장 나레이티브)
        if abs(context.sentiment_score) > 0.8:
            score += 0.4

        # 개인 심리 (무리 행동)
        if context.volatility > 0.7:
            score += 0.3

        return max(0, min(1, score))

    def anticipate_macro_trends(self, company: Company, context: MarketContext) -> float:
        """거시 동향 예측"""
        score = 0.5

        # 통화/금리 민감도
        if company.sector.lower() in ['finance', 'real_estate', 'utilities']:
            score += 0.2

        # 경기 순환성
        if company.sector.lower() in ['industrial', 'materials', 'energy']:
            score += 0.2

        return max(0, min(1, score))

    def generate_soros_reasoning(self, score: float, company: Company, context: MarketContext) -> str:
        """소로스 스타일의 추론 생성"""
        reasons = []

        if score > 0.7:
            reasons.append("Strong reflexive patterns identified with positive feedback loops")
        elif score < 0.4:
            reasons.append("Negative feedback loops indicate reversal potential")

        if context.volatility > 0.7:
            reasons.append("High volatility creates reflexive opportunities")

        if abs(context.sentiment_score) > 0.6:
            reasons.append("Market perception diverging from reality")

        if company.business_complexity > 0.6:
            reasons.append("Complex business creates perception-reality gap")

        return ". ".join(reasons) + ". This reflects the reflexive dynamics I've identified in the market."

# 거장 뇌 팩토리
def create_investor_brain(investor_type: str) -> InvestorBrain:
    """거장 유형에 맞는 뇌 생성"""

    if investor_type.lower() in ['warren buffett', 'buffett']:
        return WarrenBuffettBrain()
    elif investor_type.lower() in ['peter lynch', 'lynch']:
        return PeterLynchBrain()
    elif investor_type.lower() in ['howard marks', 'marks']:
        return HowardMarksBrain()
    elif investor_type.lower() in ['george soros', 'sorros']:
        return GeorgeSorosBrain()
    else:
        raise ValueError(f"Unknown investor type: {investor_type}")

# 데모 실행
def demo_investor_brains():
    """거장 뇌 시스템 데모"""

    # 시장 상황 설정
    current_context = MarketContext(
        phase=MarketPhase.BULL_MARKET,
        volatility=0.3,
        sentiment_score=0.7,
        valuation_level=0.8,
        key_themes=['AI', 'clean_energy', 'inflation'],
        risk_factors=['high_valuation', 'geopolitical_tension']
    )

    # 테스트 기업들
    companies = {
        'apple': Company(
            ticker='AAPL',
            name='Apple Inc.',
            sector='technology',
            pe_ratio=36.6,
            pb_ratio=54.8,
            roe=171.4,
            debt_equity=152.4,
            revenue_growth=7.9,
            business_complexity=0.3,  # 비교적 단순
            moat_strength=0.9,  # 강력한 브랜드
            growth_stage='mature'
        ),

        'tesla': Company(
            ticker='TSLA',
            name='Tesla Inc.',
            sector='automotive',
            pe_ratio=65.2,
            pb_ratio=15.8,
            roe=21.3,
            debt_equity=0.8,
            revenue_growth=47.2,
            business_complexity=0.7,  # 복잡
            moat_strength=0.6,  # 중간
            growth_stage='growth'
        ),

        'coca_cola': Company(
            ticker='KO',
            name='Coca-Cola',
            sector='consumer_staples',
            pe_ratio=28.5,
            pb_ratio=11.2,
            roe=45.3,
            debt_equity=2.1,
            revenue_growth=5.1,
            business_complexity=0.2,  # 매우 단순
            moat_strength=0.95,  # 매우 강력
            growth_stage='mature'
        )
    }

    # 거장 뇌 생성
    buffett_brain = create_investor_brain('warren buffett')
    lynch_brain = create_investor_brain('peter lynch')
    marks_brain = create_investor_brain('howard marks')
    soros_brain = create_investor_brain('george soros')

    print("🧠 Investor Brain Analysis System")
    print("=" * 60)
    print(f"Market Context: {current_context.phase.value}, Volatility: {current_context.volatility}")
    print()

    for ticker, company in companies.items():
        print(f"📊 {ticker} - {company.name}")
        print(f"   P/E: {company.pe_ratio:.1f} | ROE: {company.roe:.1f}% | Growth: {company.revenue_growth:.1f}%")

        # 버핏 분석
        buffett_decision = buffett_brain.analyze_company(company, current_context)
        print(f"   🏛️  Buffett: {buffett_decision.action.upper()} ({buffett_decision.confidence:.2f})")
        print(f"      Reasoning: {buffett_decision.reasoning[:80]}...")

        # 린치 분석
        lynch_decision = lynch_brain.analyze_company(company, current_context)
        print(f"   📈 Lynch: {lynch_decision.action.upper()} ({lynch_decision.confidence:.2f})")
        print(f"      Reasoning: {lynch_decision.reasoning[:80]}...")

        # 막스 분석
        marks_decision = marks_brain.analyze_company(company, current_context)
        print(f"   📊 Marks: {marks_decision.action.upper()} ({marks_decision.confidence:.2f})")
        print(f"      Reasoning: {marks_decision.reasoning[:80]}...")

        # 소로스 분석
        soros_decision = soros_brain.analyze_company(company, current_context)
        print(f"   🔄 Soros: {soros_decision.action.upper()} ({soros_decision.confidence:.2f})")
        print(f"      Reasoning: {soros_decision.reasoning[:80]}...")
        print()

if __name__ == "__main__":
    demo_investor_brains()