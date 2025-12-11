"""
FastAPI 메인 서버
프롬프트 엔지니어링 자동화 API
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import asyncio

from .services import (
    IntentAnalyzer,
    TrendCollector,
    PromptGenerator,
    ConfirmationModule,
)
from .models.schemas import (
    UserQuery,
    IntentAnalysisResult,
    TrendResult,
    GeneratedPrompts,
    PromptStrategyType,
)

# FastAPI 앱 초기화
app = FastAPI(
    title="프롬프트 엔지니어링 자동화 API",
    description="AI를 활용한 최적화된 프롬프트 자동 생성 시스템",
    version="1.0.0",
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인만 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 서비스 인스턴스
intent_analyzer = IntentAnalyzer()
trend_collector = TrendCollector()
prompt_generator = PromptGenerator()
confirmation_module = ConfirmationModule()


# 응답 모델
class AnalysisResponse(BaseModel):
    """분석 응답"""

    query: str
    intent: IntentAnalysisResult
    trends: TrendResult
    confirmation_message: str


class PromptsResponse(BaseModel):
    """프롬프트 생성 응답"""

    prompts: GeneratedPrompts
    selection_message: str


class FinalPromptRequest(BaseModel):
    """최종 프롬프트 요청"""

    strategy_type: PromptStrategyType


# API 엔드포인트


@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "프롬프트 엔지니어링 자동화 API",
        "version": "1.0.0",
        "endpoints": {
            "analyze": "/api/analyze",
            "generate_prompts": "/api/generate-prompts",
            "full_pipeline": "/api/pipeline",
        },
    }


@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {"status": "healthy"}


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_query(query: UserQuery):
    """
    1단계: 사용자 쿼리 분석 및 트렌드 수집

    Args:
        query: 사용자 쿼리

    Returns:
        분석 결과 및 확인 메시지
    """
    try:
        # 1. 의도 분석
        intent = await intent_analyzer.analyze(query.query)

        # 2. 트렌드 수집
        trends = await trend_collector.collect(intent.keywords, intent)

        # 3. 확인 메시지 생성
        confirmation_msg = confirmation_module.generate_confirmation_message(
            query.query, intent, trends
        )

        return AnalysisResponse(
            query=query.query,
            intent=intent,
            trends=trends,
            confirmation_message=confirmation_msg,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"분석 실패: {str(e)}")


@app.post("/api/generate-prompts", response_model=PromptsResponse)
async def generate_prompts(analysis: AnalysisResponse):
    """
    2단계: 5가지 프롬프팅 전략 생성

    Args:
        analysis: 1단계에서 받은 분석 결과

    Returns:
        생성된 프롬프트들
    """
    try:
        # 프롬프트 생성
        prompts = await prompt_generator.generate_all(
            analysis.query, analysis.trends, analysis.intent
        )

        # 선택 메시지 생성
        selection_msg = confirmation_module.generate_strategy_selection_message(
            len(prompts.prompts)
        )

        return PromptsResponse(prompts=prompts, selection_message=selection_msg)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"프롬프트 생성 실패: {str(e)}")


@app.post("/api/pipeline")
async def full_pipeline(query: UserQuery):
    """
    전체 파이프라인: 분석 → 프롬프트 생성을 한 번에 수행

    Args:
        query: 사용자 쿼리

    Returns:
        전체 결과 (분석 + 프롬프트)
    """
    try:
        # 1단계: 분석
        analysis_result = await analyze_query(query)

        # 2단계: 프롬프트 생성
        prompts_result = await generate_prompts(analysis_result)

        return {
            "analysis": analysis_result,
            "prompts": prompts_result,
            "status": "success",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"파이프라인 실패: {str(e)}")


# 개별 프롬프트 조회


@app.get("/api/strategies")
async def get_available_strategies():
    """
    사용 가능한 프롬프팅 전략 목록 조회

    Returns:
        전략 목록
    """
    strategies = [
        {
            "type": "cot",
            "name": "사고 연쇄 (CoT)",
            "icon": "🧠",
            "description": "논리적 단계별 사고",
            "best_for": "복잡한 계획/분석",
        },
        {
            "type": "few_shot",
            "name": "예시 학습 (Few-Shot)",
            "icon": "📝",
            "description": "예시를 통한 스타일 모방",
            "best_for": "블로그/에세이",
        },
        {
            "type": "meta",
            "name": "전문가 모드 (Meta-Prompting)",
            "icon": "👨‍🏫",
            "description": "전문가 페르소나",
            "best_for": "객관적 분석",
        },
        {
            "type": "self_refine",
            "name": "자체 개선 (Self-Refine)",
            "icon": "🔄",
            "description": "반복적 개선",
            "best_for": "고퀄리티 콘텐츠",
        },
        {
            "type": "structured",
            "name": "구조화 분석 (Structured)",
            "icon": "📊",
            "description": "체계적 보고서",
            "best_for": "데이터 분석/리서치",
        },
    ]

    return {"strategies": strategies}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
