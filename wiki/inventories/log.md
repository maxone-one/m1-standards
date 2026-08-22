# Compile Log — inventories

## 2026-07-06 — Compiler-Config nachgezogen (Lint-Fund)

**Trigger:** Direktvergleich mit Andrej Karpathys "LLM Wiki"-Pattern (nuc-optimizer-Session). Fund: `inventories` hatte bereits `schema.md` + `log.md`, aber kein `.wiki-compiler.json` wie der `maxone-mail-pilot`-Pilot. Zusätzlich fehlte der Scope komplett im "Wiki-Status"-Abschnitt von `~/.claude/INDEX.md`, obwohl 7 Topics aktiv sind (nur `telegram` hat einen Log-Eintrag).

**Aktion:** `.wiki-compiler.json` nach mail-pilot-Vorbild angelegt (Sources, article_sections aus schema.md übernommen, topic_hints auf alle 7 vorhandenen Topics erweitert). `INDEX.md` Wiki-Status um `inventories` und `vanfree` ergänzt.

**Offen:** Compile-Log-Einträge für `brevo-accounts`, `mail-aliases`, `paperclip`, `runners`, `servers`, `vector-ops` fehlen noch (nur `telegram` dokumentiert). Beim nächsten Anfassen jeweils nachtragen.

## 2026-05-04 — Initial scope

**Trigger:** Max-Direktive 2026-05-04 — "solche Sachen müssen alle in der
Wiki zusammengetragen werden". Auslöser war eine Frage nach Telegram-IDs,
die ich gestellt habe obwohl die Antwort längst im Secret-Store + in
verstreuten Memory-Einträgen lag.

**Sources verarbeitet:**
- `/opt/secrets/karastelev/telegram.env` (Max User-ID + Schreibstudio-Bot)
- `/opt/secrets/vector/keys.env` (Schaltzentrale-Chat-ID + Vector-Bot)
- `/opt/secrets/global/telegram.consumers.md` (Bot-Token-Konsumenten-Inventar, unvollständig)
- `/opt/slf-mail-bridge/.env` (slf-mail-bridge Token + Chat)
- `/opt/zentinel-vigil/.env` (zentinel-vigil — wiederverwendet slf-bridge-Token)
- `~/.claude/memory/telegram-kunden-kopie-an-max.md` (chat_id 8029592472 explizit)

**Output:**
- 1 Topic: `telegram` (Bots, Chat-IDs, User-IDs, Konsumenten)
- 0 Concepts (kein Cross-Cutting nötig bei einem Topic)

**Outcomes:**
- Memory-Einträge `telegram-ids-inventory.md` und
  `vigil-ist-weiblich-anrede.md` bleiben (das eine ist Pointer, das andere
  reine Verhaltensregel).
- Architektur-Lücke dokumentiert: keine zentrale `telegram.directory.md`
  im Secret-Store; `consumers.md` veraltet.

## Future Triggers

- Wenn slf-mail-bridge gestoppt wird → Tabellenzeile entfernen.
- Wenn neuer Bot eingeführt wird → Tabelle erweitern + secret-store
  consumers.md updaten.
- Wenn Token rotiert wird → "Last verified rotation"-Datum setzen.
