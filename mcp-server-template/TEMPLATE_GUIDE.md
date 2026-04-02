# 🛠 MCP Server Template — 사용 가이드

이 템플릿은 **Flask MCP Gateway + FastAPI Backend + LangGraph + APScheduler + Slack Human Review** 구조를 재사용 가능하게 정리한 것입니다.

새 프로젝트 시작 시 `# TODO` 주석을 따라 도메인 로직만 채워 넣으면 됩니다.

---

## 🚀 빠른 시작

```bash
git clone https://github.com/kxmdoyn/mcp-server-template.git my-mcp-project
cd my-mcp-project
cp .env.example .env       # 환경변수 설정
pip install -r requirements.txt
python mcp_server.py       # FastAPI 백엔드 (port 8000)
python gateway.py          # MCP Gateway (port 5000)
```

---

## 📁 파일별 수정 가이드

### 반드시 수정해야 하는 파일

| 파일 | 수정 내용 |
|---|---|
| `gateway.py` | `TOOL_MAP`에 실제 Tool 함수 등록 |
| `app_mcp/tools/your_tools.py` | 도메인 Tool 로직 구현 |
| `app_mcp/core/config.py` | 도메인별 환경변수 추가 |
| `app_mcp/graph/flow.py` | 워크플로우 노드 추가/제거 |
| `app_mcp/core/scheduler.py` | Job 주기 및 로직 수정 |
| `.env.example` → `.env` | 실제 API Key, DB URL 등 입력 |

### 선택적으로 수정하는 파일

| 파일 | 수정 내용 |
|---|---|
| `app_mcp/services/notifications.py` | Slack 카드 메시지 커스터마이징 |
| `app_mcp/api/human_review.py` | Human Review DB 연동 구현 |
| `app_mcp/api/mcp.py` | `/mcp/run` 요청 스키마 수정 |
| `app_mcp/graph/flow_interrupt.py` | Slack 승인 요청 내용 수정 |

### 수정 불필요한 파일 (인프라 레이어)

| 파일 | 설명 |
|---|---|
| `mcp_server.py` | FastAPI 앱 생성 및 라우터 등록 |
| `app_mcp/core/db.py` | DB 연결 및 세션 관리 |
| `gateway.py` (라우팅 부분) | `/mcp` 엔드포인트 라우팅 로직 |
| `app_mcp/graph/flow.py` (그래프 조립 부분) | LangGraph 노드 연결 구조 |

---

## 🔧 새 프로젝트 적용 순서

**Step 1. Tool 구현**
```
app_mcp/tools/your_tools.py 에 도메인 함수 작성
```

**Step 2. Gateway 등록**
```python
# gateway.py
from app_mcp.tools.your_tools import get_data, analyze_data

TOOL_MAP = {
    "get_data": get_data,
    "analyze_data": analyze_data,
}
```

**Step 3. 워크플로우 노드 추가**
```python
# app_mcp/graph/flow.py
def your_domain_step(state: FlowState) -> FlowState:
    result = your_logic(state["raw_data"])
    return {**state, "step_result": result}

builder.add_node("your_domain_step", your_domain_step)
builder.add_edge("validate_data", "your_domain_step")
builder.add_edge("your_domain_step", "summarize")
```

**Step 4. 스케줄러 주기 설정**
```python
# app_mcp/core/scheduler.py
scheduler.add_job(realtime_job, "interval", minutes=15)   # 주기 조정
scheduler.add_job(periodic_job, "cron", day=1, hour=0)    # cron 조정
```

**Step 5. 환경변수 설정**
```bash
cp .env.example .env
# .env 파일에 실제 값 입력
```

---

## 🏗 전체 아키텍처

```
Claude AI (MCP Client)
        │
        ▼
gateway.py (Flask, port 5000)
  └── TOOL_MAP → 도메인 Tool 함수 호출
        │
        ▼
mcp_server.py (FastAPI, port 8000)
  ├── /mcp/run         → LangGraph 워크플로우 실행
  ├── /human-review/*  → Slack 승인 웹훅 수신
  └── APScheduler
        ├── realtime_job  (interval, 15분)
        └── periodic_job  (cron, 매월 1일)
              │
              ▼
        app_mcp/graph/flow.py (LangGraph)
          load_data → validate → [도메인 노드] → summarize
          → generate_output → [Human Review] → finalize
              │
              ▼ (Human Review 시)
        Slack 승인 카드 발송
        → 담당자 클릭
        → 워크플로우 재개
```

---

## 📦 기반 프로젝트

이 템플릿은 **Koscom AI Agent Challenge 2025 대상 수상작**인  
[K-WON Risk Management AI Agent](https://github.com/dancom-MCP-AI-Agent/final_koscom_ai_agent_public)의  
인프라 레이어를 추출하여 범용화한 것입니다.

원본 구현: [report-master MCP Server](https://github.com/kxmdoyn/kwon-report-master-agent)
