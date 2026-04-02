# 🧩 MCP Templates

![Python](https://img.shields.io/badge/Python-3.10+-111111?style=flat-square&logo=python&logoColor=EA0029)
![Flask](https://img.shields.io/badge/Flask-111111?style=flat-square&logo=flask&logoColor=EA0029)
![FastAPI](https://img.shields.io/badge/FastAPI-111111?style=flat-square&logo=fastapi&logoColor=EA0029)
![Claude](https://img.shields.io/badge/Claude_API-111111?style=flat-square&logoColor=EA0029)
![LangGraph](https://img.shields.io/badge/LangGraph-111111?style=flat-square&logoColor=EA0029)
![License](https://img.shields.io/badge/license-MIT-EA0029?style=flat-square)

**Koscom AI Agent Challenge 2025 대상 수상작**에서 추출한 MCP Server 템플릿 모음입니다.

Claude AI + MCP 기반 AI Agent를 빠르게 시작할 수 있도록 인프라 레이어를 재사용 가능한 형태로 정리했습니다.

→ 원본 프로젝트: [K-WON Risk Management AI Agent](https://github.com/dancom-MCP-AI-Agent/final_koscom_ai_agent_public)

---

## 📦 템플릿 비교

| | 01_mcp-chat | 02_mcp-fullstack | 03_mcp-langgraph |
|---|---|---|---|
| **난이도** | ⭐ 쉬움 | ⭐⭐ 보통 | ⭐⭐⭐ 복잡 |
| **프론트엔드** | ✅ 채팅 UI | ✅ 대시보드 + 채팅 | ❌ |
| **MCP 서버 수** | 단일 | 멀티 | 단일 |
| **LangGraph** | ❌ | ❌ | ✅ |
| **APScheduler** | ❌ | ❌ | ✅ |
| **Slack 승인** | ❌ | ❌ | ✅ |
| **DB** | ❌ | ❌ | ✅ SQLAlchemy |
| **서버 구성** | Flask × 2 | Flask × N | Flask + FastAPI |

---

## 🗂 구조

```
mcp-templates/
├── README.md
├── 01_mcp-chat/            ← Claude 채팅 + 단일 MCP
├── 02_mcp-fullstack/       ← 대시보드 + 채팅 + 멀티 MCP
└── 03_mcp-langgraph/       ← LangGraph + APScheduler + Slack Human Review
```

---

## 01 `mcp-chat` — 심플 채팅 템플릿

**Claude AI + 단일 MCP 서버** 채팅 앱입니다.

Tool 함수 하나 구현하고 등록하면 바로 동작합니다.

```
브라우저 → app.py (Flask) → Claude API → MCP Gateway → Tool 함수
```

**이런 프로젝트에 적합:**
- Claude에게 특정 데이터를 조회/분석시키고 싶을 때
- 빠르게 프로토타입 만들 때
- MCP 처음 써보는 경우

**시작:**
```bash
cd 01_mcp-chat
cp .env.example .env
pip install -r requirements.txt
python mcp_server/gateway.py   # 터미널 1
python app.py                  # 터미널 2
```

---

## 02 `mcp-fullstack` — 대시보드 + 채팅 템플릿

**실시간 대시보드 + Claude 채팅 + 멀티 MCP 서버** 구조입니다.

대시보드 좌측 패널이 10초마다 자동 갱신되고, 채팅으로 Tool을 호출하면 대시보드도 함께 업데이트됩니다.

```
브라우저 (대시보드 + 채팅)
    │
frontend/app.py (Flask)
    ├── MCP Server 1 (port 5001)
    └── MCP Server 2 (port 5002)
```

**이런 프로젝트에 적합:**
- 실시간 모니터링 대시보드가 필요할 때
- MCP 서버를 여러 개 연동해야 할 때
- 데이터 시각화 + AI 채팅을 함께 제공할 때

**시작:**
```bash
cd 02_mcp-fullstack
cp .env.example .env
pip install -r requirements.txt
python mcp_servers/your_mcp/gateway.py   # 터미널 1
python frontend/app.py                   # 터미널 2
```

---

## 03 `mcp-langgraph` — LangGraph 워크플로우 템플릿

**LangGraph multi-step reasoning + APScheduler + Slack Human Review** 구조입니다.

Koscom AI Agent Challenge 2025 대상 수상작의 `report-master` MCP 서버에서 인프라 레이어를 추출했습니다.

```
gateway.py (Flask, MCP Client 연결)
    │
mcp_server.py (FastAPI)
    ├── LangGraph 워크플로우 (12단계 reasoning)
    ├── APScheduler (15분 interval + 월간 cron)
    └── Slack Human Review (승인/반려 루프)
```

**이런 프로젝트에 적합:**
- 복잡한 multi-step AI 워크플로우가 필요할 때
- 자동화 보고서 생성, 규제 대응 등 정기 배치 작업
- 사람의 최종 승인이 필요한 Human-in-the-loop 시스템
- 스케줄러 기반 자동화 파이프라인

**시작:**
```bash
cd 03_mcp-langgraph
cp .env.example .env
pip install -r requirements.txt
python mcp_server.py   # 터미널 1 (FastAPI, port 8000)
python gateway.py      # 터미널 2 (Flask MCP Gateway, port 5000)
```

---

## 🔧 어떤 템플릿을 골라야 할까?

```
새 프로젝트 시작
    │
    ├── 프론트엔드 필요?
    │       │
    │       ├── No  → 03_mcp-langgraph
    │       │
    │       └── Yes
    │               │
    │               ├── MCP 서버 1개, 심플하게 → 01_mcp-chat
    │               │
    │               └── 대시보드 + 멀티 MCP   → 02_mcp-fullstack
    │
    └── LangGraph / 스케줄러 / Slack 승인 필요? → 03_mcp-langgraph
```

---

## 📄 License

MIT License © 2026 [kxmdoyn](https://github.com/kxmdoyn)

---

> 본 템플릿은 **Koscom AI Agent Challenge 2025 대상 수상작**  
> [K-WON Risk Management AI Agent](https://github.com/dancom-MCP-AI-Agent/final_koscom_ai_agent_public)의  
> 인프라 레이어를 추출하여 범용화한 것입니다.
