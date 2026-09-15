---
title: traefik-probe-fix.sh — Probe nach dem Deploy, ohne Traefik-Neustart
scope: deploy-prod
updated: 2026-09-15
---

# traefik-probe-fix.sh

Liegt auf maxone-prod unter `/usr/local/bin/traefik-probe-fix.sh`, versioniert in maxone.one
unter `infra/prod-bin/`, Test `test/traefik-probe-fix.test.sh`. Aufgerufen am Ende der
`deploy.sh` von maxone-v2, plansey-2026, repivot, maxone-toolkit, wired-team und von
`maxone.one/scripts/deploy-world-app.sh`.

## Was es tut (seit 15.09.2026)

- Probt jede Adresse bis zu sechsmal im Abstand von fünf Sekunden (`PROBE_VERSUCHE`,
  `PROBE_WARTEN`). Ein kurzer 502 direkt nach dem Neuanlegen heilt darin.
- Bleibt eine Adresse bei 000, 502 oder 504, legt es einen Task in `vector.agent_ops_tasks` an
  (`source traefik-probe-fix`, `issue_type deploy-probe-failed`, `assigned_to vault`,
  `severity critical`), ohne Duplikat, solange derselbe Befund offen ist. Vaults Job `vault-ops`
  in `vector-green` holt ihn innerhalb von zwei Minuten.
- Endet dann mit Rückgabewert 1. Aufrufer mit `set -e` ohne `|| true` brechen ab.
- `PROBE_KONTEXT='Build, Farbe, Rückweg'` vor dem Aufruf landet im Vault-Task.
- Jeder Lauf, auch der gesunde, schreibt eine Zeile nach `/var/log/traefik-probe-fix.log`.

**Es startet Traefik nie neu** [B: maxone.one BUGS.md F-98]. Ein Neustart unterbricht jeden
Dienst hinter Traefik, nicht nur den ausgerollten. Der alte Neustart-Zweig war zudem seit Mai
tot: `curl -w '%{http_code}' ... || echo '000'` liefert bei einem Verbindungsfehler `000000`,
das kein Muster trifft. Gemessen am echten curl 8.5.0 auf NUC und maxone-prod.

## Der Fall, für den der Neustart gedacht war

Der Container hat beim Recreate eine neue IP, Traefik hält die alte, der TLS-Handshake klappt,
die Antwort kommt nie. Bestätigte Fälle: slf-kong am 27.04. und 06.05.2026, vector-blue am
19.04.2026, dort mit fehlendem `traefik.docker.network`-Label als Ursache
(`inventories/topics/vector-ops.md`). Die frühere Angabe im INDEX, das seien „95 Prozent der
Fälle", stand ohne Beleg.

**Von Hand neu starten nur, wer vorher belegt hat, dass es der Cache ist:** Container `healthy`,
im richtigen Netz mit Label, und von außen trotzdem stumm.

## Der einzige automatische Neustart: watchdog-healer

Container `watchdog-healer` auf maxone-watchdog (Repo `m1-watchdog`, `healer/healer.sh`). Probt
acht Kernadressen alle 30 Sekunden, löst nach zwei Fehlschlägen in Folge über einen
eingeschränkten Schlüssel `/usr/local/bin/watchdog-restart-traefik.sh` auf maxone-prod aus,
zehn Minuten Sperrfrist, Meldung in die Schaltzentrale.

**Stand 15.09.2026:** in 90 Tagen keine Auslösung (`docker logs watchdog-healer`), und er trägt
denselben `000000`-Fehler, ist bei Zeitüberschreitung also blind. An werkstatt gemeldet.
