# Telegram — Bots, Chat-IDs, Konsumenten

**Last updated:** 2026-05-04
**Coverage:** high — alle aktiven Bots/Chats verifiziert via `getMe` und Service-`.env`-Walk

## Summary

Max betreibt zwei Telegram-Bots: einen geteilten **VECTOR-Bot** (`@hey_vectorbot`),
den alle automatisierten Notification-Quellen verwenden, und einen
projektspezifischen **Schreibstudio-Bot** (`@Schreibstudio_Bot`) nur für
karastelev.de. Nachrichten gehen entweder in die **Schaltzentrale-Supergroup**
(`-1003748244504`, Audit-Trail + Ops) oder direkt an **Max' privaten Chat**
(`8029592472`).

Die Quelldateien für IDs sind im Secret-Store auf maxone-prod verstreut.
Source-of-Truth ist je Konsument die jeweilige `.env` — diese Wiki spiegelt nur.

## Source-of-Truth

| Information | Datei (auf maxone-prod, sofern nicht anders) | Lookup-Befehl |
|---|---|---|
| Max User-ID `8029592472` | `/opt/secrets/karastelev/telegram.env` (`TELEGRAM_ALLOWED_CHAT_IDS`) | `grep TELEGRAM_ALLOWED_CHAT_IDS /opt/secrets/karastelev/telegram.env` |
| Schaltzentrale `-1003748244504` | `/opt/secrets/vector/keys.env` (`TELEGRAM_ALLOWED_CHAT_ID`) | `grep TELEGRAM_ALLOWED_CHAT_ID /opt/secrets/vector/keys.env` |
| VECTOR-Bot-Token | `/opt/secrets/vector/keys.env` (`TELEGRAM_BOT_TOKEN`) | (token) |
| Schreibstudio-Bot-Token | `/opt/secrets/karastelev/telegram.env` (`TELEGRAM_BOT_TOKEN`) | (token) |
| Konsumenten-Inventar (alt) | `/opt/secrets/global/telegram.consumers.md` | unvollständig — gilt nur für VECTOR-Bot, listet nur 2 von 5 Konsumenten |

Volle ID-Suche: `grep -rln '<gesuchte-id>' /opt/secrets/`

## Chat- und User-IDs

| ID | Typ | Bezeichnung | Verwendet von |
|---|---|---|---|
| `8029592472` | private (User) | Max Karastelev persönlich | Schreibstudio-Bot, zentinel-vigil (Privatchat) |
| `-1003748244504` | supergroup | Schaltzentrale | VECTOR, slf-mail-bridge, zentinel-vigil (Spam-Audit), maxone-watchdog Kuma |
| `-1003748244504` Thread `70` | supergroup forum-topic | Schaltzentrale → Watchdog-Topic | maxone-watchdog Kuma (`telegramMessageThreadID=70`) |

## Bots

| Bot-Name | Username | Bot-ID | Zweck |
|---|---|---|---|
| VECTOR | `@hey_vectorbot` | `8461005808` | Geteilter Notification-Bot für alle automatisierten Ops-Quellen |
| Schreibstudio | `@Schreibstudio_Bot` | `8701513347` | karastelev.de / Schreibstudio (separate Identität, eigener Token) |

`getMe`-Verifikation: `curl -s "https://api.telegram.org/bot$TOKEN/getMe"`.

## Bot-Konsumenten

Welcher Service nutzt welchen Bot und schreibt in welchen Chat?

| Konsument | Standort | Bot | Default-Chat | Sonderzweck |
|---|---|---|---|---|
| VECTOR (maxone-Agent) | maxone-prod `/opt/vector/.env` | VECTOR | Schaltzentrale | Web-Chat + TG-DMs an Kunden, "Kopie an Max" → User-ID `8029592472` |
| slf-mail-bridge | maxone-prod `/opt/slf-mail-bridge/.env` | VECTOR | Schaltzentrale | IMAP-Forwarder für `max@stadtlahnflow.de` (wird durch zentinel-vigil abgelöst) |
| zentinel-vigil | maxone-prod `/opt/zentinel-vigil/.env` | VECTOR | Privatchat (`8029592472`) für non-spam, Schaltzentrale für spam | Inbox-AI für `max@stadtlahnflow.de` |
| maxone-watchdog Kuma | Falkenstein `167.235.226.129`, Kuma SQLite (`watchdog-kuma:/app/data/kuma.db`, `notification` table) | VECTOR | Schaltzentrale Thread 70 | Uptime-Alerts, Failsafe (Vector-Webhook ist primary) |
| Schreibstudio | maxone-prod `/opt/secrets/karastelev/telegram.env` | Schreibstudio | Max User-ID | karastelev.de Telegram-Integration |

## Operational Patterns

### Telegram-User-ID einer Person ermitteln
1. Person schreibt einmalig dem Bot in DM.
2. Bot-Owner ruft Update-Stream ab:
   `curl -s "https://api.telegram.org/bot$TOKEN/getUpdates" | jq '.result[].message.from'`
3. `id`-Feld notieren — das ist die User-ID. In Memory/Konfig speichern, nicht erneut fragen.

### Neuen Konsumenten anlegen
1. Service nutzt **immer** den VECTOR-Bot, außer es ist eine eigene Marke (wie Schreibstudio).
2. Token aus `/opt/secrets/vector/keys.env` (`TELEGRAM_BOT_TOKEN`) ins Service-`.env` kopieren.
3. Standard-Chat-ID = Schaltzentrale (`-1003748244504`). Privater Pfad nur wenn explizit gewünscht.
4. Diese Wiki-Tabelle ergänzen + `/opt/secrets/global/telegram.consumers.md` updaten.

### Bot-Token-Rotation (VECTOR-Bot)
Reihenfolge zwingend, um keinen Konsumenten zu verwaisen:
1. @BotFather neuen Token generieren — alten NICHT löschen.
2. `/opt/secrets/vector/keys.env` updaten (Source-of-Truth).
3. Alle Konsumenten in der Tabelle oben (vector, slf-mail-bridge, zentinel-vigil, watchdog-kuma) updaten + verifizieren.
4. Erst dann alten Token via @BotFather widerrufen.
5. "Last verified rotation" hier notieren.

**Last verified rotation:** never — Token aus Initial-Setup, noch nie rotiert.

### Schaltzentrale Forum-Threads
Schaltzentrale ist eine Supergroup mit Forum-Topics (`is_forum: true`).
Thread-IDs via `telegramMessageThreadID` (Kuma) oder
`message_thread_id` Parameter beim sendMessage. Aktuell genutzt: Thread `70`
für Watchdog-Alerts. Andere Threads existieren, aber nicht systematisch
inventarisiert — bei Bedarf via Bot mit `getForumTopicIconStickers`/Web-UI prüfen.

## Architektur-Lücken

1. **Keine zentrale Telegram-Directory.** IDs liegen in 5+ Dateien.
   Vorschlag: `/opt/secrets/global/telegram.directory.md` (nicht
   `consumers.md`, das ist nur für Bot-Konsumenten gedacht) als Master mit
   allen User-IDs / Chat-IDs / Bot-Mappings. Diese Wiki-Datei wäre dann
   ein Mirror.

2. **`telegram.consumers.md` veraltet** — listet nur 2 von 5 Konsumenten
   (vector + watchdog-kuma fehlen slf-bridge, zentinel-vigil, schreibstudio).
   Beim nächsten Token-Touch nachziehen.

3. **slf-mail-bridge wird abgelöst** — sobald zentinel-vigil 24h stabil ist,
   bridge stoppen und Tabellen-Zeile entfernen.

## Sources

- `/opt/secrets/karastelev/telegram.env` — Max User-ID + Schreibstudio-Bot-Token
- `/opt/secrets/vector/keys.env` — VECTOR-Bot-Token + Schaltzentrale-Chat-ID
- `/opt/secrets/global/telegram.consumers.md` — Bot-Konsumenten-Inventar (unvollständig)
- `/opt/slf-mail-bridge/.env` — slf-mail-bridge wiederverwendet VECTOR-Bot
- `/opt/zentinel-vigil/.env` — zentinel-vigil wiederverwendet VECTOR-Bot
- `watchdog-kuma:/app/data/kuma.db` (notification table, id=1) — Kuma Telegram-Notification-Config (Falkenstein)
- `~/.claude/memory/feedback_telegram_kunden_kopie_an_max.md` — Verhaltensregel: Bot-Nachrichten an Kunden gehen Kopie an User-ID `8029592472`
