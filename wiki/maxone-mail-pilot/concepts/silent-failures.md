---
concept: Silent Failures Across the Stack
last_compiled: 2026-05-02
topics_connected: [mail-architecture, zentinel-rules, failure-modes]
status: active
---

# Silent Failures Across the Stack

## Pattern

In der Mail-Pipeline liegt das größte Risiko nicht bei lautem Versagen (5xx, Throw, Crash), sondern bei **stillschweigendem Erfolgs-Schein**. Mehrere Schichten der Pipeline antworten "OK" oder schreiben "sent" — auch wenn das eigentliche Outcome (Mail zugestellt? Sent-Kopie gespeichert? Anhang sichtbar?) **nicht eingetreten ist**. Jeder Vorfall in [[../topics/failure-modes]] hatte mindestens eine silent-failure-Komponente; mehrere hatten silent-failure als **alleinigen** Trigger.

Die strukturelle Ursache: jede Schicht (Brevo, Stalwart, RocksDB, Frontend) hat ihren eigenen "alles in Ordnung"-Zustand. Diese Zustände komponieren nicht. Brevo-OK + Stalwart-OK + DB-OK + UI-OK heißt nicht "Mail erfolgreich verarbeitet". Wer einer einzelnen Schicht glaubt, baut Diagnose-Werkzeuge, die genau die wichtigsten Fehler nicht erkennen.

## Instances

- **2026-04-10** in [[../topics/failure-modes]] / [[../topics/mail-architecture]]: **Stalwart `Email/import` antwortet 200 ohne Side-Effect**, wenn der referenzierte Blob in einem fremden Account liegt. `try/catch` fängt nichts. 7 Sent-Kopien gingen 5 Tage lang verloren.
- **2026-04-10** in [[../topics/failure-modes]] / [[../topics/mail-architecture]]: **Brevo schreibt intern `event=error` nach Rückgabe einer `messageId`**. DB-Logik schreibt `status='sent'` weil sie der `messageId` glaubt. Empfänger meldet 7 Tage später dass nichts angekommen war.
- **2026-03-24** in [[../topics/failure-modes]] / [[../topics/zentinel-rules]]: **Stalwart RocksDB hat Vorrang vor `config.toml` ohne Hinweis**. Wer Passwörter in der Config ändert, sieht in der Config dass es geändert ist — Stalwart liest die Änderung gar nicht. 30 Min Diagnose-Zeit verloren.
- **2026-04-05** in [[../topics/failure-modes]] / [[../topics/zentinel-rules]]: **`unban-stalwart.sh` jq-Filter `.data.items[]?` zog 0 Keys** weil Stalwart `.data.items` als Map liefert (nicht Array). Skript meldete "alles in Ordnung". Restart-Loop lief weiter.
- **2026-04-28** in [[../topics/failure-modes]] / [[../topics/mail-architecture]]: **Frontend-Filter `!a.cid` blendet Anhänge aus ohne Sichtbarkeit**. UI zeigt keinen "ich habe etwas gefiltert"-Hinweis. User sieht keine Mail mit Anhang, weil er den Anhang nicht sieht — und nimmt an, dass keiner kam.
- **2026-04-28** in [[../topics/failure-modes]]: **Traefik Round-Robin zwischen Blue+Green** ohne Banner, ohne Logs. User sieht den Fix in 50 % der Requests, in 50 % nicht. "Ich hab doch deployed" und "ist nicht live" sind beide wahr.

## What This Means

Drei strategische Implikationen:

1. **Trau keinem 200, wenn das Outcome außerhalb der Antwort liegt.** Wenn dein Code "Send-Erfolg" auf "Brevo-200" reduziert, hast du den Outcome nicht geprüfte. Brevo-200 = "wir haben deine Anfrage akzeptiert", nicht "wir haben sie zugestellt". Stalwart-200 auf `Email/import` = "Request war wohlgeformt", nicht "der Blob existiert in deinem Account". **Verifikation muss out-of-band passieren** — separater Endpunkt, separater Zustand, separater Test. Genau das ist `ensureBrevoDomainAuthenticated()` (Pre-Flight) und der Brevo-Bounce-Watchdog (Post-hoc).

2. **Frontend-Filter brauchen einen "ich habe gefiltert"-Indikator.** `EmailDetail.svelte:106` war ein Beispiel: ein einzeiliger Filter ohne Sichtbarkeit. Wenn ein Filter K1 (Null Datenverlust) gefährden kann, MUSS der User sehen können, dass er filterte — auch dann, wenn der Filter aktuell richtig wäre. Sonst wird ein Bug in dem Filter erst durch Glück (Mail-Größen-Diff) entdeckt.

3. **Defense-in-Depth ist nicht "extra Vorsicht", sondern Pflicht.** Jede Regel im [[../topics/zentinel-rules]]-Set adressiert nur eine Schicht. Regel 12 (Disziplin) hatte 2026-04-03 nicht ausgereicht; Regel 20 (Code) muss als zweite Verteidigung dazu kommen. Jeder neue Pipeline-Bug, der "silent" sein kann, braucht **mindestens zwei** unabhängige Detection-Pfade — sonst liegen wir ein-fail entfernt vom nächsten 7-Tage-Outage.

## Sources

- [[../topics/failure-modes]]
- [[../topics/mail-architecture]]
- [[../topics/zentinel-rules]]
