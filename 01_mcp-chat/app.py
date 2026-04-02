"""
app.py — MCP Chat Template (심플 버전)

Claude AI + 단일 MCP 서버 연결 채팅 앱

구조:
    Flask 웹 서버 (이 파일)
    → Claude API (tool_use)
    → MCP Gateway (mcp_server/gateway.py)

Usage:
    python app.py
    → http://localhost:5000

TODO: 도메인에 맞게 수정할 부분은 # TODO 주석 참고
"""

import json
import os

import requests
from anthropic import Anthropic
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

load_dotenv()

app = Flask(__name__, template_folder="frontend/templates", static_folder="frontend/static")

# ─────────────────────────────────────────────
# 설정
# TODO: MCP 서버 URL 및 포트 수정
# ─────────────────────────────────────────────
MCP_URL = os.getenv("MCP_URL", "http://localhost:5001/mcp")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
PROJECT_NAME = os.getenv("PROJECT_NAME", "MCP Chat")

client = Anthropic(api_key=ANTHROPIC_API_KEY)
conversation_history = []


# ─────────────────────────────────────────────
# Claude Tool 정의
# TODO: 실제 도메인 Tool로 교체
# ─────────────────────────────────────────────

CLAUDE_TOOLS = [
    {
        "name": "example_tool",
        "description": "TODO: 실제 Tool 설명으로 교체. 어떤 상황에서 이 Tool을 써야 하는지 명확하게 작성",
        "input_schema": {
            "type": "object",
            "properties": {
                "param1": {
                    "type": "string",
                    "description": "TODO: 파라미터 설명",
                },
            },
            "required": ["param1"],
        },
    },
    # TODO: 추가 Tool 정의
    # {
    #     "name": "your_tool",
    #     "description": "...",
    #     "input_schema": {...},
    # },
]


# ─────────────────────────────────────────────
# MCP Tool 실행
# ─────────────────────────────────────────────

def call_mcp(tool_name: str, params: dict) -> dict:
    """MCP Gateway로 Tool 호출"""
    try:
        resp = requests.post(
            MCP_URL,
            json={"tool": tool_name, "params": params},
            timeout=20,
        )
        resp.raise_for_status()
        data = resp.json()
        return data.get("result", data)
    except requests.exceptions.Timeout:
        return {"error": "MCP 서버 타임아웃"}
    except Exception as e:
        return {"error": str(e)}


def execute_tool(tool_name: str, tool_input: dict) -> dict:
    """
    Tool 이름에 따라 MCP 호출 라우팅

    TODO: Tool이 여러 개라면 아래처럼 분기 추가
    """
    # TODO: 실제 Tool 이름으로 교체
    return call_mcp(tool_name, tool_input)


# ─────────────────────────────────────────────
# 시스템 프롬프트
# TODO: 도메인에 맞게 수정
# ─────────────────────────────────────────────

def build_system_prompt() -> str:
    return f"""당신은 {PROJECT_NAME} AI 어시스턴트입니다.

# 사용 가능한 Tool

TODO: 각 Tool의 용도와 사용 시점을 여기에 명확하게 작성하세요.
Claude가 어떤 상황에서 어떤 Tool을 써야 하는지 이해할 수 있도록 구체적으로 설명하세요.

예시:
- example_tool: 사용자가 X를 요청할 때 사용. param1에는 Y를 넘기세요.

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


@app.route("/api/chat", methods=["POST"])
def chat():
    global conversation_history

    try:
        user_message = request.json.get("message", "").strip()
        if not user_message:
            return jsonify({"error": "메시지가 비어있습니다"}), 400

        messages = conversation_history.copy()
        messages.append({"role": "user", "content": user_message})

        final_answer = ""
        max_rounds = 5

        # Multi-step Tool 실행 루프 (수정 불필요)
        for _ in range(max_rounds):
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                system=build_system_prompt(),
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
                result = execute_tool(tb.name, tb.input)
                tool_results["content"].append({
                    "type": "tool_result",
                    "tool_use_id": tb.id,
                    "content": json.dumps(result, ensure_ascii=False),
                })
            messages.append(tool_results)

        if not final_answer:
            final_answer = "죄송합니다. 처리 중 문제가 발생했습니다."

        # 히스토리 저장 (최근 20개)
        conversation_history.extend([
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": final_answer},
        ])
        conversation_history = conversation_history[-20:]

        return jsonify({"response": final_answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/reset", methods=["POST"])
def reset():
    global conversation_history
    conversation_history = []
    return jsonify({"status": "ok"})


@app.route("/api/health")
def health():
    try:
        resp = requests.get(MCP_URL.replace("/mcp", "/health"), timeout=3)
        mcp_status = "connected" if resp.ok else "error"
    except Exception:
        mcp_status = "disconnected"
    return jsonify({"status": "ok", "mcp": mcp_status})


if __name__ == "__main__":
    print("=" * 50)
    print(f"🚀 {PROJECT_NAME} Chat App")
    print(f"   http://localhost:5000")
    print(f"   MCP: {MCP_URL}")
    print("=" * 50)
    app.run(debug=True, port=5000, host="0.0.0.0")
