"""
app_mcp/services/notifications.py

Slack 알림 서비스
- 실시간 경보 발송
- Human Review 승인 요청 카드 발송

TODO: Slack 카드 메시지 내용을 도메인에 맞게 수정
"""

from __future__ import annotations

import logging
import os
from typing import Any, Dict

import requests

logger = logging.getLogger(__name__)

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN", "")
PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL", "http://localhost:8000")


def send_alert(message: str, level: str = "warning") -> bool:
    """
    실시간 경보 Slack 발송

    Args:
        message: 알림 메시지
        level: "info" | "warning" | "critical"

    TODO: 메시지 포맷 도메인에 맞게 수정
    """
    if not SLACK_WEBHOOK_URL:
        logger.warning("[notifications] SLACK_WEBHOOK_URL 미설정")
        return False

    # 레벨별 이모지
    emoji = {"info": "ℹ️", "warning": "⚠️", "critical": "🚨"}.get(level, "📢")

    payload = {
        "text": f"{emoji} *{level.upper()}* {message}"
    }

    try:
        resp = requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=10)
        resp.raise_for_status()
        logger.info("[notifications] 경보 발송 완료: level=%s", level)
        return True
    except Exception as e:
        logger.error("[notifications] 경보 발송 실패: %s", e)
        return False


def send_slack_human_review_request(
    period: str,
    task_id: int,
    summary: Dict[str, Any],
    output_path: str = "",
) -> bool:
    """
    Human Review 승인 요청 Slack 카드 발송

    Args:
        period: 처리 기간
        task_id: HumanReviewTask ID
        summary: 요약 정보
        output_path: 생성된 파일 경로

    TODO: 카드 내용(blocks)을 도메인에 맞게 수정
    """
    if not SLACK_WEBHOOK_URL:
        logger.warning("[notifications] SLACK_WEBHOOK_URL 미설정")
        return False

    approve_url = f"{PUBLIC_BASE_URL}/human-review/decision"

    # TODO: Slack Block Kit으로 카드 커스터마이징
    payload = {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"📋 Human Review 요청 — {period}",
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    # TODO: summary 내용 도메인에 맞게 수정
                    "text": f"*Task ID*: {task_id}\n*Period*: {period}\n*Output*: {output_path or '생성 중'}"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "✅ 승인"},
                        "style": "primary",
                        "url": f"{approve_url}?task_id={task_id}&decision=approve",
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "🔄 반려/재생성"},
                        "style": "danger",
                        "url": f"{approve_url}?task_id={task_id}&decision=revise",
                    },
                ]
            }
        ]
    }

    try:
        resp = requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=10)
        resp.raise_for_status()
        logger.info("[notifications] Human Review 카드 발송 완료: task_id=%s", task_id)
        return True
    except Exception as e:
        logger.error("[notifications] Human Review 카드 발송 실패: %s", e)
        return False
