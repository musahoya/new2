"""
의도 파악 엔진
사용자의 쿼리를 분석하여 의도, 키워드, 대상 독자 등을 파악합니다.
"""
import httpx
from ..config import settings
from ..models.schemas import IntentAnalysisResult, IntentCategory, OutputType
import json


class IntentAnalyzer:
    """사용자 의도 분석기"""

    def __init__(self):
        self.api_key = settings.google_gemini_api_key
        self.model = settings.gemini_model
        self.api_url = settings.gemini_api_url

    async def analyze(self, user_query: str) -> IntentAnalysisResult:
        """
        사용자 쿼리를 분석하여 의도를 파악합니다.

        Args:
            user_query: 사용자 입력 쿼리

        Returns:
            IntentAnalysisResult: 분석된 의도 결과
        """

        prompt = f"""
다음 사용자 쿼리를 분석하여 의도를 파악해주세요.

사용자 쿼리: "{user_query}"

다음 항목들을 JSON 형식으로 반환해주세요:
{{
    "primary_intent": "정보 검색" | "콘텐츠 생성" | "문제 해결" | "학습/교육" | "창작",
    "keywords": ["키워드1", "키워드2", "키워드3"],  // 3-5개의 핵심 키워드
    "target_audience": "대상 독자 설명",  // 예: "20-30대 커플", "투자자", "개발자" 등
    "output_type": "블로그" | "리포트" | "에세이" | "분석" | "가이드" | "튜토리얼",
    "domain": "주제 분야",  // 예: "여행", "투자", "기술", "교육" 등
    "confidence": 0.0-1.0  // 분석 신뢰도
}}

분석 시 고려사항:
1. 사용자가 무엇을 원하는지 (목적)
2. 어떤 형태의 결과물이 필요한지 (형식)
3. 누구를 위한 것인지 (대상)
4. 어느 분야/주제인지 (영역)

JSON만 반환하고 다른 설명은 하지 마세요.
"""

        try:
            async with httpx.AsyncClient() as client:
                url = f"{self.api_url}/{self.model}:generateContent?key={self.api_key}"

                payload = {
                    "contents": [{
                        "parts": [{
                            "text": prompt
                        }]
                    }],
                    "generationConfig": {
                        "temperature": 0.3,
                        "maxOutputTokens": 1024,
                    }
                }

                response = await client.post(url, json=payload, timeout=30.0)
                response.raise_for_status()

                result = response.json()

                # Gemini 응답에서 텍스트 추출
                text = result['candidates'][0]['content']['parts'][0]['text']

                # JSON 추출 (마크다운 코드 블록 제거)
                text = text.strip()
                if text.startswith('```json'):
                    text = text[7:]
                if text.startswith('```'):
                    text = text[3:]
                if text.endswith('```'):
                    text = text[:-3]
                text = text.strip()

                # JSON 파싱
                result_dict = json.loads(text)

            # IntentAnalysisResult 객체로 변환
            return IntentAnalysisResult(
                primary_intent=IntentCategory(result_dict["primary_intent"]),
                keywords=result_dict["keywords"],
                target_audience=result_dict["target_audience"],
                output_type=OutputType(result_dict["output_type"]),
                domain=result_dict["domain"],
                confidence=result_dict["confidence"],
            )

        except Exception as e:
            # 에러 발생 시 기본값 반환
            print(f"Intent analysis error: {e}")
            return IntentAnalysisResult(
                primary_intent=IntentCategory.INFO_SEARCH,
                keywords=[user_query],
                target_audience="일반 사용자",
                output_type=OutputType.GUIDE,
                domain="일반",
                confidence=0.5,
            )
