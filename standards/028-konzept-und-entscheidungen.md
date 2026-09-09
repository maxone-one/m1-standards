# 028: Konzept und Entscheidungen (CONCEPT.md · DECISIONS.md)

**Status:** active
**Seit:** 2026-05-30 (Konzept), 2026-05-31 (Entscheidungen), zusammengeführt 2026-09-09
**Gilt für:** alle Projekte mit `status: live` oder `status: dev`

> **Herkunft:** Diese Nummer führt zusammen, was bis zum 09.09.2026 als
> `029-concept-reference.md` und `031-decisions-md.md` getrennt lag. Sie gehören zusammen,
> weil das eine ohne das andere verrottet: **CONCEPT.md sagt, was das Produkt ist,
> DECISIONS.md sagt, was davon nicht mehr gilt.** Wer nur das Konzept liest, baut in eine
> Richtung, die vor drei Monaten aufgegeben wurde.

## Inhalt

- [A] CONCEPT.md, das Produkt und seine Sprache
- [B] Die Ausbaustufe: das lebende, code-verankerte Projekt-Brain
- [C] DECISIONS.md, was nicht mehr gilt

---

## A: CONCEPT.md

Jedes Projekt führt eine `CONCEPT.md` im Repo-Root. Sie dokumentiert das vollständige
Produkt-Konzept: Vision, Positionierung, Produkttiers, Zielgruppen, Geschäftsmodell, Sprache.

**Zweck:** Ein Agent, der in das Projekt einsteigt, soll das Konzept aus dieser Datei
verstehen, ohne Code zu lesen, ohne zu raten, ohne zu fragen. `CONCEPT.md` ist die einzige
Wahrheit über *was* das Produkt ist und *wie* darüber gesprochen wird.

**Timing:** Die Datei wird angelegt, bevor Code oder Copy für ein neues Projekt entsteht.
Sie wird aktualisiert, sobald sich Positionierung, Produkttiers, Geschäftsmodell oder
Zielgruppen ändern, nicht nachträglich, sondern als erster Schritt bei
richtungsverändernden Entscheidungen.

**Pflicht-Abschnitte:** `## Vision` (ein Satz: was das Produkt ist und welches Problem es
löst, konkret statt generisch), `## Positionierung` (warum jetzt, was ist der Moat),
`## Produkttiers` (Tabelle: Tier, Zugang, Kosten, Funktion), `## Zielgruppen` (pro Gruppe:
wer, welches Problem, welcher Wert), `## Geschäftsmodell` (wer zahlt, wer nicht, warum das
funktioniert), `## Sprache` (mit `### Sagen` und `### NICHT sagen`). Optional: Roadmap-
Richtung, Wettbewerbs- und Markt-Kontext.

**Ist:** Konzept-Referenz für Agenten, Copy-Anker, Sprach-Leitfaden, Produkt-Wahrheit.
**Ist nicht:** PLAN.md (offene Tasks), CLAUDE.md (technische Regeln), HANDOFF.md
(Server-Zustand), BUGS.md (bekannte Fehler). Alle koexistieren. CONCEPT.md ist die einzige,
die ausschließlich über *Inhalt und Bedeutung* des Produkts spricht.

---

## B: Die Ausbaustufe, das lebende Projekt-Brain

**Gilt für:** empfohlen für jedes Projekt mit `status: live`, dessen Feature- und
Routen-Fläche groß genug ist, dass Code-Scannen pro Frage spürbar Token kostet.
Referenz-Implementierung: stadt-lahn-flow.

Für Projekte mit echtem Code reicht die statische Konzept-Referenz nicht: Dort kommt die
Frage "wo liegt Funktion X" und "wie mache ich Y" laufend auf, und ein Agent, der sie nicht
aus einer Datei beantworten kann, scannt jedes Mal den Code und verbrennt Token.

**Das Prinzip:** Eine Einstiegsdatei beantwortet vier Fragen (was, wo, wie, warum), wobei
jede Antwort entweder **aus Code generiert** ist (kann nicht driften) oder **bewusst
kuratiert** (braucht Urteilsvermögen).

Der Kern-Trick: **Verankere die Wahrheit dort, wo sie ohnehin gepflegt werden muss.** SLFs
Feature-Liste (`src/lib/features-registry.ts`) ist nicht bloß Doku, sie rendert `/roadmap`,
`/preise` und `/features`. Sie kann gar nicht veralten, ohne dass das Produkt selbst
kaputtgeht. **Eine Doku, die niemand zum Funktionieren braucht, verrottet. Eine, die das
Produkt zum Laufen braucht, nicht.**

**Drei Eimer, jede Information gehört in genau einen:**

| Eimer | Inhalt | Wer pflegt | Driftet |
|---|---|---|---|
| **Generiert** (Maschinen-Wahrheit) | Feature-/Routen-/Endpoint-/Env-Katalog, "wo liegt was" | Generator aus dem Code-Anker | nein, aus Code abgeleitet |
| **Kuratiert** (Urteil) | Was ist das Produkt, Architektur-Karte, Rezepte ("wie mache ich X"), bekannte Lücken | Agent von Hand, selten | nur bei Architektur-Änderung |
| **Protokolliert** (append-only) | Entscheidungen `D-NNN` mit Datum und Begründung, das "warum" | Agent ergänzt, nie umschreiben | nein, nur Anhängen (Abschnitt C) |

**Verankerungs-Strategien**, je nach Projekttyp: **1. Produkt-getrieben** (SLF-Fall), es gibt
bereits eine typisierte Liste, die das Produkt nutzt, der Katalog wird daraus generiert.
**2. Konvention-getrieben**, keine Registry, aber das Dateisystem ist die Wahrheit
(Next.js-`app/`-Router gleich Routen, `commands/` gleich CLI-Befehle, `.env.example` gleich
Konfig-Fläche); der Generator scannt es, kein Pflegeaufwand. **3. Hand-Anker mit
Drift-Check**, wo nichts ableitbar ist (Architektur-Karte, Rezepte), schreibt der Agent von
Hand, aber ein Test prüft, dass jeder genannte Pfad noch existiert. So kann der kuratierte
Teil unvollständig sein, aber nie auf Totes zeigen.

**Selbsterhaltung, vier Mechanismen, einander absichernd**, damit die Pflege nicht an der
Disziplin des Agenten hängt (die mit langer Session nachlässt):

1. **Generator mit `--check`:** kompiliert Anker zu Katalog, idempotent ohne Zeitstempel
   (zweimal laufen erzeugt keinen Diff), `--check` meldet read-only bei Abweichung und
   schreibt nichts, taugt also für Drift-Läufe.
2. **Definition of Done in der Projekt-CLAUDE.md:** Eine Feature-/Routen-/lib-Änderung ist
   erst fertig, wenn Registry, Code-Karte, ggf. `D-NNN` mitgezogen und der Generator
   gelaufen ist.
3. **Drift-Achse im `/drift`-Command:** read-only Statusanzeige über `--check`.
4. **Stop-Hook:** stupst, wenn Feature-Code geändert wurde, aber das Brain nicht. Der
   einzige Mechanismus, den die Harness erzwingt statt des Agenten, deshalb der wichtigste
   gegen Vergesslichkeit.

Härteste Schicht obendrauf: das **CI-Gate**. Der `--check`-Lauf im Deploy lässt den Build
fehlschlagen, wenn das Brain verrottet ist. Ein veraltetes Brain wird so nie deployt.

**Konsum-Regel** (der eigentliche Token-Spareffekt, fest in die Projekt-CLAUDE.md): 1. Bei
Produktfragen zuerst CONCEPT.md. 2. Bei "wo liegt X" die Registry plus Code-Karte (der
Pointer führt zur einen Datei). 3. Code nur lesen, wenn das Brain schweigt oder gerade etwas
geändert wird. Kein Tree-Scan, kein erneutes Durchforsten von PRDs.

**Verhältnis zur Basis-Regel:** Der "wo liegt was"-Teil ist kein von Hand gepflegter
Tech-Text, sondern aus Code abgeleitet, verletzt den Geist von Abschnitt A also nicht.
Einzige hand-kuratierte technische Ergänzung sind Architektur-Karte und Rezepte,
gerechtfertigt, weil das "wie" aus reinem Code-Lesen teuer zu rekonstruieren ist.

**Referenz-Implementierung (stadt-lahn-flow):** `CONCEPT.md` (Brain mit Index, "Was ist",
Architektur-Karte, generiertem Katalog zwischen `BEGIN/END GENERATED FEATURES`, Rezepten und
stabilem Gate-1-Teil), `src/lib/features-registry.ts` (das "was"), `src/lib/feature-code.ts`
(das "wo"), `scripts/gen-product-brain.mjs` (Generator plus `--check`), `docs/DECISIONS.md`
(das "warum"), `scripts/brain-reminder.mjs` plus Stop-Hook (der Stupser).

---

## C: DECISIONS.md

**Das Problem:** In lang laufenden Projekten entsteht Drift. Das PRD beschreibt
Desktop-First, die Plattform ist längst Web-only. Ein Agent, der zu spät einsteigt, liest
das PRD und baut in die falsche Richtung, ohne es zu wissen. Dieses Muster ist unvermeidlich:
Konzepte werden zu Beginn geschrieben, Entscheidungen fallen laufend.

**DECISIONS.md ist die Lösung:** Eine einzige Datei dokumentiert alle strategischen Pivots,
Abweichungen und bewussten "Nicht-mehr-gültig"-Entscheidungen. Wer sie liest, weiß, was noch
gilt, ohne PRD und Konzept komplett zu lesen. Jedes Projekt mit einem PRD, CONCEPT.md oder
Visionsdokument führt eine `docs/DECISIONS.md`.

**Wann einen Eintrag schreiben:** Eine Aussage im PRD oder Konzept ist nicht mehr gültig.
Eine strategische Weichenstellung fällt (Geschäftsmodell, Zielgruppe, Tech-Stack). Max sagt
explizit "das haben wir so entschieden" zu etwas Nicht-Offensichtlichem. Eine frühere
Annahme hat sich als falsch erwiesen.

**Timing:** Sofort wenn die Entscheidung fällt, nicht im nächsten Sprint, nicht "später".
Wer die Entscheidung trifft, schreibt den Eintrag. Das ist der erste Schritt, bevor Code
oder Copy geändert wird.

```markdown
# Strategische Entscheidungen — <ProjektName>

Diese Datei hat Vorrang vor PRD und Konzept. Jede Entscheidung hier überschreibt
Aussagen in den anderen Dokumenten. Immer mit Datum und Begründung dokumentieren.

---

## <Kurztitel der Entscheidung> (entschieden <YYYY-MM-DD>)

<Was wurde entschieden — ein Satz.>

<Warum: Begründung, was die Alternative gewesen wäre, welcher Vorfall oder welche
Erkenntnis dazu geführt hat.>

**Konsequenz für PRD/Konzept:** <Welche Abschnitte sind jetzt überholt oder falsch?>
```

**Drei-Quellen-Hierarchie**, die Lese-Reihenfolge beim Session-Start: 1. **DECISIONS.md**,
was ist anders als beschrieben? 2. **CONCEPT.md**, was ist das Produkt? 3. **PRD**, wie wird
ein Feature spezifiziert? 4. **PLAN.md**, was wird gerade gebaut?

**Widersprüche:** DECISIONS.md gewinnt immer. PLAN.md gewinnt bei der Reihenfolge.

---

## Audit

```bash
# CONCEPT.md: Pflicht-Abschnitte
for section in "## Vision" "## Positionierung" "## Produkttiers" \
               "## Zielgruppen" "## Geschäftsmodell" "## Sprache"; do
  grep -q "$section" CONCEPT.md || echo "FEHLT: $section"
done

# Brain-Ausbaustufe: wenn ein Generator vorhanden ist, muss der Katalog frisch sein
if [ -f scripts/gen-product-brain.mjs ]; then
  npm run gen:brain -- --check || echo "BRAIN VERALTET: Generator laufen lassen und committen"
fi

# DECISIONS.md: Pflicht, sobald ein PRD existiert
if ls docs/prd/ docs/PRD*.md 2>/dev/null | grep -q .; then
  test -f docs/DECISIONS.md || echo "FEHLT: docs/DECISIONS.md (PRD vorhanden, keine Entscheidungs-Übersicht)"
fi
```

## Warum diese Regeln

Ein Agent, der das Konzept nicht kennt, rät. Raten führt zu Copy, die das Produkt reduziert,
zu falschem Framing, zu inkonsistenter Kommunikation über Sessions hinweg und zu Fehlern,
die Max korrigieren muss, statt vorwärts zu kommen. **CONCEPT.md kostet einmal 20 Minuten
und spart pro Session Korrekturrunden. DECISIONS.md kostet pro Eintrag 5 Minuten und spart
die Stunden, in denen ein Agent in die falsche Richtung läuft.**

## Verwandte Standards

- [023-gates-und-review.md](023-gates-und-review.md) Gate 1: CONCEPT.md entsteht vor Code.
  Der stabile Gate-1-Konzeptteil bleibt am Ende der Datei, der Brain-Teil ist das laufend
  gepflegte Davor.
- [029-plan-und-fehlerregister.md](029-plan-und-fehlerregister.md) und
  [027-projektakte.md](027-projektakte.md): Das Brain verlinkt auf sie, ersetzt sie nicht.
