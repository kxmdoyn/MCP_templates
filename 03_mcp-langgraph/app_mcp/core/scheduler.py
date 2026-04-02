"""
app_mcp/core/scheduler.py

APScheduler Job 등록
- realtime_job: interval 기반 주기 실행 (모니터링, 알림 등)
- periodic_job: cron 기반 정기 실행 (보고서 생성, 배치 등)

TODO: 각 Job 함수에 실제 로직 구현
"""

from __future__ import annotations

import logging
import os
from datetime import datetime

import requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────
# Job 1: 실시간 모니터링 (interval)
# TODO: 실행 주기와 로직 수정
# ─────────────────────────────────────────────

def realtime_job() -> None:
    """
    주기적으로 실행되는 실시간 모니터링 Job.

    TODO: 아래 로직을 실제 모니터링 로직으로 교체
    예시:
        - 외부 API 데이터 수집
        - 임계값 초과 시 Slack 알림 발송
        - DB에 스냅샷 저장
    """
    logger.info("[scheduler] ▶ realtime_job 실행")

    try:
        # TODO: 실제 모니터링 로직 구현
        # from app_mcp.services.monitor import check_and_alert
        # check_and_alert()
        logger.info("[scheduler] ✅ realtime_job 완료")
    except Exception as e:
        logger.exception("[scheduler] ❌ realtime_job 실패: %s", e)


# ─────────────────────────────────────────────
# Job 2: 정기 배치 작업 (cron)
# TODO: cron 주기와 로직 수정
# ─────────────────────────────────────────────

def periodic_job() -> None:
    """
    정기적으로 실행되는 배치 Job (기본: 매월 1일 00:05).

    TODO: 아래 로직을 실제 배치 로직으로 교체
    전략: LangGraph 워크플로우를 직접 호출하지 않고
          FastAPI 엔드포인트를 HTTP 호출하여 재사용성 확보
    """
    base_url = os.getenv("SCHEDULER_BASE_URL", "http://127.0.0.1:8000").rstrip("/")

    # TODO: 실제 엔드포인트와 payload로 수정
    url = f"{base_url}/mcp/run"
    payload = {
        "period": datetime.now().strftime("%Y-%m"),
        # "your_param": "your_value",
    }

    logger.info("[scheduler] ▶ periodic_job 실행: url=%s", url)

    try:
        resp = requests.post(url, json=payload, timeout=30)
        if resp.status_code // 100 == 2:
            logger.info("[scheduler] ✅ periodic_job 완료: %s", resp.text)
        else:
            logger.error("[scheduler] ❌ periodic_job HTTP 에러: %s %s", resp.status_code, resp.text)
    except Exception as e:
        logger.exception("[scheduler] ❌ periodic_job 실패: %s", e)


# ─────────────────────────────────────────────
# 스케줄러 등록 (mcp_server.py on_startup에서 호출)
# TODO: 주기(minutes/cron) 조정
# ─────────────────────────────────────────────

def register_scheduler(scheduler: AsyncIOScheduler) -> None:
    logger.info("[scheduler] Job 등록 시작")

    # Job 1: interval — 15분마다
    # TODO: minutes 값 조정
    scheduler.add_job(
        realtime_job,
        "interval",
        minutes=15,
        id="realtime_job",
        replace_existing=True,
        coalesce=True,
        max_instances=1,
    )
    logger.info("[scheduler] ✔ realtime_job 등록 (15분 간격)")

    # Job 2: cron — 매월 1일 00:05
    # TODO: cron 표현식 조정 (day/hour/minute)
    scheduler.add_job(
        periodic_job,
        "cron",
        day=1,
        hour=0,
        minute=5,
        id="periodic_job",
        replace_existing=True,
        coalesce=True,
        max_instances=1,
    )
    logger.info("[scheduler] ✔ periodic_job 등록 (매월 1일 00:05)")
