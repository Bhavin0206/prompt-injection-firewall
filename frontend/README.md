# Frontend — Prompt Injection Firewall

React UI for the **Prompt Injection Firewall** (ET AI Hackathon 2026 — Agentic Edition, Problem 2).

This app lets a user paste or upload content and see whether the firewall marks it
**SAFE** ✅ or **BLOCKED** 🚫, with a clear reason.

> **Scope today:** **Mode A — Manual (Way 1)** is built.
> **Mode B — Agent (Way 2)** comes later and is shown as a placeholder in the header.

---

## Tech Stack

- **React 19** + **Vite 8**
- **CSS Modules** for component-scoped styles
- **React Context** for the dark/light theme
- **pdfjs-dist** — reads text out of PDFs in the browser
- **Tailwind CSS** (available for utility styling)

---

## What it can do (Mode A)

- Paste text, email, source code, or log output
- Upload a file (PDF, `.eml`, text, source code) — read **in the browser**, never uploaded
- One-click demo samples (a SAFE example and a MALICIOUS example)
- Color-coded verdict: **SAFE** (green) / **BLOCKED** (red) with attack type, reason, confidence
- Scan history log
- Dark / light theme toggle (remembered on reload)

---

## Getting Started

```bash
# from the frontend folder
npm install
npm run dev
```

Open **http://localhost:5173**.

### Scripts

| Command | What it does |
|---|---|
| `npm run dev` | Start the dev server (hot reload) |
| `npm run build` | Production build into `dist/` |
| `npm run preview` | Preview the production build |
| `npm run lint` | Lint with oxlint |

---

## Configuration

Copy `.env.example` to `.env` if you need to change the backend URL:

```
VITE_API_BASE_URL=http://localhost:8000
```

---

## Project Structure

```
src/
├── components/
│   ├── common/      # Button, Card, Badge, Spinner, TextArea
│   └── layout/      # Header, PageLayout
├── features/
│   └── scan/        # Mode A (Way 1)
│       ├── api/     # scanApi + mockScan
│       ├── components/  # ScanInput, FileUpload, SampleButtons, VerdictCard, ScanLog
│       ├── data/    # demo samples
│       └── hooks/   # useScan
├── pages/           # ScanPage
├── services/        # apiClient (talks to the backend)
├── context/         # ThemeContext
├── config/          # env/config
├── utils/           # constants, file reading
└── styles/          # global theme + CSS variables
```

---

## Notes

- The UI currently uses a **mock scan** (`features/scan/api/mockScan.js`) so it works
  before the backend exists. Swap it for the real `POST /scan` when the backend is ready.
- Mode B (Agent) is a placeholder until its UI is built.
