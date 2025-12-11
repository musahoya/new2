"""
사용자 확인 모듈
트렌드 수집 후 사용자에게 확인 메시지를 생성합니다.
"""
from ..models.schemas import IntentAnalysisResult, TrendResult


class ConfirmationModule:
    """사용자 확인 모듈"""

    @staticmethod
    def generate_confirmation_message(
        query: str, intent: IntentAnalysisResult, trends: TrendResult
    ) -> str:
        """
        사용자 확인 메시지를 생성합니다.

        Args:
            query: 사용자 쿼리
            intent: 의도 분석 결과
            trends: 트렌드 결과

        Returns:
            확인 메시지
        """

        message = f"""
📌 **이런 내용을 찾았어요!**

━━━━━━━━━━━━━━━━━━━━━━━━━━

**🎯 주제 분석:**
- 입력하신 내용: "{query}"
- 파악된 목적: {intent.primary_intent.value}
- 예상 형식: {intent.output_type.value}
- 대상 독자: {intent.target_audience}

━━━━━━━━━━━━━━━━━━━━━━━━━━

**🔥 최신 트렌드 TOP 10:**

{chr(10).join(f"{i+1}. {trend}" for i, trend in enumerate(trends.trends))}

━━━━━━━━━━━━━━━━━━━━━━━━━━

**💬 요약:**
{trends.summary}

━━━━━━━━━━━━━━━━━━━━━━━━━━

**✅ 이 방향이 맞나요?**

- 맞다면 → 5가지 프롬프팅 전략을 생성해드립니다
- 수정이 필요하다면 → 어떤 부분을 조정할지 알려주세요
"""

        return message

    @staticmethod
    def generate_strategy_selection_message(prompts_count: int = 5) -> str:
        """
        프롬프트 전략 선택 메시지를 생성합니다.

        Args:
            prompts_count: 생성된 프롬프트 개수

        Returns:
            선택 메시지
        """

        message = f"""
✨ **{prompts_count}가지 프롬프팅 전략을 생성했어요!**

각 전략을 확인하고 원하는 것을 선택해주세요.

━━━━━━━━━━━━━━━━━━━━━━━━━━

**1️⃣ 사고 연쇄 (CoT)**
🧠 논리적 단계별 사고
💡 최적: 복잡한 계획/분석에 최적

**2️⃣ 예시 학습 (Few-Shot)**
📝 스타일 모방 & 형식 통일
💡 최적: 블로그/에세이 작성

**3️⃣ 전문가 모드 (Meta-Prompting)**
👨‍🏫 전문가 페르소나 부여
💡 최적: 객관적 리뷰/분석

**4️⃣ 자체 개선 (Self-Refine)**
🔄 초안 → 수정 → 완성
💡 최적: 고퀄리티 콘텐츠

**5️⃣ 구조화 분석 (Structured)**
📊 체계적 보고서 형식
💡 최적: 데이터 분석/리서치

━━━━━━━━━━━━━━━━━━━━━━━━━━

어떤 전략을 사용하시겠어요?
"""

        return message
