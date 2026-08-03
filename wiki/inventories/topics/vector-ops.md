---
title: Vector Ops — Diagnose & Reparatur
scope: inventories
updated: 2026-05-31
---

# Vector Ops — Diagnose & Reparatur

## Wann nutzen

Sobald VECTOR (agent.maxone.one, Web-Chat oder Telegram) als "verschwunden" / "down" / "kaputt" gemeldet wird. VECTOR kann sich nicht selbst heilen — sofort selbst diagnostizieren.

## Diagnostic Runbook

```bash
# 1. Containerstatus
ssh -i ~/.ssh/id_ed25519 root@128.140.40.235 "docker ps --filter name=vector"

# 2. Externe Erreichbarkeit
curl -sI https://agent.maxone.one/health
curl -sI https://agent.maxone.one/widget/vector-chat.js

# 3. Traefik-Routing: Labels + Netzwerk prüfen
ssh -i ~/.ssh/id_ed25519 root@128.140.40.235 "docker inspect vector-blue | jq '.[0].NetworkSettings.Networks | keys'"

# 4. Vector-Logs
ssh -i ~/.ssh/id_ed25519 root@128.140.40.235 "docker logs vector-blue --tail 100 | grep -iE 'err|fail'"

# 5. Fix anwenden, VAULT-Task anlegen wenn noch offen
```

## Bekannter Root Cause (2026-04-19)

`vector-blue` war auf 3 Docker-Netzen (`agent-network`, `coolify`, `supabase-slf_slf-internal`), aber Traefik nur auf `coolify`. Ohne `traefik.docker.network=coolify`-Label hat Traefik ein nicht-geteiltes Netz gewählt → 504. Fix: Label in `/opt/vector/docker-compose.yml` für beide Profile (blue + green) ergänzen, Container recreaten. Danach `traefik-probe-fix.sh` ausführen.

## Nach dem Fix

VAULT-Task in `ops_tasks`-Tabelle anlegen wenn noch offene Punkte existieren (VECTOR greift es automatisch).
