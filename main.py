#!/usr/bin/env python3
"""
🚀 StockOracle FastAPI Backend
Railway 배포용 API 서버
"""

import os
import sys
from pathlib import Path

# advanced_ai 모듈 경로 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import json
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# AI 엔진 import
from advanced_ai.investor_brain import (
    create_investor_brain,
    Company,
    MarketContext,
    MarketPhase,
    InvestorDecision
)

app = FastAPI(
    title="StockOracle API",
    description="🧠 거장 투자자들의 뇌를 시뮬레이션하는 AI API",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://*.railway.app",
        os.getenv("FRONTEND_URL", "*")
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== Pydantic Models ====================

class CompanyInput(BaseModel):
    ticker: str
    name: str
    sector: str
    pe_ratio: float
    pb_ratio: float
    roe: float
    debt_equity: float
    revenue_growth: float
    business_complexity: float = 0.5
    moat_strength: float = 0.5
    growth_stage: str = "mature"

class MarketContextInput(BaseModel):
    phase: str = "bull_market"  # bull_market, bear_market, transition, uncertain
    volatility: float = 0.3
    sentiment_score: float = 0.5
    valuation_level: float = 0.5
    key_themes: List[str] = []
    risk_factors: List[str] = []

class AnalysisRequest(BaseModel):
    company: CompanyInput
    context: Optional[MarketContextInput] = None
    investors: List[str] = ["warren_buffett", "peter_lynch", "howard_marks", "george_soros"]

class InvestorDecisionResponse(BaseModel):
    investor: str
    action: str
    confidence: float
    reasoning: str
    emotional_state: str
    key_factors: List[str]
    time_horizon: str

class AnalysisResponse(BaseModel):
    ticker: str
    company_name: str
    decisions: List[InvestorDecisionResponse]
    consensus: str
    consensus_confidence: float

# ==================== Helper Functions ====================

def get_market_phase(phase_str: str) -> MarketPhase:
    """문자열을 MarketPhase enum으로 변환"""
    phase_map = {
        "bull_market": MarketPhase.BULL_MARKET,
        "bear_market": MarketPhase.BEAR_MARKET,
        "transition": MarketPhase.TRANSITION,
        "uncertain": MarketPhase.UNCERTAIN
    }
    return phase_map.get(phase_str.lower(), MarketPhase.UNCERTAIN)

def get_investor_name(investor_type: str) -> str:
    """투자자 타입을 이름으로 변환"""
    name_map = {
        "warren_buffett": "Warren Buffett",
        "buffett": "Warren Buffett",
        "peter_lynch": "Peter Lynch",
        "lynch": "Peter Lynch",
        "howard_marks": "Howard Marks",
        "marks": "Howard Marks",
        "george_soros": "George Soros",
        "soros": "George Soros"
    }
    return name_map.get(investor_type.lower(), investor_type)

def calculate_consensus(decisions: List[InvestorDecisionResponse]) -> tuple:
    """거장들의 합의 계산"""
    action_scores = {"buy": 1, "hold": 0, "sell": -1, "avoid": -0.5}
    
    total_score = 0
    total_confidence = 0
    
    for decision in decisions:
        score = action_scores.get(decision.action.lower(), 0)
        total_score += score * decision.confidence
        total_confidence += decision.confidence
    
    avg_score = total_score / len(decisions) if decisions else 0
    avg_confidence = total_confidence / len(decisions) if decisions else 0
    
    if avg_score > 0.3:
        consensus = "BUY"
    elif avg_score < -0.3:
        consensus = "AVOID"
    else:
        consensus = "HOLD"
    
    return consensus, avg_confidence

# ==================== API Endpoints ====================

@app.get("/")
async def root():
    """API 상태 확인"""
    return {
        "status": "🚀 StockOracle API is running!",
        "version": "1.0.0",
        "endpoints": {
            "analyze": "/api/analyze",
            "investors": "/api/investors",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {"status": "healthy", "service": "stockoracle-api"}

@app.get("/healthz")
async def health_check_z():
    """Alternative health check endpoint"""
    return {"status": "healthy", "service": "stockoracle-api"}

@app.get("/")
async def root():
    """API 상태 확인"""
    return {
        "status": "🚀 StockOracle API is running!",
        "version": "1.0.0",
        "endpoints": {
            "analyze": "/api/analyze",
            "investors": "/api/investors",
            "health": "/health"
        }
    }

@app.get("/api/investors")
async def get_investors():
    """사용 가능한 거장 투자자 목록"""
    investors = [
        {
            "id": "warren_buffett",
            "name": "Warren Buffett",
            "title": "Chairman & CEO, Berkshire Hathaway",
            "philosophy": "Value investing with focus on moats",
            "style": "Long-term, conservative"
        },
        {
            "id": "peter_lynch",
            "name": "Peter Lynch",
            "title": "Former Manager, Fidelity Magellan Fund",
            "philosophy": "Growth investing, invest in what you know",
            "style": "Medium-term, growth-oriented"
        },
        {
            "id": "howard_marks",
            "name": "Howard Marks",
            "title": "Co-Chairman, Oaktree Capital",
            "philosophy": "Cycle awareness and risk management",
            "style": "Contrarian, risk-focused"
        },
        {
            "id": "george_soros",
            "name": "George Soros",
            "title": "Chairman, Soros Fund Management",
            "philosophy": "Reflexivity theory and macro investing",
            "style": "Short-term, aggressive"
        }
    ]
    return {"investors": investors}

@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_stock(request: AnalysisRequest):
    """주식 분석 - 거장들의 관점에서"""
    
    try:
        # Company 객체 생성
        company = Company(
            ticker=request.company.ticker,
            name=request.company.name,
            sector=request.company.sector,
            pe_ratio=request.company.pe_ratio,
            pb_ratio=request.company.pb_ratio,
            roe=request.company.roe,
            debt_equity=request.company.debt_equity,
            revenue_growth=request.company.revenue_growth,
            business_complexity=request.company.business_complexity,
            moat_strength=request.company.moat_strength,
            growth_stage=request.company.growth_stage
        )
        
        # MarketContext 설정
        if request.context:
            context = MarketContext(
                phase=get_market_phase(request.context.phase),
                volatility=request.context.volatility,
                sentiment_score=request.context.sentiment_score,
                valuation_level=request.context.valuation_level,
                key_themes=request.context.key_themes,
                risk_factors=request.context.risk_factors
            )
        else:
            # 기본 시장 상황
            context = MarketContext(
                phase=MarketPhase.UNCERTAIN,
                volatility=0.3,
                sentiment_score=0.5,
                valuation_level=0.5,
                key_themes=["AI", "inflation"],
                risk_factors=["geopolitical"]
            )
        
        # 각 거장의 분석 수행
        decisions = []
        for investor_type in request.investors:
            try:
                brain = create_investor_brain(investor_type)
                decision = brain.analyze_company(company, context)
                
                decisions.append(InvestorDecisionResponse(
                    investor=get_investor_name(investor_type),
                    action=decision.action,
                    confidence=decision.confidence,
                    reasoning=decision.reasoning,
                    emotional_state=decision.emotional_state,
                    key_factors=decision.key_factors,
                    time_horizon=decision.time_horizon
                ))
            except ValueError as e:
                # 알 수 없는 투자자 타입은 건너뜀
                continue
        
        if not decisions:
            raise HTTPException(status_code=400, detail="No valid investors specified")
        
        # 합의 계산
        consensus, consensus_confidence = calculate_consensus(decisions)
        
        return AnalysisResponse(
            ticker=company.ticker,
            company_name=company.name,
            decisions=decisions,
            consensus=consensus,
            consensus_confidence=consensus_confidence
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/investors/{investor_id}/data")
async def get_investor_data(investor_id: str):
    """거장 투자자 상세 데이터"""
    
    data_path = Path(__file__).parent.parent / "data" / "investors" / f"{investor_id}.json"
    
    if not data_path.exists():
        raise HTTPException(status_code=404, detail=f"Investor {investor_id} not found")
    
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    return data

# ==================== Run Server ====================

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

