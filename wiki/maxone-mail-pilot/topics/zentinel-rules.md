---
topic: zentinel-rules
last_compiled: 2026-07-29
source_count: 2
status: active
---

> **Teil-Nachzug 2026-07-29:** nur Regel 27 aus der Bibel ergänzt (F-61). Die
> Regeln 25 und 26 der Bibel fehlen in dieser Liste weiterhin, ein voller
> Neu-Kompilat steht aus. Bei Widerspruch gewinnt die Bibel.

# Zentinel/Stalwart Rules

## Summary [coverage: high -- 2 sources]

Sources span 2026-03 bis 2026-05, Stand Bibel `Last updated: 2026-05-22`. 24 unverhandelbare Regeln aus echten Outages auf maxone-prod (24.03., 05.04., 10.04., 28.04., 16.05., 21.05.2026). Jeder Verstoß kostet Zeit, Vertrauen oder Geld. Diese Liste ist kein Style-Guide — sie ist Disziplin. Wer an Zentinel, Stalwart oder `email-client` arbeitet, liest sie zuerst. Stand: 2026-05-22, alle 24 Regeln implementiert.

## Architecture [coverage: medium -- 1 source]

Die Regeln gruppieren sich in **drei Klassen**:

1. **Niemals-Regeln (Verbote)** — Operationen, die Stalwart oder Brevo in einen kaputten Zustand bringen.
2. **Immer-Regeln (Pflichten)** — Operationen, die jeder Eingriff machen MUSS (Health-Checks, korrekte Hostnames, container-loopback).
3. **Code-Regeln (Implementierungs-Pflicht)** — bestimmte Code-Patterns (`{accountId}`-Substitution, `disposition`-Filter, Domain-Preflight).

Die volle Architektur, in der diese Regeln greifen: [[mail-architecture]].

## Key Rules [coverage: high -- 2 sources]

### Verbote (Niemals)

- **Regel 1** — Niemals `docker run` gegen Stalwart auf Prod. Erzeugt Orphans, lockt RocksDB. Immer `docker compose` oder `docker exec stalwart-mail …`.
- **Regel 2** — Niemals Credentials im Klartext in CLI-Befehlen (kein `curl -u user:pass`, kein `docker exec -e KEY=VAL` mit Geheimnissen). Aus `/opt/secrets/<projekt>/keys.env` laden — siehe [[secrets-tls]].
- **Regel 3** — Niemals Passwörter ungefragt ändern. Erst Max fragen, dann das volle Rotations-Protokoll: Store → alle .env → `--force-recreate` → JEDEN Endpunkt testen → Drive-Backup → Vector informieren.
- **Regel 4** — Niemals Health-Checks mit Fake-Credentials. Stalwart bannt eine IP nach **2** fehlgeschlagenen Auth-Versuchen. `Basic healthcheck:invalid` triggert Auto-Ban. Health-Check ohne Authorization-Header (`fetch('http://stalwart-mail:8080/jmap/session')`) oder mit echten Credentials.
- **Regel 5** — Niemals einen Recovery-Pfad benutzen, der selbst gebannt werden kann. Bei Recovery NIE vom Host gegen `http://stalwart-mail:8080/api/...` curlen — die Bridge-Gateway-IP landet im selben Auto-Ban. Stattdessen `docker exec stalwart-mail stalwart-cli -u http://localhost:8080`.
- **Regel 6** — Niemals `reload-config` als Heilung für blocked-ip glauben. Stalwart cached den Auto-Ban im Speicher. Nach `delete-config 'server.blocked-ip.<IP>'` IMMER `docker restart stalwart-mail`.
- **Regel 7** — Niemals RocksDB und `config.toml` verwechseln. Wenn ein User in der RocksDB existiert, ignoriert Stalwart `config.toml`. `fallback-admin` greift nur wenn der User NICHT in der DB ist. Passwortwechsel über `stalwart-cli`, nicht in der Config-Datei.
- **Regel 8** — Niemals `--console` in Stalwart v0.15.x. Crasht mit Rust-Panic. Nur `server list-config` / `add-config` / `delete-config`.
- **Regel 9** — Niemals `SUPABASE_SERVICE_ROLE_KEY` rotieren ohne Migration-Playbook. `jmap_password` in `maxone.email_accounts` ist mit dem Key AES-GCM-verschlüsselt. Rotation ohne Re-Encrypt killt **alle** Mail-Konten gleichzeitig.
- **Regel 10** — Niemals blind Schleifen drehen. Nach 2 Versuchen ohne Lösung: STOP, recherchieren, dann handeln.
- **Regel 11** — Niemals Brevo SMTP-Keys teilen. Jedes Projekt eigener Brevo-Account, eigener Key.
- **Regel 17** — Niemals Live-Edge-Function-Datei auf dem Server editieren. Repo-Edit → Commit → CI-Deploy. Direkt-Edits in `/opt/supabase/docker/volumes/functions/*/index.ts` werden beim nächsten Deploy überschrieben.

### Pflichten (Immer)

- **Regel 12** — Neue Domain MUSS am selben Tag in Brevo authentifiziert werden. Sonst werden ausgehende Mails stillschweigend verworfen — Stalwart hat keine Spur, keine Sent-Kopie. Allein Disziplin reicht nicht: Regel 20 erzwingt das programmatisch.
- **Regel 13** — Niemals `jq`-Filter ohne echtes Sample-Payload committen. Stalwart liefert `.data.items` als **Map** (nicht Array). Korrekt: `.data.items | keys[]`, nicht `.data.items[]? | .key`.
- **Regel 14** — Immer `/jmap/session` direkt — nie `/.well-known/jmap` (307-Redirect, Deno-fetch folgt unzuverlässig).
- **Regel 15** — Immer interne Hostnames aus dem Edge-Runtime: `stalwart-mail:8080`, nie Public-URL. Public = TLS-Handshake = mehr Failure-Modi = Self-Ban-Risiko.
- **Regel 16** — Immer Orphan-Check nach `docker run`: `docker ps -a --filter ancestor=stalwartlabs/stalwart`. Alles außer `stalwart-mail` sofort `docker rm`.
- **Regel 18** — Bei jedem Stalwart-Touch `zentinel-health` vor und nach prüfen. Erwartet: `healthy=true, failedCount=0, primaryError=null`.

### Code-Patterns (Implementierungs-Pflicht)

- **Regel 19** ✅ — JMAP `uploadUrl` muss `{accountId}` ENTHALTEN, nicht weg-gestripped werden. Beim Host-Rewrite Template-Segment behalten und in `uploadBlob()` ersetzen. **Falsch:** `session.uploadUrl.split("{")[0]` → Blob landet in Default-Account `"a"`, Stalwart antwortet 200 ohne Side-Effect, Sent-Ordner bleibt leer (silent black hole — siehe [[../concepts/silent-failures]]).
- **Regel 20** ✅ — Brevo-Domain-Preflight VOR jedem Send: `GET /v3/senders/domains`, prüfe `authenticated:true && verified:true`. Cache 24h pro Domain, fail-open bei Brevo-API-Outage. Bei fehlender Auth: `status='rejected_unauthenticated_domain'` setzen, NICHT `'sent'`.
- **Regel 21** ✅ — Attachment-Filter: `!(a.cid && a.disposition !== 'attachment')`. `cid` allein bedeutet NICHT Inline-Image (Gmail hängt `cid` RFC-konform auch an echte Attachments). Inline = `cid` UND `disposition !== "attachment"`. Echte Anhänge mit `cid` MÜSSEN sichtbar bleiben.
- **Regel 22** ✅ — Blue/Green-Swap ist ERST FERTIG, wenn der inaktive Slot gestoppt ist. Auf maxone-prod läuft Traefik standalone — beide Slot-Router haben dieselbe Rule, ohne `docker stop` macht Traefik Round-Robin und User sieht den Fix mal/mal nicht. Reihenfolge: neuen Slot bauen → healthy warten → Health-Check direkt → **`docker stop` alter Slot** → `docker ps`-Verifikation.
- **Regel 27** ✅ (2026-07-29, F-61) — **JMAP liefert Message-IDs OHNE spitze Klammern, `maxone.sent_emails.message_id` speichert sie MIT.** RFC 8621 `asMessageIds`: „surrounding angle brackets ('<>') are removed". Jeder Vergleich normalisiert beide Seiten oder fragt beide Schreibweisen ab, sonst trifft er nie. Gilt für jede Zuordnung über Kennungen (Empfangsbestätigung, Thread-Bildung, Zustellungs-Abgleich). **Zwei Lehrsätze am selben Fall:** (1) eine Kennzahl, die dauerhaft auf null steht, ist erst dann ein Defekt, wenn belegt ist, dass überhaupt je etwas hätte gezählt werden können (hier wurde nie eine Bestätigung angefordert, der Vergleich lief also nie); (2) eine Fehlermeldung nennt die Schicht, in der sie ausgesprochen wird, nicht die, in der der Fehler liegt (`Account not found` klang nach Stalwart und war eine Datenbankzeile aus `getJmapClient`, das selbst auf `is_active` filtert). Handler, die über Konten schleifen, filtern an der Quelle auf `is_active`.
- **Regel 23** ✅ — Mailbox-Passwortänderung MUSS alle abhängigen Stores synchronisieren. Stalwart RocksDB + `maxone.email_accounts` (AES-GCM-verschlüsselt) + aktive SnappyMail-Sessions. Sonst triggert der MDN-Checker (IP `10.0.2.3`, läuft alle 3 Min) mit dem alten Passwort einen endlosen Ban-Zyklus. Endpunkte ohne Sync-Mechanismus MÜSSEN `warning`-Feld in HTTP-Response zurückgeben. Siehe Standard 016.

### Infrastruktur-Pflichten (Container/Host)

- **Regel 24** ✅ — Stalwart MUSS `mem_limit` haben, der Host darf NIE `swapoff -a` unter Druck machen. `/opt/stalwart/docker-compose.yml` (Repo: `ops/stalwart/docker-compose.yml`): `mem_limit: 512m`, `mem_reservation: 256m`. Idle ~172 MB → 3x Headroom. `/opt/swap-guard.sh` v2 droppt nur Caches + restartet Kongs — kein `swapoff` mehr, weil das unter RAM-Druck globalen OOM-Killer triggert (Kernel zieht Swap-Inhalt zurück in bereits volles RAM). Standard 028 verlangt `mem_limit` für ALLE Container — Sweep mit `docker ps -q | xargs -n1 docker inspect --format '{{.Name}} {{.HostConfig.Memory}}'`, Zeilen mit `0` sind Verletzungen. Manuell via `docker run` gestartete Container (z.B. `paperclip-db`): `docker update --memory` runtime + systemd-Override mit `ExecStartPost` für Persistenz.

## Notable Failures [coverage: low -- 1 source]

Jede Regel kommt aus einem konkreten Vorfall — die volle Postmortem-Liste lebt in [[failure-modes]]. Mapping Regel → Vorfall:

- Regeln 1, 2, 3, 7, 8, 10 → **2026-03-24 Stalwart Admin Lockout**
- Regeln 4, 5, 6, 13, 18 → **2026-04-05 Self-Inflicted Fail2Ban Loop**
- Regeln 12, 17, 19, 20 → **2026-04-10 Sent-Items-Blackhole + Brevo Silent Rejection**
- Regeln 21, 22 → **2026-04-28 Unsichtbarer Anhang + Blue/Green Split-Brain**
- Regel 23 → **2026-05-16 Mailbox-Passwort-Desync (hey@viktoria-from.de)**
- Regel 24 → **2026-05-21 Globaler OOM-Storm (swap-guard + ungecapptes Stalwart)**

## Operational Patterns [coverage: medium -- 2 sources]

**Sicherheits-Checkliste vor JEDEM Stalwart/Zentinel-Eingriff:**

- Bibel + ZENTINEL-KNOWLEDGE-BASE.md gelesen?
- `zentinel-health` JETZT geprüft? Ausgangszustand?
- `docker run` geplant? → STOP, geht es ohne?
- Credentials in CLI? → STOP, aus `/opt/secrets/` laden.
- Health-Check mit Auth-Header? → STOP, ohne Auth.
- Vom Host gegen `stalwart-mail:8080` curlen? → STOP, container-loopback.
- `reload-config` als Fix für blocked-ip? → STOP, `delete-config` + `docker restart`.
- Passwort ändern? → STOP, erst Max fragen.
- Plan B nach 2 Fehlversuchen?
- `zentinel-health` NACH dem Eingriff prüfen?
- Vector informieren?

Wenn auch nur ein Punkt unklar: nicht handeln, Max fragen.

**Verbotene Befehle** (Auszug, volle Liste in der Bibel Sektion II):

- `docker run --rm stalwartlabs/stalwart …`
- `curl -u 'user:pass' http://stalwart-mail:8080/...` (vom Host)
- `curl … -H "Authorization: Basic <fake>"` gegen Stalwart
- `stalwart-cli reload-config` (allein als Heilung für blocked-ip)
- `stalwart-cli --console …`
- `delete-config 'server.blocked-ip.*'` (Wildcard wird nicht unterstützt)
- `docker compose up --build` auf Prod
- `git reset --hard` / `git clean -fd` auf `/opt/vector`

**Erlaubte Recovery-Patterns** siehe [[mail-architecture#operational-patterns]].

## Sources

- [[../../briefings/ZENTINEL-STALWART-BIBEL]] — Regeln 1-22 mit Lehren, Vorfälle I-IV, Sicherheits-Checkliste V
- `~/.claude/CLAUDE.md` — Sektion "Stalwart-Fehler Lehren (GLOBALE REGEL — NIE WIEDER!)" + "Zentinel/Stalwart/Mail: Bibel ist Pflicht"
