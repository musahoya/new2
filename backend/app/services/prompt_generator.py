"""
프롬프트 생성 엔진
5가지 프롬프팅 전략을 사용하여 최적화된 프롬프트를 생성합니다.
"""
from typing import List
from ..models.schemas import (
    PromptStrategy,
    PromptStrategyType,
    GeneratedPrompts,
    IntentAnalysisResult,
    TrendResult,
)


class PromptGenerator:
    """프롬프트 생성기"""

    def __init__(self):
        self.strategies = {
            PromptStrategyType.COT: self.generate_cot,
            PromptStrategyType.FEW_SHOT: self.generate_few_shot,
            PromptStrategyType.META: self.generate_meta,
            PromptStrategyType.SELF_REFINE: self.generate_self_refine,
            PromptStrategyType.STRUCTURED: self.generate_structured,
        }

    async def generate_all(
        self, query: str, trends: TrendResult, intent: IntentAnalysisResult
    ) -> GeneratedPrompts:
        """
        모든 프롬프팅 전략을 사용하여 프롬프트를 생성합니다.

        Args:
            query: 사용자 쿼리
            trends: 트렌드 결과
            intent: 의도 분석 결과

        Returns:
            GeneratedPrompts: 생성된 모든 프롬프트
        """

        prompts = []

        for strategy_type, generator_func in self.strategies.items():
            prompt_strategy = generator_func(query, trends, intent)
            prompts.append(prompt_strategy)

        return GeneratedPrompts(
            prompts=prompts, query=query, intent=intent, trends=trends
        )

    def generate_cot(
        self, query: str, trends: TrendResult, intent: IntentAnalysisResult
    ) -> PromptStrategy:
        """Chain of Thought (사고 연쇄) 프롬프트 생성"""

        prompt_content = f"""다음 단계에 따라 차근차근 생각해 봐:

**주제: {query}**

**1단계: 현재 상황 분석**
- {trends.trends[0]}를 고려했을 때의 현황
- 사용자가 원하는 것: {intent.primary_intent.value}
- 대상 독자: {intent.target_audience}

**2단계: 핵심 요소 파악**
- 트렌드 1: {trends.trends[1] if len(trends.trends) > 1 else '관련 트렌드'}
- 트렌드 2: {trends.trends[2] if len(trends.trends) > 2 else '관련 트렌드'}
- 이들이 주제에 미치는 영향 분석

**3단계: 구체적 계획 수립**
다음 관점에서 접근:
- [A] {trends.trends[3] if len(trends.trends) > 3 else '첫 번째 접근법'}
- [B] {trends.trends[4] if len(trends.trends) > 4 else '두 번째 접근법'}
- [C] {trends.trends[5] if len(trends.trends) > 5 else '세 번째 접근법'}

**4단계: 최종 정리 및 제안**
- {intent.output_type.value} 형식으로 정리
- 핵심 메시지와 실행 가능한 제안 포함

각 단계별로 왜 그렇게 판단했는지 논리적으로 설명하며 답변해줘.
"""

        return PromptStrategy(
            type=PromptStrategyType.COT,
            name="사고 연쇄 (CoT)",
            description="논리적 단계별 사고 과정을 통한 분석",
            icon="🧠",
            best_for="복잡한 계획, 분석, 문제 해결",
            prompt=prompt_content,
        )

    def generate_few_shot(
        self, query: str, trends: TrendResult, intent: IntentAnalysisResult
    ) -> PromptStrategy:
        """Few-Shot Learning 프롬프트 생성"""

        # 의도에 따른 예시 생성
        examples = self._get_examples_for_intent(intent)

        prompt_content = f"""아래 예시들의 스타일을 참고하여 {intent.output_type.value} 형식으로 작성해줘:

{examples}

이제 다음 주제로 작성해줘:

**주제:** {query}

**반영할 최신 트렌드:**
- {trends.trends[0]}
- {trends.trends[1] if len(trends.trends) > 1 else ''}
- {trends.trends[2] if len(trends.trends) > 2 else ''}

**대상 독자:** {intent.target_audience}

**작성 규칙:**
1. 위 예시들의 톤과 구조를 유지할 것
2. 최신 트렌드를 자연스럽게 녹여낼 것
3. {intent.target_audience}가 공감할 수 있는 내용으로 작성
4. {intent.output_type.value} 형식에 맞는 길이와 구조 유지
"""

        return PromptStrategy(
            type=PromptStrategyType.FEW_SHOT,
            name="예시 학습 (Few-Shot)",
            description="구체적인 예시를 통한 스타일 모방",
            icon="📝",
            best_for="블로그, 에세이, 스타일 통일이 필요한 콘텐츠",
            prompt=prompt_content,
        )

    def generate_meta(
        self, query: str, trends: TrendResult, intent: IntentAnalysisResult
    ) -> PromptStrategy:
        """Meta-Prompting (전문가 페르소나) 프롬프트 생성"""

        prompt_content = f"""당신은 15년 경력의 {intent.domain} 분야 전문가입니다.

**전문 지식:**
- {trends.trends[0]}에 대한 심층 이해
- {trends.trends[1] if len(trends.trends) > 1 else intent.domain + ' 최신 동향'} 전문가
- 풍부한 실무 경험과 데이터 분석 능력 보유

**페르소나:**
- 역할: {intent.domain} 전문 컨설턴트
- 강점: 객관적 데이터 기반 분석, 실용적 조언
- 스타일: 전문적이지만 이해하기 쉽게 설명

**작성할 주제:**
"{query}"

**반영할 최신 정보:**
{chr(10).join(f"- {t}" for t in trends.trends[:5])}

**작성 규칙:**
1. 전문가 관점에서 객관적으로 분석
2. 데이터와 사례를 근거로 제시
3. {intent.target_audience}가 이해할 수 있는 수준으로 설명
4. 실용적이고 실행 가능한 조언 제공
5. {intent.output_type.value} 형식으로 체계적으로 구성

전문가로서 깊이 있는 분석과 통찰을 제공해주세요.
"""

        return PromptStrategy(
            type=PromptStrategyType.META,
            name="전문가 모드 (Meta-Prompting)",
            description="전문가 페르소나를 부여한 심층 분석",
            icon="👨‍🏫",
            best_for="전문적 리뷰, 객관적 분석, 권위 있는 콘텐츠",
            prompt=prompt_content,
        )

    def generate_self_refine(
        self, query: str, trends: TrendResult, intent: IntentAnalysisResult
    ) -> PromptStrategy:
        """Self-Refine (자체 개선) 프롬프트 생성"""

        prompt_content = f""""{query}"에 대한 {intent.output_type.value}를 3단계로 개선하며 작성해줘:

**[1단계: 초안 작성]**
일단 다음을 고려해서 빠르게 작성:
- 핵심 주제: {query}
- 주요 트렌드: {trends.trends[0]}
- 대상: {intent.target_audience}

초안을 작성한 후 "=== 초안 완료 ===" 표시

**[2단계: 1차 수정]**
초안을 검토하고 다음을 개선:

✅ 추가할 내용:
- {trends.trends[1] if len(trends.trends) > 1 else '부족한 정보'} 보완
- {trends.trends[2] if len(trends.trends) > 2 else '추가 트렌드'} 반영

✅ 수정할 부분:
- 애매한 표현을 명확하게
- 구조와 흐름 개선
- 불필요한 반복 제거

1차 수정 후 "=== 1차 수정 완료 ===" 표시

**[3단계: 최종본]**
1차 수정본을 다시 검토하고:

✅ 마지막 점검:
- {trends.trends[3] if len(trends.trends) > 3 else '최신 정보'} 최종 반영
- {intent.target_audience}에게 더 와닿게 조정
- 임팩트 있는 시작과 마무리
- 전체 톤과 일관성 확인

✅ 폴리싱:
- 문장 다듬기
- 가독성 향상
- {intent.output_type.value} 형식에 최적화

최종본 작성 후 "=== 최종본 완료 ===" 표시

**중요:** 각 단계를 모두 보여주고, 무엇을 왜 수정했는지 간단히 설명해줘.
"""

        return PromptStrategy(
            type=PromptStrategyType.SELF_REFINE,
            name="자체 개선 (Self-Refine)",
            description="초안부터 시작해 반복적으로 개선",
            icon="🔄",
            best_for="고퀄리티 콘텐츠, 정교한 글쓰기",
            prompt=prompt_content,
        )

    def generate_structured(
        self, query: str, trends: TrendResult, intent: IntentAnalysisResult
    ) -> PromptStrategy:
        """Structured Context (구조화된 분석) 프롬프트 생성"""

        prompt_content = f""""{query}"를 체계적으로 분석하여 {intent.output_type.value} 형식의 보고서로 작성:

## 📋 1. 개요 및 현황 분석

### 1.1 주제 정의
- 핵심 주제: {query}
- 분석 목적: {intent.primary_intent.value}
- 대상 독자: {intent.target_audience}

### 1.2 현재 상황
- 시장/분야 동향: {trends.trends[0]}
- 주요 이슈: {trends.trends[1] if len(trends.trends) > 1 else '관련 이슈'}
- 최신 데이터: {trends.trends[2] if len(trends.trends) > 2 else '통계 및 데이터'}

## 🔍 2. 트렌드 인사이트

### 2.1 주요 트렌드
{chr(10).join(f"**트렌드 {i+1}:** {t}" for i, t in enumerate(trends.trends[:5]))}

### 2.2 트렌드 분석
- 각 트렌드의 의미와 영향
- 상호 연관성 분석
- 향후 전망

## 💡 3. 실전 활용 방안

### 3.1 즉시 적용 가능한 전략
[구체적 액션 아이템 3-5가지]

### 3.2 중장기 전략
[지속 가능한 접근법]

### 3.3 주의사항 및 위험 요소
[고려해야 할 사항들]

## 📊 4. 결론 및 제언

### 4.1 핵심 요약
- 주요 발견사항 (3-5개 포인트)
- 가장 중요한 인사이트

### 4.2 최종 제언
- {intent.target_audience}를 위한 구체적 조언
- 다음 단계 액션 플랜

---

**작성 시 유의사항:**
- 각 섹션을 체계적으로 작성
- 데이터와 근거를 명확히 제시
- 실용적이고 실행 가능한 내용 포함
- {intent.output_type.value} 형식에 맞게 구조화
"""

        return PromptStrategy(
            type=PromptStrategyType.STRUCTURED,
            name="구조화 분석 (Structured)",
            description="체계적인 보고서 형식의 심층 분석",
            icon="📊",
            best_for="데이터 분석, 리서치 보고서, 체계적 정리",
            prompt=prompt_content,
        )

    def _get_examples_for_intent(self, intent: IntentAnalysisResult) -> str:
        """의도에 따른 예시 생성"""

        if intent.output_type.value == "블로그":
            return """
**[예시 1: 여행 블로그]**
"첫눈이 내리는 날, 손을 꼭 잡고 걷고 싶은 곳. 북촌 한옥마을 골목길에는 따스한 불빛이 켜지고,
겨울 바람에 실려오는 따끈한 붕어빵 냄새가 발걸음을 멈추게 한다..."

**[예시 2: 맛집 블로그]**
"을지로 골목 깊숙한 곳, 70년 전통의 작은 식당. 낡은 간판 뒤로 숨은 진짜 맛을 찾아가는 설렘.
첫 입에 느껴지는 깊은 육수의 풍미는..."
"""
        elif intent.output_type.value == "리포트":
            return """
**[예시: 시장 분석 리포트]**
"2025년 1분기 시장 분석 결과, 3가지 주요 트렌드가 관찰되었다.
첫째, AI 기술 도입률이 전년 대비 47% 증가했으며..."
"""
        else:
            return """
**[예시: 가이드]**
"초보자를 위한 3단계 가이드를 소개합니다.
1단계: 기본 개념 이해하기 - 가장 먼저 알아야 할 핵심은..."
"""
