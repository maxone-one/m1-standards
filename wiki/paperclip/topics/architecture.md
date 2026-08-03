---
topic: Paperclip Architektur
scope: paperclip
last_updated: 2026-05-11
---

# Paperclip — Architektur

## Was es ist

`paperclipai` (npm, MIT, v2026.403.0) ist eine **Multi-Agent-Orchestrierungsplattform**. Konzepte:
- **Company-Manifest** — Unternehmenskontext, der jedem Agenten mitgegeben wird
- **Agent-MDs** — Persona, Adapter, Modell, Skills pro Agent
- **Prompts** — System-Prompts pro Agent, versionierbar
- **CLI** — `npx paperclipai run` startet die Runtime

Aktuell läuft **ein Agent**: `vector` (CEO & Orchestrator, Adapter `claude_local`, Modell `claude-opus-4-6`). VANGUARD-Familie (Vox, Viper, Vision) noch nicht hinterlegt.

## Abgrenzung zu /opt/vector/

| | Paperclip (`/opt/paperclip/`) | Vector-Server (`/opt/vector/`) |
|---|---|---|
| Was | Agent-Runtime, Orchestrierung, Memory | Telegram-Bot, Web-Chat, Widget-API |
| URL | `paperclip.maxone.one` | `agent.maxone.one` |
| Datenbank | `paperclip-db` (Postgres 17) | Redis + Supabase |
| Status | idle seit 2026-04-13 | aktiv |

Vector *als Agent* ist in Paperclip konfiguriert — aber Vector's Chat-Frontend ist eigenständig.

## Pfade auf maxone-prod

| Pfad | Zweck |
|------|-------|
| `/opt/paperclip/app/` | npm-Setup (package.json, node_modules) |
| `/opt/paperclip/company-pkg/` | Company-Manifest + Agent-MDs — **unser Code** |
| `/opt/paperclip/prompts/` | System-Prompts pro Agent — **unser Code** |
| `/root/.paperclip/instances/default/` | Runtime: config, DB, logs, secrets — **hardcoded durch paperclipai-Paket** |
| `/opt/paperclip/sync-claude-auth.sh` | Cron: OAuth-Token root→paperclip-user kopieren |

`/root/.paperclip/` ist vom Paket hardcoded — bleibt bei Rebrand unverändert (Punkt 8 der Rebrand-Checkliste).

## Komponenten

| Komponente | Status |
|------------|--------|
| `paperclip.service` (systemd, läuft als root) | active running (seit 2026-04-18) |
| `paperclip-db` (Docker postgres:17-alpine) | up, NEVER_RESTART in local-watchdog |
| Traefik-Route `paperclip.maxone.one` | TLS DNS-01, ForwardAuth via `maxone-v2-blue:3000/api/auth/verify` |
| Cron `*/15 * * * *` sync-claude-auth | active |

## Request-Flow

```
Browser → paperclip.maxone.one
       → Traefik
       → ForwardAuth → maxone-v2-blue:3000/api/auth/verify  ← OHNE maxone-v2 kein Login
       → Backend http://10.0.1.1:3200
       → paperclipai runtime
       → paperclip-db (state)
       → claude_local Adapter → claude subprocess (CLAUDE_CODE_OAUTH_TOKEN)
```

## Modell-Anbindung (CRITICAL)

Adapter `claude_local` muss über `claude -p ...` Subprocess mit `CLAUDE_CODE_OAUTH_TOKEN` laufen — **nicht** via Anthropic API / `ANTHROPIC_API_KEY`. Status der Adapter-Implementierung: **vor Wieder-Inbetriebnahme prüfen** (globale CLAUDE.md-Regel 2026-04-20).

## Auth (zwei Ebenen)

- **Lese-Zugriff:** `PAPERCLIP_API_KEY` (in `/opt/secrets/paperclip/keys.env`)
- **Schreib-/Board-Zugriff:** `PAPERCLIP_BOARD_TOKEN`
- **UI-Login:** ForwardAuth über maxone.one → Session-Cookie
