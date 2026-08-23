# Google Calendar API — Bibel der Lehren

**Zweck:** Sammelt jede Erfahrung, jeden Fehler und jede Tücke rund um die **Google Calendar
API**, toolbezogen und projektübergreifend. Wer einen Kalender anbindet, liest sie **vorher**.
Das Pendant zu `BUGS.md` und `IRRTUEMER.md`, nur nicht am Projekt, sondern am Werkzeug.

**Last updated:** 2026-08-24 (GCAL-11 und GCAL-12 aus BUG-065; angelegt 2026-08-19)
**Geltungsbereich:** `maxone-vera` (Kalender „Vera Test", Paket `kalender/`), Cloud-Projekt
`maxone-vera`, OAuth mit Refresh Token. Originaldoku in [`doku/`](doku/).

---

## I. Die unverhandelbaren Regeln

### GCAL-01 — NIEMALS annehmen, Eigentümerschaft ersetze den Testnutzer-Eintrag
Im Testmodus verlangt Google jede Person als **Testnutzer**, auch den Eigentümer des Projekts.
Ohne Eintrag endet die Zustimmung mit `access_denied` („The developer hasn't given you access
to this app").
*Lehre:* 16.08.2026, zehn Minuten Vermutung gegen eine Minute Versuch. **Eine Annahme am
echten Konto auszuprobieren schlägt jede Konsolen-Interpretation.**

### GCAL-02 — NIEMALS einen Refresh Token im Testmodus für dauerhaft halten
Er verfällt. Für `maxone-vera` fiel das erste Ablaufdatum rechnerisch auf den 23.08.2026.
Das Fehlerbild ist heimtückisch: Vera sagt im Gespräch „Ich erreiche gerade den Kalender
nicht", und niemand merkt es vorher.
*Lehre:* Phase 2. **Der Wächter, der das meldet, bevor es ein Anrufer hört, ist bis heute
nicht gebaut.**

### GCAL-03 — NIEMALS ganztägige Einträge für blockierend halten
Google setzt sie standardmäßig auf **„Verfügbar"**. Eine eingetragene Urlaubswoche blockiert
damit nichts, und ein Assistent bietet mitten im Urlaub Termine an.
*Lehre:* D-09. Die Abhilfe ist eine **Handlung im Kalender** (auf „Beschäftigt" stellen),
keine Codezeile, und sie ging mit dem nie ausgeführten Plan 02-05 unter.

### GCAL-04 — NIEMALS `sendNotifications` benutzen
Der Parameter ist abgekündigt, richtig ist **`sendUpdates`** (`all`, `externalOnly`, `none`).
**Und selbst `none` garantiert keine Stille:** Die Doku sagt ausdrücklich, dass einzelne
Mails trotzdem verschickt werden können.
*Lehre:* `doku/events-insert.txt`. Für einen Testbetrieb mit fremden Personen heißt das: Die
einzige sichere Bremse ist, **keine Teilnehmeradresse zu setzen**, nicht ein Parameter.
Vera setzt `sendUpdates` korrekt und kennt einen Not-Aus für Einladungen
(`kalender/schreiben.py`).

### GCAL-05 — NIEMALS eigene Event-IDs vergeben, ohne die Regeln zu kennen
Erlaubt sind nur base32hex-Zeichen (`a`–`v`, `0`–`9`), Länge 5 bis 1024, eindeutig je
Kalender. **Google garantiert nicht, dass eine Kollision beim Anlegen erkannt wird**, deshalb
UUID nach RFC4122. `icalUID` und `id` sind nicht dasselbe, und beim Anlegen darf nur eines
gesetzt werden.
*Lehre:* `doku/events-insert.txt`. Vera vergibt keine eigenen IDs und ist damit auf der
sicheren Seite.

### GCAL-06 — NIEMALS Meet-Konferenzdaten zwischen Terminen wiederverwenden
Die Doku warnt ausdrücklich: Das führt zu Zugriffsproblemen und legt Besprechungsdetails
gegenüber Unbeteiligten offen. Für jeden Termin `createRequest` neu. Wer Konferenzdaten
ändert, muss zusätzlich `conferenceDataVersion=1` mitschicken, sonst wird die Änderung
stillschweigend verworfen.
*Lehre:* `doku/events-insert.txt`.

### GCAL-07 — NIEMALS `eventType` nachträglich ändern wollen
Er ist nach dem Anlegen unveränderlich, und `fromGmail` lässt sich überhaupt nicht anlegen.
*Lehre:* `doku/events-insert.txt`.

### GCAL-08 — IMMER die Doppelbuchung in der Datenbank verhindern, nicht im Programm
Ein `EXCLUDE`-Constraint über `tstzrange(start_ts, ende_ts)` lässt zwei überlappende
bestätigte Termine gar nicht erst entstehen. Eine Prüfung im Code davor ist Komfort, keine
Garantie.
*Lehre:* KAL-03, bewiesen am 17.08.2026 mit 14 Fällen und zwei echt gleichzeitigen
Transaktionen. **Aber der Constraint kennt nur die eigenen Buchungen, nicht den fremden
Kalender** — wer wirklich wissen will, ob ein Zeitpunkt frei ist, muss beides fragen.

### GCAL-09 — Die Einladung ist nicht die Buchung
Schlägt der Versand fehl, existiert der Termin trotzdem. Ein Werkzeug muss deshalb den
**Zustand** melden (`GEBUCHT` / `NICHT GEBUCHT`), nicht den nächsten Satz.
*Lehre:* BUG-006, 17.08.2026: Vera meldete einem Anrufer einen Termin, den es nicht gab.

### GCAL-11 — Beim Löschen ist `sendUpdates` standardmäßig `none`, beim Anlegen nicht
`events.delete` schickt **ohne** ausdrückliches `sendUpdates` **keine Absage an die Gäste**
`[B: developers.google.com, events.delete, gezogen am 24.08.2026]`. Wer einen Termin mit
Teilnehmern löscht und nichts weiter angibt, hinterlässt bei jedem Gast eine Einladung zu
einem Termin, den es nicht mehr gibt — und im eigenen Kalender sieht alles aufgeräumt aus.
*Lehre:* BUG-065, 24.08.2026. **Die Vorgabe ist genau dort still, wo Stille schadet.** Beim
Anlegen fällt eine fehlende Einladung sofort auf, weil niemand zusagt; beim Löschen fällt
eine fehlende Absage niemandem auf, bis der Gast vor verschlossener Tür steht. Wer löscht,
entscheidet `sendUpdates` deshalb ausdrücklich, und die Frage lautet nicht „soll ich
benachrichtigen", sondern **„hat dieser Termin je einen Gast gehabt"**.

### GCAL-12 — Ein Kalender-Anbindung ohne Löschweg ist nicht fertig
Wer nur `insert` baut, baut ein System, das Termine anlegen und nie zurücknehmen kann. Das
fällt nicht beim Bauen auf, sondern erst, wenn jemand seine Angabe korrigiert: Dann entsteht
der neue Termin, der alte bleibt, und beide sind gleich gültig.
*Lehre:* BUG-065, 24.08.2026, gefunden zwei Tage nach dem Vorfall und nur, weil jemand nach
einem Gesprächsprotokoll fragte. Vera konnte fünf Monate lang buchen und nicht absagen.
**Der Prüfsatz für jede Anbindung: Zu jedem Weg, der etwas in der Welt entstehen lässt,
gehört der Weg, der es wieder wegnimmt** — und zwar bevor der erste echte Datensatz
entsteht, nicht nachdem der erste falsche steht.

### GCAL-10 — Eine Projektliste, die direkt nach dem Anlegen leer ist, belegt nichts
Das Anlegen läuft asynchron. Wer noch einmal klickt, hat zwei Projekte.
*Lehre:* 16.08.2026, seither existiert das Waisenprojekt `maxone-vera-505718`.

---

## II. Verbotene Griffe

- **Kein Verifizierungsantrag, solange die Datenschutzerklärung Google nicht beschreibt.**
  Google prüft nicht, *ob* eine existiert, sondern *was* darin steht. Ein Dokument über eine
  Sache ist nicht die Sache.
- **Keine Integrationstests gegen `VERA_DB_DSN`.** Die Fixture leert `buchungen`. Testlauf
  ausschließlich über `VERA_TEST_DSN`, ohne Rückfall (BUG-008).
- **Keine Kalenderarbeit ohne die drei Google-Umgebungsvariablen.** Fehlen sie, sagt Vera im
  Gespräch „Ich erreiche gerade den Kalender nicht", und das kostet echte Testgespräche
  (17.08.2026, zwei Stück).

---

## III. Erlaubte Operationen (Cheatsheet)

```bash
# Trägt der Zugang noch? Fragt den echten Kalender, nicht die Konfiguration
python -c "from kalender.zugang import dienst; print(dienst().calendarList().list().execute()['items'][0]['summary'])"

# Freie Plätze rechnen lassen (ohne zu buchen)
python -c "from kalender.slots import zwei_vorschlaege; print(zwei_vorschlaege())"

# Doku persistent nachziehen (kein .md-Endpunkt, deshalb Text-Strip)
# siehe wiki/google-calendar/doku/, gezogen am 19.08.2026
```

---

## IV. Die Vorfälle (kurz)

### 2026-08-16 — `access_denied` trotz Eigentümerschaft
Siehe GCAL-01. Beendet wurde der Irrtum nicht durch Nachdenken, sondern durch einen echten
Zustimmungsdurchlauf.

### 2026-08-17 — Vera erreicht den Kalender nicht, zwei Testgespräche verloren
Der Worker war ohne die drei Google-Variablen neu gestartet worden. Seither gehört die
vollständige Umgebung in den Startbefehl.

### 2026-08-18 — BUG-021, gebucht wurde ein anderer Tag als zugesagt
Das Werkzeug gab nur einen gesprochenen Satz zurück, das Sprachmodell musste daraus ein
`start_iso` rekonstruieren und verfehlte Tag und Zeitzone. **Maschinenwerte gehören nie aus
einem Satz rekonstruiert.**

---

## V. Checkliste vor jedem Eingriff am Kalender

1. Zugang prüfen (GCAL-02), bevor irgendetwas anderes vermutet wird.
2. Läuft der Test gegen `VERA_TEST_DSN`? Sonst nicht starten.
3. Geht eine Einladung an eine **fremde** Person? Dann `sendUpdates` prüfen und im Zweifel
   die Teilnehmeradresse weglassen (GCAL-04).
4. Nach der Änderung: ein echter Buchungslauf, danach im Kalender **nachsehen**, nicht auf
   die Rückgabe vertrauen.

---

## VI. Querverweise

- [Google Cloud](../google-cloud/INDEX.md) — Projekt, OAuth-Zustimmung, Verifizierung
- `vera/BUGS.md` (BUG-005, BUG-006, BUG-008, BUG-021), `vera/IRRTUEMER.md`
- `vera/.planning/phases/02-kalender-und-terminvergabe/OFFENE-AUFLAGEN.md`
- Originaldoku: [`doku/`](doku/)

---

## VII. Updates an dieser Bibel

Jede neue Lehre kommt als nummerierte Regel dazu, mit `*Lehre:*`, Datum und Beleg.
Widerlegtes wird nicht gelöscht, sondern mit Korrekturvermerk versehen.
