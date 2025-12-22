#!/usr/bin/env python3
"""
🚀 StockOracle FastAPI Backend
Railway 배포용 API 서버
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(
    title="StockOracle API",
    description="🧠 거장 투자자들의 뇌를 시뮬레이션하는 AI API",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """API 상태 확인"""
    return {
        "status": "🚀 StockOracle API is running!",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "investors": "/api/investors"
        }
    }

@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {"status": "healthy", "service": "stockoracle-api"}

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

# ==================== Run Server ====================

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)