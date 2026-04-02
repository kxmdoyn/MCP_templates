"""
app_mcp/graph/flow_interrupt.py

LangGraph Human-in-the-loop 인터럽트 핸들러

흐름:
    generate_output 완료
    → DB에 HumanReviewTask 생성
    → Slack에 승인 요청 카드 발송
    → 담당자 클릭 (승인/반려)
    → /slack/interactions 웹훅 수신
    → 워크플로우 재개
"""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any, Dict

from app_mcp.core.db import get_db
from app_mcp.services.notifications import send_slack_human_review_request

logger = logging.getLogger(__name__)


async def _handle_human_review_async(
    state: Dict[str, Any],
    thread_id: str | None,
) -> None:
    """
    DB에 HumanReviewTask 생성 후 Slack 승인 요청 발송

    TODO: 필요에 따라 summary 가공 방식 수정
    """
    period = state.get("period", "unknown")
    summary = state.get("summary") or {}
    output_path = state.get("output_path") or ""

    # TODO: Slack 카드에 표시할 요약 정보 구성
    summary_for_slack: Dict[str, Any] = {
        "status": summary.get("status", "N/A"),
        "period": period,
        # "your_summary_field": summary.get("your_field", "N/A"),
    }

    # DB에 HumanReviewTask 생성
    async with get_db() as db:
        from app_mcp.crud.human_review import create_task
        task = await create_task(
            db,
            period=period,
            output_path=output_path,
            summary_json=json.dumps(summary, ensure_ascii=False),
            flow_run_id=thread_id,
        )

    # Slack 승인 요청 발송
    slack_res = send_slack_human_review_request(
        period=period,
        task_id=task.id,
        summary=summary_for_slack,
        output_path=output_path,
    )

    logger.info(
        "[HumanReviewInterrupt] task_id=%s, period=%s, slack=%s",
        task.id, period, slack_res,
    )


def on_human_review_interrupt(interrupt_event: Any) -> None:
    """
    LangGraph on_interrupt 훅 — generate_output 완료 후 자동 호출
    수정 불필요 (로직은 _handle_human_review_async에서)
    """
    try:
        checkpoint = getattr(interrupt_event, "checkpoint", None) or {}
        state = (checkpoint.get("state") or {}).get("values") or {}
        config = checkpoint.get("config") or {}
        thread_id = config.get("configurable", {}).get("thread_id")

        asyncio.create_task(
            _handle_human_review_async(state, thread_id)
        )

        logger.info(
            "[HumanReviewInterrupt] triggered: period=%s, thread_id=%s",
            state.get("period"), thread_id,
        )

    except Exception as e:
        logger.error("[HumanReviewInterrupt] 실패: %s", e, exc_info=True)
