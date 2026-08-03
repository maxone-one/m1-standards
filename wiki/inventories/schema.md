# Wiki Schema — inventories

Strukturkonventionen für die `inventories`-Wiki.

**Zweck:** Lookup-Wissen konsolidieren. Wenn eine Frage "wo / wer / welche ID"
nur durch Greppen über mehrere Quellen beantwortet werden kann, gehört das
Inventar hierher.

**Nicht hier:** Architektur-Erklärungen, Regeln, Failure-Modes — die gehören
in projektspezifische Wikis (z.B. `maxone-mail-pilot`).

## Topic-Aufbau

Jedes Inventar-Topic folgt dieser Struktur:

- **Summary** — was hier zu finden ist, in 2-3 Sätzen
- **Source-of-Truth** — die Datei(en) mit den authoritativen Werten + Lookup-Befehl
- **Tabelle(n)** — strukturiertes Inventar (eine Zeile pro Eintrag)
- **Operational Patterns** — wie hinzufügen, ändern, rotieren
- **Architektur-Lücken** — was fehlt, wo der Workflow noch nicht sauber ist
- **Sources** — Backlinks zu jeder Quelldatei

Die Tabelle ist das Herzstück. Felder je Topic unterschiedlich, aber:
- erste Spalte = Identifier (z.B. ID, Name)
- letzte Spalte = Quelldatei oder Kommando
- Datums-Felder im Format `YYYY-MM-DD`

## Naming Conventions

- Topic slugs: lowercase-kebab-case
- Files: `{topic-slug}.md` in `topics/`
- Dates: YYYY-MM-DD
- Links: Obsidian `[[wikilinks]]`

## Cross-Reference Rules

- Wenn ein Inventar-Eintrag in einer Domain-Wiki tiefer erklärt ist (z.B.
  Stalwart-Account-Konfiguration), Pointer dorthin.
- Inventur-Datei darf NIE Source-of-Truth sein — sie spiegelt nur. Bei
  Konflikt: die referenzierte `.env` / Config gewinnt.
- Nach jeder Source-Änderung: Wiki im selben Commit/Sprint nachziehen.

## Evolution Log

- 2026-05-04: Initial schema. Erstes Topic `telegram`.
