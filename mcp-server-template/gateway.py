"""
MCP HTTP Gateway (Flask)

- /mcp POST 엔드포인트로 Claude MCP Client 연결
- TOOL_MAP에 도구 함수 등록만 하면 동작
- 내부적으로 FastAPI 백엔드(mcp_server.py)에 REST 호출

Usage:
    python gateway.py

Port: 5000 (기본값, .env에서 MCP_GATEWAY_PORT로 변경 가능)
"""

import os
import traceback
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

MCP_BACKEND_BASE = os.getenv("MCP_BACKEND_BASE", "http://127.0.0.1:8000").rstrip("/")
MCP_GATEWAY_PORT = int(os.getenv("MCP_GATEWAY_PORT", 5000))
PROJECT_NAME = os.getenv("PROJECT_NAME", "MCP Server")

app = Flask(__name__)


# ─────────────────────────────────────────────
# Helper: FastAPI 백엔드로 프록시
# ─────────────────────────────────────────────

def _proxy_get(path: str, params=None):
    url = f"{MCP_BACKEND_BASE}{path}"
    resp = requests.get(url, params=params, timeout=20)
    resp.raise_for_status()
    return resp.json()


def _proxy_post(path: str, payload=None):
    url = f"{MCP_BACKEND_BASE}{path}"
    resp = requests.post(url, json=payload or {}, timeout=60)
    resp.raise_for_status()
    return resp.json()


# ─────────────────────────────────────────────
# TODO: 도메인 Tool 함수 정의
# 각 함수는 params(dict)를 받고 dict를 반환
# ─────────────────────────────────────────────

def tool_example_get(params: dict) -> dict:
    """
    TODO: 실제 Tool 로직으로 교체
    예시: return _proxy_get("/your/endpoint", params=params)
    """
    return {"message": "tool_example_get - 여기에 로직 구현"}


def tool_example_post(params: dict) -> dict:
    """
    TODO: 실제 Tool 로직으로 교체
    예시: return _proxy_post("/your/endpoint", params)
    """
    return {"message": "tool_example_post - 여기에 로직 구현"}


# ─────────────────────────────────────────────
# TOOL_MAP: Tool 이름 → 함수 매핑
# TODO: 실제 Tool 이름과 함수로 교체
# ─────────────────────────────────────────────

TOOL_MAP = {
    "example_get": tool_example_get,
    "example_post": tool_example_post,
    # "your_tool_name": your_tool_function,
}


# ─────────────────────────────────────────────
# MCP Endpoint (수정 불필요)
# ─────────────────────────────────────────────

@app.route("/mcp", methods=["POST"])
def mcp_root():
    try:
        data = request.json or {}
        tool_name = data.get("tool")
        params = data.get("params", {})

        print(f"🔧 MCP Tool 요청: {tool_name} | params={params}")

        if tool_name not in TOOL_MAP:
            return jsonify({
                "success": False,
                "error": f"Unknown tool: {tool_name}. Available: {list(TOOL_MAP.keys())}"
            }), 404

        result = TOOL_MAP[tool_name](params)

        return jsonify({
            "success": True,
            "result": result
        })

    except Exception as e:
        print(f"❌ MCP Error: {e}")
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e),
            "trace": traceback.format_exc()
        }), 500


@app.route("/health", methods=["GET"])
def health():
    try:
        backend = requests.get(f"{MCP_BACKEND_BASE}/health", timeout=5).json()
        return jsonify({"status": "ok", "backend": backend, "tools": list(TOOL_MAP.keys())})
    except Exception:
        return jsonify({"status": "gateway_only", "tools": list(TOOL_MAP.keys())})


@app.route("/tools", methods=["GET"])
def list_tools():
    """등록된 Tool 목록 확인"""
    return jsonify({"tools": list(TOOL_MAP.keys())})


if __name__ == "__main__":
    print("=" * 60)
    print(f"🚀 {PROJECT_NAME} MCP Gateway 시작")
    print(f"   - MCP Endpoint : http://0.0.0.0:{MCP_GATEWAY_PORT}/mcp")
    print(f"   - Backend API  : {MCP_BACKEND_BASE}")
    print(f"   - Tools        : {', '.join(TOOL_MAP.keys())}")
    print("=" * 60)
    app.run(host="0.0.0.0", port=MCP_GATEWAY_PORT, debug=True)
