# 🖥 MCP Fullstack Template

![Python](https://img.shields.io/badge/Python-3.10+-111111?style=flat-square&logo=python&logoColor=EA0029)
![Flask](https://img.shields.io/badge/Flask-111111?style=flat-square&logo=flask&logoColor=EA0029)
![Claude](https://img.shields.io/badge/Claude_API-111111?style=flat-square&logoColor=EA0029)
![License](https://img.shields.io/badge/license-MIT-EA0029?style=flat-square)

**Claude AI + 멀티 MCP 서버 + 실시간 대시보드** 풀스택 템플릿입니다.

`# TODO` 주석을 따라 도메인 로직만 채워 넣으면 대시보드 + 채팅이 결합된 MCP 앱을 만들 수 있습니다.

---

## ⚡ 빠른 시작

```bash
git clone https://github.com/kxmdoyn/mcp-fullstack-template.git
cd mcp-fullstack-template
cp .env.example .env
pip install -r requirements.txt

# 터미널 1: MCP 서버 1
python mcp_servers/your_mcp/gateway.py

# 터미널 2: MCP 서버 2 (필요시)
# MCP_PORT=5002 MCP_SERVER_NAME="Server 2" python mcp_servers/your_mcp/gateway.py

# 터미널 3: 프론트엔드
python frontend/app.py
# → http://localhost:5000
```

---

## 🏗 아키텍처

```
브라우저
  ├── 대시보드 (좌측 패널) — /api/dashboard 10초마다 자동 갱신
  └── 채팅 UI (우측 패널) — /api/chat

frontend/app.py (Flask, port 5000)
  ├── Claude API (tool_use)
  └── 멀티 MCP 라우팅 (TOOL_ROUTING)
        ├── mcp_servers/your_mcp/gateway.py  (port 5001)
        └── mcp_servers/your_mcp/gateway.py  (port 5002)
              │
              ▼
        도메인 Tool 함수
```

---

## 📁 구조

```
mcp-fullstack-template/
├── frontend/
│   ├── app.py                    # Flask 웹 서버 + Claude 연동
│   └── templates/
│       └── index.html            # 대시보드 + 채팅 UI
├── mcp_servers/
│   └── your_mcp/
│       └── gateway.py            # MCP Gateway (복사해서 서버마다 사용)
├── requirements.txt
└── .env.example
```

---

## 🔧 적용 방법

**1. MCP 서버 추가** (`mcp_servers/your_mcp/gateway.py` 복사)

```python
TOOL_MAP = {
    "your_tool": your_function,
}
```

**2. 라우팅 등록** (`frontend/app.py`)

```python
MCP_SERVERS = {
    "mcp_1": "http://localhost:5001/mcp",
    "mcp_2": "http://localhost:5002/mcp",
}

TOOL_ROUTING = {
    "your_tool": "mcp_1",
}
```

**3. Claude Tool 정의** (`frontend/app.py`)

```python
CLAUDE_TOOLS = [
    {
        "name": "your_tool",
        "description": "...",
        "input_schema": {...},
    }
]
```

**4. 대시보드 UI 수정** (`frontend/templates/index.html`)

```javascript
// loadDashboard() 함수에서 실제 데이터 필드로 교체
document.getElementById('metric-1').textContent = data.your_field;
```

---

## 📦 기반 프로젝트

Koscom AI Agent Challenge 2025 **대상 수상작**의 프론트엔드 + 멀티 MCP 구조를 추출하여 범용화했습니다.

→ [K-WON Risk Management AI Agent](https://github.com/dancom-MCP-AI-Agent/final_koscom_ai_agent_public)

---

## 📄 License

MIT License © 2026 kxmdoyn
