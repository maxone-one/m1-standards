---
topic: mail-architecture
last_compiled: 2026-05-27
source_count: 5
status: active
---

# Mail Architecture (maxone)

## Summary [coverage: high -- 4 sources]

Sources span 2026-03 to 2026-04. Recent consensus (alle Einträge <3mo, frisch).

**Warum Brevo überhaupt (Grundlage):** Hetzner sperrt **ausgehenden Port 25** auf den Cloud-Servern (verifiziert 2026-05-29). Stalwart kann daher Mail **nicht** direkt an Empfänger-MX zustellen — das ist die ursprüngliche, harte Veranlassung für Brevo als Outbound, nicht Komfort. Konsequenz: **alles**, was Stalwart selbst verschickt (z.B. Sieve `vacation` / Auto-Reply), braucht einen **Brevo-Smarthost-Relay** (`smtp-relay.brevo.com:587`), sonst hängt es still in der Queue. Auto-Reply lieferte 2026-05-29 extern nicht aus, genau aus diesem Grund (Smarthost noch nicht konfiguriert). Details: Bibel Regel 25.

maxone hat **eine geteilte Mail-Pipeline**: Outbound geht über **Brevo** (`api.brevo.com/v3/smtp/email`), Inbound und der **Sent-Folder** liegen in **Stalwart** (JMAP). Beide werden von einer einzigen Supabase Edge Function namens `email-client` orchestriert. Stalwart-Logs zeigen daher **niemals** ausgehende Zentinel-Mails — wer "hat X meine Mail bekommen?" untersucht, fragt zuerst die Brevo Events API, nicht Stalwart. Zentinel selbst ist kein eigener Container, sondern die Route `/admin/email` in den `maxone-v2-blue/green` Containern auf `maxone-prod`. Cross-cutting: viele Failure-Modi der Pipeline sind **silent** (200 OK ohne Side-Effect, `event=error` nach `messageId`, RocksDB-vs-Config-Präzedenz) — siehe [[../concepts/silent-failures]].

## Architecture [coverage: high -- 3 sources]

**Container und ihre Rollen** (Server: `maxone-prod`, `128.140.40.235`):

| Komponente | Container | Rolle |
|---|---|---|
| Outbound-Send | (kein Container — Brevo-API) | `api.brevo.com/v3/smtp/email` — pro Projekt eigener API-Key |
| Inbound + Sent-Folder | `stalwart-mail` | JMAP-Server, RocksDB als interner Store |
| Send-Code | `supabase-edge-functions` | Edge Function `email-client`, Pfad `/home/deno/functions/email-client/` |
| Zentinel-UI | `maxone-v2-blue` / `maxone-v2-green` | Route `/admin/email` (kein eigener Container) |
| Health-Watchdog | Edge Function `zentinel-health` | Reach-Check + Alarmierung |

**Send-Pipeline** (Repo: `maxone.one/supabase/functions/email-client/handlers/send.ts`):

1. **Brevo-Domain-Preflight** ([[zentinel-rules#regel-20]]) — prüfe `GET /v3/senders/domains`, dass `domain_name` mit `authenticated:true && verified:true` enthalten ist. Cache 24h pro Domain. Fail-open bei Brevo-Outage.
2. **Brevo-Send** — `POST /v3/smtp/email`. Bei Erfolg liefert Brevo eine `messageId`.
3. **JMAP Sent-Copy** — Blob-Upload via `uploadUrl` ([[zentinel-rules#regel-19]] — `{accountId}` Template muss erhalten bleiben), dann `Email/import`.
4. **Tracking** — Eintrag in `maxone.sent_emails` mit Status `sent` (oder `rejected_unauthenticated_domain` wenn Preflight failt).

**JMAP-Adressierung** (kritisch für Edge-Functions):

- IMMER `stalwart-mail:8080` intern (nie `https://mail.maxone.one` von Edge aus).
- IMMER `/jmap/session` direkt — nie `/.well-known/jmap` (307-Redirect, Deno-fetch folgt unzuverlässig).

**Diagnose-Reihenfolge** bei "Mail nicht angekommen?":

1. **Brevo Events API** zuerst (`/v3/smtp/statistics/events`) — Domain-Owner-Auth, sucht nach `event=delivered|error|bounce`.
2. **Stalwart-Logs nur** wenn Brevo `delivered` zeigt aber Empfänger nichts hat (sehr selten).
3. **Stalwart-Index als Forensik** — `Email/get` mit `partId` und `disposition` hilft bei Anhang-Diagnose ([[zentinel-rules#regel-21]]).

## Projekt-Status [coverage: medium -- 1 source]

Welche Projekte haben einen **eigenen** Brevo-Account vs. nutzen den Maxone-Shared-Account?

| Projekt | Brevo-Account | Domain-Auth | Secrets-Pfad | Stand |
|---|---|---|---|---|
| maxone.one | Maxone-Org (shared) | maxone.one auth+verified | `/opt/secrets/global/keys.env` | live |
| venfree | venfree-Org (`mail@venfree.de`, Org `6a10d33f1e4d419de9018610`) | venfree.de auth+verified | `/opt/secrets/vanfree/brevo.env` | **live seit 2026-05-27** |
| slf | eigener Brevo (siehe `/opt/secrets/slf/`) | je Domain | `/opt/secrets/slf/keys.env` | live |
| Cleanup-Auftrag | — | — | — | venfree-Domain im Maxone-Account entfernen (offen) |

Regel: Ein Brevo-Account je Projekt ([[zentinel-rules#regel-11]]). Der `BREVO_API_KEY` in `/opt/secrets/global/keys.env` ist **nicht** für Outbound, sondern für Vector zum Key-Rotation-Management.

## Key Rules [coverage: high -- 2 sources]

Volle Liste: [[zentinel-rules]]. Die für das Architektur-Verständnis kritischen sind:

- **Outbound != Inbound** — Stalwart-Logs sind kein Beleg für Sendeerfolg. Das ist Brevo.
- **Edge-Funktionen rufen intern** — `stalwart-mail:8080`, kein Public-Hostname.
- **`{accountId}`-Template darf nicht weg-gestripped werden** — sonst landen Sent-Blobs im Default-Account `"a"` statt im Caller-Account, und Stalwart antwortet 200 ohne Side-Effect (silent black hole).
- **Domain-Preflight vor Send** — fehlende Brevo-Auth wird sonst stillschweigend mit `event=error` verworfen, DB schreibt trotzdem `status='sent'`.

## Notable Failures [coverage: medium -- 1 source]

Dieser Topic verweist nur auf die [[failure-modes]]-Single-Source-of-Truth. Architektur-relevante Vorfälle:

- **2026-04-10 — Sent-Items-Blackhole + Brevo Silent Rejection.** uploadUrl-Bug + fehlende Domain-Auth. Lehren: [[zentinel-rules#regel-19]], [[zentinel-rules#regel-20]].
- **2026-04-28 — Unsichtbarer Anhang + Blue/Green Split-Brain.** Frontend-Filter + Round-Robin zwischen Slots. Lehren: [[zentinel-rules#regel-21]], [[zentinel-rules#regel-22]].

Volle Postmortems: [[failure-modes]].

## Operational Patterns [coverage: high -- 2 sources]

**Health-Check (sicher, jederzeit):**

```bash
ssh root@128.140.40.235 "curl -sS \
  -H 'X-Health-Key: \$(grep ^ZENTINEL_HEALTH_KEY /opt/supabase/docker/.env | cut -d= -f2)' \
  https://panel.maxone.one/functions/v1/zentinel-health | jq '.healthy,.failedCount,.primaryError'"
```

Erwartet: `true, 0, null`.

**Restart-Reihenfolge nach Stalwart-Vorfall:**

```bash
docker restart stalwart-mail
sleep 10
docker restart supabase-edge-functions
sleep 8
docker restart maxone-app-blue   # bzw. -green je nach aktivem Slot
```

Niemals alles gleichzeitig — Edge-Functions cachen sonst eine kaputte JMAP-Verbindung und re-bannen sich beim Start.

**Bei Verdacht "Mail nicht angekommen":**

1. Brevo Events API (Domain-Owner-Auth) → `delivered`, `error`, `bounce`?
2. `maxone.sent_emails` → Status `sent` oder `rejected_unauthenticated_domain`?
3. Stalwart `Email/get` nur wenn Schritt 1+2 keinen Befund haben (Anhang-Forensik o.ae.).

Siehe auch: [[../concepts/silent-failures]] für die Klasse von Bugs, die diese Pipeline besonders trifft.

## Sources

- [[../../briefings/ZENTINEL-STALWART-BIBEL]] — Regel 12, 14, 15, 19, 20, 21, 22 + Vorfälle 2026-04-10 und 2026-04-28
- `~/.claude/CLAUDE.md` — Block "Zentinel/Stalwart/Mail: Bibel ist Pflicht (OBERSTE PRIORITÄT, 2026-04-27)"
- `maxone.one/supabase/functions/email-client/handlers/send.ts` — Send-Code (referenziert)
- `zentinel-health` Edge Function — Watchdog (referenziert)
- `c:/Users/max/Projects/venfree/PLAN.md` "Schritt 9b" (2026-05-27) — Trennung Brevo-Account venfree von Maxone-Shared
