---
topic: failure-modes
last_compiled: 2026-05-22
source_count: 3
status: active
---

# Failure Modes — die sechs großen Vorfälle

## Summary [coverage: high -- 3 sources]

Sources span 2026-03-24 bis 2026-05-21. Sechs große Vorfälle in zwei Monaten — fünf in der Mail/Stalwart-Pipeline, einer auf der darunter liegenden Host-Infrastruktur (OOM-Storm 2026-05-21, der Stalwart als ungecappten Mit-Trigger hatte). Das ist die kanonische Postmortem-Sammlung; alle anderen Topics ([[mail-architecture]], [[zentinel-rules]], [[secrets-tls]]) verweisen hierher statt zu duplizieren. Gemeinsamer Kern: **silent failures** + **defense-as-trigger** (Stalwart 200 ohne Side-Effect, Brevo `event=error` nach `messageId`, RocksDB-vs-Config-Präzedenz, Frontend-Filter ohne Sichtbarkeit, `swapoff -a` als vermeintliche Defense die selbst OOM-Killer triggert) — siehe [[../concepts/silent-failures]].

## Architecture [coverage: low -- 1 source]

Diese Datei ist eine Postmortem-Liste, kein Architektur-Topic. Lese `[trigger → amplifier → endstate → permanent fix → lessons]` als Standard-Schema für jeden Vorfall.

## Key Rules [coverage: medium -- 1 source]

Aus jedem Vorfall sind unverhandelbare Regeln entstanden — vollständig dokumentiert in [[zentinel-rules#key-rules]]. Mapping (newest first):

- **2026-05-21** → Regel 24
- **2026-05-16** → Regel 23
- **2026-04-28** → Regeln 21, 22
- **2026-04-10** → Regeln 12, 17, 19, 20
- **2026-04-05** → Regeln 4, 5, 6, 13, 18
- **2026-03-24** → Regeln 1, 2, 3, 7, 8, 10

## Notable Failures [coverage: high -- 1 source]

### 2026-08-04 — Neuer Alias steht im Principal und wird trotzdem mit 550 abgewiesen

- **Trigger:** `impressum@griddone.de` per Management-API an den Principal `hallo@griddone.de` gehängt (`PATCH /api/principal/<name>` mit `[{"action":"addItem","field":"emails","value":"…"}]`, Antwort 200). Ein `GET` auf den Principal zeigte die Adresse danach sauber in `emails`.
- **Symptom:** SMTP wies sie weiter ab. `RCPT TO:<impressum@griddone.de>` gegen `localhost:25` gab `550 5.1.2 Mailbox does not exist`, während der ältere Alias `mastr@griddone.de` derselben Adresse mit `250 2.1.5 OK` antwortete. Die Kontrollprobe am zweiten Alias war der Punkt, an dem klar wurde: Aliase funktionieren, dieser eine ist nur nicht angekommen.
- **Ursache:** Verzeichnis-Cache. Stalwart hält die Adressliste im Speicher und liest sie nach einem API-Schreibvorgang nicht neu ein.
- **Fix:** `GET /api/reload` (200), danach sofort `250 2.1.5 OK`. Kein Container-Neustart nötig, und keiner erlaubt: der Mailserver bedient alle Postfächer, ein Restart für einen Alias steht in keinem Verhältnis.
- **Lehre:** Nach jeder Principal-Änderung per API gehört der Reload dazu, und der Beleg ist die SMTP-Probe, nicht die API-Antwort. Ein `200` auf das Schreiben sagt nur, dass geschrieben wurde, nicht dass zugestellt wird. Steht die Adresse in einem Pflichtdokument (Impressum nach §5 DDG), ist der ungeprüfte Weg ein Rechtsrisiko. Kanonisch: Standard 007-A.

### 2026-05-21 — Globaler OOM-Storm (swap-guard + ungecapptes Stalwart)

- **Trigger:** Zwei Faktoren in Kombination. (a) `stalwart-mail` lief ohne `mem_limit` (= Host-Total 7.6 GB Headroom). (b) `/opt/swap-guard.sh` (cron `*/5 * * * *`) machte `swapoff -a && swapon -a` bei Swap > 2 GB. Kernel zieht beim Swapoff ALLES aus Swap zurück ins RAM — bei knappem RAM (Spike durch Faktor a) → globaler OOM-Killer.
- **Verstärker:** Watchdog-Logs zeigten nur Kong-Recreations (Mitigation, nicht Ursache). Die Verbindung Faktor (a) + (b) war im Mental-Model nicht vorhanden, weil swap-guard als "Defense" wahrgenommen wurde — nicht als Trigger.
- **Endzustand:** 2026-05-21 21:25:42 — OOM-Killer killt swapoff-Prozess + voltfair-server runner Node (2.3 GB). ~17 Stunden bis Root-Cause-Identifikation am 2026-05-22.
- **Permanenter Fix:** [[zentinel-rules#regel-24]]. `/opt/swap-guard.sh` v2 ohne swapoff, nur Cache-Drop + proaktiver Kong-Restart. `mem_limit: 512m` für Stalwart (live 33% Auslastung). Sweep der ~65 maxone-prod-Container: einziger weiterer ungecappter = `paperclip-db` (49 MB idle), via `docker update` + systemd-Override gefixt. Stalwart-Compose ins Repo: `ops/stalwart/docker-compose.yml` (commit `694d725a`).
- **Lehre:** Defense-Mechanismen müssen für ihr eigenes Failure-Pattern getestet werden. `swapoff -a` IST der Trigger unter RAM-Druck, nicht die Heilung. Standard 028 (mem_limit für ALLE Container) ist nicht optional — auch nicht für "nur idle" Container, denn der unkontrollierte Spike kommt erst noch.

### 2026-05-16 — Mailbox-Passwort-Desync + Ban-Zyklus (hey@viktoria-from.de)

- **Trigger:** Passwort für `hey@viktoria-from.de` über `/api/atelier/mailbox-password` geändert. Stalwart RocksDB aktualisiert, maxone-Supabase `email_accounts` (mit AES-GCM-verschlüsseltem JMAP-Passwort) nicht.
- **Verstärker:** `email-client` MDN-Checker (IP `10.0.2.3`) läuft alle ~3 Min und authentifiziert sich pro Konto via JMAP. Mit altem Passwort → `security.authentication-ban`. Ban läuft ab → erneuter Ban. 45+ Events zwischen 15:41 und 21:34 UTC.
- **Endzustand:** SnappyMail-Login mit `AUTHENTICATIONFAILED` geblockt. Stalwart-Neustart 21:32 UTC löscht den Ban — MDN-Checker triggert ihn 21:34 UTC neu. Zyklus nicht ohne Store-Sync stoppbar.
- **Permanenter Fix:** [[zentinel-rules#regel-23]]. Standard 016 (mailbox-password-sync) verlangt: Stalwart-Änderung MUSS `email_accounts` + Browser-Sessions synchron mitziehen, sonst `warning`-Feld in HTTP-Response.
- **Lehre:** Zwei unabhängige Passwort-Stores ohne Sync-Mechanismus = garantierte Desync bei der ersten Änderung. Der MDN-Checker macht aus einem stillen Bug einen lauten Ban-Zyklus — gut für Diagnose, schlecht für Nutzer.

### 2026-04-28 — Unsichtbarer Anhang + Blue/Green Split-Brain

- **Trigger:** `EmailDetail.svelte:106` filterte Anhänge mit `!a.cid` als Inline-Image aus. Gmail hängt `cid` aber RFC-konform AUCH an echte File-Attachments.
- **Konkreter Fall:** Maik Franz schickte 28.04.2026 08:56 lokal an `max@maxone.one` ein PDF-Angebot (`Max Karastelev – TZ.pdf`, 212 KB). JMAP-Index hatte den Anhang korrekt mit `partId="4"`, `disposition="attachment"`, `cid="f_moi9vkqa0"`, `type="application/pdf"`. **UI zeigte aber keinen Anhang.**
- **Verstärker (potentiell):** Diagnostische Suche nach "hat Maik je ein Angebot geschickt?" hätte **falsch-negativ** geantwortet, wenn nicht zufällig die Mail-Größe (331 KB vs. 40 KB Standard-Reply) als Indikator entdeckt worden wäre.
- **Folge-Bug (Split-Brain):** Nach Green-Deploy war Blue NICHT gestoppt → beide Slots lieferten parallel mit identischer Traefik-Rule → Round-Robin. User sah den Anhang abwechselnd. `docker stop maxone-v2-blue` um 11:58 stellte Eindeutigkeit her. **+5 Min Diagnose-Zeit für "deploy ist live aber nicht zu sehen"-Verwirrung.**
- **Permanenter Fix:** [[zentinel-rules#regel-21]] (Filter-Logik: `!(a.cid && a.disposition !== 'attachment')`), [[zentinel-rules#regel-22]] (Swap erst fertig wenn Old-Slot gestoppt).
- **Lehre:** Frontend-Filter sind Single-Point-of-Failure für K1 (Null Datenverlust), weil Backend-Daten korrekt sind und User keinen Hinweis bekommt was er nicht sieht. Blue/Green ohne Stop-Old-Slot ist Split-Brain.
- **Historisch wahrscheinlich:** Maiks Mail vom 10.03.2026 ("Angebot zugeschickt") hatte vermutlich denselben Bug — nicht verifizierbar weil JMAP-Read heute keinen Anhang mehr in der Antwort hat.

### 2026-04-10 — Sent-Items-Blackhole + Brevo Silent Rejection (Doppelschlag)

- **Trigger 1 (uploadUrl-Bug):** `JmapClient.init()` warf via `.split("{")[0]` das `{accountId}/`-Template-Segment der `uploadUrl` weg. Resultat: Blob-Uploads landeten im Default-Account `"a"` statt im Caller-Account `"x"`. `Email/import` verwies auf einen "fremden" Blob → Stalwart antwortete 200 ohne Side-Effect → Sent-Ordner blieb 5 Tage leer.
- **Trigger 2 (Brevo silent rejection 2026-04-03):** Mail `max@maxone.one → r.jenau@linagames.de` ("Re: AW: Brettspiel Wetzlar") wurde von Brevo mit `error: "Sending has been rejected because the sender ... is not valid"` verworfen, weil `maxone.one` erst 2026-04-05 17:21 UTC in Brevo authentifiziert wurde — **2 Tage nach dem ersten Send.** DB-Status war `sent`, Empfänger meldete 7 Tage später dass nichts angekommen war.
- **Verstärker:** `try/catch` in `saveSentCopy` fing nichts (Stalwart 200), DB-Logik schreibt `status='sent'` sobald Brevo `messageId` zurückgibt — auch wenn Brevo unmittelbar danach intern `event=error` setzt.
- **Endzustand:** 7 Sent-Kopien zwischen 03.04. und 10.04. als Blob-Orphans in Account `"a"` verloren; 1 Mail (Brettspiel Wetzlar) nie ausgeliefert. Per Re-Import-Skript wiederhergestellt; die Brevo-rejected Mail bleibt verloren (kein Geschäftsdruck), in DB als `status='rejected_unauthenticated_domain'` markiert.
- **Permanenter Fix:** [[zentinel-rules#regel-19]] (uploadUrl-Substitution mit `{accountId}`-Erhaltung), [[zentinel-rules#regel-20]] (`ensureBrevoDomainAuthenticated()` Pre-Flight, 24h-Cache, fail-open). Beide deployed 2026-04-10, 4 Tests grün.
- **Ableitung:** Bei JEDER URL aus einer JMAP-Session-Response, die ein Template-Segment enthält (`{accountId}`, `{blobId}`, `{name}`, `{type}`), MUSS dieses Segment beim Host-Rewrite erhalten bleiben und in der jeweiligen Methode ersetzt werden.

### 2026-04-05 — Self-Inflicted Fail2Ban Loop

- **Trigger:** `zentinel-health` Reach-Check schickte alle 2 Min `Basic healthcheck:invalid` an `/jmap/session` → Stalwart bannte die Edge-Runtime-IP `10.0.2.3` nach 2 Calls.
- **Verstärker 1:** `unban-stalwart.sh` jq-Filter (`.data.items[]? | .key`) zog 0 Keys, weil Stalwart `.data.items` als Map (nicht Array) liefert → Skript dachte alles sei gut.
- **Verstärker 2:** Recovery-Pfad lief vom Host gegen `http://stalwart-mail:8080/api/...` → Host-IP wurde selbst gebannt.
- **Endzustand:** Restart-Loop alle 2 Minuten bis Max die Timer manuell stoppte.
- **Permanenter Fix:** Commit `1a04dc0` — Reach-Check ohne Authorization-Header, `unban-stalwart.sh` über container-loopback `stalwart-cli`, Verifizierung via `zentinel-health` statt "Skript ist nicht abgestürzt", 9-Layer-Defense für Vector-Chat (KB §11.11), Brevo-Bounce-Watchdog timer.
- **Lehre:** Ein Recovery-Pfad, der selbst gebannt werden kann, ist kein Recovery-Pfad. Container-loopback ist die einzige sichere Diagnose-Route gegen Stalwart von einem Host aus.

### 2026-03-24 — Stalwart Admin Lockout

- **Trigger:** `docker run` als Test-Container blockierte Stalwart-Ports und lockte die RocksDB.
- **Verstärker:** Passwort in `config.toml` geändert, ohne zu wissen dass die RocksDB-DB Vorrang hat. Login funktionierte trotzdem mit altem Passwort → 30 Min Suchen.
- **Self-Damage:** Mehrere blinde Restart-Versuche; im Verlauf wurden Brevo-Credentials in einem `docker exec -e KEY=VAL`-Befehl gesetzt → Klartext-Passwörter in shell-history und docker-events. Konsequenz: Brevo-Key-Rotation → SMTP-Konfiguration in allen Projekten neu setzen → Downtime.
- **Endzustand:** Brevo-Key rotiert; Stalwart-Admin via `stalwart-cli` neu gesetzt; alle Orphans entfernt.
- **Permanenter Fix:** [[zentinel-rules#regel-1]], [[zentinel-rules#regel-2]], [[zentinel-rules#regel-3]], [[zentinel-rules#regel-7]], [[zentinel-rules#regel-8]], [[zentinel-rules#regel-10]].

## Operational Patterns [coverage: medium -- 1 source]

**Was alle vier Vorfälle gemeinsam haben:**

1. **Silent failure**: keiner gab den User einen klaren Fehlerton. uploadUrl-Bug → 200, Brevo silent reject → `event=error` nach `messageId`, RocksDB-Präzedenz → kein Warning, Frontend-Filter → kein Hinweis "Anhang vorhanden aber gefiltert". Vergleichend: [[../concepts/silent-failures]].
2. **Diagnose dauerte länger als der Fix**: in 3 von 4 Fällen war das Reproduzieren/Verstehen schwerer als die Code-Änderung selbst. Lehre: Postmortems mit Trigger/Amplifier/Endstate disziplinieren das Diagnose-Wissen.
3. **Defense added an genau einer Stelle, wo es nicht reicht**: Regel 12 (Disziplin-Domain-Auth) war nicht genug → Regel 20 erzwingt es im Code. Health-Check-Bug fixed → 9-Layer-Defense kam hinterher. Frontend-Filter-Fix → Regel 22 Swap-Disziplin obendrauf. Pattern: jede Regel adressiert nur eine Schicht — Defense-in-Depth ist die Norm, nicht die Ausnahme.

**Wann hierher zurückkehren:** Bevor du eine Diagnose startest, Section "Notable Failures" durchscannen. Symptom-Match (Sent leer? Anhang fehlt? Stalwart restart-loop?) → spart oft den ganzen Diagnose-Pfad.

## Sources

- [[../../briefings/ZENTINEL-STALWART-BIBEL]] — Sektion IV "Die vier großen Vorfälle"
- `~/.claude/CLAUDE.md` — Block "Stalwart-Fehler Lehren (GLOBALE REGEL — NIE WIEDER!)"
