# prompt-injection-firewall

An AI-powered firewall that sits in front of an AI agent, scans all incoming
content, and blocks malicious prompt injections while letting safe content pass.

**Hackathon:** ET AI Hackathon 2026 — Agentic Edition (Presented by Accenture)
**Problem Statement:** Problem 2 — Agentic Cybersecurity: Prompt Injection Firewall

## Structure
- `frontend/` — React UI (Presentation layer)
  - Mode A (Way 1): chat / upload — manual
  - Mode B (Way 2): "Run Agent" dashboard — automatic
- `backend/` — FastAPI + firewall core + LangGraph agent

## Stack
React · FastAPI · LangGraph (Python) · ChromaDB (local) · LLM · GitHub

## Two ways it works
- **Way 1 (Manual):** user pastes/uploads content → firewall checks → safe passes, malicious is blocked.
- **Way 2 (Automatic):** agent fetches content (web/email/API/files) → firewall auto-scans → dashboard shows results.
