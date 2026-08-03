# Wiki Schema

This file defines the structure and conventions for the maxone-mail-pilot knowledge base. Generated on first compile, co-evolved between human and LLM on subsequent runs.

**Human:** You can edit this file to rename topics, merge them, add conventions, or change the article structure. The compiler respects your changes on the next run.

**Compiler:** Read this file before classifying sources. Follow its conventions. Add new topics here when discovered. Never remove topics without human approval.

## Topics

- `mail-architecture`: Brevo + Stalwart split, Send-Pipeline, JMAP-Adressierung, Diagnose-Reihenfolge
- `zentinel-rules`: Die 22 unverhandelbaren Regeln, gruppiert in Verbote / Pflichten / Code-Patterns
- `secrets-tls`: Secrets-Hierarchie, `SUPABASE_SERVICE_ROLE_KEY`-Verkettung mit `jmap_password`, DNS-01-only für TLS
- `failure-modes`: Postmortems der vier großen Mail-Vorfälle (2026-03-24, 2026-04-05, 2026-04-10, 2026-04-28)

## Concepts

Cross-cutting patterns that span 3+ topics. Interpretive, not just factual.

- `silent-failures`: 200-OK-aber-Outcome-fehlt-Fehlerklasse durch alle Schichten — connects [mail-architecture, zentinel-rules, failure-modes]

## Article Structure

Each topic article follows the configured `article_sections`:
- **Summary** [coverage] — standalone briefing, führt Datums-Range, 2-3 Absätze
- **Architecture** [coverage] — Komponenten, Datenflüsse, Container/Service-Layout
- **Key Rules** [coverage] — unverhandelbare Regeln und ihre Begründung
- **Notable Failures** [coverage] — Verweise auf failure-modes mit 1-2-Zeilen-Pointer (failure-modes selbst hat hier die Vollversion)
- **Operational Patterns** [coverage] — sichere Befehle, Recovery-Reihenfolgen
- **Sources** — Backlinks zu jeder Quelldatei

Coverage tags pro Section: `[coverage: high -- N sources]`, `[coverage: medium -- N sources]`, `[coverage: low -- N sources]`.

## Naming Conventions

- Topic slugs: lowercase-kebab-case
- Files: `{topic-slug}.md` in `topics/`, `{concept-slug}.md` in `concepts/`
- Dates: YYYY-MM-DD format everywhere
- Links: Obsidian `[[wikilinks]]` mit relativen Pfaden von `topics/`
- Konzept-Verweise aus Topics: `[[../concepts/silent-failures]]`
- Topic-Verweise aus Concepts: `[[../topics/failure-modes]]`

## Cross-Reference Rules

- Topics that share 3+ sources sollten sich gegenseitig in Summary oder Key Rules referenzieren.
- **Failure Modes sind Single-Source-of-Truth** in `failure-modes.md`. Andere Topics nennen Vorfälle nur als 1-2-Zeilen-Pointer und verlinken nach `failure-modes#YYYY-MM-DD`.
- Cross-cutting concepts (silent-failures) werden aus jedem Topic referenziert, das eine Instanz beisteuert.
- Wenn eine Regel mehrere Topics berührt, lebt sie nur in `zentinel-rules.md` und wird von anderen Topics verlinkt (`[[zentinel-rules#regel-N]]`).

## Evolution Log

- 2026-05-02: Initial schema generated. 4 Topics (mail-architecture, zentinel-rules, secrets-tls, failure-modes), 1 Concept (silent-failures). Manual compile run — Plugin nicht installiert.
- 2026-05-02: Refactor — failure-modes als eigenes Topic extrahiert (war zuvor in mail-architecture und zentinel-rules dupliziert). Concept brevo-vs-stalwart durch silent-failures ersetzt (größere cross-cutting Tiefe). Coverage-Tags auf Section-Ebene umgestellt.
