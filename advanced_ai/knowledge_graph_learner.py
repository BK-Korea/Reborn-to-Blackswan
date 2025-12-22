#!/usr/bin/env python3
"""
🧠 Knowledge Graph & Continuous Learning System
"과거 데이터로 학습하고, 현재 상황에 적응하는 동적 AI"
"""

import networkx as nx
import numpy as np
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass
import json
from datetime import datetime, timedelta
import sqlite3
from collections import defaultdict, deque

@dataclass
class KnowledgeTriple:
    """지식 트리플 (주어-관계-객체)"""
    subject: str
    predicate: str
    object: str
    confidence: float  # 0-1
    source: str
    timestamp: datetime
    context: Dict

@dataclass
class LearningExperience:
    """학습 경험"""
    investor_id: str
    prediction: str
    actual_outcome: str
    accuracy_score: float
    situation_context: Dict
    timestamp: datetime

class KnowledgeGraph:
    """투자 지식 그래프"""

    def __init__(self):
        self.graph = nx.DiGraph()
        self.confidence_decay = 0.995  # 시간에 따른 신뢰도 감쇠
        self.min_confidence = 0.1

    def add_knowledge(self, triple: KnowledgeTriple) -> None:
        """지식 추가"""
        edge_id = (triple.subject, triple.object)

        if self.graph.has_edge(*edge_id):
            # 기존 엣지 업데이트
            existing = self.graph[edge_id[0][edge_id[1]]
            # 가중 평균으로 신뢰도 업데이트
            total_weight = existing['weight'] + triple.confidence
            new_confidence = (existing['confidence'] * existing['weight'] +
                              triple.confidence * triple.confidence) / total_weight

            self.graph[edge_id[0]][edge_id[1]]['confidence'] = new_confidence
            self.graph[edge_id[0]][edge_id[1]]['weight'] = total_weight
            self.graph[edge_id[0]][edge_id[1]]['recent_sources'].append(triple.source)
        else:
            # 새 엣지 추가
            self.graph.add_edge(
                triple.subject,
                triple.object,
                predicate=triple.predicate,
                confidence=triple.confidence,
                weight=triple.confidence,
                source=triple.source,
                timestamp=triple.timestamp,
                context=triple.context,
                recent_sources=[triple.source]
            )

    def get_relationships(self, entity: str, predicate: str = None) -> List[Dict]:
        """특정 개체의 관계 조회"""
        relationships = []

        for _, target, data in self.graph.out_edges(entity, data=True):
            if predicate is None or data.get('predicate') == predicate:
                relationships.append({
                    'object': target,
                    'predicate': data.get('predicate'),
                    'confidence': data.get('confidence', 0),
                    'source': data.get('source'),
                    'timestamp': data.get('timestamp')
                })

        return relationships

    def find_similar_situations(self, current_context: Dict, top_k: int = 5) -> List[Dict]:
        """과거 유사 상황 찾기"""
        similar_situations = []

        # 현재 컨텍스트에서 핵심 키워드 추출
        current_keywords = set(current_context.get('key_themes', []))
        current_phase = current_context.get('market_phase')

        for subject, obj, data in self.graph.edges(data=True):
            context = data.get('context', {})
            past_keywords = set(context.get('key_themes', []))
            past_phase = context.get('market_phase')

            # 유사도 계산
            keyword_overlap = len(current_keywords & past_keywords)
            phase_match = 1.0 if past_phase == current_phase else 0.0

            similarity = (keyword_overlap * 0.7 + phase_match * 0.3)

            if similarity > 0.3:  # 최소 유사도 임계치
                similar_situations.append({
                    'subject': subject,
                    'object': obj,
                    'similarity': similarity,
                    'context': context,
                    'confidence': data.get('confidence', 0),
                    'timestamp': data.get('timestamp')
                })

        # 유사도 순 정렬
        similar_situations.sort(key=lambda x: x['similarity'], reverse=True)
        return similar_situations[:top_k]

class ContinuousLearningSystem:
    """지속적 학습 시스템"""

    def __init__(self, db_path: str = "learning_system.db"):
        self.knowledge_graph = KnowledgeGraph()
        self.db_path = db_path
        self.learning_history = deque(maxlen=1000)  # 최근 1000개 경험

        self.init_database()

    def init_database(self) -> None:
        """데이터베이스 초기화"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learning_experiences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                investor_id TEXT NOT NULL,
                prediction TEXT NOT NULL,
                actual_outcome TEXT NOT NULL,
                accuracy_score REAL,
                situation_context TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS knowledge_triples (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                predicate TEXT NOT NULL,
                object TEXT NOT NULL,
                confidence REAL NOT NULL,
                source TEXT NOT NULL,
                context TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        conn.close()

    def learn_from_quote(self, investor_id: str, quote: str, context: Dict) -> None:
        """인용문으로부터 학습"""

        # 1. 엔티티 추출 (간단 버전)
        entities = self.extract_entities(quote)

        # 2. 관계 추론
        relationships = self.infer_relationships(quote, entities, investor_id)

        # 3. 지식 그래프에 추가
        for rel in relationships:
            triple = KnowledgeTriple(
                subject=rel['subject'],
                predicate=rel['predicate'],
                object=rel['object'],
                confidence=rel['confidence'],
                source=f"quote_{investor_id}_{datetime.now().strftime('%Y%m%d')}",
                timestamp=datetime.now(),
                context=context
            )
            self.knowledge_graph.add_knowledge(triple)
            self.save_knowledge_to_db(triple)

    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """텍스트에서 엔티티 추출"""
        entities = {
            'companies': [],
            'concepts': [],
            'emotions': [],
            'timeframes': []
        }

        # 간단한 키워드 기반 추출
        company_patterns = [
            'Apple', 'AAPL', 'Microsoft', 'MSFT', 'Google', 'GOOGL',
            'Tesla', 'TSLA', 'Amazon', 'AMZN', 'Berkshire', 'BRK'
        ]

        concept_patterns = [
            'moat', 'growth', 'value', 'dividend', 'debt', 'cash flow',
            'intrinsic value', 'margin of safety', 'competitive advantage'
        ]

        emotion_patterns = [
            'bullish', 'bearish', 'optimistic', 'pessimistic', 'cautious',
            'excited', 'worried', 'confident', 'doubtful'
        ]

        text_lower = text.lower()

        for pattern in company_patterns:
            if pattern.lower() in text_lower:
                entities['companies'].append(pattern)

        for pattern in concept_patterns:
            if pattern in text_lower:
                entities['concepts'].append(pattern)

        for pattern in emotion_patterns:
            if pattern in text_lower:
                entities['emotions'].append(pattern)

        return entities

    def infer_relationships(self, quote: str, entities: Dict, investor_id: str) -> List[Dict]:
        """관계 추론"""
        relationships = []

        # 감성-기업 관계
        sentiment = self.analyze_sentiment(quote)
        for company in entities['companies']:
            relationships.append({
                'subject': investor_id,
                'predicate': f'is_{sentiment}_on',
                'object': company,
                'confidence': 0.8
            })

        # 개념-기업 관계
        for concept in entities['concepts']:
            for company in entities['companies']:
                if f'{concept} {company}'.lower() in quote.lower():
                    relationships.append({
                        'subject': company,
                        'predicate': 'has',
                        'object': concept,
                        'confidence': 0.7
                    })

        return relationships

    def analyze_sentiment(self, text: str) -> str:
        """감성 분석"""
        positive_words = ['great', 'wonderful', 'excellent', 'fantastic', 'love', 'excited']
        negative_words = ['terrible', 'awful', 'worried', 'concerned', 'avoid', 'scared']

        text_lower = text.lower()

        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)

        if positive_count > negative_count:
            return 'bullish'
        elif negative_count > positive_count:
            return 'bearish'
        else:
            return 'neutral'

    def learn_from_outcome(self, prediction: Dict, actual_outcome: Dict) -> None:
        """실제 결과로부터 학습"""

        investor_id = prediction['investor_id']
        predicted_action = prediction['action']
        actual_performance = actual_outcome.get('performance', 0)
        time_horizon = actual_outcome.get('time_horizon', '1y')

        # 예측 정확도 계산
        if predicted_action == 'buy' and actual_performance > 0.05:
            accuracy = 1.0
        elif predicted_action == 'sell' and actual_performance < -0.05:
            accuracy = 1.0
        elif predicted_action == 'avoid' and actual_performance < -0.1:
            accuracy = 0.8
        else:
            accuracy = max(0, 1 - abs(actual_performance) * 10)

        experience = LearningExperience(
            investor_id=investor_id,
            prediction=predicted_action,
            actual_outcome=str(actual_performance),
            accuracy_score=accuracy,
            situation_context=prediction.get('context', {}),
            timestamp=datetime.now()
        )

        # 학습 기록 저장
        self.learning_history.append(experience)
        self.save_experience_to_db(experience)

        # 관련 지식 업데이트
        self.update_related_knowledge(experience)

    def update_related_knowledge(self, experience: LearningExperience) -> None:
        """관련 지식 업데이트"""

        if experience.accuracy_score > 0.8:
            # 예측이 맞았을 때: 관련 지식 강화
            context = experience.situation_context
            mentioned_companies = context.get('mentioned_companies', [])

            for company in mentioned_companies:
                # 긍정적 경험 강화
                triple = KnowledgeTriple(
                    subject=experience.investor_id,
                    predicate='successful_prediction_on',
                    object=company,
                    confidence=0.9,
                    source='learning_outcome',
                    timestamp=experience.timestamp,
                    context={'accuracy': experience.accuracy_score}
                )
                self.knowledge_graph.add_knowledge(triple)

        elif experience.accuracy_score < 0.3:
            # 예측이 틀렸을 때: 관련 지식 약화
            context = experience.situation_context
            mentioned_companies = context.get('mentioned_companies', [])

            for company in mentioned_companies:
                triple = KnowledgeTriple(
                    subject=experience.investor_id,
                    predicate='unsuccessful_prediction_on',
                    object=company,
                    confidence=0.7,
                    source='learning_outcome',
                    timestamp=experience.timestamp,
                    context={'accuracy': experience.accuracy_score}
                )
                self.knowledge_graph.add_knowledge(triple)

    def predict_investor_behavior(self, investor_id: str, current_context: Dict) -> Dict:
        """거장 행동 예측"""

        # 1. 과거 유사 상황 찾기
        similar_situations = self.knowledge_graph.find_similar_situations(current_context)

        # 2. 관련 지식 조회
        relevant_knowledge = self.knowledge_graph.get_relationships(investor_id)

        # 3. 패턴 분석
        patterns = self.analyze_patterns(investor_id, similar_situations, relevant_knowledge)

        # 4. 예측 생성
        prediction = self.generate_prediction(investor_id, patterns, current_context)

        return prediction

    def analyze_patterns(self, investor_id: str, situations: List[Dict], knowledge: List[Dict]) -> Dict:
        """패턴 분석"""
        patterns = {
            'bullish_on_companies': [],
            'bearish_on_situations': [],
            'preferred_timeframes': [],
            'key_factors': [],
            'confidence_level': 0.5
        }

        # 감성 패턴 분석
        bullish_count = 0
        total_mentions = 0

        for rel in knowledge:
            if 'bullish_on' in rel.get('predicate', ''):
                patterns['bullish_on_companies'].append(rel['object'])
                bullish_count += 1
            elif 'bearish_on' in rel.get('predicate', ''):
                patterns['bearish_on_situations'].append(rel['object'])
            total_mentions += 1

        # 신뢰도 레벨 계산
        if total_mentions > 0:
            patterns['confidence_level'] = min(1.0, bullish_count / total_mentions * 2)

        return patterns

    def generate_prediction(self, investor_id: str, patterns: Dict, context: Dict) -> Dict:
        """예측 생성"""

        base_confidence = patterns['confidence_level']

        # 현재 컨텍스트 적용
        context_adjustment = 1.0
        if context.get('market_phase') == 'bear_market':
            if investor_id == 'Warren Buffett':
                context_adjustment = 1.2  # 버핏은 불황을 좋아
            else:
                context_adjustment = 0.8

        final_confidence = min(1.0, base_confidence * context_adjustment)

        return {
            'investor_id': investor_id,
            'predicted_action': self.recommend_action(patterns, context),
            'confidence': final_confidence,
            'reasoning': self.generate_reasoning(patterns, context),
            'key_factors': patterns['key_factors'],
            'context': context
        }

    def recommend_action(self, patterns: Dict, context: Dict) -> str:
        """행동 추천"""

        # 현재 상황에서 언급된 회사들
        mentioned_companies = context.get('mentioned_companies', [])

        for company in mentioned_companies:
            if company in patterns['bullish_on_companies']:
                return 'buy'
            elif company in patterns['bearish_on_situations']:
                return 'avoid'

        return 'hold'

    def generate_reasoning(self, patterns: Dict, context: Dict) -> str:
        """추론 이유 생성"""

        reasoning_parts = []

        if patterns['bullish_on_companies']:
            reasoning_parts.append(f"History shows bullish stance on {', '.join(patterns['bullish_on_companies'][:3])}")

        if patterns['confidence_level'] > 0.7:
            reasoning_parts.append("Strong historical confidence in this type of situation")

        if context.get('market_phase') == 'bear_market':
            reasoning_parts.append("Current bear market creates opportunity for value investors")

        return ". ".join(reasoning_parts) if reasoning_parts else "Based on historical patterns and current market conditions."

    def save_knowledge_to_db(self, triple: KnowledgeTriple) -> None:
        """지식을 DB에 저장"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO knowledge_triples
            (subject, predicate, object, confidence, source, context)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            triple.subject,
            triple.predicate,
            triple.object,
            triple.confidence,
            triple.source,
            json.dumps(triple.context)
        ))

        conn.commit()
        conn.close()

    def save_experience_to_db(self, experience: LearningExperience) -> None:
        """학습 경험을 DB에 저장"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO learning_experiences
            (investor_id, prediction, actual_outcome, accuracy_score, situation_context)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            experience.investor_id,
            experience.prediction,
            experience.actual_outcome,
            experience.accuracy_score,
            json.dumps(experience.situation_context)
        ))

        conn.commit()
        conn.close()

# 데모 실행
def demo_learning_system():
    """학습 시스템 데모"""

    # 시스템 초기화
    learning_system = ContinuousLearningSystem()

    print("🧠 Continuous Learning System Demo")
    print("=" * 50)

    # 1. 과거 인용문으로 학습
    print("\n📚 Learning from historical quotes...")

    quotes = [
        {
            'investor': 'Warren Buffett',
            'quote': "Apple has a consumer product that is extraordinarily sticky. People love their iPhone.",
            'context': {'market_phase': 'bull_market', 'key_themes': ['technology', 'consumer']}
        },
        {
            'investor': 'Peter Lynch',
            'quote': "I'm always looking for companies with 20-30% earnings growth that the market doesn't recognize yet.",
            'context': {'market_phase': 'transition', 'key_themes': ['growth', 'undervalued']}
        },
        {
            'investor': 'Warren Buffett',
            'quote': "Coca-Cola sells 1.9 billion servings a day. That's a business I can understand.",
            'context': {'market_phase': 'neutral', 'key_themes': ['consumer', 'simple']}
        }
    ]

    for quote_data in quotes:
        learning_system.learn_from_quote(
            quote_data['investor'],
            quote_data['quote'],
            quote_data['context']
        )
        print(f"   ✓ Learned from {quote_data['investor']} quote")

    # 2. 현재 상황에서 예측
    print("\n🔮 Making predictions for current market...")

    current_context = {
        'market_phase': 'bear_market',
        'key_themes': ['ai_hype', 'inflation_concerns'],
        'mentioned_companies': ['Apple', 'Tesla'],
        'volatility': 0.8
    }

    for investor in ['Warren Buffett', 'Peter Lynch']:
        prediction = learning_system.predict_investor_behavior(investor, current_context)
        print(f"\n   {investor}:")
        print(f"     Action: {prediction['predicted_action'].upper()}")
        print(f"     Confidence: {prediction['confidence']:.2f}")
        print(f"     Reasoning: {prediction['reasoning']}")

    # 3. 결과로부터 학습 (시뮬레이션)
    print("\n📈 Learning from outcomes...")

    outcomes = [
        {
            'investor': 'Warren Buffett',
            'prediction': {'action': 'buy', 'context': current_context},
            'result': {'performance': 0.25, 'time_horizon': '2y'}
        }
    ]

    for outcome in outcomes:
        learning_system.learn_from_outcome(
            outcome['prediction'],
            outcome['result']
        )
        print(f"   ✓ Learned from {outcome['investor']} outcome (25% gain)")

    print("\n🎯 Learning system is now smarter!")

if __name__ == "__main__":
    demo_learning_system()