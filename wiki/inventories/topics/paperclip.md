# Paperclip — Multi-Agent-Orchestrator

## Summary

Paperclip ist die orchestrierende Plattform für die 14 Agenten der
Vision-Familie (`paperclipai@2026.403.0`, MIT, eigenes Repo unter
[github.com/maxone-one/paperclip](https://github.com/maxone-one/paperclip)).
Läuft auf maxone-prod als systemd-Service unter `/opt/paperclip/`,
embedded PostgreSQL auf Port 54329, HTTP auf 127.0.0.1:3200, extern via
`paperclip.maxone.one` hinter `maxone-forward-auth`.

Dieses Topic listet die UUIDs der 14 Agenten + Company, damit man
sie nicht jedesmal aus paperclip-db ziehen muss.

## Source-of-Truth

| Schicht | Quelle | Lookup |
|---|---|---|
| DB-Wahrheit | paperclip-db (Container) | `ssh root@maxone-prod "docker exec paperclip-db psql -U paperclip -d paperclip -c 'SELECT id,name FROM agents ORDER BY name;'"` |
| Repo-Spec | `c:/Users/max/Projects/paperclip/company-pkg/agents/<slug>.md` | lokal |
| Live-Instructions | `/root/.paperclip/instances/default/companies/<co-uuid>/agents/<agent-uuid>/instructions/AGENTS.md` | SSH |
| System-Prompts | `c:/Users/max/Projects/vector/knowledge/character-prompts/PROMPT-<NAME>.md` (SSoT) → `c:/Users/max/Projects/paperclip/prompts/PROMPT-<NAME>.md` (gespiegelt) → `/opt/paperclip/prompts/PROMPT-<NAME>.md` (Prod) | s.o. |

## Company

| Feld | Wert |
|---|---|
| Company-UUID | `c5852825-aaaa-4e30-bb9f-2ced0c85e7d6` |
| Company-Pkg | `c:/Users/max/Projects/paperclip/company-pkg/COMPANY.md` |

## Agent-UUIDs (alle 14)

Stand: 2026-05-11. Adapter `claude_local`, Modell `claude-opus-4-7`,
Instructions-Bundle-Mode `managed`.

| Name | UUID | Rolle |
|---|---|---|
| VECTOR | `097989ce-b845-4615-a367-37662e01727d` | CEO & Orchestrator |
| VALOR | `b16d3da5-51d1-416a-82dc-a94ee8d69c6e` | Sales / Setter-Opener-Closer |
| VANTAGE | `88d06cbc-6063-4028-8dfc-b59d8445464c` | CMO — Positionierung, Messaging |
| VAULT | `94a57cae-5d37-4d30-8985-a464321666d0` | CTO — Backend, APIs, Security |
| VEGA | `ca19011a-25d6-41b5-ae4a-854570a888b6` | Video Production |
| VERA | `658e066a-e4f9-4645-a29b-2c6042e758d6` | KI-Telefonassistentin |
| VIGIL | `4d84d4b2-7a3c-4a27-a593-7245f1315756` | COO — Inbox-Türsteher |
| VIKTORIA | `4414cd4a-ec86-43fc-b9ce-ad96f90ac909` | Head of HR + Fotografie |
| VIPER | `3a37ee3e-94b2-4f06-9b34-5b98c7326190` | Head of Finance |
| VISOR | `8d61020d-50f3-439f-8cc1-8fc4e306287a` | QA Engineer |
| VISTA | `e9781fa3-1f47-4320-95d9-8e2df9d17fa9` | CDO / Frontend |
| VORTEX | `0173b99e-6c69-47d3-a751-3e5966991195` | Lead-Generierung / Outreach |
| VOX | `18e90a4b-9dd1-4b1e-b303-1379e4aaf90d` | Strategic Observer |
| VYBORA | `cc788c8d-642e-4a5c-9a4e-170ccc085599` | KI-Coding-Mitarbeiterin (Kunden) |

## Service & Infra

| Feld | Wert |
|---|---|
| Service | `systemctl {status,restart,stop,start} paperclip` |
| Working-Dir Prod | `/opt/paperclip/` (Git-Working-Tree seit 2026-05-11) |
| Remote | `https://github.com/maxone-one/paperclip.git` |
| HTTP intern | `http://127.0.0.1:3200` |
| HTTP extern | `https://paperclip.maxone.one/` (hinter `maxone-forward-auth`) |
| Embedded Postgres | `127.0.0.1:54329` (lokal in `/root/.paperclip/instances/default/db`) |
| User | `paperclip:paperclip` |
| Adapter | `claude_local` (CLI-Subprocess via `CLAUDE_CODE_OAUTH_TOKEN`) |

## Operational Patterns

### Neuer Agent
1. `c:/Users/max/Projects/vector/knowledge/character-prompts/PROMPT-<NAME>.md` schreiben (SSoT)
2. `cp` nach `c:/Users/max/Projects/paperclip/prompts/`
3. `c:/Users/max/Projects/paperclip/company-pkg/agents/<slug>.md` mit Frontmatter (siehe paperclip/CLAUDE.md)
4. Commit + Push beide Repos
5. Prod: `cd /opt/paperclip && git pull --ff-only`
6. `chown -R paperclip:paperclip /opt/paperclip/company-pkg /opt/paperclip/prompts`
7. INSERT-Row + managed-instructions-Setup in paperclip-db (Pattern siehe bestehende Agents)
8. `systemctl restart paperclip`

### Prompt-Update bestehender Agent
1. character-prompts SSoT editieren
2. `cp` nach paperclip/prompts/
3. Commit + Push beide Repos
4. Prod: `git pull --ff-only` — der `post-merge`-Hook (seit 2026-05-11)
   spiegelt AGENTS.md, setzt chown, restartet paperclip automatisch.
   Manueller `cp`-Schritt entfaellt.

### DB-Inspektion
```bash
ssh root@maxone-prod "docker exec paperclip-db psql -U paperclip -d paperclip -c 'SELECT name, adapter_config FROM agents ORDER BY name;'"
```

## Architektur-Lücken

- Kein End-to-End-Smoke-Test im Repo. Manuelle UI-Validierung pro Agent.
- `paperclip.maxone.one` hängt an `maxone-forward-auth` (geteilte
  maxone-Session). Direkter Zugriff ohne maxone-Login = 401.

## Behoben

- 2026-05-11: AGENTS.md-Sync nicht mehr manuell. `post-merge`-Hook in
  `/opt/paperclip/.git/hooks/post-merge` ruft
  `scripts/sync-managed-instructions.sh` (idempotent, DB-driven, restartet
  nur bei tatsaechlicher Aenderung). Installer:
  `scripts/install-hooks.sh`.

## Sources

- [[c:/Users/max/Projects/paperclip/CLAUDE.md]] — Repo-Einstieg, Anti-Drift-Regeln
- [[c:/Users/max/Projects/paperclip/README.md]] — Pfad-Doku, Deploy
- [[c:/Users/max/Projects/paperclip/HANDOFF.md]] — Briefing
- [[c:/Users/max/Projects/vector/IDENTITY.md]] — "Ein Vector, überall"-Regel
- [[c:/Users/max/Projects/vector/knowledge/character-prompts/]] — SSoT aller Vision-Familie-Prompts
- Traefik: `/opt/traefik/dynamic/paperclip.yaml` auf maxone-prod
