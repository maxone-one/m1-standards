---
topic: mail-architecture
last_compiled: 2026-05-27
source_count: 5
status: active
---

# Mail Architecture (maxone)

## Summary [coverage: high -- 4 sources]

> **KORREKTUR 06.08.2026, gilt vor allem Folgenden:** Dieser Abschnitt beschreibt Brevo als
> Outbound-Weg. Das stimmt seit dem 13.07.2026 nicht mehr. **Jeder transaktionale und 1:1-Versand
> läuft self-hosted über Stalwart-Submission, Brevo ausschließlich für Outreach-Kampagnen**
> (globale Regel „Mailversand: NIEMALS Brevo"). Der Weg führt heute über das **Mail-Gateway**
> (`mailgate-app` auf maxone-prod, `mailgate.maxone.one/v1/tx`), das sich per SMTP an
> `mail.maxone.one:587` anmeldet, und zwar **mit dem Postfach, das als Absender dient**
> (`provider_accounts.default_sender` = SMTP-Login, `api_key` = dessen Passwort). Alles unterhalb
> zu Brevo als Standard-Outbound ist historisch. `[B: mailgate-DB und Live-SMTP-Test, 06.08.2026]`

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

## Absender-Adressen und Aliasse (Stand 06.08.2026)

**Wer als Absender auftreten darf, hängt am SMTP-Login, nicht am Code.** Das Mail-Gateway meldet
sich mit dem Postfach an, das als Absender dient. Stalwart prüft danach, ob die `MAIL FROM`-Adresse
diesem Principal gehört. Belegt am 06.08.2026 mit einem Login als `anfragen@maxone.one`:

| MAIL FROM | Antwort |
|---|---|
| `anfragen@maxone.one` (Principal-Name) | `250 2.1.0 OK` |
| `faktura@maxone.one` (Alias desselben Principals) | `250 2.1.0 OK` |
| `max@maxone.one` (fremder Principal) | `501 5.5.4 You are not allowed to send from this address` |

**Daraus folgt die billige Lösung für einen neuen Absender:** ein Alias am bestehenden Principal
genügt, kein zweites Postfach, kein Passwort, kein Eintrag in `provider_accounts`.

```bash
# Alias anlegen (RocksDB, nicht config.toml)
curl -X PATCH -u "$STALWART_ADMIN_USER:$STALWART_ADMIN_PASS" \
  -H 'Content-Type: application/json' \
  -d '[{"action":"addItem","field":"emails","value":"neue@maxone.one"}]' \
  https://mail.maxone.one/api/principal/anfragen@maxone.one
```

**Zwei Fallen, beide am 06.08.2026 belegt:**

1. **Eine Adresse kann nur an einem Principal hängen.** Der Versuch, `faktura@maxone.one`
   zusätzlich am Hauptpostfach `max@maxone.one` (id 23) zu hinterlegen, antwortete mit `200` und
   änderte nichts. Klassisches „200 OK ohne Side-Effect", siehe [[../concepts/silent-failures]].
   Der Altbestand `anfragen@maxone.one` liegt trotzdem doppelt vor, als eigener Principal (id 46)
   **und** als Alias an id 23. Bei der Zustellung gewinnt das Alias, ankommende Post landet im
   Ordner „Anfragen" bei Max.
2. **Ein Alias am Login-Principal ist für die Zustellung eine Sackgasse.** Post an
   `faktura@maxone.one` landet im Postfach von Principal 46, und das ist in Zentinel gar nicht als
   Konto geführt, also sieht es niemand. Behoben durch ein Sieve-Skript **`weiterleitung-an-max`**
   in ebendiesem Principal (`redirect :copy "max@maxone.one";`), installiert über ManageSieve auf
   Port 4190. `:copy` lässt die Kopie liegen, damit bei einer Störung nichts verloren geht.
   **Vorsicht bei Principals, die Zentinel verwaltet:** Dort installiert `sieve-sync` genau ein
   aktives Skript `zentinel-rules` und würde ein eigenes verdrängen. Principal 46 ist kein
   Zentinel-Konto, deshalb war der Weg hier frei.

**Prüfen ohne eine Mail zu senden:** Eine SMTP-Sitzung bis `RCPT TO` und dann `QUIT` beantwortet
die Zustellfrage, ohne dass etwas rausgeht. Immer mit Gegenprobe auf eine erfundene Adresse, sonst
misst man einen Catch-All statt einer echten Zuordnung (`gibtesnicht@maxone.one` → `550 5.1.2`).

## Sources

- [[../../briefings/ZENTINEL-STALWART-BIBEL]] — Regel 12, 14, 15, 19, 20, 21, 22 + Vorfälle 2026-04-10 und 2026-04-28
- Live-Erhebung am Stalwart-Principal und am Mail-Gateway, 06.08.2026 (Abschnitt „Absender-Adressen und Aliasse")
- `~/.claude/CLAUDE.md` — Block "Zentinel/Stalwart/Mail: Bibel ist Pflicht (OBERSTE PRIORITÄT, 2026-04-27)"
- `maxone.one/supabase/functions/email-client/handlers/send.ts` — Send-Code (referenziert)
- `zentinel-health` Edge Function — Watchdog (referenziert)
- `c:/Users/max/Projects/venfree/PLAN.md` "Schritt 9b" (2026-05-27) — Trennung Brevo-Account venfree von Maxone-Shared
