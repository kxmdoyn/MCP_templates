"""
app_mcp/graph/flow.py

LangGraph 기반 multi-step reasoning pipeline

구조:
    load_data → validate → [your steps] → summarize → generate_output → human_review → finalize

TODO: 도메인에 맞게 노드 추가/제거
"""

from __future__ import annotations

import logging
from typing import Any, Dict, TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────
# 1) State 정의
# TODO: 도메인에 맞는 상태 필드 추가
# ─────────────────────────────────────────────

class FlowState(TypedDict, total=False):
    # 입력
    period: str                         # 처리 기간 또는 식별자

    # 데이터 로드 결과
    raw_data: Dict[str, Any]

    # TODO: 도메인별 중간 처리 결과 필드 추가
    # step1_result: Dict[str, Any]
    # step2_result: Dict[str, Any]

    # 요약 및 출력
    summary: Dict[str, Any]
    output_path: str                    # 생성된 파일 경로 등

    # Human Review 제어
    task_id: int
    human_decision: str | None          # "pending" | "approve" | "revise"
    human_feedback: str | None
    revision_count: int
    max_revisions: int

    # 재시도 제어
    retry_counts: Dict[str, int]
    max_retries: Dict[str, int]


# ─────────────────────────────────────────────
# 2) 노드 구현
# TODO: 각 노드에 실제 도메인 로직 구현
# ─────────────────────────────────────────────

def load_data(state: FlowState) -> FlowState:
    """
    Step 1: 데이터 로드
    TODO: DB/API에서 실제 데이터 로드로 교체
    """
    logger.info("[flow] load_data 실행")

    if state.get("raw_data"):
        return state  # 이미 데이터가 있으면 스킵

    # TODO: 실제 데이터 로드 로직
    # from app_mcp.services.data_service import load_raw_data
    # raw_data = load_raw_data(state.get("period"))
    raw_data = {"sample": "data"}  # 교체 필요

    return {**state, "raw_data": raw_data}


def validate_data(state: FlowState) -> FlowState:
    """
    Step 2: 데이터 품질 검증
    TODO: 실제 검증 로직 구현
    """
    logger.info("[flow] validate_data 실행")

    raw_data = state.get("raw_data", {})

    # TODO: 실제 검증 로직
    # if not raw_data:
    #     raise ValueError("데이터가 없습니다")

    return state


# TODO: 도메인 처리 노드 추가
# def your_domain_step(state: FlowState) -> FlowState:
#     """
#     Step N: 도메인별 처리
#     TODO: 실제 처리 로직 구현
#     """
#     logger.info("[flow] your_domain_step 실행")
#     result = your_logic(state["raw_data"])
#     return {**state, "step_result": result}


def summarize(state: FlowState) -> FlowState:
    """
    Step N: 결과 요약
    TODO: 실제 요약 로직 구현
    """
    logger.info("[flow] summarize 실행")

    # TODO: 실제 요약 로직
    summary = {
        "status": "completed",
        "period": state.get("period"),
        # "your_summary_field": ...,
    }

    return {**state, "summary": summary}


def generate_output(state: FlowState) -> FlowState:
    """
    Step N+1: 최종 출력물 생성 (DOCX, JSON, 이메일 등)
    TODO: 실제 출력물 생성 로직 구현
    """
    logger.info("[flow] generate_output 실행")

    # TODO: 실제 출력 생성 로직
    # from app_mcp.reports.generator import generate_report
    # output_path = generate_report(state["summary"])
    output_path = "artifacts/output.txt"  # 교체 필요

    return {**state, "output_path": output_path}


def finalize(state: FlowState) -> FlowState:
    """
    마지막 Step: Human Review 승인 후 최종 처리
    TODO: 배포, 알림 발송 등 후처리 로직 구현
    """
    logger.info("[flow] finalize 실행")

    # TODO: 최종 후처리
    # from app_mcp.services.notifications import notify_complete
    # notify_complete(state["summary"], state["output_path"])

    return state


# ─────────────────────────────────────────────
# 3) Human Review 라우팅 (수정 불필요)
# ─────────────────────────────────────────────

def route_human_review(state: FlowState) -> str:
    decision = state.get("human_decision", "pending")
    revision_count = state.get("revision_count", 0)
    max_revisions = state.get("max_revisions", 3)

    if decision == "approve":
        return "finalize"
    elif decision == "revise" and revision_count < max_revisions:
        return "summarize"  # 재생성 루프
    else:
        return "finalize"  # max_revisions 초과 시 강제 종료


# ─────────────────────────────────────────────
# 4) 그래프 조립
# TODO: 노드 추가 시 아래에 add_node / add_edge 추가
# ─────────────────────────────────────────────

def build_graph():
    builder = StateGraph(FlowState)

    # 노드 등록
    builder.add_node("load_data", load_data)
    builder.add_node("validate_data", validate_data)
    # TODO: 추가 노드 등록
    # builder.add_node("your_domain_step", your_domain_step)
    builder.add_node("summarize", summarize)
    builder.add_node("generate_output", generate_output)
    builder.add_node("finalize", finalize)

    # 엣지 연결
    builder.add_edge(START, "load_data")
    builder.add_edge("load_data", "validate_data")
    # TODO: 추가 노드 연결
    # builder.add_edge("validate_data", "your_domain_step")
    # builder.add_edge("your_domain_step", "summarize")
    builder.add_edge("validate_data", "summarize")
    builder.add_edge("summarize", "generate_output")

    # Human Review 분기
    builder.add_conditional_edges(
        "generate_output",
        route_human_review,
        {
            "finalize": "finalize",
            "summarize": "summarize",
        }
    )
    builder.add_edge("finalize", END)

    return builder.compile(checkpointer=MemorySaver())


graph = build_graph()
