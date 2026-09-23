# Backend — Prompt Injection Firewall

FastAPI backend + firewall core + LangGraph agent.

## Structure (layered)
```
app/
├── main.py            # FastAPI entry point
├── core/config.py     # settings / env
├── api/routes/        # HTTP endpoints (health, scan, agent, logs)
├── services/          # orchestration (no AI logic)
├── domain/            # the CORE
│   ├── firewall/      # detectors + engine + neutralizer
│   └── agents/        # LangGraph agent + tools
├── infrastructure/    # ChromaDB, LLM client, OCR
└── schemas.py         # request/response models
```

## Setup
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run
```powershell
uvicorn app.main:app --reload --port 8000
```
- API docs: http://localhost:8000/docs
- Health:   http://localhost:8000/health
