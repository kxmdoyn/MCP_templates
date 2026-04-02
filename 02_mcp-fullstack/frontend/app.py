"""
frontend/app.py — MCP Fullstack Template

Claude AI + 멀티 MCP 서버 연결 대시보드 + 채팅 앱

구조:
    Flask 웹 서버 (이 파일)
    → Claude API (tool_use)
    → 여러 MCP Gateway (mcp_servers/*/gateway.py)
    → 백엔드 데이터 API (선택)

Usage:
    python frontend/app.py
    → http://localhost:5000

TODO: 도메인에 맞게 수정할 부분은 # TODO 주석 참고
"""

import json
import os
import traceback

import requests
from anthropic import Anthropic
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

load_dotenv()

app = Flask(__name__, template_folder="templates", static_folder="static")

# ─────────────────────────────────────────────
# 설정
# TODO: MCP 서버 URL 추가/수정
# ─────────────────────────────────────────────
PROJECT_NAME = os.getenv("PROJECT_NAME", "MCP Dashboard")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:4000")

# MCP 서버 URL 목록
# TODO: 실제 MCP 서버 URL로 수정
MCP_SERVERS = {
    "mcp_1": os.getenv("MCP_1_URL", "http://localhost:5001/mcp"),
    "mcp_2": os.getenv("MCP_2_URL", "http://localhost:5002/mcp"),
    # "mcp_3": os.getenv("MCP_3_URL", "http://localhost:5003/mcp"),
}

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", ""))
conversation_history = []


# ─────────────────────────────────────────────
# MCP 호출 헬퍼
# ─────────────────────────────────────────────

def call_mcp(server_key: str, tool_name: str, params: dict) -> dict:
    """특정 MCP 서버의 Tool 호출"""
    url = MCP_SERVERS.get(server_key)
    if not url:
        return {"error": f"Unknown MCP server: {server_key}"}
    try:
        resp = requests.post(
            url,
            json={"tool": tool_name, "params": params},
            timeout=20,
        )
        resp.raise_for_status()
        data = resp.json()
        return data.get("result", data)
    except requests.exceptions.Timeout:
        return {"error": f"{server_key} 타임아웃"}
    except Exception as e:
        return {"error": str(e)}


# ─────────────────────────────────────────────
# 백엔드 데이터 조회
# TODO: 실제 백엔드 API 엔드포인트로 수정
# ─────────────────────────────────────────────

def fetch_dashboard_data() -> dict | None:
    """대시보드용 실시간 데이터 조회"""
    try:
        # TODO: 실제 엔드포인트로 수정
        resp = requests.get(f"{BACKEND_URL}/api/status", timeout=5)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"❌ 백엔드 조회 실패: {e}")
        return None


# ─────────────────────────────────────────────
# Claude Tool 정의
# TODO: 실제 도메인 Tool로 교체
# ─────────────────────────────────────────────

CLAUDE_TOOLS = [
    # MCP 1 Tools
    {
        "name": "mcp1_tool_a",
        "description": "TODO: MCP 1의 Tool A 설명 — 어떤 상황에서 쓰는지 명확하게",
        "input_schema": {
            "type": "object",
            "properties": {
                "param1": {"type": "string", "description": "TODO"},
            },
        },
    },
    # MCP 2 Tools
    {
        "name": "mcp2_tool_a",
        "description": "TODO: MCP 2의 Tool A 설명",
        "input_schema": {
            "type": "object",
            "properties": {
                "param1": {"type": "string", "description": "TODO"},
            },
        },
    },
    # TODO: 추가 Tool 정의
]

# Tool → MCP 서버 라우팅 맵
# TODO: 실제 Tool 이름과 서버 키로 수정
TOOL_ROUTING = {
    "mcp1_tool_a": "mcp_1",
    "mcp2_tool_a": "mcp_2",
    # "your_tool": "mcp_1",
}


def execute_tool(tool_name: str, tool_input: dict) -> dict:
    """Tool 이름으로 적절한 MCP 서버에 라우팅"""
    server_key = TOOL_ROUTING.get(tool_name)
    if not server_key:
        return {"error": f"Unknown tool: {tool_name}"}
    return call_mcp(server_key, tool_name, tool_input)


# ─────────────────────────────────────────────
# 시스템 프롬프트
# TODO: 도메인에 맞게 수정
# ─────────────────────────────────────────────

def build_system_prompt(dashboard_data: dict | None = None) -> str:
    data_section = ""
    if dashboard_data:
        data_section = f"""
# 현재 실시간 데이터
{json.dumps(dashboard_data, ensure_ascii=False, indent=2)}
"""

    return f"""당신은 {PROJECT_NAME} AI 어시스턴트입니다.
{data_section}

# 사용 가능한 Tool

TODO: 각 Tool의 용도와 사용 시점을 명확하게 작성하세요.

- mcp1_tool_a: TODO 설명
- mcp2_tool_a: TODO 설명

# 응답 가이드

- 항상 한국어로 답변하세요.
- Tool 결과를 바탕으로 구체적인 수치와 함께 설명하세요.
- 비전문가도 이해할 수 있게 쉽게 설명하세요.
"""


# ─────────────────────────────────────────────
# Flask 라우트
# ─────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html", project_name=PROJECT_NAME)


@app.route("/api/dashboard")
def dashboard_data():
    """대시보드 실시간 데이터 API"""
    data = fetch_dashboard_data()
    if data is None:
        return jsonify({"error": "백엔드 연결 실패"}), 503
    return jsonify(data)


@app.route("/api/chat", methods=["POST"])
def chat():
    global conversation_history

    try:
        user_message = request.json.get("message", "").strip()
        if not user_message:
            return jsonify({"error": "메시지가 비어있습니다"}), 400

        dashboard_data = fetch_dashboard_data()
        system_prompt = build_system_prompt(dashboard_data)

        messages = conversation_history.copy()
        messages.append({"role": "user", "content": user_message})

        final_answer = ""
        tools_used = []
        max_rounds = 5

        for _ in range(max_rounds):
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                system=system_prompt,
                messages=messages,
                tools=CLAUDE_TOOLS,
                tool_choice={"type": "auto"},
                max_tokens=2000,
            )

            assistant_content = response.content
            messages.append({"role": "assistant", "content": assistant_content})

            tool_blocks = [b for b in assistant_content if getattr(b, "type", None) == "tool_use"]

            if not tool_blocks:
                final_answer = "".join(
                    getattr(b, "text", "")
                    for b in assistant_content
                    if getattr(b, "type", None) == "text"
                )
                break

            tool_results = {"role": "user", "content": []}
            for tb in tool_blocks:
                tools_used.append(tb.name)
                try:
                    result = execute_tool(tb.name, tb.input)
                except Exception as e:
                    result = {"error": str(e)}

                tool_results["content"].append({
                    "type": "tool_result",
                    "tool_use_id": tb.id,
                    "content": json.dumps(result, ensure_ascii=False),
                })
            messages.append(tool_results)

        if not final_answer:
            final_answer = "죄송합니다. 처리 중 문제가 발생했습니다."

        conversation_history.extend([
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": final_answer},
        ])
        conversation_history = conversation_history[-20:]

        return jsonify({
            "response": final_answer,
            "tools_used": tools_used,
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route("/api/reset", methods=["POST"])
def reset():
    global conversation_history
    conversation_history = []
    return jsonify({"status": "ok"})


@app.route("/api/health")
def health():
    mcp_status = {}
    for key, url in MCP_SERVERS.items():
        try:
            resp = requests.get(url.replace("/mcp", "/health"), timeout=3)
            mcp_status[key] = "connected" if resp.ok else "error"
        except Exception:
            mcp_status[key] = "disconnected"
    return jsonify({"status": "ok", "mcp_servers": mcp_status})


if __name__ == "__main__":
    print("=" * 60)
    print(f"🚀 {PROJECT_NAME}")
    print(f"   http://localhost:5000")
    for k, v in MCP_SERVERS.items():
        print(f"   {k}: {v}")
    print("=" * 60)
    app.run(debug=True, port=5000, host="0.0.0.0")
