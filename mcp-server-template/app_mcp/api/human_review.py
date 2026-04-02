"""
app_mcp/api/human_review.py

Slack 승인/반려 웹훅 수신 엔드포인트

흐름:
    담당자가 Slack 카드에서 버튼 클릭
    → POST /human-review/decision
    → DB 상태 업데이트
    → LangGraph 워크플로우 재개
"""

import logging
from fastapi import APIRouter
from pydantic import BaseModel

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/human-review", tags=["human_review"])


class DecisionRequest(BaseModel):
    task_id: int
    decision: str               # "approve" | "revise"
    feedback: str | None = None


@router.post("/decision")
async def receive_decision(req: DecisionRequest):
    """
    Slack 버튼 클릭 → 워크플로우 재개

    TODO: 실제 DB 업데이트 및 워크플로우 재개 로직 구현
    """
    logger.info(
        "[human_review] decision 수신: task_id=%s, decision=%s",
        req.task_id, req.decision,
    )

    try:
        # TODO: DB에서 task 조회 및 상태 업데이트
        # async with get_db() as db:
        #     task = await crud_hr.get_task(db, req.task_id)
        #     await crud_hr.update_decision(db, req.task_id, req.decision, req.feedback)

        # TODO: LangGraph 워크플로우 재개
        # from app_mcp.graph.flow import graph
        # config = {"configurable": {"thread_id": task.flow_run_id}}
        # await graph.aupdate_state(config, {"human_decision": req.decision})

        return {
            "success": True,
            "task_id": req.task_id,
            "decision": req.decision,
            "message": "TODO: 실제 구현 필요",
        }

    except Exception as e:
        logger.exception("[human_review] 처리 실패: %s", e)
        return {"success": False, "error": str(e)}


@router.get("/tasks")
async def list_pending_tasks():
    """
    TODO: DB에서 pending 상태 task 목록 조회
    """
    return {"tasks": [], "message": "TODO: 구현 필요"}
