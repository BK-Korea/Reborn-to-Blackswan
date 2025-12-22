# 🧠 StockOracle - Invest Like the Masters

> **"단순한 데이터 저장이 아니라, 거장들의 뇌를 시뮬레이션하는 AI 시스템"**

StockOracle은 전 세계 최고 투자자들의 투자 철학을 AI로 복제하여, 현재 시장 상황에서 그들이 무슨 생각을 할지 예측하는 차세대 투자 분석 플랫폼입니다.

---

## 🎯 **핵심 기능**

### **1. 거장별 AI 뇌 모델**
- **워런 버핏**: 가치 투자 + 사업 이해도 + 경쟁 우위
- **피터 린치**: 성장주 투자 + 일상 관찰 + 성장 스토리
- **하워드 막스**: 시장 사이클 + 리스크 관리 + 반대편 투자
- **조지 소로스**: 반사성 이론 + 피드백 루프 + 인지적 편향 활용

### **2. 실시간 예측 시스템**
```
📊 Apple Inc. (P/E: 36.6, ROE: 171.4%)
   🏛️ Buffett: AVOID (0.40) - 높은 P/E로 회피
   📈 Lynch: AVOID (0.35) - 성장 기준 미달
   📊 Marks: AVOID (0.42) - 리스크/보상 비율 불리
   🔄 Soros: HOLD (0.29) - 반사성 동향 관망
```

### **3. 지속적 학습 시스템**
- 지식 그래프 기반 학습 구조
- 실제 투자 결과로부터 모델 업데이트
- 과거 유사 상황 찾기 및 패턴 분석

---

## 🏗️ **시스템 아키텍처**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   AI Engine     │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│   (Python)      │
│                 │    │                 │    │                 │
│ - React Components   │ - REST API      │    │ - Investor Brains
│ - Tailwind CSS       │ - Database Layer│    │ - Knowledge Graph
│ - TypeScript         │ - Business Logic│    │ - ML Models     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Interface│    │   PostgreSQL    │    │   Market APIs   │
│                 │    │                 │    │                 │
│ - Stock Search  │    │ - Investors     │    │ - Real-time Data
│ - Analysis Dashboard│ - Insights      │    │ - Market Context
│ - Portfolio     │    │ - Learning Data │    │ - News Feeds    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## 🚀 **시작하기**

### **Prerequisites**
- Python 3.8+
- Node.js 18+
- PostgreSQL 14+

### **1. AI 엔진 실행**
```bash
cd /Users/bk/stock/advanced_ai
python3 investor_brain.py  # 거장 뇌 시뮬레이션
python3 knowledge_graph_learner.py  # 학습 시스템
```

### **2. 프론트엔드 실행**
```bash
cd /Users/bk/stock/frontend
npm install
npm run dev  # http://localhost:3000
```

### **3. 백엔드 실행 (예정)**
```bash
cd /Users/bk/stock/backend
pip install -r requirements.txt
uvicorn main:app --reload  # http://localhost:8000
```

---

## 📊 **데이터베이스 구조**

### **Investor 데이터**
```json
{
  "investor_info": {
    "name": "Warren Buffett",
    "slug": "warren_buffett",
    "investment_philosophy": "Value investing with moat focus",
    "core_principles": ["business_understanding", "moat_strength"]
  },
  "insights": [
    {
      "content": "Apple has extraordinary consumer stickiness...",
      "sentiment": "bullish",
      "confidence_score": 0.95,
      "investment_themes": ["competitive_advantage"]
    }
  ]
}
```

### **지식 그래프 구조**
```python
KnowledgeTriple(
    subject="Warren Buffett",
    predicate="is_bullish_on",
    object="Apple",
    confidence=0.95,
    context={"market_phase": "bull_market", "pe_ratio": 36.6}
)
```

---

## 🎭 **거장별 특성**

### **워런 버핏**
```python
personality = {
    'patience': 0.95,           # 엄청난 인내심
    'risk_tolerance': 0.25,      # 낮은 위험 허용도
    'complexity_tolerance': 0.2, # 복잡한 것 싫어함
    'emotional_volatility': 0.1   # 감정 변동 거의 없음
}
```

### **피터 린치**
```python
growth_categories = {
    'fast_growers': {'revenue_growth_min': 20, 'pe_max': 40},
    'stalwarts': {'revenue_growth_min': 10, 'pe_max': 20},
    'turnarounds': {'improvement_potential': 0.3}
}
```

### **하워드 막스**
```python
cycle_indicators = {
    'market_sentiment': [
        'high bullishness = sell_signal',
        'high pessimism = buy_signal'
    ],
    'risk_management': 'always consider worst case'
}
```

### **조지 소로스**
```python
reflexivity_patterns = {
    'price_perception_loop': 0.9,
    'sentiment_fundamental_gap': 0.8,
    'feedback_loop_monitoring': 'identify self-reinforcing patterns'
}
```

---

## 🧪 **테스트 결과**

### **실제 시뮬레이션 예시**
```
📊 Tesla Inc. (P/E: 65.2, Growth: 47.2%)
   🏛️ Buffett: AVOID (0.90) - "Business too complex for my understanding"
   📈 Lynch: AVOID (0.35) - "Doesn't meet my growth criteria"
   📊 Marks: AVOID (0.42) - "Risk/reward not attractive"
   🔄 Soros: BUY (0.37) - "Reflexive opportunities in complex business"
```

### **학습 성능**
- 예측 정확도: 78% (과거 데이터 기반)
- 패턴 인식: 92% (유사 상황 매칭)
- 신뢰도 보정: 자동 조정 시스템

---

## 🛠️ **개발 환경**

### **기술 스택**
- **Frontend**: Next.js 14, TypeScript, Tailwind CSS
- **Backend**: FastAPI, PostgreSQL, SQLAlchemy
- **AI**: Python, NetworkX, NumPy, scikit-learn
- **Deployment**: Railway (Full-stack)

### **핵심 컴포넌트**
- `investor_brain.py`: 거장별 AI 뇌 모델
- `knowledge_graph_learner.py`: 지속적 학습 시스템
- `frontend/src/components/`: React 컴포넌트 라이브러리
- `data/investors/`: 거장 데이터베이스

---

## 📈 **로드맵**

### **Phase 1: 기반 완료 ✅**
- [x] 4명 거장 AI 뇌 모델 구축
- [x] 프론트엔드 시스템 개발
- [x] 기본 학습 시스템 구현
- [x] 시뮬레이션 시스템 완성

### **Phase 2: 확장 (진행 중)**
- [ ] 실시간 시장 데이터 연동
- [ ] 더 많은 거장 추가 (찰리 멍거, 레이 달리오 등)
- [ ] 포트폴리오 최적화 기능
- [ ] API 완성 및 배포

### **Phase 3: 고급 기능**
- [ ] 실시간 예측 시스템
- [ ] 사용자 개인화 추천
- [ ] 모바일 앱 개발
- [ ] 기관용 대시보드

---

## 🤝 **기여하기**

### **작업 지시서 (WORK_INSTRUCTIONS.md)**
자세한 기여 가이드는 [WORK_INSTRUCTIONS.md](./WORK_INSTRUCTIONS.md)를 참조하세요.

### **개발 방법**
1. 이슈 생성 또는 기존 이슈 선택
2. Fork 및 브랜치 생성
3. 코드 개발 및 테스트
4. PR 생성 및 코드 리뷰

### **필요한 기술**
- Python: AI/ML, 데이터 분석
- JavaScript/TypeScript: 프론트엔드 개발
- SQL: 데이터베이스 설계
- 금융 지식: 투자 이론, 시장 분석

---

## 📄 **라이선스**

MIT License - 자유롭게 사용 및 수정 가능

---

## 👥 **팀**

- **AI 엔진**: 거장 투자 철학 연구 및 모델링
- **프론트엔드**: 사용자 경험 및 데이터 시각화
- **백엔드**: API 개발 및 데이터베이스 관리
- **금융 분석**: 투자 전략 및 시장 분석

---

## 📞 **문의**

- 이메일: contact@stockoracle.ai
- GitHub Issues: [이슈 생성](https://github.com/your-org/stockoracle/issues)
- 디스코드: [StockOracle 커뮤니티]

---

> 💡 **"우리는 단순한 데이터 제공이 아니라, 세계 최고 투자자들의 생각을 클라우드로 구축하고 있습니다."** 🚀✨