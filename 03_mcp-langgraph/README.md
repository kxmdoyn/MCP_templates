# 🧩 MCP Server Template

![Python](https://img.shields.io/badge/Python-3.10+-111111?style=flat-square&logo=python&logoColor=EA0029)
![FastAPI](https://img.shields.io/badge/FastAPI-111111?style=flat-square&logo=fastapi&logoColor=EA0029)
![LangGraph](https://img.shields.io/badge/LangGraph-111111?style=flat-square&logoColor=EA0029)
![License](https://img.shields.io/badge/license-MIT-EA0029?style=flat-square)

**Flask MCP Gateway + FastAPI Backend + LangGraph + APScheduler + Slack Human Review**  
구조를 재사용 가능하게 추출한 MCP Server 템플릿입니다.

`# TODO` 주석을 따라 도메인 로직만 채워 넣으면 바로 동작하는 MCP Server를 만들 수 있습니다.

---

## ⚡ 빠른 시작

```bash
git clone https://github.com/kxmdoyn/mcp-server-template.git
cd mcp-server-template
cp .env.example .env
pip install -r requirements.txt

# 터미널 1: FastAPI 백엔드
python mcp_server.py

# 터미널 2: MCP Gateway
python gateway.py
```

---

## 🏗 아키텍처

```
Claude AI (MCP Client)
        │
        ▼
gateway.py          Flask MCP Gateway      (port 5000)
        │
        ▼
mcp_server.py       FastAPI Backend        (port 8000)
  ├── LangGraph     multi-step workflow
  ├── APScheduler   interval + cron jobs
  └── Slack         Human-in-the-loop 승인
```

---

## 📁 구조

```
mcp-server-template/
├── gateway.py                     # MCP HTTP Gateway (Flask)
├── mcp_server.py                  # FastAPI 백엔드 엔트리포인트
├── requirements.txt
├── .env.example
├── TEMPLATE_GUIDE.md              # 상세 적용 가이드 ← 먼저 읽기
└── app_mcp/
    ├── core/
    │   ├── config.py              # 환경변수 설정
    │   ├── db.py                  # DB 연결 (SQLAlchemy async)
    │   └── scheduler.py           # APScheduler Job 등록
    ├── graph/
    │   ├── flow.py                # LangGraph 워크플로우
    │   └── flow_interrupt.py      # Human Review 인터럽트
    ├── tools/
    │   └── your_tools.py          # ← 도메인 Tool 구현 위치
    ├── api/
    │   ├── mcp.py                 # /mcp/run 엔드포인트
    │   └── human_review.py        # Slack 승인 웹훅
    └── services/
        └── notifications.py       # Slack 알림
```

---

## 🔧 적용 방법

**1. Tool 구현**

```python
# app_mcp/tools/your_tools.py
async def get_your_data(param: str) -> dict:
    # 실제 데이터 조회 로직
    return {"data": ...}
```

**2. Gateway 등록**

```python
# gateway.py
TOOL_MAP = {
    "get_your_data": get_your_data,
}
```

**3. 워크플로우 노드 추가**

```python
# app_mcp/graph/flow.py
def your_step(state): ...
builder.add_node("your_step", your_step)
builder.add_edge("validate_data", "your_step")
```

자세한 내용은 **[TEMPLATE_GUIDE.md](./TEMPLATE_GUIDE.md)** 참고

---

## 📦 기반 프로젝트

Koscom AI Agent Challenge 2025 **대상 수상작**의 인프라 레이어를 추출하여 범용화했습니다.

→ [K-WON Risk Management AI Agent](https://github.com/dancom-MCP-AI-Agent/final_koscom_ai_agent_public)  
→ [Report-Master MCP Server](https://github.com/kxmdoyn/kwon-report-master-agent)

---

## 📄 License

MIT
