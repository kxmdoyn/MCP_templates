"""
FastAPI MCP Backend

- APScheduler로 자동 Job 실행
- LangGraph 워크플로우 연동
- Slack Human Review 웹훅 수신

Usage:
    python mcp_server.py
    또는
    uvicorn mcp_server:app --reload

Port: 8000 (기본값)
"""

import logging
import os

import uvicorn
from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app_mcp.core.config import get_settings
from app_mcp.core.db import init_db
from app_mcp.core.scheduler import register_scheduler

# ─────────────────────────────────────────────
# TODO: 필요한 라우터 import 후 아래 include_router에 등록
# ─────────────────────────────────────────────
from app_mcp.api.mcp import router as mcp_router
from app_mcp.api.human_review import router as human_review_router

# TODO: 추가 라우터 예시
# from app_mcp.api.your_routes import router as your_router

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARTIFACT_DIR = os.path.join(BASE_DIR, "artifacts")
os.makedirs(ARTIFACT_DIR, exist_ok=True)

scheduler = AsyncIOScheduler()


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.project_name,
        version="0.1.0",
        description="MCP Server Template — FastAPI Backend",
    )

    # ─────────────────────────────────────────────
    # 라우터 등록
    # TODO: 추가 라우터는 여기에 include
    # ─────────────────────────────────────────────
    app.include_router(mcp_router)
    app.include_router(human_review_router)
    # app.include_router(your_router)

    @app.on_event("startup")
    async def on_startup():
        await init_db()
        logger.info("✅ DB initialized")

        register_scheduler(scheduler)
        scheduler.start()
        logger.info("✅ APScheduler started")

    @app.on_event("shutdown")
    async def on_shutdown():
        if scheduler.running:
            scheduler.shutdown(wait=False)
            logger.info("APScheduler stopped")

    @app.get("/health")
    async def health_check():
        return {"status": "ok", "project": settings.project_name}

    return app


app = create_app()


if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "mcp_server:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=True,
    )
