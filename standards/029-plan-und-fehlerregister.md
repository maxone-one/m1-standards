# 029: Plan und Fehlerregister (PLAN.md · BUGS.md)

**Status:** active
**Seit:** 2026-05-18, zusammengeführt 2026-09-09
**Gilt für:** alle Projekte mit `status: live` oder `status: dev`

> **Herkunft:** Diese Nummer führt zusammen, was bis zum 09.09.2026 als `024-plan-tracker.md`
> und `025-bug-registry.md` getrennt lag. Beide lösen dasselbe Problem: **Zwischen Sessions
> geht Kontext verloren.** PLAN.md hält fest, was vereinbart ist, BUGS.md, was schon versucht
> wurde. Ohne beides beginnt ein Agent jedes Mal von vorne und „erinnert" sich an Dinge, die
> nie vereinbart wurden.

## Inhalt

- [A] PLAN.md, was vereinbart ist
- [B] BUGS.md, was schon versucht wurde
- [C] Muster-Feld und Cross-Project-Erkennung

---

## A: PLAN.md

Jedes Projekt führt eine `PLAN.md` im Repo-Root mit zwei Pflicht-Abschnitten:

1. **`## Noch offen`**, alle freigegebenen, noch nicht umgesetzten Pläne
2. **`## Erledigt`**, abgeschlossene Pläne mit Datum

**Timing-Regel:** Wenn ein Plan in einer Session freigegeben wird (Max sagt "ja, mach das"),
wird `PLAN.md` aktualisiert **bevor** der erste Code geändert wird. Das ist der explizite
Startschuss, nicht das Commit, nicht das Deploy.

**Kein PRD nötig:** PLAN.md ist das Planungsdokument, wenn kein CONCEPT.md vorhanden ist.
Auch ein Einzeiler ("Fix Login-Bug") ist ein gültiger Eintrag.

```markdown
# PLAN — <ProjektName>

## Noch offen

- [ ] **<Titel>** — <Kurzbeschreibung>
  - Freigegeben: YYYY-MM-DD
  - Details: <was genau, welche Dateien, welche Entscheidungen>

## Erledigt

- [x] **<Titel>** — <Kurzbeschreibung> — <Datum>
```

Checkboxen sind nicht zwingend, aber empfohlen, sie sind schnell scanbar und von Werkzeugen
lesbar. Leere Abschnitte sind gültig (`_(kein aktiver Plan)_`).

**Drei Garantien:**

| Garantie | Ohne PLAN.md | Mit PLAN.md |
|---|---|---|
| Session-Kontinuität | Kontext in CLAUDE.md oder nirgends | Explizite Done/Open-Liste im Repo |
| Freigabe-Nachweis | "Haben wir das besprochen?" unklar | Datum + Beschreibung im `## Noch offen` |
| Kein Scope-Creep | Claude baut was es "denkt" | Nur was in PLAN.md steht, wird gebaut |

**Abgrenzung:** [002-server-ordnung.md](002-server-ordnung.md) B (HANDOFF) ist server-seitig,
PLAN.md ist repo-seitig. [028-konzept-und-entscheidungen.md](028-konzept-und-entscheidungen.md)
ist konzeptionell, PLAN.md operativ. Das Launch-Gate in
[023-gates-und-review.md](023-gates-und-review.md) ist einmalig, PLAN.md läuft weiter.
Wenn CONCEPT.md vorhanden: PLAN.md kann darauf verweisen (`Details: siehe CONCEPT.md §3`).

---

## B: BUGS.md

Jedes Projekt bekommt eine `BUGS.md` im Repo-Root, eine persistente Bug-Wissensbasis.
Claude liest sie vor jeder Debugging-Session und hält sie nach jedem Schritt aktuell.

```markdown
# BUGS — <projektname>

## Aktive Bugs

### BUG-001 — <kurzer Titel>
**Status:** open | investigating
**Erstellt:** YYYY-MM-DD
**Muster:** `slug-in-kebab-case`   ← optional, für cross-project Erkennung (s. C)
**Symptom:** Was der User sieht / was kaputt ist.
**Root Cause:** (leer bis geklärt)
**Fehlgeschlagene Ansätze:**
- YYYY-MM-DD — Ansatz: <was versucht wurde> → Warum gescheitert: <Grund>
**Fix:** (leer bis gelöst)

---

## Geschlossene Bugs

### BUG-000 — <Titel>
**Status:** fixed | wont-fix
**Erstellt:** YYYY-MM-DD
**Geschlossen:** YYYY-MM-DD
**Muster:** `slug-in-kebab-case`   ← auch nach dem Fix stehen lassen
**Fix:** Was letztendlich funktioniert hat und warum.
**Fehlgeschlagene Ansätze:**
- YYYY-MM-DD — Ansatz: <was versucht wurde> → Warum gescheitert: <Grund>
```

### Sechs Pflicht-Regeln

**1. Lesen vor jeder Debugging-Session.** `BUGS.md` steht neben `HANDOFF.md` in der
Pflichtlektüre beim Session-Start. Vor dem ersten Debugging-Schritt prüfen, ob der gemeldete
Bug bereits einen Eintrag hat.

**2. Eintrag anlegen: spätestens beim ersten fehlgeschlagenen Ansatz.** Also sobald ein Ansatz
fehlschlägt **oder** ein Bug mehr als eine Session benötigt. Nicht abwarten bis der Fix
gefunden ist, der Eintrag entsteht während der Untersuchung, nicht danach.

**3. Fehlgeschlagenen Ansatz sofort dokumentieren**, direkt nach dem Erkennen, nicht erst am
Session-Ende. Der "Warum gescheitert"-Teil ist Pflicht. "Hat nicht funktioniert" reicht
nicht, die Ursache des Scheiterns ist die eigentliche Information.

**4. Bug schließen**, sobald ein Fix verifiziert ist (nicht nur committed, sondern getestet):
`**Status:**` auf `fixed`, `**Fix:**` mit vollständiger Erklärung füllen, `**Geschlossen:**`
ergänzen, Eintrag in `## Geschlossene Bugs` verschieben. Fehlgeschlagene Ansätze bleiben im
geschlossenen Eintrag, sie sind wertvoller als der Fix selbst, weil sie Folgefehler verhindern.

**5. BUGS.md wird committet.** Projekt-Wissen, kein persönlicher Scratchpad. Konvention:
`fix(bugs): close BUG-001 — <titel>`, `chore(bugs): add BUG-002 — <titel>`,
`chore(bugs): update BUG-001 — fehlgeschlagener Ansatz ergänzt`.

**6. IDs sind fortlaufend und eindeutig.** `BUG-001`, `BUG-002`, …, niemals eine ID
wiederverwenden, auch nicht nach Löschen eines Eintrags. Geschlossene Einträge bleiben in
`BUGS.md`, werden nicht gelöscht.

**Was BUGS.md nicht ist:** **Kein Ticket-System** (keine Prioritäten, Assignees, Sprints,
dafür gibt es Linear/GitHub Issues). **Kein Changelog** (fixe Bugs gehören ins Commit, BUGS.md
ergänzt es, ersetzt es nicht). **Kein HANDOFF.md-Ersatz** (HANDOFF beschreibt den Zustand,
BUGS die Debugging-Geschichte).

Ein leeres `BUGS.md` zum Kopieren liegt unter `templates/BUGS.md`.

---

## C: Muster-Feld, Cross-Project-Erkennung und Global Fix

Das optionale `**Muster:**`-Feld taggt einen Bug mit einem Slug, der die Root-Cause-Klasse
beschreibt, unabhängig vom Projekt: `css-var-missing-fallback`, `ssr-date-hydration`,
`supabase-rls-missing`, `next-image-missing-alt`.

**Slug-Konventionen:** Kebab-case, nur `a-z`, `0-9`, `-`. Beschreibt das *Muster* (was
strukturell falsch ist), nicht das Symptom. Gleicher Slug = gleiche Root-Cause-Klasse, auch
in anderen Projekten.

Sobald derselbe Slug in `BUGS.md` von ≥2 Projekten auftaucht, erscheint im Audit-Report eine
`[MUSTER]`-Zeile mit Label, den bekannten und den noch offenen Projekten.

**Claude's Reaktion auf `[MUSTER]`:** 1. Alle genannten offenen Projekte in einem Sprint
fixen. 2. Gleichzeitig alle übrigen Projekte nach dem Muster scannen (dort sind Instanzen
vielleicht noch nicht als Bug eingetragen). 3. Bug-Einträge schließen. 4.
`registry/bug-patterns.yml` mit `global_fix_status: fixed` und Datum aktualisieren.

**`registry/bug-patterns.yml`** ist die zentrale Musterliste: vom Audit automatisch befüllt,
enthält `label`, `description`, `example_fix`, und `global_fix_status:
pending | in-progress | fixed | wont-fix` trackt den Fortschritt.

---

## Audit

**PLAN.md:** existiert im Repo-Root (FAIL wenn nicht), `## Noch offen` vorhanden (FAIL),
`## Erledigt` vorhanden (FAIL). Der Inhalt wird nicht geprüft, ein leerer Abschnitt ist
gültig. Der Audit prüft die Struktur, nicht die Qualität.

**BUGS.md:** fehlt im Repo-Root → WARN. Keine `## Aktive Bugs`-Sektion → WARN. Keine
`## Geschlossene Bugs`-Sektion → WARN. Aktiver Eintrag ohne Fehlgeschlagene-Ansätze-Block
→ INFO.

**Cross-Project (nach runChecks):** Muster-Slug in ≥2 BUGS.md → `[MUSTER]`-Zeile. Muster mit
`global_fix_status: pending` und ≥1 offenem Projekt → `Offen in: … → Global Fix ausstehend`.
Neue Muster werden automatisch in `bug-patterns.yml` eingetragen.

**Migration:** Neue Projekte legen PLAN.md vor Gate 1 an
([023-gates-und-review.md](023-gates-und-review.md)). Bestand: sofort anlegen, auch leer.
Keine Ausnahme für `status: live`, das Anlegen dauert 30 Sekunden.

## Verwandte Standards

- [002-server-ordnung.md](002-server-ordnung.md) B, HANDOFF.md (Pflichtlektüre neben BUGS.md)
- [022-tests-und-code-qualitaet.md](022-tests-und-code-qualitaet.md), Test-First verhindert Bug-Regression
- [025-ssot-und-versionsmarker.md](025-ssot-und-versionsmarker.md), viele Bugs entstehen aus dupliziertem Zustand
