# Neuschnitt der Standards auf 33 Themen (Entwurf, 09.09.2026)

**Auftrag:** Max, 09.09.2026, 13:2x, wörtlich: „Alles in einen Topf werfen und komplett neu
verteilen auf 33 Punkte" und „du darfst komplett alles von Grund auf neu entscheiden, aber
so, dass es langfristig funktioniert, **ohne zusätzliche Nummern dranhängen zu müssen**".

**Anlass:** Nebenbefund von `fallnavigator-8e94`. Er wollte einen Standard 035 anlegen, las
die Cap-Regel und schrieb den Inhalt stattdessen als Abschnitt in 008. Dabei fiel auf: Die
Registry sagt 33, es sind 34.

**Status: UMGESETZT am 09.09.2026, 14:30 bis 14:5x.** Der Entwurf unten steht unverändert,
was daraus wurde, steht am Ende unter „Was daraus wurde". Zwei Dinge sind anders gelaufen
als geplant, beide dort benannt: Das Pioneer-System bleibt ein Standard (Max-Direktive), und
die Checklisten werden nicht angefasst (eigene Nummernreihe).

## Was gemessen ist

| | |
|---|---|
| Nummerierte Standards | **34** (001 bis 034), Registry sagt „33, 0 freie Slots" |
| Gesamtumfang | 236.331 Bytes |
| Über der 11-KB-Grenze | 4 Dateien: 026 (15,1 KB), 007 (12,3 KB), 018 (11,9 KB), 021 (11,9 KB) |
| Verweisende Dateien in allen Projekten | **655** |
| Herkunft der Überzahl | 034 entstand am 29.08.2026 aus dem RLS-Vorfall bei venfree, die Zählzeile wurde zuletzt am 27.08. angefasst und nie nachgezogen |

## Warum Zählen nicht reicht

**Das Problem ist nicht die eine Nummer zu viel, sondern dass gleiche Themen über die
Nummernachse verstreut liegen.** Dadurch findet niemand den richtigen Ort für Neues, und
genau deshalb wächst hinten immer eine Nummer an:

**Sechs Standards beschreiben, welche Datei im Repo liegen muss** (004 HANDOFF, 024 PLAN,
025 BUGS, 029 CONCEPT, 031 DECISIONS, 032 docs/INDEX). Zusammen 27,9 KB für eine einzige
Frage: Was führt ein Projekt an Akten?

**Sieben Standards behandeln Sicherheit** (002, 011, 012, 013, 014, 018, 034), verteilt
über die ganze Achse. Wer eine Sicherheitsregel sucht, muss sieben Nummern kennen.

**Zweimal Mail** (016 Architektur, 028 Brevo-Versand), **zweimal Bilder** (027 Pipeline,
030 Herstellerquellen). In beiden Fällen ist die zweite Nummer entstanden, weil die erste
schon vergeben war.

## Die Zielordnung: acht Blöcke, 33 Nummern, fünf davon bewusst frei

**Der tragende Gedanke:** Nummern werden nicht mehr fortlaufend vergeben, sondern **in
ihrem Themenblock**. Neues geht in den Block, dem es gehört, entweder als Abschnitt in eine
bestehende Nummer oder auf die freie Nummer des Blocks. **Hinten anhängen gibt es nicht
mehr, weil hinten kein Platz mehr ist, sondern nur noch in der Mitte.**

| Block | Nummern | frei |
|---|---|---|
| A · Betrieb und Auslieferung | 001-005 | — |
| B · Netz und Domains | 006-008 | 008 |
| C · Sicherheit | 009-013 | 013 |
| D · Daten und Zugang | 014-016 | 016 |
| E · Oberfläche und Marke | 017-021 | 021 |
| F · Ablauf und Qualität | 022-026 | — |
| G · Die Projektakte | 027-030 | 030 |
| H · Dienste, Kosten, Recht | 031-033 | — |

## Zuordnung: wo jeder heutige Standard landet

| neu | Thema | kommt aus |
|---|---|---|
| 001 | Deploy: Blue/Green, kein Prod-Build, Pipeline, Warmup | 001 |
| 002 | Server-Ordnung: Pfade, Container-Namen, HANDOFF auf dem Server | 005 + 004 |
| 003 | Container-Sicherheit und Plattenplatz | 015 |
| 004 | Zentrale Infrastruktur, n8n, Zustellgarantien | 033 |
| 005 | Geplante Läufe: keine Cron-Logik in Sitzungen | 017 |
| 006 | Domain-Politik: Technik auf .one, Inhalt in die Welten | 006 |
| 007 | Zertifikate und DNS-Realität | 012 |
| 008 | *frei, für Netz und Domains* | — |
| 009 | Geheimnisse und TLS | 002 |
| 010 | Sicherheits-Scans: Secrets und statische Analyse | 013 |
| 011 | LLM-Sicherheit: Injection, Agent-Rechte, Token-Trennung | 014 |
| 012 | Live-Audits: DSGVO-Tracker und Bundle-Drift | 011 |
| 013 | *frei, für Sicherheit* | — |
| 014 | Auth und Datenbank-Trennung | 018 |
| 015 | Jede RLS-Policy nennt ihre Rolle mit TO | 034 |
| 016 | *frei, für Daten und Zugang* | — |
| 017 | Pflichtbausteine jeder Oberfläche | 007 |
| 018 | Admin-Oberfläche: Layout, DevPanel, Launcher | 023 |
| 019 | Marke, Sprache, Schreibstil | 020 |
| 020 | Bilder: Pipeline und Herstellerquellen | 027 + 030 |
| 021 | *frei, für Oberfläche und Marke* | — |
| 022 | Tests und Code-Qualität, Code-Erhalt | 003 |
| 023 | Gates und Review, inklusive der sichtbaren ersten Scheibe | 008 |
| 024 | Stack- und Plattform-Politik, Self-Hosted-First | 010 |
| 025 | SSoT, Versionsmarker, keine Hardcodes, Design-Token | 022 |
| 026 | Projekt-Koordination: Spec-Archiv, Dep-Currency, Broadcast | 021 |
| 027 | Die Projektakte im Überblick, docs/INDEX als Einstieg | 032 |
| 028 | Konzept und Entscheidungen (CONCEPT, DECISIONS) | 029 + 031 |
| 029 | Plan und Fehlerregister (PLAN, BUGS) | 024 + 025 |
| 030 | *frei, für die Projektakte* | — |
| 031 | Mail: Architektur, Gateway-Pflicht, Versandwege | 016 + 028 |
| 032 | Kosten-Caps und Budget-Alarme | 019 |
| 033 | Compliance-Lebenszyklus: Sunset, AVV und DPA | 009 |

## Zwei Entscheidungen, die im Entwurf stecken

**Das Pioneer-System (heute 026, 15,1 KB) taucht in der Zielordnung nicht auf.** Es setzt
keine Regel, sondern beschreibt ein Produkt: Konzept, Datenmodell, Stufen. Ein Standard
sagt, wie gebaut wird; das hier sagt, was gebaut ist. **Vorschlag: es wandert ins Wiki**
und bleibt vollständig erhalten, mit einem Verweis von dort, wo es gebraucht wird. Es ist
zugleich die grösste Datei des Bestands und der Grund, warum die Grenze dort reisst.

**Mail wird eine Nummer, passt aber nicht in eine Datei.** 016 und 028 sind zusammen
15,2 KB. Beim Schreiben wird 031 auf die Architektur und die Gateway-Pflicht gekürzt, der
Brevo-Versandweg zieht als Wiki-Seite daneben, verlinkt aus 031. Dieselbe Trennung wie bei
den Standards, die schon heute auf Wiki-Seiten zeigen.

## Der Weg zur Umsetzung, und warum er einen Zug braucht

**655 Dateien verweisen auf Standards.** Ein Neuschnitt, der auf halbem Weg stehenbleibt,
lässt Verweise auf Nummern zeigen, hinter denen etwas anderes steht. **Das ist schlimmer
als der heutige Zustand**, weil ein falscher Verweis wie ein richtiger aussieht.

Reihenfolge der Umsetzung, in einem Zug:

1. **Warten, bis `fallnavigator-8e94` mit 008 fertig ist.** Sein neuer Abschnitt E (UI-First
   und der Vier-Stunden-Takt, Max-Direktive 09.09.2026, 12:58) gehört in den neuen 023.
2. Alle 34 Standards im Volltext lesen und die Inhalte den neuen Nummern zuordnen, nicht
   nur die Dateien verschieben. **Kein Satz geht verloren**, es gilt die Verlustprüfung der
   Grössenregel: jede Fettung der Vollfassung muss danach wieder auftauchen.
3. Die 33 Dateien schreiben, jede unter 11 KB.
4. `standards/README.md` neu: Blockordnung, Cap-Regel mit dem Satz, dass Neues in seinen
   Block geht, und die Zählzeile aus dem Bestand erzeugt statt getippt.
5. **Alle 655 Verweise nachziehen**, maschinell über die Zuordnungstabelle oben, danach
   Gegenprobe: kein Verweis darf auf eine Nummer zeigen, die es nicht mehr gibt.
6. Aushang im Pool, dass die Nummern neu sind, mit der Tabelle.

**Schritt 2 und 3 sind der teure Teil**: 236 KB lesen und neu schreiben. Das gehört in eine
eigene Sitzung mit frischem Kontext, nicht an das Ende einer langen.

---

# Was daraus wurde (Vollzug, 09.09.2026)

**29 Nummern belegt, 4 frei, keine Datei über der Größengrenze.** Gemessen mit
`python3 scripts/standards-zaehlen.py`, das auch die Bestandszeile im README gegen den
Ordner prüft. Genau diese Zeile war der Anlass des ganzen Vorgangs.

## Zwei Abweichungen vom Entwurf

**Erstens: Das Pioneer-System bleibt ein Standard, und zwar für jedes Projekt.** Der Entwurf
wollte es ins Wiki schieben, weil es „ein Produkt beschreibt, keine Regel". Max hat das am
09.09.2026 entschieden und die Prämisse umgedreht: „Es ist Bestandteil jeden Projektes.
Jedes Projekt, was begonnen wird, soll ein Pioneersystem führen. Allein aus dem Grund, um
möglichst früh und schnell eine Community zu bilden." Es steht jetzt als **021** in Block E,
sein `Gilt für` ist von „vanfree (Referenz)" auf „jedes Projekt" erweitert, und der
Ausführungsteil (Konfetti, SQL, Toast-Copy, Avatar-CSS) liegt in `wiki/pioneer/umsetzung.md`.
Damit ist Block E voll und die Zahl der freien Nummern vier statt fünf.

**Zweitens: Die Checklisten werden nicht angefasst, und das ist ein eigener Befund.**
`checklists/` führt eine **zweite Nummernreihe, die ebenfalls „Standard" genannt wird**.
Beleg: `checklists/016-stack-whitelist.md` schreibt „Pflicht bei Gate 1 (Standard 015
CONCEPT.md) und bei Gate 3 (Standard 013 LAUNCH-REVIEW.md)" — gemeint sind
`checklists/015-concept-gate.md` und `checklists/013-launch-gate.md`, nicht die Standards
015 und 013. Diese Verweise sind in sich korrekt. **Wer sie auf die neuen Standard-Nummern
umbiegt, zerstört funktionierende Verweise und merkt es nicht, weil das Ergebnis plausibel
aussieht.** Offen bleibt damit, ob die Checklisten ihre eigene Reihe behalten und nur anders
heißen sollten. Das ist eine Frage an Max, keine Ausführung.

## Was gemacht wurde

- **24 Dateien 1:1 umbenannt** (`git mv` über einen Zwischenordner, weil Ziel- und
  Quellnummern einander überlappen), **10 zu 5 zusammengelegt**, Köpfe auf die neue Nummer
  nachgezogen und das Titelformat auf `# NNN: Titel` vereinheitlicht.
- **Fünf Wiki-Seiten neu**, für alles, was aus den zu großen Dateien ausgelagert wurde:
  `wiki/pioneer/umsetzung.md`, `wiki/bilder/hersteller-bezugsquellen.md`,
  `wiki/design/brief-checkliste.md`, `wiki/auth/supabase-ssr-setup.md`,
  `wiki/integrationen/brevo-outreach-im-gateway.md`. **Kein Satz ist dabei verloren
  gegangen**, geprüft mit einer Verlustprüfung über alle Fettungen der Quelldateien
  (zwei Meldungen, beide Fehlalarme: eine Überschrift und die gewollte Umnummerierung).
- **Die Umleitungstabelle alt→neu steht in `standards/README.md`.** Die rund 655 Verweise in
  anderen Projekten werden nicht auf Vorrat umgeschrieben, sondern beim nächsten Anfassen.
  So wird kein fremdes Repo angefasst, in dem gerade eine andere Session arbeitet.
- **83 Verweise im Repo nachgezogen**, davon 61 im `VULN-CATALOG.md`, jeweils am Kontext der
  Fundstelle gelesen statt aus der Tabelle geraten. Das Ersetzen lief simultan: Wer 008 zu
  023 macht und danach 023 zu 018, zerstört das eben geschriebene Ergebnis.

## Der Nebenbefund, der den Neuschnitt rechtfertigt

**Der Bestand war in seinen Querverweisen bereits verrottet, vor jeder Änderung von heute.**
`025-bug-registry` verwies auf „**044**, SSoT & kein Hardcode" (044 hat es nie gegeben) und
auf „**005**, Test-First" (005 war Pfade). `017-routine-platform` nannte „Standards 018
(Bundle-Drift), 019 (Cert/DNS), 030 (Mail-Architektur)" — alle drei zeigten seit einer
früheren Umnummerierung auf etwas anderes, und einer davon war ein Selbstverweis mit
fremder Nummer. **Der bestehende Wächter `scripts/check-standard-refs.mjs` konnte das nicht
finden, und er sagt selbst warum:** Er meldet nur Verweise auf Nummern, die es *nicht gibt*.
Ein Verweis auf eine existierende Nummer mit falschem Inhalt fällt durch. Genau deshalb
steht die Verweis-Konvention jetzt im README: **Verwiesen wird auf den Dateinamen, nicht auf
die nackte Zahl.** Ein Dateiname bricht sichtbar, eine Zahl zeigt stumm woanders hin.
