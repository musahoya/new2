"""
트렌드 수집 엔진
웹 검색을 통해 최신 트렌드 정보를 수집합니다.
"""
from anthropic import Anthropic
import httpx
from typing import List, Dict
from ..config import settings
from ..models.schemas import TrendResult, IntentAnalysisResult
import json


class TrendCollector:
    """트렌드 수집기"""

    def __init__(self):
        self.client = Anthropic(api_key=settings.anthropic_api_key)

    async def search_web(self, query: str, num_results: int = 3) -> List[Dict]:
        """
        웹 검색을 수행합니다.

        Note: 실제 웹 검색 API가 필요합니다.
        여기서는 시뮬레이션 데이터를 반환합니다.
        실제 배포 시 Brave Search API 또는 Google Custom Search API를 사용하세요.

        Args:
            query: 검색 쿼리
            num_results: 결과 개수

        Returns:
            검색 결과 리스트
        """
        # TODO: 실제 웹 검색 API 연동
        # 현재는 시뮬레이션 데이터 반환

        # Brave Search API 사용 예시 (주석 처리)
        # if settings.brave_search_api_key:
        #     async with httpx.AsyncClient() as client:
        #         response = await client.get(
        #             "https://api.search.brave.com/res/v1/web/search",
        #             headers={"X-Subscription-Token": settings.brave_search_api_key},
        #             params={"q": query, "count": num_results}
        #         )
        #         data = response.json()
        #         return [{"title": r["title"], "snippet": r["description"], "url": r["url"]}
        #                 for r in data.get("web", {}).get("results", [])]

        # 시뮬레이션 데이터
        return [
            {
                "title": f"{query}에 대한 최신 트렌드 {i+1}",
                "snippet": f"{query} 관련 최신 정보입니다. 2025년 트렌드를 반영한 내용입니다.",
                "url": f"https://example.com/{i}",
            }
            for i in range(num_results)
        ]

    async def collect(
        self, keywords: List[str], intent: IntentAnalysisResult
    ) -> TrendResult:
        """
        키워드를 기반으로 트렌드를 수집하고 정리합니다.

        Args:
            keywords: 검색할 키워드 리스트
            intent: 의도 분석 결과

        Returns:
            TrendResult: 수집된 트렌드 결과
        """

        all_results = []
        sources = []

        # 각 키워드로 검색
        for keyword in keywords[:3]:  # 상위 3개 키워드만 사용
            search_query = f"{keyword} 최신 트렌드 2025"
            results = await self.search_web(search_query, num_results=3)
            all_results.extend(results)
            sources.extend([r["url"] for r in results])

        # Claude를 사용하여 검색 결과 정리
        search_results_text = "\n\n".join(
            [
                f"제목: {r['title']}\n내용: {r['snippet']}"
                for r in all_results[:10]  # 최대 10개
            ]
        )

        prompt = f"""
다음은 "{intent.primary_intent}" 목적의 "{intent.domain}" 분야에 대한 웹 검색 결과입니다.

검색 결과:
{search_results_text}

이 검색 결과를 바탕으로 다음을 JSON 형식으로 정리해주세요:
{{
    "trends": ["트렌드1", "트렌드2", ..., "트렌드10"],  // 핵심 트렌드 10가지 (간결하게)
    "summary": "전체 트렌드 요약 (2-3문장)"
}}

트렌드는 구체적이고 실용적인 정보여야 합니다.
예시: "서울 겨울 데이트" 주제라면:
- "성수동 팝업스토어 트렌드"
- "한강 야경 카페 인기"
- "실내 액티비티 증가"
등과 같이 구체적으로 작성하세요.

JSON만 반환하고 다른 설명은 하지 마세요.
"""

        try:
            message = self.client.messages.create(
                model=settings.claude_model,
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}],
            )

            response_text = message.content[0].text.strip()
            result_dict = json.loads(response_text)

            return TrendResult(
                trends=result_dict["trends"][:10],  # 최대 10개
                summary=result_dict["summary"],
                sources=list(set(sources))[:10],  # 중복 제거 후 최대 10개
            )

        except Exception as e:
            print(f"Trend collection error: {e}")
            # 에러 발생 시 기본값 반환
            return TrendResult(
                trends=[f"{k} 관련 최신 트렌드" for k in keywords[:10]],
                summary=f"{intent.domain} 분야의 최신 트렌드입니다.",
                sources=sources[:10],
            )
