# Funktionsbasierte Mail-Aliasse pro Projekt-Domain

**Last updated:** 2026-05-23
**Coverage:** stub — pro Projekt-Welle gefuellt waehrend Brevo-Multi-Account-Rollout
**Source-Briefing:** `c:/Users/max/Projects/Zentinel/briefings/BRIEF-BREVO-MULTIACCOUNT-2026-05-22.md`

## Summary

Pro Projekt-Domain 12 funktionsbasierte Aliase. **11 davon** sind Inbound-Aliase
und werden in Stalwart auf `inbox@<domain>` zugestellt. **1 davon** (`noreply@`)
ist sender-only, lebt nur in Brevo, kein Stalwart-Routing.

Bei Provider-Wechsel (z.B. Brevo → Postmark) wandert nur das eine Alias-Routing,
nicht die Owner-Account-Mail.

## Alias-Liste (12, gilt pro Domain)

| Alias | Routing | Zweck |
|---|---|---|
| `admin@` | → `inbox@` | Owner-Root, Domain-Verifikation, Recovery |
| `billing@` | → `inbox@` | Zahlungsmittel (Mollie, PayPal, Amex, SEPA) |
| `mail@` | → `inbox@` | Mail-Versand-Provider (Brevo-Owner-Login) |
| `dns@` | → `inbox@` | Registrar + DNS (INWX, Cloudflare) |
| `cloud@` | → `inbox@` | Infra/Hosting (Hetzner, Supabase) |
| `dev@` | → `inbox@` | Dev-Tools (GitHub, Sentry, Logflare) |
| `legal@` | → `inbox@` | Rechtliches (Impressum, DSGVO) |
| `support@` | → `inbox@` | Kunden-Mail (B2C Inbound) |
| `dmarc@` | → `inbox@` | DMARC-RUA/RUF-Reports |
| `postmaster@` | → `inbox@` | RFC 2142 Pflicht |
| `abuse@` | → `inbox@` | RFC 2142 Pflicht |
| `noreply@` | — (sender-only) | Brevo Transactional Outbound; KEIN Stalwart-Alias |

## Projekt-Status

| # | Projekt | Domain | inbox@ | 11 Aliase | noreply@ (Brevo) | Welle |
|---|---|---|---|---|---|---|
| 1 | vanfree | venfree.de | `inbox@venfree.de` live | 11 + `edu@` live (Stalwart) | pending (Brevo-Ticket #5377727) | 1 |
| 2 | viktoria-from | viktoria-from.de | `hey@` (Bestand) + `mail@` → `hey@` | pending | pending | 2 |
| 3 | plansey | plansey.com | `info@` (Bestand) | pending | pending | 3 |
| 4 | voltfair | voltfair.de | pending | pending | pending | 4 |
| 5 | snapflow.one | snapflow.one | pending | pending | pending | 5 |
| 6 | repivot | repivot.in | pending | pending | pending | 6 |
| 7 | vybora | vybora.dev | pending | pending | pending | 7 |
| 8 | stadt-lahn | stadtlahnfluss.de (pending) | `max@` (Bestand) | pending | pending | 8 |

Bestaende werden nach Welle 2/3/8 in `inbox@`-Konvention migriert, ODER per
Alias-Routing eingebunden (z.B. viktoria-from: `mail@` → `hey@` zusaetzlich).

## Operational Patterns

- **Pro Domain genau EIN Mail-Empfangs-Postfach** (`inbox@<domain>` oder
  bestehender Name). Aliase enden alle dort.
- **Kein Catch-all** `*@<domain>` — Spam-Magnet.
- **Keine Plus-Adressen** (`admin+brevo@`) — manche Provider stripen sie.
- **`noreply@` nicht als Stalwart-Alias konfigurieren** — wenn jemand dorthin
  antwortet, fliegt die Mail mit MX-Lookup ueberhaupt erst zum Server. Lieber
  in Stalwart als `discard`-Route, dann landet sie nicht in `inbox@`.
- **`postmaster@` + `abuse@` MUESSEN zustellbar sein** (RFC 2142) — sonst sinkt
  Reputation bei ISPs.
- **`dmarc@` separat** halten — RUA-Reports fluten sonst die Owner-Inbox.

## Failure Modes

- **`noreply@` aus Versehen als Alias konfiguriert** → Bounces aus Brevo landen
  in `inbox@`, statt in Brevo selbst. Pruefung: `dig MX <domain>` zeigt
  Stalwart-Host, dann `stalwart-cli alias list <domain>` darf `noreply@` NICHT
  enthalten.
- **Plus-Adressen-Stolperfalle** bei externer Registrierung (Brevo, Mollie):
  manche akzeptieren `admin+brevo@`, andere stripen — nie verlassen.
- **Alias-Konflikt zwischen Projekten:** ausgeschlossen, weil alle Aliase FQDN-
  spezifisch sind (`admin@venfree.de`, nicht `admin`).

## Sources

- Briefing: `c:/Users/max/Projects/Zentinel/briefings/BRIEF-BREVO-MULTIACCOUNT-2026-05-22.md`
- RFC 2142 (mailbox names for common services)
- Standard 016-mail
- Wiki [[brevo-accounts]] — Owner-Accounts pro Projekt
- Wiki [[servers]] — Stalwart auf maxone-prod
