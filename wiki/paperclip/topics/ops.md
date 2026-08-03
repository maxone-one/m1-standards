---
topic: Paperclip Ops
scope: paperclip
last_updated: 2026-05-11
---

# Paperclip — Ops

## Status prüfen

```bash
ssh -i ~/.ssh/id_ed25519 root@128.140.40.235 "systemctl status paperclip.service"
ssh -i ~/.ssh/id_ed25519 root@128.140.40.235 "docker ps --filter name=paperclip-db"
ssh -i ~/.ssh/id_ed25519 root@128.140.40.235 "journalctl -u paperclip.service --since '1h ago' | tail -30"
```

## Start / Stop

```bash
# Starten
systemctl start paperclip.service

# Stoppen (DB separat — NEVER_RESTART gilt für DB, nicht App)
systemctl stop paperclip.service

# Nur DB neustarten
docker restart paperclip-db
```

## Aktueller Stand (2026-05-11)

- **Idle seit 2026-04-13** — kein User-Traffic, stuendliche DB-Backups (287 KB = leere DB)
- **Service läuft** (Node-Prozess seit 2026-04-18 aktiv)
- **Kein Monitoring** in Uptime-Kuma (paperclip-db ist in local-watchdog, paperclip-app NICHT)
- **Codename PENDING** — Rebrand-Name von Max ausstehend

## Bekannte Eigenheiten

- systemd-Service läuft als `root`, Cron-Skript dann als `paperclip:paperclip` — Inkonsistenz, sollte `User=paperclip` in ExecStart
- Ohne laufendes `maxone-v2-blue` ist der UI-Login gesperrt (ForwardAuth-Abhängigkeit)
- Agent-Pfade in `/root/.paperclip/` sind vom npm-Paket hardcoded — nicht umziehbar

## Rebrand-Checkliste (wenn Max den Namen festlegt)

1. `/opt/paperclip/` → `/opt/<name>/` (mv + Service-Unit anpassen)
2. `paperclip-db` Container → `<name>-db` (recreate mit altem Volume)
3. Postgres intern: `ALTER DATABASE paperclip RENAME TO <name>;`
4. `paperclip.service` → `<name>.service` + `DATABASE_URL` anpassen
5. Traefik-Route `paperclip.maxone.one` → `<name>.maxone.one` (DNS-Record neu)
6. local-watchdog NEVER_RESTART_REGEX: `<name>-db` ergänzen, alten entfernen
7. Cron-Pfad `/opt/paperclip/sync-claude-auth.sh` anpassen
8. **NICHT ändern:** `/root/.paperclip/` — vom paperclipai-Paket hardcoded
9. Memory-Eintrag anlegen mit `former_name: paperclip`

## Agent hinzufügen (VANGUARD-Familie)

Neue Agent-MD anlegen unter `/opt/paperclip/company-pkg/agents/<V-NAME>.md` nach dem Muster von `vector.md`. Adapter `claude_local` verwenden. Dann `systemctl restart paperclip.service`.

## Secrets-Ort

`/opt/secrets/paperclip/keys.env` auf maxone-prod (700/600, nur root).
