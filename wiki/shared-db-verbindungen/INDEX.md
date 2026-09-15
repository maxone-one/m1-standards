---
title: shared-db-verbindungen
description: Jahresarchiv aller Anmeldungen an shared-db auf maxone-prod. Wo es liegt, wie man darin sucht, woran man sieht, ob es läuft
---

# shared-db-verbindungen

Stand 15.09.2026, angelegt von `werkstatt-2975` nach dem Vorfall F-112 (werkstatt
`bugs/F-112-outreach-ui-befallen-und-ohne-anmeldung-leads-offengelegt.md`). Quelltext, Units und
Prüfstück: werkstatt `server/shared-db-verbindungen/`, Konzept
`.planning/CONCEPT-shared-db-verbindungsprotokoll.md`.

## Was es ist

**Postgres in `shared-db` protokolliert seit 15.09.2026 17:12 MESZ jede Verbindung**
(`log_connections = on` per `ALTER SYSTEM`, steht in `postgresql.auto.conf`). Das Docker-Log hält
davon nur vier bis fünf Tage. **Ein Timer holt die Zeilen alle 15 Minuten in eine Datei je
UTC-Tag** und bewahrt sie 365 Tage auf.

| | |
|---|---|
| Skript | `/opt/shared-db-verbindungen/abholen.py` |
| Units | `/etc/systemd/system/shared-db-verbindungen.service` und `.timer` |
| Archiv | `/var/log/shared-db-verbindungen/JJJJ-MM-TT.log`, Vortage als `.log.gz` |
| Marken | `.marke` (letzte gelesene Zeile), `.letzte-verbindung` |
| Optional | `/opt/shared-db-verbindungen/abholen.env` mit `KUMA_PUSH_URL` |

Behalten werden Zeilen mit `connection received` (Absenderadresse), `connection authorized`
(Nutzer, Datenbank, Anwendung), `authentication failed`, `no pg_hba.conf entry` und `FATAL`.
**Beide Zeilen einer Verbindung tragen dieselbe Prozessnummer in eckigen Klammern**, darüber
gehören Adresse und Nutzer zusammen.

## Suchen

Alle Anmeldungen von einer Adresse, hier `outreach-ui` im Netz `outreach_outreach-internal`:

```bash
ssh maxone-prod 'zgrep -h "host=10.0.11.5" /var/log/shared-db-verbindungen/*'
```

Alle abgewiesenen Anmeldungen:

```bash
ssh maxone-prod 'zgrep -h -E "authentication failed|no pg_hba.conf entry" /var/log/shared-db-verbindungen/*'
```

**Welche Adresse zu welchem Container gehört, steht nicht im Archiv**, und beim Neuerstellen
eines Containers kann sie wechseln. Die heutige Zuordnung eines Netzes:

```bash
ssh maxone-prod 'docker network inspect outreach_outreach-internal -f "{{range .Containers}}{{.Name}} {{.IPv4Address}}{{println}}{{end}}"'
```

## Läuft es?

```bash
ssh maxone-prod 'systemctl list-timers shared-db-verbindungen.timer; journalctl -u shared-db-verbindungen.service -n 5 --no-pager -o cat'
```

Ein Lauf endet mit `OK: … Zeilen neu, davon … Verbindungen`. Rückgabe 2 heißt Docker oder Marke
unlesbar. Rückgabe 3 ist ein `BEFUND`: zehn Minuten ohne jede Verbindungszeile. Dann zuerst
nachsehen, ob das Protokoll noch an ist:

```bash
ssh maxone-prod 'docker exec shared-db psql -U postgres -Atc "SHOW log_connections"'
```

**Einen Alarm gibt es noch nicht.** Kein Kuma-Push-Monitor ist eingetragen, und Telegram sendet
laut werkstatt-HANDOFF seit 22.08.2026 nicht. Ein Ausfall zeigt sich nur in `systemctl --failed`.

Ein Lauf von Hand ins echte Archiv ist unschädlich, Sperre und Marke verhindern Doppeltes:

```bash
ssh maxone-prod 'systemctl start shared-db-verbindungen.service'
```

## Fallen

- **`POSTGRES_USER` ist in `shared-db` nicht gesetzt.** `psql` ohne `-U postgres` versucht es als
  `root` und hinterlässt `FATAL: role "root" does not exist` im Log und damit im Archiv.
- **Die Zähler in `pg_stat_*` gelten ab ihrem letzten Reset, nicht ab dem Serverstart.** Beim
  Absturz am 08.09.2026 um 18:40 UTC gingen sie verloren, ablesbar in
  `pg_stat_bgwriter.stats_reset`.
- `docker logs --since` zeigt laut Doku Einträge „nach" dem Zeitpunkt, ohne zu sagen, ob
  einschließlich. Das Skript verwirft deshalb alles, was nicht jünger als die Marke ist.
- **Das Docker-Log von `shared-db` vor dem 15.09.2026 17:12** (ab 09.08., ohne
  Verbindungszeilen) liegt als Sicherung auf dem NUC unter
  `~/Sicherungen/outreach-vorfall-2026-09-15/`, nicht im Archiv.

## Abschalten

Nur das Archiv anhalten, die Dateien bleiben liegen:

```bash
ssh maxone-prod 'systemctl disable --now shared-db-verbindungen.timer'
```

Das Protokoll in Postgres selbst wieder ausschalten, ohne Neustart:

```bash
ssh maxone-prod 'docker exec shared-db psql -U postgres -c "ALTER SYSTEM RESET log_connections" -c "SELECT pg_reload_conf()"'
```
