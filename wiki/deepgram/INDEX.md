# Deepgram — Bibel der Lehren

**Zweck:** Diese Datei sammelt jede Erfahrung, jeden Fehler und jede Regel rund um
**Deepgram**, die Spracherkennung in Veras Ohr, damit dieselben Fehler nicht zweimal Zeit
kosten. Wer an Veras Erkennung arbeitet, liest sie **vorher**.

**Last updated:** 2026-08-19 (angelegt, Regeln DG-01 bis DG-06 aus den Vorfällen vom 17.08.2026)
**Geltungsbereich:** `maxone-vera`, Modell `nova-3`, Sprache Deutsch, angebunden über
`livekit.plugins.deepgram` in `agent/entrypoint.py`. Schlüssel `DEEPGRAM_API_KEY` aus
`/opt/secrets/maxone-vera/keys.env`.

---

## I. Die unverhandelbaren Regeln

### DG-01 — NIEMALS auf ein endgültiges Erkennungsergebnis warten, ohne eine Frist zu setzen
Deepgram liefert Zwischenergebnisse (`is_final: false`) und erst danach das endgültige. Das
Agents-SDK schreibt einen Gesprächsbeitrag **ausschließlich** bei `is_final: true` fest.
Bleibt das endgültige aus, wartet der Agent unbegrenzt und der Anrufer hört Stille. Die Frist
steht in `agent/entrypoint.py` als `_ERKENNUNG_FRIST_SEKUNDEN = 2.5`.
*Lehre:* BUG-007, 17.08.2026. Max antwortete auf die Frage nach dem Firmennamen, Deepgram
schickte genau ein Zwischenergebnis („Mixed") und nie ein endgültiges. Max musste sich
wiederholen und fragte danach, wie man auflegt.

### DG-02 — NIEMALS einen Eigennamen ohne Keyterm-Prompting erwarten
Wörter, die es im deutschen Wortschatz nicht gibt, erkennt kein Modell zuverlässig. „maxone"
kam als „Mixone" an, und zwar reproduzierbar. Keyterms werden bei der Anbindung gesetzt,
nicht im Prompt.
*Lehre:* Max' eigener Testlauf am 17.08.2026. Details: `doku/keyterm.md`.

### DG-03 — NIEMALS Deepgram über LiveKit Inference beziehen
Sonst verbraucht die Erkennung dasselbe Guthaben wie das Sprachmodell, und beides ist
gleichzeitig leer. Eigener Anbieterschlüssel, immer.
*Lehre:* DEC-26, 15.08.2026.

### DG-04 — NIEMALS die Reaktionszeit bei Deepgram suchen
Wann Vera einen Beitrag als beendet wertet, entscheiden die **Session-Optionen von LiveKit**
(`min_endpointing_delay 0.3`, `max_endpointing_delay 2.5`), nicht Deepgrams Endpointing. Wer
hier dreht, dreht am falschen Regler.
*Lehre:* mehrfach gesucht, siehe `doku/endpointing.md`.

### DG-05 — IMMER die Doku als Markdown ziehen, nie HTML kratzen
Jede Deepgram-Doku-Seite gibt es als Markdown: `.md` an die URL hängen. Das vollständige
Verzeichnis liegt unter `https://developers.deepgram.com/llms.txt` und als Kopie in
[`doku/llms.txt`](doku/llms.txt).
*Lehre:* Max-Direktive 19.08.2026, Doku wird **persistent** gezogen, nicht temporär.

### DG-06 — NIEMALS „kein Zahlungsmittel" als Anmeldeblocker behandeln
Deepgram wirbt ausdrücklich mit „no credit card required". Die Anmeldung bricht nicht ab, der
**Betrieb** verstummt später, wenn das Guthaben leer ist. Reihenfolge deshalb: erst anmelden,
dann Karte.
*Lehre:* Irrtum aus `bauplan.md`, aufgelöst in `vera/IRRTUEMER.md`, 15.08.2026.

### DG-07 — NIEMALS einem Keyterm ein Gewicht anhängen
`keyterm=maxone:0.15` ist **kein Fehler und keine Gewichtung**, sondern ein einziger
Literalbegriff namens „maxone:0.15", der nichts verstärkt. Die API nimmt es klaglos an.
Dasselbe gilt für Kommas, Semikolons und Zeilenumbrüche als Trenner: Sie trennen nicht,
sondern werden Teil des Begriffs. **Gewichte gibt es nur bei der alten Funktion `keywords`,
nicht bei `keyterm`.**
*Lehre:* `doku/keyterm.md`, gelesen am 19.08.2026. Unsere eigene Liste ist gegengeprüft und
sauber: fünf Begriffe, kein Doppelpunkt, kein Komma, 41 von 500 zulässigen Token
`[B: eigene Prüfung von `_ERKENNUNGS_BEGRIFFE`, 19.08.2026]`. **Das ist die gefährlichste Art
Fehler: einer, der keine Fehlermeldung erzeugt.**

### DG-08 — Keyterms sind ein Regler, kein Wörterbuch
Höchstens 500 Token je Anfrage, sinnvoll sind 20 bis 50 Begriffe, hart begrenzt auf 100. Über
dem Limit antwortet die API mit `Keyterm limit exceeded`. **Jeder Begriff zieht die Erkennung
in seine Richtung**, eine lange Liste holt also Wörter herbei, die niemand gesagt hat.
*Lehre:* `doku/keyterm.md`. Bei Vera stehen deshalb nur Firmenname, Domains und die zwei
Namen, die in jedem Gespräch fallen.

### DG-09 — Wer Zwischenergebnisse oder UtteranceEnd will, muss drei Schalter setzen
`interim_results=true`, `utterance_end_ms` (z. B. 1000) und `vad_events=true`. Fehlt einer,
kommt das Ereignis nie, und zwar wortlos. `endpointing` (Millisekunden Stille) ist davon
unabhängig.
*Lehre:* `doku/endpointing.md`. Direkt verwandt mit DG-01: Wer BUG-007 an der Wurzel lösen
will statt über eine Frist, braucht genau diese Schalter.

### DG-10 — Flux ist der benannte Weg für Sprachagenten, und er ist ungeprüft
Deepgram hat mit **Flux** ein Modell speziell für interaktive Sprachagenten, mit eigener
Migrationsanleitung von `nova-3`. Es ist bei uns **nicht** eingebaut und nicht getestet. Wer
wechselt, ändert damit unmittelbar, wie Endgültigkeit gemeldet wird, also DG-01 und DG-09.
*Lehre:* `doku/flux-flux-nova-3-comparison.md`, gelesen 19.08.2026.

### DG-11 — Für die Suche in Deepgrams Doku gibt es einen MCP-Server, er ist angebunden
`https://developers.deepgram.com/_mcp/server`, angebunden am 19.08.2026 in
`vera/.mcp.json` als `deepgram-doku`. Er antwortet als `fern-docs-mcp-server` und bietet ein
Werkzeug: **`searchDocs`**, eine Volltextsuche über `developers.deepgram.com`, die Passagen
samt Quell-URL zurückgibt `[B: eigene initialize- und tools/list-Abfrage, 19.08.2026]`.
**Reihenfolge bei einer Frage:** erst die abgelegte Doku in `doku/`, dann `searchDocs`, erst
danach das offene Netz.
*Lehre:* Hinweiszeile in jeder gezogenen Doku-Seite. **Wirkt erst nach einem Neustart der
Session**, MCP-Server werden beim Start geladen.

**Bei den anderen Anbietern geprüft, am selben Tag:** Cartesia hat einen unter
`docs.cartesia.ai/_mcp/server`, er verlangt aber eine **Anmeldung** (307 auf
`play.cartesia.ai/docs-auth-login`) und ist deshalb ohne interaktive Freigabe nicht
anbindbar. **LiveKit hat keinen**, `docs.livekit.io/_mcp/server` liefert die normale
HTML-Seite; dort ist MCP nur ein *Thema* der Doku, kein Dienst. **Fish Audio: 404.**

---

## II. Verbotene Befehle und Griffe

- **Kein Modellwechsel im laufenden Betrieb ohne Testlauf.** `nova-3` ist gegen Veras
  Aussprachefälle geprüft, ein anderes Modell ist es nicht.
- **Kein Keyterm-Eintrag ohne Hörprobe.** Ein Keyterm verändert die Erkennung für **jeden**
  Anrufer, nicht nur für den Fall, für den er gedacht war.
- **Kein Schlüssel in einer Kommandozeile.** Immer aus `/opt/secrets/maxone-vera/keys.env`
  laden.

---

## III. Erlaubte Operationen (Cheatsheet)

```bash
# Läuft Veras Worker? Am PORT fragen, nie am Prozessnamen (er heißt python3.13.exe)
Get-NetTCPConnection -LocalPort 8081 -ErrorAction SilentlyContinue

# Doku-Seite persistent nachziehen
curl -s -o doku/interim-results.md https://developers.deepgram.com/docs/interim-results.md

# Was hat Deepgram in einem Gespräch verbraucht? Steht im Protokoll unter usage
python -c "import json;d=json.load(open('protokolle/kunde/2026/08/DATEI.json',encoding='utf-8'));print(d['bericht']['usage'])"
```

---

## IV. Die Vorfälle (kurz)

### 2026-08-17 — BUG-007, Vera verstummt nach einem Zwischenergebnis
Erkennung liefert `is_final: false` und danach nichts. Agent wartet unbegrenzt. Behoben durch
eine Frist von 2,5 Sekunden plus Nachfragesatz, der am Sprachmodell vorbeiläuft.

### 2026-08-17 — „Mixone" statt „maxone"
Der Firmenname kam in jedem Gespräch falsch an, weil er im ersten Satz fällt. Behoben über
Keyterm-Prompting.

---

## V. Checkliste vor jedem Eingriff an der Erkennung

1. Läuft der Worker? Am **Port 8081** prüfen, nie am Prozessnamen.
2. Doku zum betroffenen Punkt **persistent** in `doku/` ziehen, bevor gebaut wird.
3. Änderung an der Erkennung heißt **immer**: Worker neu starten, `start` lädt nicht nach.
4. Nach dem Neustart ein echtes Gespräch führen. Was Vera **sagt**, fängt eine Testsuite; was
   sie **hört**, fängt erst der Anruf.
5. Kein Live-Eingriff, solange ein Raum aktiv ist (`lk.room.list_rooms`).

---

## VI. Querverweise

- [LiveKit-Bibel](../livekit/INDEX.md) — Session-Optionen, Endpointing, Werkzeuge
- [Cartesia](../cartesia/INDEX.md) — die andere Hälfte der Sprachstrecke
- `vera/BUGS.md` (BUG-007), `vera/IRRTUEMER.md`
- Originaldoku: [`doku/`](doku/)

---

## VII. Updates an dieser Bibel

Jede neue Lehre kommt als **nummerierte Regel** dazu, mit `*Lehre:*` und Datum. Wer eine
Regel widerlegt, streicht sie nicht, sondern schreibt den Korrekturvermerk darunter.
