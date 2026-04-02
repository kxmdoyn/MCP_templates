"""
app_mcp/tools/your_tools.py

도메인 Tool 구현 파일

이 파일을 복사해서 도메인별 Tool을 구현하고
gateway.py의 TOOL_MAP에 등록하세요.

TODO: 파일명과 함수명을 도메인에 맞게 변경
"""

from __future__ import annotations

import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────
# Tool 구현 예시
# TODO: 실제 도메인 로직으로 교체
# ─────────────────────────────────────────────

async def get_data(source_id: str | None = None) -> Dict[str, Any]:
    """
    데이터 조회 Tool

    Args:
        source_id: 조회할 데이터 식별자

    Returns:
        조회 결과 dict

    TODO: 실제 데이터 소스(API, DB 등)에서 데이터 조회로 교체
    """
    logger.info("[tool] get_data 호출: source_id=%s", source_id)

    # TODO: 실제 데이터 조회
    # result = await fetch_from_api(source_id)
    # 또는
    # result = await db.query(...)

    return {
        "source_id": source_id,
        "data": {},                 # TODO: 실제 데이터로 교체
        "status": "TODO: 구현 필요",
    }


async def analyze_data(data: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """
    데이터 분석 Tool

    Args:
        data: 분석할 데이터

    Returns:
        분석 결과 dict

    TODO: 실제 분석 로직으로 교체
    """
    logger.info("[tool] analyze_data 호출")

    # TODO: 실제 분석 로직
    # result = your_analysis_logic(data)

    return {
        "result": {},               # TODO: 실제 분석 결과로 교체
        "status": "TODO: 구현 필요",
    }


async def generate_report(period: str | None = None) -> Dict[str, Any]:
    """
    보고서 생성 Tool

    Args:
        period: 보고서 기간 (예: "2025-10")

    Returns:
        생성된 보고서 정보

    TODO: 실제 보고서 생성 로직으로 교체
    """
    logger.info("[tool] generate_report 호출: period=%s", period)

    # TODO: 실제 보고서 생성
    # report_path = create_docx_report(period)

    return {
        "period": period,
        "report_path": "",          # TODO: 실제 경로로 교체
        "status": "TODO: 구현 필요",
    }
