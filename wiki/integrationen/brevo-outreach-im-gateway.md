# Brevo-Outreach: die Umsetzung im Gateway

**Herkunft:** Bis zum 09.09.2026 stand das hier als Standard `028-brevo-api-outreach.md`.
Es war dort **seit dem 19.06.2026 ausdrücklich als abgelöst markiert** und galt nur noch
Gateway-intern. Beim Neuschnitt der Standards ist es hierher gewandert, **ohne dass ein Satz
entfallen ist**. Ein Standard sagt, was jedes Projekt tun muss; das hier sagt, wie ein
einzelner Dienst intern gebaut ist.

**Die Regel für Projekte steht in** [`standards/031-mail.md`](../../standards/031-mail.md)
**Abschnitt A**: Projekte rufen die Brevo-API NICHT direkt. Aller Outreach läuft über
`mail.maxone.one` (`POST /v1/outreach`), das Gateway ist der einzige Halter der
Provider-Keys. Hintergrund: Vorfall 2026-06-18, ungewollter Geist-Versand. Volle
Architektur: `erfolgsstrategie/.planning/CONCEPT-outbound-mail-safety.html`.

**Stand der Angaben: 2026-05-28.**

## Das Problem, das zur API-Nutzung führte

Vor der Umstellung liefen alle Mails über nodemailer plus Brevo-SMTP-Relay, auch
Outreach-Kampagnen. Das führte zu:

- **Tracking-Flickenteppich:** eigener Pixel (`/api/track`), eigener Click-Redirect, eigene
  `outreach_events`-Tabelle, Brevo-Webhook als Backup, vier Systeme für eine Aufgabe.
- **Manuelle Suppression:** Bounces, Unsubscribes und Spam-Complaints wurden selbst in die
  `leads`-Tabelle geschrieben. Brevo pflegte seine Suppression-Liste parallel und
  unabhängig, ohne Sync.
- **Null historische Opens:** SMTP-Sends ohne explizit konfigurierten Pixel liefern 0
  Öffnungen, weil Brevo über SMTP nur trackt, wenn Tracking im Account aktiviert ist und der
  Pixel injiziert wird.
- **Selbstgebautes Rate-Limiting:** `delay(500)` zwischen jedem Send, selbst verwaltet.
- **Kein message-ID-Anker:** Events kamen ohne eindeutige Mail-ID, die Korrelation lief über
  E-Mail-Adresse plus Zeitfenster, was bei Re-Sends falsche Zuordnungen erzeugen kann.

## Die Lösung

**Outreach-Sends (Kalt-Akquise, Sendeplan-Batches) laufen über die Brevo Transactional API.**
Alles andere (Buchungsbestätigungen, Mitglieder-Notifications, OTPs) bleibt auf SMTP.

```
POST https://api.brevo.com/v3/smtp/email
Authorization: api-key <BREVO_API_KEY>
```

| Feature | Vorher (SMTP) | Nachher (API) |
|---|---|---|
| Open-Tracking | eigener Pixel nötig | Brevo injiziert automatisch |
| Click-Tracking | eigener Redirect nötig | Brevo rewritet Links |
| Bounce-Handling | manuell in leads.bounced | Brevo-Suppression + Webhook |
| Spam-Complaint | Webhook-only | Brevo-Suppression + Webhook |
| message-ID | keiner | Brevo gibt `messageId` zurück |
| Rate-Limiting | delay(500) selbst | Brevo-intern |

## Grenze: Was auf SMTP bleibt

| Typ | Beispiele | Warum SMTP bleibt |
|---|---|---|
| Transaktional | Buchungsbestätigung, .ics-Anhang, OTP | Kein Tracking-Bedarf, einmalig |
| Mitglieder-Notifications | Vernetzung, Direktnachrichten, Challenges | Kein Kampagnen-Kontext |
| Interne Mails | Admin-Notifications, Watchdog-Alerts | Kein Tracking-Bedarf |

## Implementation-Vertrag

### 1. Zentraler Brevo-Client

**`src/lib/brevo-send.ts`**, Single Source of Truth für alle API-Sends.

```typescript
export interface BrevoRecipient {
  email: string;
  name?: string;
}

export interface BrevoSendOptions {
  to: BrevoRecipient[];
  subject: string;
  htmlContent: string;
  textContent?: string;
  sender?: { name: string; email: string };
  tags?: string[];                          // für Brevo-Statistik
  headers?: Record<string, string>;         // List-Unsubscribe etc.
  params?: Record<string, string>;          // Custom-Params für Brevo-Template-Engine
}

export interface BrevoSendResult {
  messageId: string;
}

export async function sendViaBrevoApi(
  opts: BrevoSendOptions,
): Promise<BrevoSendResult>
```

- Liest `BREVO_API_KEY` aus ENV
- Wirft bei HTTP-Fehler eine typisierte Exception
- Gibt `{ messageId }` zurück, der Aufrufer speichert ihn in `outreach_send_log`

### 2. HTML-Pipeline für Outreach

Die Template-Replacements (`{{VORNAME}}`, `{{PROFIL_SLUG}}` etc.) laufen weiterhin bei uns.
Das fertige HTML wird als `htmlContent` an die API übergeben.

**Was entfällt:** `injectOpenPixel()` (Brevo injiziert automatisch),
`createTransport().sendMail()` (ersetzt durch `sendViaBrevoApi()`).

**Was bleibt:** `buildUnsubscribeFooter()`, die eigene Abmeldelogik (`/api/unsubscribe`),
sowie `{{LEAD_HASH}}` und `{{BATCH_ID}}` für Unsubscribe-URL und `/api/track/click`.

### 3. messageId speichern

`outreach_send_log` bekommt eine Spalte `brevo_message_id text`. Wenn der Brevo-Webhook mit
`message-id` kommt, kann er exakt korreliert werden.

```sql
ALTER TABLE outreach_send_log
  ADD COLUMN IF NOT EXISTS brevo_message_id text;
```

### 4. Webhook-Handler bleibt

`/api/webhooks/brevo` bleibt unverändert. Er empfängt jetzt zuverlässiger `opened`- und
`click`-Events, weil Brevo diese über die API-Sends nativ trackt.

### 5. Tags-Konvention

| Outreach-Typ | Tags |
|---|---|
| Sendeplan-Batch | `["outreach", "sendeplan"]` |
| Persönlicher Versand | `["outreach", "persoenlich"]` |
| Entschuldigungs-Mail | `["outreach", "entschuldigung"]` |
| Custom | `["outreach", "custom"]` |

## Migrationspfad (SLF), Dateien in Reihenfolge

1. `src/lib/brevo-send.ts`, neuer Client (kein Produktions-Impact)
2. `src/app/api/cron/outreach/route.ts`, Hauptpfad, größter Impact
3. `src/lib/outreach-send.ts`, `sendPlannedBatch()`
4. `src/app/api/admin/outreach/send-persoenlich/route.ts`
5. `src/app/api/admin/outreach/send/route.ts`
6. `src/app/api/admin/outreach/send-apology/route.ts`
7. `src/app/api/admin/outreach/send-custom/route.ts`
8. `injectOpenPixel()` aus `email-unsubscribe-footer.ts` entfernen (oder als Fallback lassen)

## ENV-Variablen

| Variable | Zweck |
|---|---|
| `BREVO_API_KEY` | Transactional API Key |
| `BREVO_SMTP_USER` | Nur noch für SMTP-Pfade (Notifications, Buchungen) |
| `BREVO_SMTP_PASS` | Nur noch für SMTP-Pfade |

`BREVO_API_KEY` liegt in `/opt/secrets/slf/keys.env`.

## Audit-Checks

```bash
# Kein createTransport mehr in Outreach-Pfaden
grep -rn "createTransport" src/app/api/admin/outreach src/app/api/cron/outreach src/lib/outreach-send.ts

# Kein injectOpenPixel in Outreach-Pfaden
grep -rn "injectOpenPixel" src/app/api/admin/outreach src/app/api/cron/outreach

# Brevo-Client existiert
test -f src/lib/brevo-send.ts

# messageId-Spalte vorhanden
# → via DB-Migrationscheck
```

## Lesende Prüfung per API, Stolpersteine

Gemessen am 15.09.2026 bei der Vorfallprüfung F-112 (`werkstatt/bugs/F-112-…`), alle vier
Mandanten-Konten im Free-Plan, Aufruf von maxone-prod aus. Die Schlüssel stehen in der
Datenbank `outreach`, Tabelle `tenants`, Spalte `brevo_api_key`.

- **Ohne eigenen `User-Agent` sperrt Cloudflare.** `GET /v3/senders` mit dem Standard von
  Python-urllib: 403 „Error 1010: Access denied". Mit gesetztem User-Agent: 200.
- `GET /v3/smtp/statistics/reports`: höchstens 30 Tage je Aufruf, sonst 400 `out_of_range`.
  `aggregatedReport` nimmt auch 50 Tage.
- `GET /v3/emailCampaigns` mit `endDate` in der Zukunft: 400 „End date should not be greater
  than current date". Ohne Datumsfilter liefert `count` die Gesamtzahl. `status=scheduled`
  gibt es nicht (400 „Invalid value of status"), gültig sind u. a. `sent`, `queued`,
  `inProcess`, `draft`, `suspended`, `archive`, `inReview`.
- `GET /v3/organization/activities` (Anmeldungen, Schlüsselnutzung): 400 „Upgrade to
  Enterprise plan". **Ob ein Schlüssel lesend missbraucht wurde, ist im Free-Plan nicht
  messbar.**
- `GET /v3/whatsappCampaigns`: 403 „plan not eligible for using whatsapp".
- `GET /v3/transactionalSMS/statistics/aggregatedReport` mit `startDate=2026-05-01`,
  `endDate=2026-09-15`: 500 `invalid_request`, Ursache `[?]`.
- **Tragen:** `/account`, `/smtp/statistics/events?event=requests` (Betreff, Absender, Tag),
  `/contacts?limit=1` (`count`), `/contacts/lists`, `/processes` (Importe, Exporte),
  `/webhooks`, `/senders/domains`, `/smsCampaigns`.

## Nicht-Ziele

- Brevo-Template-Engine nutzen, unsere Templates bleiben in der DB, Rendering bei uns
- SMTP komplett abschalten, bleibt für Transaktional und Notifications
- Kontakt-Listen in Brevo pflegen, wir bleiben Source of Truth in Supabase
