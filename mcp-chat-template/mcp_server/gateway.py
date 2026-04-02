"""
mcp_server/gateway.py — MCP Gateway (심플 버전)

Usage:
    python mcp_server/gateway.py
    → http://localhost:5001/mcp

TODO: TOOL_MAP에 실제 Tool 함수 등록
"""

import os
import traceback

from dotenv import load_dotenv
from flask import Flask, jsonify, request

load_dotenv()

app = Flask(__name__)
PORT = int(os.getenv("MCP_PORT", 5001))


# ─────────────────────────────────────────────
# TODO: Tool 함수 구현
# ─────────────────────────────────────────────

def tool_example(params: dict) -> dict:
    """
    TODO: 실제 Tool 로직으로 교체
    외부 API 호출, DB 조회, 계산 등
    """
    return {
        "message": "example_tool 실행됨",
        "received_params": params,
        # TODO: 실제 결과 반환
    }


# TODO: Tool 추가
# def tool_your_tool(params: dict) -> dict:
#     ...


# ─────────────────────────────────────────────
# TOOL_MAP 등록
# TODO: 실제 Tool 이름과 함수로 교체
# ─────────────────────────────────────────────

TOOL_MAP = {
    "example_tool": tool_example,
    # "your_tool": tool_your_tool,
}


# ─────────────────────────────────────────────
# MCP 엔드포인트 (수정 불필요)
# ─────────────────────────────────────────────

@app.route("/mcp", methods=["POST"])
def mcp():
    try:
        data = request.json or {}
        tool_name = data.get("tool")
        params = data.get("params", {})

        if tool_name not in TOOL_MAP:
            return jsonify({
                "success": False,
                "error": f"Unknown tool: {tool_name}",
                "available": list(TOOL_MAP.keys()),
            }), 404

        result = TOOL_MAP[tool_name](params)
        return jsonify({"success": True, "result": result})

    except Exception as e:
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/health")
def health():
    return jsonify({"status": "ok", "tools": list(TOOL_MAP.keys())})


if __name__ == "__main__":
    print(f"🚀 MCP Gateway → http://0.0.0.0:{PORT}/mcp")
    print(f"   Tools: {list(TOOL_MAP.keys())}")
    app.run(host="0.0.0.0", port=PORT, debug=True)
