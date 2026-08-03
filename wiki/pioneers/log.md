# Compile Log — pioneers

## Rollout-Dokumentation (2026-07-06)

**Trigger:** Rollout des wiki-compiler-Musters von den beiden Piloten (`maxone-mail-pilot`, `inventories`) auf die restlichen 6 Scopes. Kein Neu-Kompilieren — Inhalt (`INDEX.md`, `topics/concept.md`, `topics/implementation.md`, `topics/per-project.md`) bestand bereits vollständig. Keine der vier Dateien trägt ein explizites `last_updated`-Frontmatter; der jüngste im Content genannte Stand ist **2026-05-19** (Tier-Ergänzung bei voltfair, Punkt-Gewichte-Anhebung bei vanfree in `per-project.md`).

**Aktion:** `.wiki-compiler.json` nachträglich angelegt. `sources` nur aus den beiden konkreten Code-Zitaten in `implementation.md` übernommen (SLF-Referenzimplementierung der Early-Slot-Formel, voltfair als abweichendes Drift-Watch-Beispiel) — beide mit Datei+Zeilenangabe im Text belegt. `article_sections` an die drei bestehenden Topics angelehnt (Concept, Canonical Spec, Per-Project Status) plus einer eigenen Sektion "Drift Watch" für die im Content explizit markierten Abweichungen ("Weicht vom Standard ab. Nicht übernehmen.").

**Nicht als Source übernommen:** `pulse-config.ts` (vanfree, in `per-project.md` erwähnt als "enthält nur 3 der 5 Quellen") — im Text nur als Dateiname ohne Pfad genannt, kein Repo-Pfad belegt, daher ausgelassen statt geraten.

## Future Triggers

- Wenn ein neues Projekt ein Pioneers-Programm bekommt → `per-project.md` um einen Abschnitt erweitern, Checkliste aus `implementation.md` abarbeiten.
- Wenn vanfree `pulse-config.ts` um die fehlenden 2 Quellen (profile_photo, referral) ergänzt → per-project.md Status aktualisieren.
- Wenn ein Projekt von der kanonischen Early-Slot-Formel abweicht → in "Drift Watch" nachtragen, mit Grund.
