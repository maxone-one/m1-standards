# Compile Log — kitchen-station

## Rollout-Dokumentation (2026-07-06)

**Trigger:** Rollout des wiki-compiler-Musters (`.wiki-compiler.json` + `log.md`) von den beiden Piloten (`maxone-mail-pilot`, `inventories`) auf die restlichen 6 Scopes. Kein Neu-Kompilieren — der Wiki-Inhalt (INDEX.md, `bugs.md`, `topics/architecture.md`, `topics/custom-kiosk-app.md`, `topics/tablet-ops.md`) bestand bereits vollständig, zuletzt inhaltlich verändert am **2026-05-18** (jüngste Frontmatter-/Bug-Einträge in `bugs.md`; INDEX + drei Topic-Artikel selbst tragen `last_updated: 2026-05-11`).

**Aktion:** `.wiki-compiler.json` nachträglich angelegt, `article_sections` aus dem tatsächlichen Aufbau der bestehenden Artikel abgeleitet (Architecture, Bug-Protokoll als eigene Sektion analog zum "Failure Modes"-Muster aus mail-pilot, Operational Patterns, Open Issues für den verlorenen Kiosk-App-Source). `sources` nur aus explizit im Content zitierten Pfaden übernommen (Bootstrap-PRD, Projekt-CLAUDE.md, Registry, Deploy-Workflow, ein Memory-Dateiname ohne vollen Pfad).

**Nicht übernommen:** Git-Commit-Hashes (`0842b9d`, `a1d22db`, `c98232e`, `0b76485`, `1725df4` etc.), die in `bugs.md` und `custom-kiosk-app.md` als Belege dienen — das sind keine Dateipfade, sondern Commit-Referenzen im Repo `maxone-one/kitchen-station`. Nicht als `sources`-Eintrag geführt, aber im Artikelinhalt selbst weiter sichtbar.

## Future Triggers

- Wenn die Kiosk-App-Source rekonstruiert oder neu gebaut wird → `custom-kiosk-app.md` Status ändert sich, echter Compile-Lauf fällig.
- Wenn ein neuer Bug in `bugs.md` einträgt → Topic-Hint `bugs` aktualisieren.
- Wenn Viktoria From nicht mehr einzige Kundin ist (weiteres Kitchen-Station-Deployment) → Architektur-Artikel auf Mehr-Kunden-Fall erweitern.
