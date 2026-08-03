# Compile Log — paperclip

## Rollout-Dokumentation (2026-07-06)

**Trigger:** Rollout des wiki-compiler-Musters von den beiden Piloten (`maxone-mail-pilot`, `inventories`) auf die restlichen 6 Scopes. Kein Neu-Kompilieren — Inhalt (`INDEX.md`, `topics/architecture.md`, `topics/ops.md`) bestand bereits vollständig, alle drei Dateien tragen `last_updated: 2026-05-11`.

**Aktion:** `.wiki-compiler.json` nachträglich angelegt. `sources` ausschließlich aus dem expliziten "Quellen"-Abschnitt in `INDEX.md` übernommen (Server-HANDOFF per SSH, lokale Source-Kopie, Upstream-GitHub-Repo). `article_sections` an den tatsächlichen zwei Topics ausgerichtet (Architecture, Operational Patterns) plus einer eigenen Sektion "Known Quirks" für die in `ops.md` explizit gelisteten Eigenheiten (systemd-User-Inkonsistenz, ForwardAuth-Abhängigkeit, hardcoded `/root/.paperclip/`-Pfade).

**Beobachtung beim Lesen:** Der Codename ist weiterhin "PENDING" (Stand `ops.md` 2026-05-11) — Rebrand-Checkliste liegt bereit, aber unausgeführt. Der Scope-Name `paperclip` bleibt bis zur Umsetzung technisch korrekt.

## Future Triggers

- Wenn Max den Rebrand-Namen festlegt → Rebrand-Checkliste in `ops.md` abarbeiten, danach Scope selbst umbenennen (`paperclip` → `<name>`) inkl. `.wiki-compiler.json`.
- Wenn die VANGUARD-Familie (Vox, Viper, Vision) als Agents hinterlegt wird → `architecture.md` "Aktuell läuft ein Agent" aktualisieren, echter Compile-Lauf fällig.
- Wenn Paperclip aus dem Idle-Zustand (seit 2026-04-13) wieder aktiven Traffic bekommt → Monitoring-Lücke (kein Uptime-Kuma für `paperclip-app`) schließen und dokumentieren.
