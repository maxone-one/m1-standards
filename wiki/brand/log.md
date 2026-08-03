# Compile Log — brand

## Rollout-Dokumentation (2026-07-06)

**Trigger:** Rollout des wiki-compiler-Musters von den beiden Piloten (`maxone-mail-pilot`, `inventories`) auf die restlichen 6 Scopes. Kein Neu-Kompilieren — Inhalt (`INDEX.md`, `visual-style.md`, `image-pipeline.md`, `photo-index.md`) bestand bereits vollständig und laufend erweitert. Kernregeln in `visual-style.md` seit "Festgelegt 2026-05-20", zuletzt inhaltlich erweitert **2026-06-27** (Geschlossenes Personen-Ensemble). `photo-index.md` "Angelegt 2026-06-26". `image-pipeline.md` trägt kein explizites Datum im Frontmatter, referenziert aber Standard 027 (maxone-standards) als kanonische Quelle.

**Aktion:** `.wiki-compiler.json` nachträglich angelegt. `sources` vollständig aus den expliziten "Sources"-Abschnitten in `image-pipeline.md` und `visual-style.md` sowie dem "Standards"-Abschnitt in `INDEX.md` übernommen (2× voltfair-GitHub-Codepfade, Standard 027, `ensemble.json` als Cast-SSoT, `MAX.md` → Brand-Foto-Setup). `article_sections` deckt alle drei inhaltlichen Artikel ab (Pflicht-Checkliste + Visual Style Rules aus visual-style.md, Image Pipeline, Photo Index) plus Summary/Sources.

**Nicht als Source übernommen:** "Entscheidung 2026-05-20 (Max + Claude-Session)" und "Erweiterung 2026-05-29" in `visual-style.md` "Sources" — das sind Ereignis-/Datums-Referenzen, keine Dateipfade.

## Future Triggers

- Wenn Vega (Video Production) oder Visor (QA Engineer) ein kanonisches Team-Portrait bekommen → Coverage-Stand in visual-style.md aktualisieren (aktuell 11 von 13 KI-Team-Mitgliedern abgedeckt).
- Wenn `ensemble.json` um eine neue Figur erweitert wird → Cross-Check gegen "Geschlossenes Personen-Ensemble"-Regel.
- Wenn ein neues Foto in `apps/*/static/images/` entsteht → sofort in `photo-index.md` nachtragen (Pflicht laut Artikel selbst).
- Wenn Standard 027-image-pipeline geändert wird → `image-pipeline.md` gegenprüfen (Standards gewinnen bei Konflikt).
