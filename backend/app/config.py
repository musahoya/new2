"""
애플리케이션 설정 관리
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """환경 변수 설정"""

    # API Keys
    google_gemini_api_key: str
    brave_search_api_key: Optional[str] = None

    # 서버 설정
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True

    # Gemini 설정
    gemini_model: str = "gemini-2.0-flash-exp"
    gemini_api_url: str = "https://generativelanguage.googleapis.com/v1beta/models"
    max_tokens: int = 4096

    # 웹 검색 설정
    search_results_limit: int = 10
    search_engine: str = "auto"  # "auto", "brave", "duckduckgo"

    class Config:
        env_file = ".env"
        case_sensitive = False


# 전역 설정 인스턴스
settings = Settings()
