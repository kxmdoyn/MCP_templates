# 💬 MCP Chat Template

![Python](https://img.shields.io/badge/Python-3.10+-111111?style=flat-square&logo=python&logoColor=EA0029)
![Flask](https://img.shields.io/badge/Flask-111111?style=flat-square&logo=flask&logoColor=EA0029)
![Claude](https://img.shields.io/badge/Claude_API-111111?style=flat-square&logoColor=EA0029)
![License](https://img.shields.io/badge/license-MIT-EA0029?style=flat-square)

**Claude AI + 단일 MCP 서버** 연결 채팅 앱 템플릿입니다.

`# TODO` 주석을 따라 Tool 로직만 채워 넣으면 바로 동작하는 MCP 채팅 앱을 만들 수 있습니다.

---

## ⚡ 빠른 시작

```bash
git clone https://github.com/kxmdoyn/mcp-chat-template.git
cd mcp-chat-template
cp .env.example .env       # API Key 입력
pip install -r requirements.txt

# 터미널 1: MCP Gateway
python mcp_server/gateway.py

# 터미널 2: 웹 앱
python app.py
# → http://localhost:5000
```

---

## 🏗 아키텍처

```
브라우저 (index.html)
    │ POST /api/chat
    ▼
app.py (Flask, port 5000)
    │ Claude API tool_use
    ▼
Claude AI
    │ Tool 호출
    ▼
mcp_server/gateway.py (Flask, port 5001)
    │
    ▼
도메인 Tool 함수
```

---

## 📁 구조

```
mcp-chat-template/
├── app.py                        # Flask 웹 서버 + Claude 연동
├── requirements.txt
├── .env.example
├── frontend/
│   └── templates/
│       └── index.html            # 채팅 UI
└── mcp_server/
    └── gateway.py                # MCP Gateway + Tool 구현
```

---

## 🔧 적용 방법

**1. Tool 구현** (`mcp_server/gateway.py`)

```python
def tool_your_tool(params: dict) -> dict:
    # 실제 로직
    return {"result": ...}

TOOL_MAP = {
    "your_tool": tool_your_tool,
}
```

**2. Claude Tool 정의** (`app.py`)

```python
CLAUDE_TOOLS = [
    {
        "name": "your_tool",
        "description": "어떤 상황에서 이 Tool을 써야 하는지",
        "input_schema": {...},
    }
]
```

**3. 시스템 프롬프트 수정** (`app.py` → `build_system_prompt()`)

---

## 📦 기반 프로젝트

Koscom AI Agent Challenge 2025 **대상 수상작**의 프론트엔드 레이어를 추출하여 범용화했습니다.

→ [K-WON Risk Management AI Agent](https://github.com/dancom-MCP-AI-Agent/final_koscom_ai_agent_public)

---

## 📄 License

MIT License © 2026 kxmdoyn
