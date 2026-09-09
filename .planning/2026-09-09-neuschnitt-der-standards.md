# Neuschnitt der Standards auf 33 Themen (Entwurf, 09.09.2026)

**Auftrag:** Max, 09.09.2026, 13:2x, wörtlich: „Alles in einen Topf werfen und komplett neu
verteilen auf 33 Punkte" und „du darfst komplett alles von Grund auf neu entscheiden, aber
so, dass es langfristig funktioniert, **ohne zusätzliche Nummern dranhängen zu müssen**".

**Anlass:** Nebenbefund von `fallnavigator-8e94`. Er wollte einen Standard 035 anlegen, las
die Cap-Regel und schrieb den Inhalt stattdessen als Abschnitt in 008. Dabei fiel auf: Die
Registry sagt 33, es sind 34.

**Status: Entwurf. Es ist noch keine Standard-Datei geändert und keine Nummer vergeben.**

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
