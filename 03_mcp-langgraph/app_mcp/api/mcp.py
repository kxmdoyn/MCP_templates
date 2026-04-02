"""
app_mcp/api/mcp.py

/mcp/run — LangGraph 워크플로우 실행 엔드포인트
/mcp/status — 실행 상태 조회

TODO: 엔드포인트 및 페이로드 스키마 수정
"""

import logging
from fastapi import APIRouter
from pydantic import BaseModel

from app_mcp.graph.flow import graph

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/mcp", tags=["mcp"])


# ─────────────────────────────────────────────
# 요청/응답 스키마
# TODO: 도메인에 맞게 수정
# ─────────────────────────────────────────────

class RunRequest(BaseModel):
    period: str                     # 처리 기간 또는 식별자
    # TODO: 추가 파라미터
    # your_param: str = ""


class RunResponse(BaseModel):
    success: bool
    period: str
    output_path: str | None = None
    summary: dict | None = None
    message: str = ""


# ─────────────────────────────────────────────
# 엔드포인트
# ─────────────────────────────────────────────

@router.post("/run", response_model=RunResponse)
async def run_flow(req: RunRequest):
    """
    LangGraph 워크플로우 실행

    TODO: initial_state에 도메인 파라미터 추가
    """
    logger.info("[mcp] /mcp/run 요청: period=%s", req.period)

    try:
        initial_state = {
            "period": req.period,
            "revision_count": 0,
            "max_revisions": 3,
            "human_decision": "pending",
            # TODO: 추가 초기 상태
        }

        config = {"configurable": {"thread_id": f"run-{req.period}"}}
        result = await graph.ainvoke(initial_state, config=config)

        return RunResponse(
            success=True,
            period=req.period,
            output_path=result.get("output_path"),
            summary=result.get("summary"),
            message="워크플로우 완료",
        )

    except Exception as e:
        logger.exception("[mcp] 워크플로우 실행 실패: %s", e)
        return RunResponse(
            success=False,
            period=req.period,
            message=str(e),
        )


@router.get("/status/{period}")
async def get_status(period: str):
    """
    TODO: DB에서 실행 상태 조회 로직 구현
    """
    return {"period": period, "status": "TODO: 구현 필요"}
