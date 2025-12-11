"""
트렌드 수집 엔진
웹 검색을 통해 최신 트렌드 정보를 수집합니다.
Brave Search API 또는 DuckDuckGo 자동 선택
"""
import httpx
from typing import List, Dict
from bs4 import BeautifulSoup
from ..config import settings
from ..models.schemas import TrendResult, IntentAnalysisResult
import json
import urllib.parse


class TrendCollector:
    """트렌드 수집기"""

    def __init__(self):
        self.api_key = settings.google_gemini_api_key
        self.model = settings.gemini_model
        self.api_url = settings.gemini_api_url
        self.brave_api_key = settings.brave_search_api_key
        self.search_engine = settings.search_engine

    async def search_web(self, query: str, num_results: int = 3) -> List[Dict]:
        """
        웹 검색을 수행합니다.
        자동으로 Brave API 또는 DuckDuckGo 선택

        Args:
            query: 검색 쿼리
            num_results: 결과 개수

        Returns:
            검색 결과 리스트
        """
        # 검색 엔진 자동 선택
        if self.search_engine == "auto":
            if self.brave_api_key:
                return await self._search_brave(query, num_results)
            else:
                return await self._search_duckduckgo(query, num_results)
        elif self.search_engine == "brave":
            return await self._search_brave(query, num_results)
        elif self.search_engine == "duckduckgo":
            return await self._search_duckduckgo(query, num_results)
        else:
            # 기본값: DuckDuckGo
            return await self._search_duckduckgo(query, num_results)

    async def _search_brave(self, query: str, num_results: int) -> List[Dict]:
        """Brave Search API 사용"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://api.search.brave.com/res/v1/web/search",
                    headers={"X-Subscription-Token": self.brave_api_key},
                    params={"q": query, "count": num_results},
                    timeout=10.0
                )
                response.raise_for_status()
                data = response.json()

                results = []
                for r in data.get("web", {}).get("results", []):
                    results.append({
                        "title": r.get("title", ""),
                        "snippet": r.get("description", ""),
                        "url": r.get("url", "")
                    })

                return results[:num_results]

        except Exception as e:
            print(f"Brave Search error: {e}, falling back to DuckDuckGo")
            return await self._search_duckduckgo(query, num_results)

    async def _search_duckduckgo(self, query: str, num_results: int) -> List[Dict]:
        """DuckDuckGo HTML 스크래핑 (무료)"""
        try:
            async with httpx.AsyncClient() as client:
                # DuckDuckGo HTML 검색
                encoded_query = urllib.parse.quote(query)
                url = f"https://html.duckduckgo.com/html/?q={encoded_query}"

                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                }

                response = await client.get(url, headers=headers, timeout=10.0)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, 'html.parser')
                results = []

                # DuckDuckGo 결과 파싱
                for result_div in soup.select('.result'):
                    try:
                        title_elem = result_div.select_one('.result__title')
                        snippet_elem = result_div.select_one('.result__snippet')
                        url_elem = result_div.select_one('.result__url')

                        if title_elem and snippet_elem:
                            title = title_elem.get_text(strip=True)
                            snippet = snippet_elem.get_text(strip=True)
                            url = url_elem.get('href', '') if url_elem else ''

                            results.append({
                                "title": title,
                                "snippet": snippet,
                                "url": url
                            })

                            if len(results) >= num_results:
                                break
                    except:
                        continue

                # 결과가 없으면 시뮬레이션 데이터 반환
                if not results:
                    results = self._get_simulation_data(query, num_results)

                return results[:num_results]

        except Exception as e:
            print(f"DuckDuckGo search error: {e}, using simulation data")
            return self._get_simulation_data(query, num_results)

    def _get_simulation_data(self, query: str, num_results: int) -> List[Dict]:
        """시뮬레이션 데이터 (fallback)"""
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
            sources.extend([r["url"] for r in results if r["url"]])

        # Gemini를 사용하여 검색 결과 정리
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
            async with httpx.AsyncClient() as client:
                url = f"{self.api_url}/{self.model}:generateContent?key={self.api_key}"

                payload = {
                    "contents": [{
                        "parts": [{
                            "text": prompt
                        }]
                    }],
                    "generationConfig": {
                        "temperature": 0.7,
                        "maxOutputTokens": 2048,
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

                result_dict = json.loads(text)

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
