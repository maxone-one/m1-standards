# Compile Log — conventions

## Rollout-Dokumentation (2026-07-06)

**Trigger:** Rollout des wiki-compiler-Musters von den beiden Piloten (`maxone-mail-pilot`, `inventories`) auf die restlichen 6 Scopes. Kein Neu-Kompilieren — Inhalt (`INDEX.md`, `topics/environment-terminology.md`) bestand bereits vollständig. `INDEX.md` trägt explizit "Last compiled: 2026-05-12"; `environment-terminology.md` bestätigt denselben Stand ("Definitionen (verbindlich, 2026-05-12)", "Staging-Architektur (Stand 2026-05-12)").

**Aktion:** `.wiki-compiler.json` nachträglich angelegt. `mode: lookup` gewählt (analog zu `inventories`, nicht `knowledge` wie mail-pilot), weil der Scope im Kern eine verbindliche Begriffs-Tabelle ist, keine narrative Wissensbasis.

**Quellenlage (ehrlich):** Der einzige im Content gefundene Doku-Verweis ist "Details: Standard 006-domain-policy" (unter "Infra-Hostname-Konvention"). Das ist eine Registry-/Standard-Nennung ohne vollständigen Dateipfad im Text — der Pfad `maxone-standards/standards/006-domain-policy` in `.wiki-compiler.json` ist nach der estate-weiten Standards-Konvention rekonstruiert, NICHT wörtlich aus dem Wiki-Content belegt. Die übrigen "Quelle"-Angaben in `environment-terminology.md" ("User-Direktive 2026-05-12", "User-Korrektur 2026-05-12") sind mündliche Direktiven, keine Dateien — nicht als `sources`-Eintrag geführt.

## Future Triggers

- Wenn eine neue Umgebungs-/Deployment-Terminologie eingeführt wird → `environment-terminology.md` erweitern.
- Wenn der dedizierte Staging-Server (Hetzner CX32, Falkenstein) tatsächlich provisioniert wird → "Staging-Architektur"-Abschnitt von "geplant" auf "Ist-Zustand" umschreiben, echter Compile-Lauf fällig.
- Wenn Standard 006-domain-policy inhaltlich geändert wird → Cross-Ref hier gegenprüfen (Standards gewinnen bei Konflikt).
