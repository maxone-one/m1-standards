---
topic: sieve-runtime
last_compiled: 2026-05-30
source_count: 4
status: active
---

# Stalwart Sieve Runtime — Trusted vs Per-Account

## Summary [coverage: high — 4 sources, alle frisch 2026-05]

Stalwart hat **zwei vollständig getrennte Sieve-Runtimes** mit unterschiedlichen Fähigkeiten — ein Detail das in der offiziellen Doku NICHT explizit dokumentiert ist und in der Praxis (B-VAC-TRUSTED 2026-05-30) zu zwei Tagen Investigation führte.

| Runtime | Trigger | Code-Pfad | Events gehandelt |
|---|---|---|---|
| **Trusted** | SMTP DATA-Phase, vor Enqueue | `crates/smtp/src/scripts/event_loop.rs` | `SendMessage`, `Reject`, `Keep`, `Discard`, `CreatedMessage` |
| **Per-Account** | Mailbox-Ingest (Delivery-Time) | `crates/email/src/sieve/ingest.rs:251` | **ALLE** Events, inkl. `DuplicateId` |

**Kritischer Unterschied:** Trusted-Scripts (`sieve.trusted.scripts.*`, gehookt via `session.data.script`) können `Event::DuplicateId` **nicht** handeln. Aktionen die DuplicateId emittieren — `vacation` (RFC 5230) ist der prominenteste Fall — laufen dort **silently no-op**: kein Log, kein Fehler, keine Queue-Eintrag, das Skript "passiert" einfach ohne Wirkung.

Per-Account-Scripts (per Postfach via JMAP `SieveScript/set` oder ManageSieve Port 4190) laufen im ingest-Pfad und handeln alles inkl. DuplicateId. Das ist der **einzige** Kontext, in dem vacation kanonisch funktioniert.

## Status nach dem Umbau [2026-06-12, live verifiziert]

Seit 12.06.2026 läuft das gesamte Routing per-account: `sieve-sync.ts` kompiliert pro JMAP-Principal EIN aktives Script `zentinel-rules` (Vacation + Spoof-Guard + Auto-Reply + Wired-Routing/Catch-All + Benutzer-Regeln + Noise-Filter) und installiert es via JMAP `SieveScript/set`. Das alte `zentinel-vacation`-Script ist dadurch deaktiviert. Trusted-Scripts bleiben eingemottet installiert (rcpt_gate-Reject funktioniert weiter). Drilltests grün (Regel-Treffer mailboxId 23, Catch-All 145). Bibel Regel 26.

## Wann was nutzen [KORRIGIERT 2026-06-12 — fileinto geht NICHT mehr trusted]

**WARNUNG (v0.15.5, live bewiesen 2026-06-12):** Die SMTP-DATA-Stage (`session.data.script`) unterstützt **kein `fileinto`**. Der ScriptResult kennt nur Accept/Reject/Discard/Replace + Header-/Envelope-Modifikationen (`crates/smtp/src/inbound/data.rs`, `crates/smtp/src/scripts/event_loop.rs`: unsupported-Event → silent `break`). Das galt vermutlich schon immer für diese Binary-Generation; aufgefallen nach Container-Neuaufbau 22.05.2026, als das gesamte Zentinel-Folder-Routing (auto-sort + user-filters) lautlos wirkungslos wurde. Volle Beweiskette: erfolgsstrategie/.planning/zentinel-haertung/04-befund-data-stage.md.

**Per-Account Sieve (ManageSieve / JMAP) — die EINZIGE Runtime mit vollem fileinto:**
- ALLES Folder-Routing (`fileinto :create`), auch Catch-All-Sortierung und Auto-Submitted-Sortierung
- Vacation / Abwesenheitsnotiz / Out-of-office
- `notify` mit Dedup-Anforderung
- `redirect :copy` mit Loop-Schutz
- Alles wo "schon mal gesehen" eine Rolle spielt
- ACHTUNG: nur EIN aktives Script pro Konto → Vacation + Filter-Regeln müssen in EIN Script kompiliert werden

**Trusted Sieve (`session.data.script`, `session.rcpt.script`):**
- `reject` (rcpt_gate funktioniert)
- Header hinzufügen, Envelope ändern, Discard
- NICHT: fileinto, Folder-Routing jeder Art

## Implementierung (B-VAC-TRUSTED Path A, 2026-05-30) [coverage: high]

Repo: `maxone.one/supabase/functions/email-client/`

**JMAP-Client-Erweiterung** (`jmap.ts`):
- `JmapClient.request(methodCalls, extraUsing)` — `extraUsing: ["urn:ietf:params:jmap:sieve"]` für Sieve-Calls
- `findSieveScriptByName(jmap, name)` — `SieveScript/get` mit leerem `ids` (alle Scripts), in JS nach Name filtern (siehe [[#stalwart-jmap-quirks]])
- `upsertActiveSieveScript(jmap, name, contents)` — Blob upload (Content-Type `application/sieve`), dann `SieveScript/set` create-or-update mit `onSuccessActivateScript`
- `deleteSieveScriptByName(jmap, name)` — siehe Disable-Pfad-Workaround unten

**Handler** (`handlers/accounts.ts setVacation`):
- DB-Upsert in `email_vacation` (unverändert)
- Wenn `enabled && message.trim()`: Sieve-Body bauen + `upsertActiveSieveScript(jmap, "zentinel-vacation", body)`
- Wenn `disabled`: `upsertActiveSieveScript(jmap, "zentinel-vacation", "keep;\n")` (No-Op-Body — siehe Quirks)
- Auth: bestehender per-account `jmap_password` aus `email_accounts` — kein neuer Cred-Pfad

**Trusted Script** (`handlers/sieve-sync.ts compileRules`):
- Vacation-Block ist **entfernt** — user-filters trägt nur noch Folder-/Filter-Regeln
- Wäre der Block dort drin, würde er silently nichts tun

## Stalwart JMAP-Quirks [coverage: high — alle live-verifiziert 2026-05-30]

Drei Stalwart-spezifische Eigenheiten, die nicht in der JMAP-Sieve-Spec stehen und bei der Implementierung biten:

**1. `SieveScript/query` exposed KEINEN `name`-Filter.**
Lösung: `SieveScript/get` mit leerem `ids` (alle Scripts laden), in JS nach Name filtern. Bei <10 Scripts pro Account billig.

**2. `onSuccessActivateScript: null` deaktiviert das aktive Script NICHT zuverlässig.**
JMAP-Spec sagt: `null` setzt "kein Script aktiv". Stalwart loggt nur einen State-Change ohne tatsächliche Deaktivierung. Workaround gibt es nicht — Stalwart will immer mindestens ein aktives Script pro Account.

**3. Das aktive Sieve-Script kann nicht destroyed werden.**
`SieveScript/set destroy` gibt `notDestroyed: {type: "scriptIsActive", description: "Deactivate Sieve script before deletion."}`. Und Punkt 2 erlaubt keine Deaktivierung.

Lösung für "Vacation aus / kein OOO mehr": Body des Scripts mit Noop überschreiben. Script bleibt active, hat aber keine Wirkung. **Body MUSS minimal-Sieve sein**: `require [];` (leere Liste) wird vom Parser abgelehnt ("Expected token string"). Bare `keep;` ohne require-Statement ist erlaubt und der minimale Noop.

## Frankensteins-Principal-Falle [coverage: medium — 1 source, verifiziert 2026-05-30]

Wenn man Sieve für einen Frankenstein-KI-Account installiert (z.B. `frankensteins@maxone.one`), landet das Script unter dem **Principal `vector@maxone.one`** — alle 32 Frankensteins-Aliasse (vega, viper, vault, vista, vortex, vox, vybora, viktoria, vigil, valor, vantage, vera, visor + jeweils `.frankenstein`-Suffix) gehören zum selben Principal.

Konsequenz: Vacation auf "frankensteins" feuert für ALLE 32 Aliasse. Wenn man pro-Alias diskriminieren will, braucht das Sieve-Script eine `envelope :is "to" "<alias>"`-Bedingung.

Output-Detail: OOO-From-Header zeigt `vector@maxone.studio` (Principal-Primary), nicht den Empfänger-Alias.

Code-Verweis: [[../../projects/c--Users-max-Projects-Zentinel/memory/reference-frankensteins-principal]] für die volle Alias-Liste.

## Smoke-Test-Pattern [coverage: high]

Pro vacation-Install:
1. Vacation per UI/API aktivieren (frankensteins@maxone.one + Test-Subject + Test-Body)
2. Stalwart Admin-API prüfen: `GET /api/principal/<principal>?type=individual` zeigt enabledPermissions inkl. `jmap-sieve-script-set`/`get`/`query`
3. Test-Mail von externem Mail-Account senden (Gmail funktioniert)
4. Erwartung: OOO innerhalb 30s im externen Posteingang, From-Header = Principal-Primary
5. Disable-Test: Vacation deaktivieren, zweite Test-Mail → KEINE OOO mehr (Body ist `keep;`)

Erfolgskriterium: Sieve-Skript ist installiert UND der OOO-Roundtrip läuft live durch.

## Sources

- [[../../projects/c--Users-max-Projects-Zentinel/memory/feedback-stalwart-sieve-per-account]] — die Hauptregel
- [[../../projects/c--Users-max-Projects-Zentinel/memory/reference-stalwart-sieve-quirks]] — JMAP-Implementierungs-Eigenheiten
- Zentinel-Repo `BUGS.md` — B-VAC-TRUSTED Resolution-Eintrag
- Stalwart-Source 2026-05-30: `crates/email/src/sieve/ingest.rs:251`, `crates/smtp/src/scripts/event_loop.rs`, `crates/sieve/src/runtime/actions/action_vacation.rs`
