# 📋 StockOracle 작업 지시서

> **"다른 개발자나 AI가 이 프로젝트를 쉽게 이해하고 기여할 수 있도록 상세한 가이드"**

---

## 🎯 **프로젝트 개요**

StockOracle은 세계 최고 투자자들의 사고방식을 AI로 복제하여 투자 결정을 돕는 차세대 금융 플랫폼입니다. 단순한 데이터 분석을 넘어, 각 거장의 투자 철학과 성격을 모델링하여 현재 시장 상황에서 그들이 어떤 결정을 내릴지 예측합니다.

### **핵심 가치**
- **뇌 시뮬레이션**: 거장들의 실제 사고방식 복제
- **문맥 인식**: 현재 시장 상황에 따른 동적 예측
- **지속적 학습**: 실제 결과로부터 모델 개선

---

## 🏗️ **시스템 아키텍처 이해**

### **컴포넌트 구조**
```
/Users/bk/stock/
├── 📁 advanced_ai/              # AI 엔진 핵심
│   ├── investor_brain.py        # 거장별 뇌 모델 ★★★
│   ├── knowledge_graph_learner.py # 학습 시스템 ★★
│   └── learning_system.md       # 학습 이론 ★
├── 📁 frontend/                 # Next.js 프론트엔드
│   └── src/
│       ├── app/                # App Router pages
│       ├── components/         # React 컴포넌트
│       └── lib/               # 유틸리티 함수
├── 📁 data/                    # 데이터베이스
│   └── investors/             # 거장 데이터 ★★★
├── 📁 prototype/               # 초기 프로토타입
└── 📁 backend/                # FastAPI 백엔드 (개발 중)
```

**중요도**: ★★★ (매우 중요), ★★ (중요), ★ (참고)

---

## 🧠 **핵심: 거장별 AI 뇌 모델**

### **1. 구조 이해**

#### **기반 클래스 (`InvestorBrain`)**
```python
class InvestorBrain:
    def __init__(self, name: str):
        self.personality = {
            'patience': 0.5,           # 인내심 (0-1)
            'risk_tolerance': 0.5,     # 위험 허용도
            'complexity_tolerance': 0.5, # 복잡성 허용도
            'emotional_volatility': 0.5  # 감정 변동성
        }

    def analyze_company(self, company, context):
        # 각 거장 클래스에서 오버라이드
        raise NotImplementedError
```

#### **거장별 특성**
- **워런 버핏**: `patience: 0.95`, `complexity_tolerance: 0.2`
- **피터 린치**: `risk_tolerance: 0.6`, `growth_orientation: 0.8`
- **하워드 막스**: `cycle_positioning: 0.25`, `risk_control: 0.25`
- **조지 소로스**: `reflexivity_identification: 0.3`, `complexity_tolerance: 0.9`

### **2. 새로운 거장 추가 방법**

#### **Step 1: 데이터 파일 생성**
```bash
# /Users/bk/stock/data/investors/new_investor.json
{
  "investor_info": {
    "name": "New Investor",
    "slug": "new_investor",
    "title": "Title, Company",
    "investment_philosophy": "Core philosophy in 1-2 sentences",
    "famous_quotes": ["Quote 1", "Quote 2"]
  },
  "insights": [
    {
      "id": "investor_001",
      "content": "Specific insight about investing...",
      "source": "Source of insight",
      "source_type": "memo|speech|interview",
      "date_said": "YYYY-MM-DD",
      "sentiment": "bullish|bearish|neutral",
      "confidence_score": 0.85,
      "investment_themes": ["theme1", "theme2"]
    }
  ]
}
```

#### **Step 2: AI 뇌 클래스 구현**
```python
# /Users/bk/stock/advanced_ai/investor_brain.py

class NewInvestorBrain(InvestorBrain):
    """새로운 투자자 뇌 모델"""

    def __init__(self):
        super().__init__("New Investor")

        # 성격 특성 (연구 기반)
        self.personality = {
            'patience': 0.x,
            'risk_tolerance': 0.x,
            'complexity_tolerance': 0.x,
            'time_preference': 'short|medium|long_term',
            'emotional_volatility': 0.x
        }

        # 핵심 투자 원칙 (연구 기반)
        self.core_principles = {
            'principle1': 0.3,
            'principle2': 0.2,
            # 합계 1.0이 되도록 가중치 분배
        }

    def analyze_company(self, company: Company, context: MarketContext) -> InvestorDecision:
        """투자자 방식으로 기업 분석"""

        # 1. 핵심 평가 지표 계산
        score1 = self.evaluate_metric1(company)
        score2 = self.evaluate_metric2(company, context)

        # 2. 종합 점수 계산
        total_score = (
            score1 * self.core_principles['principle1'] +
            score2 * self.core_principles['principle2']
        )

        # 3. 시장 상황 조정
        context_adjustment = self.calculate_context_adjustment(context)
        final_score = max(0, total_score * context_adjustment)

        # 4. 결정 반환
        return InvestorDecision(
            action="buy|hold|sell|avoid",
            confidence=final_score * self.confidence_calibration,
            reasoning=self.generate_reasoning(final_score, company, context),
            emotional_state="emotional_description",
            key_factors=["factor1", "factor2"],
            time_horizon="investment_timeframe"
        )
```

#### **Step 3: 팩토리 함수 업데이트**
```python
# create_investor_brain 함수에 추가
def create_investor_brain(investor_type: str) -> InvestorBrain:
    if investor_type.lower() in ['new investor', 'new']:
        return NewInvestorBrain()
    # ... 기존 코드
```

#### **Step 4: 데모에 추가**
```python
# demo_investor_brains() 함수에 추가
new_brain = create_investor_brain('new investor')
new_decision = new_brain.analyze_company(company, context)
print(f"   🎯 New: {new_decision.action.upper()} ({new_decision.confidence:.2f})")
```

### **3. 테스트 및 검증**

#### **실행 테스트**
```bash
cd /Users/bk/stock/advanced_ai
python3 investor_brain.py
```

#### **예상 결과**
- 각 거장의 일관된 성격 반영
- 현실적인 투자 결정 패턴
- 시장 상황에 따른 다른 반응

---

## 📊 **데이터베이스 관리**

### **거장 데이터 가이드라인**

#### **Insight 데이터 구조**
```json
{
  "id": "unique_identifier",
  "content": "Actual quote or insight text",
  "source": "Where it came from",
  "source_type": "memo|speech|interview|book",
  "date_said": "YYYY-MM-DD",
  "context": "Situation when said",
  "companies_mentioned": ["Company1", "TICKER1"],
  "sentiment": "bullish|bearish|neutral|cautiously_bullish",
  "investment_themes": ["theme1", "theme2"],
  "confidence_score": 0.85,
  "tags": ["tag1", "tag2"]
}
```

#### **품질 기준**
- **내용**: 실제 인용문 또는 정확한 요약
- **감성**: 맥락에 맞는 정확한 감성 분석
- **신뢰도**: 출처의 신뢰도 기반 (0.5-1.0)
- **테마**: 투자 관련 주제 태깅

### **데이터 소스**
- **공식 문서**: 주주 서신, 연차 보고서
- **인터뷰**: Bloomberg, CNBC, Financial Times
- **서적**: 투자 관련 서적
- **강연**: 대학 강연, 컨퍼런스 발표

---

## 🤖 **AI/ML 시스템 이해**

### **1. 지식 그래프 학습**

#### **핵심 개념**
```python
# 지식 트리플 (주어-관계-객체)
KnowledgeTriple(
    subject="Warren Buffett",
    predicate="is_bullish_on",
    object="Apple",
    confidence=0.95,
    context={"market_phase": "bull_market"}
)
```

#### **학습 루프**
1. **데이터 수집**: 새로운 인사이트, 시장 데이터
2. **패턴 인식**: 유사 상황 찾기
3. **예측**: 현재 상황에서의 거장 행동 예측
4. **피드백**: 실제 결과로 모델 업데이트

### **2. 모델 개선 방법**

#### **정확도 향상**
- **데이터 양**: 더 많은 양질의 인사이트
- **맥락 정보**: 시장 상황, 시점, 관련 이벤트
- **개인화**: 각 거장의 뉘앙스 포착

#### **성능 측정**
```python
# 예측 정확도 계산
def calculate_accuracy(prediction, actual_outcome):
    if prediction.action == 'buy' and actual_outcome.performance > 0.05:
        return 1.0
    elif prediction.action == 'sell' and actual_outcome.performance < -0.05:
        return 1.0
    else:
        return max(0, 1 - abs(actual_outcome.performance) * 10)
```

---

## 🎨 **프론트엔드 개발**

### **컴포넌트 구조**

#### **핵심 컴포넌트**
- **`StockSearchBar`**: 주식 검색 및 자동완성
- **`InvestorInsightCard`**: 거장 인사이트 카드
- **`StockAnalysisDashboard`**: 종목 분석 대시보드
- **`MarketContextDisplay`**: 시장 상황 표시

#### **스타일 가이드**
```css
/* 색상 팔레트 */
--navy-50: #f8fafc;
--navy-900: #0f172a;
--primary-600: #3b82f6;
--success-600: #22c55e;

/* 컴포넌트 스타일 */
.card: bg-white rounded-xl shadow-lg;
.btn-primary: bg-primary-600 hover:bg-primary-700;
.glass: backdrop-filter: blur(10px);
```

### **새로운 페이지 추가**

#### **1. 페이지 생성**
```tsx
// /Users/bk/stock/frontend/src/app/investors/[slug]/page.tsx
export default function InvestorPage({ params }: { params: { slug: string } }) {
  return <InvestorProfile slug={params.slug} />;
}
```

#### **2. 컴포넌트 개발**
```tsx
// /Users/bk/stock/frontend/src/components/investors/InvestorProfile.tsx
export function InvestorProfile({ slug }: { slug: string }) {
  const investor = getInvestorBySlug(slug);
  const insights = getInvestorInsights(slug);

  return (
    <div className="container mx-auto px-6 py-8">
      <InvestorHeader investor={investor} />
      <InsightsList insights={insights} />
    </div>
  );
}
```

---

## 🔄 **개발 워크플로우**

### **1. 새로운 기능 개발**

#### **Step 1: 이슈 생성**
```
Title: [FEAT] 기능 이름
Description:
- 목표: 무엇을 구현할 것인가
- 방법: 어떻게 구현할 것인가
- 기대 결과: 어떤 결과를 기대하는가
```

#### **Step 2: 브랜치 생성**
```bash
git checkout -b feature/기능이름
```

#### **Step 3: 개발 및 테스트**
- AI 모델 변경: `python3 investor_brain.py`로 테스트
- 프론트엔드: `npm run dev`로 확인
- 데이터: JSON 구조 검증

#### **Step 4: PR 생성**
```markdown
## 변경 내용
- 기능 1 구현
- 기능 2 수정

## 테스트 결과
- [x] AI 모델 정상 작동
- [x] 프론트엔드 렌더링 확인
- [x] 데이터 무결성 검증

## 스크린샷
(필요시)
```

### **2. 버그 수정**

#### **디버깅 방법**
- **AI 모델**: `print()` 디버깅으로 점수 계산 확인
- **프론트엔드**: React DevTools로 상태 확인
- **데이터**: JSON Linter로 구조 확인

---

## 📋 **체크리스트**

### **새로운 거장 추가**
- [ ] 투자 철학 연구 및 정리
- [ ] 데이터 파일 생성 (`data/investors/`)
- [ ] AI 뇌 클래스 구현 (`advanced_ai/`)
- [ ] 팩토리 함수 업데이트
- [ ] 데모에 추가 및 테스트
- [ ] README.md 업데이트

### **새로운 기능 개발**
- [ ] 요구사항 분석
- [ ] 설계 문서 작성
- [ ] 핵심 로직 구현
- [ ] 테스트 코드 작성
- [ ] UI/UX 개발
- [ ] 통합 테스트
- [ ] 문서 업데이트

### **코드 품질**
- [ ] 타입 힌트 추가 (Python)
- [ ] TypeScript 타입 정의
- [ ] 에러 핸들링
- [ ] 로깅 추가
- [ ] 성능 최적화

---

## 🛠️ **개발 환경 설정**

### **로컬 개발**
```bash
# AI 엔진
cd /Users/bk/stock/advanced_ai
python3 -m venv venv
source venv/bin/activate
pip install networkx numpy

# 프론트엔드
cd /Users/bk/stock/frontend
npm install
npm run dev
```

### **테스트 데이터**
```bash
# 샘플 데이터 확인
ls /Users/bk/stock/data/investors/
# AI 모델 테스트
python3 /Users/bk/stock/advanced_ai/investor_brain.py
```

---

## 📞 **문의 및 지원**

### **기술 질문**
- **AI/ML**: 거장 모델링, 학습 알고리즘
- **프론트엔드**: React, TypeScript, 스타일링
- **데이터**: JSON 구조, 데이터 수집
- **금융**: 투자 이론, 시장 분석

### **커뮤니케이션**
- **GitHub Issues**: 기술적 문제 및 기능 요청
- **코드 리뷰**: 모든 PR은 최소 1명의 리뷰 필요
- **문서화**: 중요한 변경은 반드시 문서 업데이트

---

## 🎯 **성공 기준**

### **기술적 성공**
- [ ] 5명 이상의 거장 AI 모델 구현
- [ ] 70% 이상의 예측 정확도
- [ ] 실시간 데이터 연동
- [ ] 사용자 친화적 UI/UX

### **비즈니스 성공**
- [ ] 1000+ 활성 사용자
- [ ] 긍정적인 사용자 피드백
- [ ] 기관 고객 확보
- [ ] 지속적인 수익 모델

---

> 💡 **기여하는 모든 개발자와 AI에게:**
> 이 프로젝트는 단순한 코드가 아니라, 세계 최고의 투자 지혜를 디지털로 영구화하는 역사적인 작업입니다. 당신의 기여가 미래 투자자들의 길잡이가 될 것입니다. 🚀✨