"""
데이터 스키마 정의
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


class UserQuery(BaseModel):
    """사용자 쿼리"""

    query: str = Field(..., description="사용자 입력 쿼리")
    context: Optional[str] = Field(None, description="추가 컨텍스트")


class IntentCategory(str, Enum):
    """의도 카테고리"""

    INFO_SEARCH = "정보 검색"
    CONTENT_CREATION = "콘텐츠 생성"
    PROBLEM_SOLVING = "문제 해결"
    LEARNING = "학습/교육"
    CREATIVE = "창작"


class OutputType(str, Enum):
    """출력 타입"""

    BLOG = "블로그"
    REPORT = "리포트"
    ESSAY = "에세이"
    ANALYSIS = "분석"
    GUIDE = "가이드"
    TUTORIAL = "튜토리얼"


class IntentAnalysisResult(BaseModel):
    """의도 분석 결과"""

    primary_intent: IntentCategory
    keywords: List[str]
    target_audience: str
    output_type: OutputType
    domain: str
    confidence: float = Field(..., ge=0.0, le=1.0)


class TrendResult(BaseModel):
    """트렌드 검색 결과"""

    trends: List[str] = Field(..., max_length=10)
    summary: str
    sources: List[str]


class ConfirmationResponse(BaseModel):
    """사용자 확인 응답"""

    confirmed: bool
    feedback: Optional[str] = None


class PromptStrategyType(str, Enum):
    """프롬프트 전략 타입"""

    COT = "cot"  # Chain of Thought
    FEW_SHOT = "few_shot"  # Few-Shot Learning
    META = "meta"  # Meta-Prompting
    SELF_REFINE = "self_refine"  # Self-Refine
    STRUCTURED = "structured"  # Structured Context


class PromptStrategy(BaseModel):
    """프롬프트 전략"""

    type: PromptStrategyType
    name: str
    description: str
    icon: str
    best_for: str
    prompt: str


class GeneratedPrompts(BaseModel):
    """생성된 프롬프트들"""

    prompts: List[PromptStrategy]
    query: str
    intent: IntentAnalysisResult
    trends: TrendResult


class PromptResponse(BaseModel):
    """최종 프롬프트 응답"""

    selected_strategy: PromptStrategyType
    final_prompt: str
    metadata: Dict[str, Any]
