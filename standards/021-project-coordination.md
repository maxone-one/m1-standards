# 021: Projekt-Koordination (Spec-Archiv · Dep-Currency · Cross-Project-Broadcast)

**Status:** active
**Seit:** 2026-05-04 (Spec-Archiv), 2026-05-11 (Dep-Currency + Broadcast)
**Gilt für:** alle Projekte mit Phasen/Sprints und allen aktiven Projekten im maxone-Universum

## Inhalt

- [A] Spec-Archiv: PRD/TODO/DONE-Lifecycle
- [B] Tech-Stack-Currency: Dependencies aktuell halten
- [C] Cross-Project Incident Broadcast (CPIB)
- [D] Projektregel gehört ins Repo, persönliche Ausnahme nie

---

## A: Spec-Archiv

Jede Phase besteht aus drei Dateien, nie einer:
- `PRD.md`, Spezifikation (was/warum/wie)
- `TODO.md`, offene Items (kontinuierlich → DONE.md)
- `DONE.md`, append-only Log mit Sign-Off

**Pfad:** `docs/phases/<phase-name>/` oder `briefings/<phase-name>/`

**Abschluss:** wenn TODO.md leer + Sign-Off in DONE.md → alles nach `docs/archive/<phase>/`, Stub `DEPRECATED.md` mit Forward-Pointer am ursprünglichen Pfad.

**Drei Kategorien für Arbeit außerhalb aktiver Phasen:**
- **A**, Mid-Phase Scope-Add (in TODO.md mit Tag `[scope-add — YYYY-MM-DD]`)
- **B**, Post-Completion Feature (eigene Mini-Phase, wenn > 1h oder Sign-Off nötig)
- **C**, Micro-Maintenance (< 1h, in `LIVING.md` im Repo-Root, append-only, jährlich rotieren)

**Cross-Repo Mirror:** `maxone-one/specs-archive` synct alle `docs/archive/**` via systemd-timer auf maxone-prod alle 60s. Schreibrichtung nur Projekt → Mirror.

**Warum:** Token-Ökonomie (eine wachsende PRD = 500+ Zeilen, Claude lädt alles; drei Dateien = Claude lädt nur TODO.md ~50 Zeilen), Repo-Verwahrlosung, lebenslange Projekte ohne Schema.

---

## B: Tech-Stack-Currency

Dependency-Drift wird proaktiv gepflegt. Pflicht-Kadenz:

- **Patch + Minor: alle 4-6 Wochen**, `npm update` in einem PR. Bei grünem `tsc` + Build + Tests → merge + deploy ohne Rückfrage.
- **Major-Bumps: einzeln**, pro Paket eigener PR, CHANGELOG lesen, Reihenfolge: Build-Tools (vite, typescript) vor Lint-Tools vor App-Libraries.
- **Security-Fix (npm audit high/critical):** separater PR, nicht im Feature-Branch parken.

**Sweep starten:**
```bash
git pull --rebase
npm outdated        # was ist Drift?
npm audit           # was ist sicherheitsrelevant?
```

Wenn `npm outdated` > 5 Patch/Minor oder Repo > 6 Wochen ohne Sweep: **erst Sweep, dann Feature**.

**Unfixbare Pakete** (vom Registry entfernt): Migration planen, `xlsx` → `exceljs`/papaparse, `request` → native `fetch`, `moment` → `date-fns`.

**Pausierte Projekte:** mindestens 1× pro Quartal `npm outdated` + `npm audit` Snapshot. Bei Vulns: Sweep auch im pausierten State.

**Skip-Bedingungen:** `status: sunset`, archive-only Mirror, kein Lockfile.

**Warum:** Erzwungener Notfall-Major (Sicherheitslücke in v3, Fix in v5, wer sweept war auf v5), unfixbare Pakete (xlsx 2024 vom Registry entfernt), Stack-Whitelist-Drift.

---

## C: Cross-Project Incident Broadcast (CPIB)

Sobald ein Fehler oder eine Änderung mehr als ein Projekt betrifft, MUSS innerhalb der laufenden Session eine Broadcast-Datei angelegt werden:

```
maxone-standards/broadcasts/BCAST-YYYY-MM-DD-<slug>.md
```

**Zwei Typen:** Incident Broadcast (reaktiv) · Change Notice (proaktiv, vor Deployment).

**Format:**
```markdown
# BCAST-YYYY-MM-DD-<slug>

**Typ:** incident | change-notice
**Status:** open
**Verursachend:** <projektname>

## Was ist passiert / Was ändert sich
## Fehlermuster (reproduzierbar)
## Betroffene Projekte
| Projekt | Status | Fix-Commit | Gelöst am |
|---|---|---|---|

## Fix-Muster
## Audit-Grep-Pattern (Pflicht)
**Fail-Grep:** <regex>
```

**Abschluss:** alle Projekte in Tabelle auf `resolved` → Status → `closed` (Datei bleibt als Archiv).

**Auflösung pro Projekt:**
```
fix(<projekt>): resolve BCAST-YYYY-MM-DD-<slug>
```

**Warum:** Drift entsteht wenn Änderung in A still B-N bricht. Vorfall 2026-04-22: `maxone.studio`→`maxone.one`-Wechsel, hardkodierte Studio-URLs in mehreren Projekten, Entdeckung Wochen später.

## D: Was das Projekt auf einem zweiten Rechner braucht, gehört ins Repo (2026-06-04, neu gefasst 2026-08-22 von Max)

Die Linie verläuft **nicht** zwischen Claude und Nicht-Claude, und auch **nicht** zwischen Projektregel und persönlicher Ausnahme, sondern allein am Leitsatz vom 18.08.2026: **„Alles, was ich lokal ändere und für meine Architektur benötige, muss auch auf einem anderen Rechner funktionieren."** Bedienung ist Teil der Architektur.

**Gehört ins Repo:** `CLAUDE.md`, `AGENTS.md`, `.claude/settings.json`, **`.claude/settings.local.json`**

**Gehört nie ins Repo:** Laufzeit-Artefakte, die auf jeder Maschine neu entstehen (`*.session`, `.claude/*.lock`, `.claude/shell-snapshots/`, `.claude/todos/`, `.claude/statsig/`, `.claude/projects/`), alles mit einem Geheimnis darin (`.env`, `*.pem`, Schlüssel, Recovery-Codes), dazu die Umgebungsdateien fremder Werkzeuge (`.clinerules`, `.cursorrules`, `.antigravityrules`).

**Durchsetzung:** allein `~/.gitignore_global`, konfiguriert via `git config --global core.excludesfile ~/.gitignore_global`. Sie ist die harte Quelle, dieser Standard beschreibt sie nur. Wer beide gegeneinander liest und einen Widerspruch findet, korrigiert den Standard, nicht die Datei.

**Verboten:** ein Eintrag für `CLAUDE.md`, `AGENTS.md` oder `.claude/settings*.json` in einer projektlokalen `.gitignore` — sie sollen ja mitwandern.

**Die eine Prüfung vor dem Committen der `settings.local.json`:** Steht in einem der Erlaubnis-Muster ein Geheimnis, also ein Token, ein Key, ein Passwort in einem einmal freigegebenen Kommando? Dann kommt das Muster raus, nicht die Datei. Ein öffentlicher SSH-Key ist keines.

**Warum:** `settings.local.json` trägt die Dauererlaubnisse, die ein Mensch über Monate weggeklickt hat. Sie sind kein Beiwerk der Bedienung, sie **sind** die Bedienung. Ein frischer Rechner mit Code ohne sie fragt bei jedem Handgriff neu; in `vector` wären das 69 Rückfragen für ein einziges Projekt.

<!-- FALLGESCHICHTE, kostet nichts im Kontext.

ERSTE FASSUNG, bis 2026-08-19: „Claude-Konfigurationsdateien sind rein lokal und duerfen in
keinem Git-Repository auftauchen", betroffen waren CLAUDE.md, AGENTS.md und .claude/
vollstaendig. Sie widersprach seit dem 18.08.2026 dem Leitsatz und erzeugte im
Hygiene-Check von /drift taeglichen Fehlalarm. Gemeldet von `werkstatt` am 19.08.2026.

ZWEITE FASSUNG, 2026-08-19 bis 2026-08-22, gesetzt von `vera` um 14:17 (dort TODO 44): Die
Linie verlaufe zwischen Projektregel und persoenlicher Ausnahme, settings.local.json gehoere
nie ins Repo. Ihr Beleg war ihr eigenes Repo, wo die getrackte Datei
{"permissions":{"allow":[]}} enthielt, also nichts. Der Schluss war zu breit: Aus einer
leeren Datei folgt, dass SIE DORT nichts trug, nicht dass sie ueberall nichts traegt.

Zwei Fehler trug diese Fassung ausserdem mit sich. Erstens hat eine KI-Session eine Regel
gegen Max' vier Tage alten Leitsatz gesetzt, ohne ihn zu fragen. Zweitens behauptete der
Absatz „Durchsetzung", die Zeile **/.claude/settings.local.json stehe in
~/.gitignore_global. Sie stand dort nie. Der Kopf jener Datei sagt seit dem 18.08. das
Gegenteil und schliesst unter .claude/ nur Laufzeit-Artefakte aus. Der Standard hat also
eine Durchsetzung behauptet, die es nicht gab, und drei Tage lang hat niemand nachgesehen.

AUFGEFALLEN am 22.08.2026 im /drift von `vector`: Der Lauf meldete die dort getrackte
settings.local.json als Befund, Max widersprach („das hat alles schon seine Richtigkeit"),
und seine Sorge galt nicht dem Befund, sondern der Frage, warum das System es nicht wusste.
Geprueft wurden daraufhin die 69 Erlaubnis-Muster der Datei gegen Token-, Key- und
Passwortmuster: null Treffer, der einzige Schluessel darin ist der oeffentliche Teil eines
SSH-Keys. Damit fiel der letzte Einwand, und Max hat entschieden.

DIE LEHRE, die ueber diesen Fall hinausgeht: Ein Standard, der eine Durchsetzung behauptet,
muss sie belegen koennen. Steht in einer Regel „liegt in Datei X", dann ist Datei X die
haerteste Quelle und die Regel nur ihre Beschreibung. -->

**Bestehende Repos:** nichts zu tun. Repos, die die Datei nach der zweiten Fassung entfernt haben, nehmen sie mit `git add -f .claude/settings.local.json` wieder auf, sofern die Geheimnis-Prüfung oben sauber ist.

---

## Audit

**Spec-Archiv:** Orphan-PRDs (`*.md` mit `PRD-` im Namen außerhalb Archive-Pfaden) → WARN; drei-Datei-Konsistenz in Phasen-Ordnern → fehlt eine → WARN; DEPRECATED-Forward-Pointer → fehlt → WARN.

**Dep-Currency:** `npm outdated` > 20 Patch/Minor → WARN; > 50 → FAIL; `npm audit` high/critical mit Fix → WARN; letzter Sweep > 90 Tage → WARN.

**CPIB:** offener Broadcast mit Projekt in Tabelle als `open` → **FAIL**; Broadcast > 30 Tage offen → FAIL; Fail-Grep-Pattern trifft auf Projekt-Code → FAIL.
