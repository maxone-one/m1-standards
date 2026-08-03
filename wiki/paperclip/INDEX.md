---
scope: paperclip
summary: Multi-Agent-Orchestrator-Plattform (Codename pending). Hostet Vector + künftig VANGUARD-Familie.
last_updated: 2026-05-11
---

# Wiki — Paperclip (Codename pending)

## Wann diese Wiki nutzen

- Fragen zu "Was ist Paperclip?", "Wie starte/deploye ich Paperclip?"
- Vor Arbeit an `/opt/paperclip/` auf maxone-prod
- Rebrand-Planung (Codename noch offen)
- Agents hinzufügen / company-Manifest bearbeiten

**NICHT hier:** Vector-Web-Chat (`agent.maxone.one`) und Telegram-Bot leben in `/opt/vector/` — das ist NICHT Paperclip. Nur weil Vector *in* Paperclip als Agent läuft, heißt das nicht, dass `/opt/vector/` zu Paperclip gehört.

## Topics

- [architecture.md](topics/architecture.md) — Komponenten, Pfade, Wer redet mit wem, Modell-Anbindung
- [ops.md](topics/ops.md) — Start/Stop, Logs, DB-Backup, Rebrand-Checkliste, bekannte Eigenheiten

## Quellen

- HANDOFF auf Server: `ssh root@128.140.40.235 "cat /opt/paperclip/HANDOFF.md"`
- Source lokal: `c:\Users\max\Projects\paperclip-source\`
- GitHub (OSS, MIT): https://github.com/paperclipai/paperclip (~60k Stars)
