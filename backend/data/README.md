# Sample sources (Way 2 demo)

`sample_sources/` holds example files the autonomous agent can fetch and scan.
Some are safe, some contain prompt-injection attacks in realistic places.

| File | Kind | Expected verdict |
|---|---|---|
| `email_safe.eml` | normal email | ✅ SAFE |
| `email_malicious.eml` | obvious injection (ignore-previous + steal credentials) | 🚫 BLOCKED |
| `meeting_notes.txt` | normal notes | ✅ SAFE |
| `support_ticket.txt` | instruction hidden in a support ticket | 🚫 BLOCKED |
| `product_page.html` | injection hidden in an invisible `<div>` | 🚫 BLOCKED |
| `deploy_script.py` | injection hidden in a code comment | 🚫 BLOCKED |

The `POST /api/agent/run` endpoint uses this folder automatically when no
sources are given, so the demo works with a single click.
