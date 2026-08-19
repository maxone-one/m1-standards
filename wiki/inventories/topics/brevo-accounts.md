# Brevo-Accounts pro maxone-Projekt

**Last updated:** 2026-08-19 (Nachtrag aus Postfach-Belegen, siehe unten)
**Coverage:** vollständige Account-Trennung am 2026-05-31 durchgezogen — alle Welle-1-bis-8-Domains aus dem Karastoni-Hauptaccount migriert, Per-Domain-Routing in `maxone.sponsored_customers` aktiv
**Source-Briefing:** `c:/Users/max/Projects/Zentinel/briefings/BRIEF-BREVO-MULTIACCOUNT-2026-05-22.md`

## Summary

Pro eigenstaendiger maxone-Firma ein eigener Brevo-Account (Modell A:
physisches Postfach pro Projekt, kein Forward). Owner-Login folgt der
Konvention `mail@<projektdomain>`. Free-Plan bis 300 Mails/Tag.
Bei Exit: Brevo Owner-Email-Wechsel + Domain-Transfer, keine Restkopplung
an `@maxone.one`.

## Source-of-Truth

| Information | Datei (auf maxone-prod) | Lookup-Befehl |
|---|---|---|
| API-Key pro Projekt | `/opt/secrets/<projekt>/brevo.env` (`BREVO_API_KEY`) | `cat /opt/secrets/<projekt>/brevo.env` |
| Postfach-Passwort (OTP-Lookup) | `/opt/secrets/<projekt>/mail-inbox.env` | `cat /opt/secrets/<projekt>/mail-inbox.env` |
| Maxone-Bestand (sponsored) | `/opt/secrets/maxone/brevo.env` | (token) |

## Accounts (Stand 2026-05-31)

| Brevo-Account | Owner-Login | user_id | Domains | Send-Routing | Secret-Store-Pfad |
|---|---|---|---|---|---|
| **Karastoni (Haupt)** | `karastoni@googlemail.com` | 10621970 (maxone.studio) | `maxone.studio`, `maxone.one`, `repivot.me` | Default (Env-Var `BREVO_API_KEY`) | `/opt/secrets/global/brevo.env` |
| **karastelev.de** | `max@karastelev.de` (seit 02.06.2026, vorher `karastoni+karastelev@googlemail.com`) | 11311384 | `karastelev.de`, `snapflow.one`, `vybora.dev` | `sponsored_customers.brevo_api_key` per Domain | `/opt/secrets/karastelev/brevo.env` |
| **Venfree** | `mail@venfree.de` | 11289010 | `venfree.de` | `sponsored_customers.brevo_api_key` | `/opt/secrets/vanfree/brevo.env` |
| **Stadt Lahn Flow** (SLF) | `mail@stadtlahnfluss.de` | 11288725 | `stadtlahnflow.de`, `stadtlahnfluss.de` | `sponsored_customers.brevo_api_key` | `/opt/secrets/slf/keys.env` |
| **Voltfair** | `inbox@voltfair.de` | 11289276 | `voltfair.de` | `sponsored_customers.brevo_api_key` | `/opt/secrets/voltfair/keys.env` |
| **Viktoria From Fotografie** | `max+viktoria@maxone.one` (seit 11.06.2026, vorher `mail@viktoria-from.de`) | 11288841 | `viktoria-from.de` | `sponsored_customers.brevo_api_key` (PLUS Sponsor-Footer aus DB) | `/opt/secrets/viktoria-from/keys.env` |
| **GridDone** | `hallo@griddone.de` | `[?]` nicht erhoben | `griddone.de` `[A:]` | `[?]` nicht erhoben, vermutlich noch kein Routing-Eintrag | `[?]` nicht erhoben |

### Was 2026-05-31 passierte (Domain-Trennung)

Vor heute hostete der **Karastoni-Hauptaccount alle 11 Domains** — Alt-Setup vor der Welle-1-bis-8-Brevo-Multi-Account-Strategie. Heute durchgezogen:

1. **Per-Domain-Send-Routing aufgebaut** über `maxone.sponsored_customers.brevo_api_key`. Edge-Code (`send.ts:90-99`) liest `sponsor?.brevo_api_key ?? null` und übergibt das als `overrideApiKey` an `sendEmailViaBrevo`. Footer-HTML/Text-Felder mit leerem String für reine Routing-Einträge (Viktoria behält den echten Sponsor-Footer).
2. **6 Domains aus Karastoni-Hauptaccount via `DELETE /v3/senders/domains/<domain>` entfernt** — karastelev.de, snapflow.one, vybora.dev, venfree.de, stadtlahnflow.de, voltfair.de. Sie sind alle in ihren eigenen Accounts authenticated+verified, der Routing-Eintrag schickt Sends dorthin.
3. **stadtlahnfluss.de + viktoria-from.de in eigene Accounts migriert** — DNS-Brevo-Code-TXT bei INWX via `updateRecord` aktualisiert (DKIM-CNAMEs + DMARC bleiben identisch, weil Brevo-Plattform-Standard), `PUT /v3/senders/domains/<domain>/authenticate` triggert auth, dann aus Hauptaccount gelöscht.
4. **Live-Smoke-Tests grün:** max@karastelev.de, max@stadtlahnfluss.de, hey@viktoria-from.de — alle gesendet von Zentinel, in Gmail innerhalb 15-20s angekommen, jeweils über den korrekten Brevo-Account.

### Nachtrag 19.08.2026 — drei Abweichungen, aus Postfach-Belegen erhoben

Gefunden beim DOPPELKONTEN-SCAN der Werkstatt, nicht bei einer Brevo-Prüfung. Alles
Folgende stammt aus Mails in Max' Postfächern, **nicht aus der Brevo-Oberfläche oder der
API**; wer den Bestand hart braucht, prüft gegen `/v3/account` mit dem jeweiligen Key.

**GridDone ist ein siebtes Konto und war hier nicht geführt.** `[B:` vollständige Kette im
Postfach `hallo@griddone.de` am 29.06.2026: „Complete your registration" 19:52, „Welcome to
Brevo!" 19:55, „Your account is validated" 20:00, „A new API key has been created in your
account" 20:02`]`. Es folgt der Konvention dieses Dokuments, es fehlte nur, weil der Stand
hier der 31.05. war und das Konto vier Wochen später entstand. Offen bleiben user_id,
Secret-Store-Pfad und ob `griddone.de` einen Routing-Eintrag in `sponsored_customers` hat.

**Zwei Owner-Logins sind gewechselt worden, beide im Juni.** `[B:` Brevo-Mails „Confirm
your new login email" mit Wortlaut „You have requested to change your Brevo login email
address to …" — an `max@karastelev.de` am 02.06.2026, viermal zwischen 22:15 und 23:17, und
an `max+viktoria@maxone.one` am 11.06.2026, zweimal`]`. Die Tabelle oben trägt jetzt die
neuen Adressen und die alten in Klammern daneben.

**Und eine Warnung an alle, die dieses Dokument für einen Doppelkonten-Verdacht heranziehen:**
Am 18.06.2026 um 07:57 ging an `max@maxone.one` eine Brevo-Sicherheitswarnung, „ein anderes
Brevo-Konto hat versucht, den SMS-Newsletter-Opt-in mit der Telefonnummer zu aktivieren, die
mit Ihrem Konto verknüpft ist". **Das ist keine Kollision, sondern die erwartbare Folge
dieses Modells:** sieben Konten teilen eine Telefonnummer. Die Meldung ist am 19.08.2026
einmal als Beleg für ein Doppelkonto gelesen worden, und das war falsch.

### repivot.me — bewusste Ausnahme

Bleibt im Karastoni-Hauptaccount (Option B). Begründung: null aktive Zentinel-Postfächer auf repivot.me, kein Send-Verkehr → eigener Brevo-Account würde keinen Mehrwert bringen, dafür Web-UI-Sign-up + Email-Phone-Verification kosten.

### Per-Domain-Routing in `sponsored_customers` (Stand 2026-05-31)

```
domain              key_prefix       granted_by
------------------  ---------------  --------------
karastelev.de       xkeysib-cc9379   system-routing (karastelev.de-Account)
snapflow.one        xkeysib-cc9379   system-routing (karastelev.de-Account)
vybora.dev          xkeysib-cc9379   system-routing (karastelev.de-Account)
venfree.de          xkeysib-5652fb   system-routing (Venfree-Account)
stadtlahnflow.de    xkeysib-b61629   system-routing (SLF-Account)
stadtlahnfluss.de   xkeysib-b61629   system-routing (SLF-Account)
voltfair.de         xkeysib-116afa   system-routing (Voltfair-Account)
viktoria-from.de    xkeysib-13aeb6   max@maxone.one (Viktoria-Account, mit Sponsor-Footer)
```

Domains die NICHT in `sponsored_customers` stehen (maxone.studio, maxone.one, repivot.me) → Edge fällt auf `BREVO_API_KEY` aus `Deno.env` zurück = Karastoni-Hauptaccount-Key.

### List-Unsubscribe-Header beim karastelev.de-Account abschalten (Ticket eingereicht 2026-05-31)

Brevo erlaubt das nur via Support-Ticket pro Account (siehe Brevo Help). **Max-Direktive 2026-05-31:** nur EIN Ticket aufmachen, am karastelev.de-Account (user_id 11311384), weil dort das ursprüngliche Bug-Symptom auftauchte (private 1:1-Mail "hi max" wurde von Zentinel als Newsletter erkannt). Die anderen 5 Brevo-Accounts werden NICHT mit einem Ticket angegangen, sie hosten Customer-/Wave-Domains, da ist `List-Unsubscribe` weniger störend bzw. teilweise gewollt für Marketing-Sends.

Ticket **[#5389401](https://help.brevo.com/hc/de/requests/5389401)** eingereicht 2026-05-31 23:42 (EN), Status `Offen`. Antwort von Brevo abwarten, bei OK Verify-Send von max@karastelev.de an externes Konto, Headers prüfen, dann hier auf "live" updaten.

Im Zuge der Aktion wurde der `companyName` des Brevo-Accounts von "Schreibstudio" (Altlast aus einer früheren Auto-Session) auf `karastelev.de` umbenannt. **Direktive Max 2026-05-31:** Schreibstudio darf existieren (Telegram-Bot, andere Kontexte), aber niemals als Brevo-Referenz auftauchen.

### vanfree — Detail-Status 2026-05-23

- Brevo-Owner-Account: registriert + verifiziert, Owner `mail@venfree.de`
- Domain `venfree.de`: verifiziert in Brevo (DKIM Brevo + SPF + Verify-Code propagiert)
- API-Key `vanfree-app-prod`: generiert, gegen `/v3/account` validiert (plan=free)
- Secret-Store: `/opt/secrets/vanfree/brevo.env` enthaelt `BREVO_API_KEY`, Backup `/opt/secrets/.backups/vanfree/brevo.env.2026-05-23`
- **SMTP-Send: BLOCKIERT** — Brevo gibt `permission_denied`: *"Your SMTP account is not yet activated. Please contact us at contact@brevo.com to request activation"*. Account-level Anti-Spam-Gate (nicht Sender-level).
- **Aktion:** Zendesk-Ticket [#5377727](https://help.brevo.com/hc/de/requests/5377727) offen seit 2026-05-23 00:51, Subject `Account activation request – venfree (mail@venfree.de)`. Identity-Disclosure (Max sole proprietor, brand under maxone.one), Use-Case (transactional + opt-in newsletter), Compliance (Double-Opt-In, Unsubscribe, keine gekauften Listen), KI-Signatur.
- **Rollback:** `/opt/vanfree/.env.local` haelt weiterhin Maxone-Shared-Key (`vanfree-app-green` laeuft, Pioneer-Mails gehen ueber Maxone-Brevo-Account raus). Backup `/opt/vanfree/.env.local.bak.pre-brevo-swap-20260523`.
- **Next:** Brevo-Antwort abwarten → Re-Swap ENV + Smoke-Test → Status `live` → Wiki update → venfree.de aus Maxone-Brevo-Account entfernen.
- **Cleanup-Targets im Maxone-Brevo-Account** (Stand 2026-05-23, ERST nach Re-Swap entfernen):
  - Sender `noreply@venfree.de` (id=6, active) — DELETE `/v3/senders/6`
  - Domain `venfree.de` (authenticated + verified) — DELETE `/v3/senders/domains/venfree.de`
  - Maxone-Sender insgesamt heute: `noreply@maxone.studio` (1), `noreply@stadtlahnfluss.de` (2), `noreply@stadtlahnflow.de` (3), `noreply@venfree.de` (6). Domains: maxone.studio, voltfair.de, stadtlahnfluss.de, maxone.one, viktoria-from.de, karastelev.de, stadtlahnflow.de, venfree.de.
  - Maxone-Owner-Email: `karastoni@googlemail.com`, Plan: free+sms.

## Sender-Konvention pro Account

| Alias-Typ | Verwendung in Brevo |
|---|---|
| `noreply@<domain>` | Default Transactional-Sender |
| `support@<domain>` | Kunden-Replies (optional, wenn Brevo-Inbox genutzt) |
| `mail@<domain>` | Brevo-Owner-Login, NICHT als Sender |

## Operational Patterns

- **Pre-Brevo-Check:** Vor Brevo-Account-Registrierung Test-Mail von Gmail an
  `inbox@<domain>` schicken und in Zentinel sehen. Wenn das nicht zustellbar
  ist, geht auch die OTP-Mail von Brevo verloren.
- **OTP-Abruf:** `mcp__zentinel__search_emails` mit Query `"Brevo confirm"` —
  4-stelliger Code im Subject oder Body.
- **DKIM-Dual-Pattern:** Stalwart-DKIM-Selektor unter `mail._domainkey.<domain>`,
  Brevo-DKIM unter `mail._domainkey.brevo.<domain>` — beide parallel, kein Konflikt.
- **SPF-Combined:** EIN TXT-Record `v=spf1 include:_spf.brevo.com include:spf.mail.maxone.one ~all`
  (niemals zwei separate SPF-Records — RFC verbietet).
- **Reaktivierung:** Free-Accounts inaktiviert nach 14 Tagen — eine
  Monitoring-Mail/Woche an `dmarc@<domain>` haelt den Account warm.

## Failure Modes

- **OTP-Mail kommt nicht an** → DNS-Propagation noch nicht durch ODER MX falsch
  ODER `inbox@`-Postfach nicht aktiv. `dig MX <domain>` + Test-Mail von Gmail.
- **Brevo-Domain-Verify schlaegt fehl** → DKIM-/Verify-TXT falsch propagiert.
  `dig +short TXT brevo-code.<domain>` und `dig +short TXT mail._domainkey.brevo.<domain>`.
- **Erste Mail im Spam** → DMARC fehlt oder `p=reject` zu frueh. Start mit
  `p=none; rua=mailto:dmarc@<domain>`, erst nach 14 Tagen `p=quarantine`.
- **SMTP `permission_denied` trotz gueltigem API-Key** (vanfree, 2026-05-23) →
  Brevo-Anti-Spam-Gate auf Account-Level. API-Key validiert gegen `/v3/account` OK,
  aber Send schlaegt fehl mit *"Your SMTP account is not yet activated."*
  Loesung: Zendesk-Ticket bei Brevo-Support oeffnen
  (https://help.brevo.com/hc/de/requests/new), Identity + Use-Case + Compliance
  offenlegen, KI-Signatur einhalten. ETA 1-3 Werktage. Bis dahin Rollback auf
  alten Key (Maxone-Shared) im Compose-ENV, NICHT live schalten.
- **Brevo Multi-Account: Pflicht-Schritt vor ENV-Swap** → API-Key generiert
  != Account sende-faehig. Ab Welle 2 PFLICHT: Vor ENV-Swap einen Test-Send
  per `/v3/smtp/email` machen. Bei `permission_denied` direkt Zendesk-Ticket,
  ENV-Swap erst nach gruener SMTP-Test.

## Sources

- Briefing: `c:/Users/max/Projects/Zentinel/briefings/BRIEF-BREVO-MULTIACCOUNT-2026-05-22.md`
- Standard 016-mail
- Standard 003-secrets-store
- Standard 004-tls-dns01
- Wiki [[mail-aliases]] — Alias-Routing pro Domain
- Wiki [[servers]] — maxone-prod als Stalwart + Secret-Store-Host
