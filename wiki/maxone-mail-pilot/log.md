# Compile Log

## 2026-05-02 — Refactor (Phase A + B in einem Pass)

**Topics updated:** mail-architecture, zentinel-rules, secrets-tls
**New topics:** failure-modes (extrahiert aus mail-architecture + zentinel-rules)
**Concepts replaced:** brevo-vs-stalwart → silent-failures (größeres cross-cutting Frame)
**Sources scanned:** 4 (ZENTINEL-STALWART-BIBEL.md, ~/.claude/CLAUDE.md mail-Blöcke, 2 Memory-Dateien)
**Sources changed:** 0 (Quellen unverändert seit Initial Compile, refactor war pure Output-Anpassung)

**Drift-Korrekturen gegenüber Plugin-Spec (Phase A):**
- Coverage-Tags umgestellt: vorher pro Artikel, jetzt **pro Section** (Plugin-Spec Phase 3 §7)
- Time-decay: Summary-Sektionen führen jetzt mit Source-Date-Range (Plugin-Spec Phase 3 §8)
- INDEX.md auf Tabellen-Format mit "Also Known As"/Aliases (Plugin-Spec Phase 4)
- schema.md auf Template-Format mit Topics/Concepts/Article-Structure/Naming-Conventions/Cross-Ref-Rules/Evolution-Log
- Concept-Frontmatter angepasst: `concept`, `last_compiled`, `topics_connected`, `status`
- Concept-Format umgestellt auf Pattern / Instances / What This Means / Sources (Plugin-Spec Phase 3.5)
- `.compile-state.json` mit `source_locations`, `total_sources_scanned`, `concepts` ergänzt
- Topic-Frontmatter um `source_count` und `status: active` ergänzt

**Strukturelle Refactors (Phase B):**
- failure-modes als eigenes Topic — vorher waren die 4 Vorfälle in mail-architecture#failure-modes UND zentinel-rules#failure-modes dupliziert, jetzt Single-Source-of-Truth in `failure-modes.md`. Andere Topics nutzen 1-2-Zeilen-Pointer mit `[[failure-modes#YYYY-MM-DD]]`.
- Concept-Wechsel: `brevo-vs-stalwart` paraphrasierte mail-architecture nur. Neuer Concept `silent-failures` trägt eine echte cross-cutting Erkenntnis (200-OK-aber-Outcome-fehlt durch alle Schichten — Stalwart, Brevo, RocksDB, Frontend).
- schema.md getrimmt: vorher Container-/Code-Pfad-Karten (duplizierte mail-architecture), jetzt reine Topic/Concept-Liste + Naming-Conventions + Cross-Ref-Rules.

**Wiki-first Durchsetzung (Phase C):**
- Block in `c:/Users/max/Projects/maxone.one/CLAUDE.md` ergänzt: "Bei Mail-Fragen → Wiki zuerst, Bibel nur für Tiefe / unbekannte Vorfälle". Pflicht-Pfad: `~/.claude/wiki/maxone-mail-pilot/INDEX.md`.

## 2026-05-02 — Initial pilot compile (manual)

**Compiler:** Manual run (LLM following the wiki-compiler 5-phase algorithm by hand). Plugin nicht installiert — `~/.claude/wiki/maxone-mail-pilot/` ist ein lokaler Standalone-Pilot außerhalb jedes Repos.

**Phase 1 — Scan:**
- Primäre Quelle: `c:/Users/max/Projects/maxone.one/briefings/ZENTINEL-STALWART-BIBEL.md` (343 Zeilen, 22 Regeln, 4 Vorfälle)
- Sekundär: `~/.claude/CLAUDE.md` Mail-Blöcke (Zentinel/Stalwart/Mail-Bibel-Pflicht, Stalwart-Fehler-Lehren, Secrets-Hierarchie, Zentraler Secrets-Store, TLS-DNS-01-only)
- Memory-Files: keine direkt mail-relevant

**Phase 2 — Klassifizierung:**
- Initial: 3 Topics (mail-architecture, zentinel-rules, secrets-tls), 1 Concept (brevo-vs-stalwart)
- Topic-Hint-Mapping: jede Bibel-Regel einer Klasse zugeordnet (Verbot / Pflicht / Code-Pattern)

**Phase 3-5:** Initial articles geschrieben — siehe Refactor-Eintrag oben für die nach-Korrekturen.

## Was nicht im Pilot ist

- ZENTINEL-KNOWLEDGE-BASE.md (1003 Zeilen) — bewusst weggelassen, Pilot soll testen ob die Bibel allein genug Wert trägt
- ZENTINEL-K3-DRILL-RUNBOOK.md, ZENTINEL-MONETIZATION-ROADMAP.md, ZENTINEL-PHASE0-TRACKER.md — referenziert in [[schema]], aber nicht eingelesen
- Vector-Knowledge-Mirror (`C:/Users/max/Projects/vector/knowledge/`) — separate Pipeline
- Code-Inhalt von `email-client/handlers/send.ts` und `EmailDetail.svelte` — nur referenziert, nicht eingelesen (knowledge mode)

## Nächste Schritte (offen)

- **Plugin tatsächlich installieren** und denselben Compile durchlaufen lassen — Self-Test ob mein manueller Output dem Plugin-Output entspricht. Aktuell `spec_aligned: true` als best-effort-Behauptung, nicht verifiziert.
- **Source-Hashes** für Auto-Stale-Detection (Plugin macht das anscheinend automatisch via PostCompact-Hook; manuell nicht).
- **ZENTINEL-KNOWLEDGE-BASE.md ergänzen** wenn Bibel-only-Pilot Lücken hat (der "spec coverage low" auf Notable Failures in mail-architecture deutet darauf hin).
