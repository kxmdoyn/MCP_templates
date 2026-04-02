"""
app_mcp/core/config.py

환경변수 설정 관리
TODO: 필요한 설정 항목 추가
"""

from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ─────────────────────────────────────────────
    # 기본 설정 (수정 불필요)
    # ─────────────────────────────────────────────
    project_name: str = "MCP Server"
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    # ─────────────────────────────────────────────
    # DB 설정
    # TODO: 사용하는 DB에 맞게 수정
    # ─────────────────────────────────────────────
    database_url: str = "sqlite+aiosqlite:///./mcp_template.db"

    # ─────────────────────────────────────────────
    # Slack 설정 (Human-in-the-loop 사용 시)
    # ─────────────────────────────────────────────
    slack_webhook_url: str = ""
    slack_signing_secret: str = ""
    slack_bot_token: str = ""

    # ─────────────────────────────────────────────
    # 스케줄러 설정
    # ─────────────────────────────────────────────
    scheduler_base_url: str = "http://127.0.0.1:8000"

    # ─────────────────────────────────────────────
    # TODO: 도메인별 추가 설정
    # 예시:
    # your_api_key: str = ""
    # your_api_base_url: str = ""
    # ─────────────────────────────────────────────

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
