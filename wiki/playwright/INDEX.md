# Playwright: Bedienhandbuch

Angelegt 11.08.2026 nach einer Bestandsaufnahme: Playwright-Wissen lag in **291 Dateien**
verstreut, darunter sieben eigene Memories in vier verschiedenen Projekt-Namespaces, und
zwei davon widersprachen sich seit vier Wochen. Genau das meint Max' Satz „damit du dich
nicht ständig aufgrund des Tools im Kreis drehst".

**Das Bedienbare steht oben, die Nachweise stehen unten.**

## Welchen Server nehme ich?

| Lage | Server | Profil |
|---|---|---|
| **Der Normalfall, Max' Arbeit** | `playwright` | `~/.playwright-mcp-profile` |
| Max' **zweites Konto** bei einem Dienst, der nur eines zulässt | `playwright-privat` | `~/.playwright-mcp-profile-2` |
| alles andere | **gar nicht** | |

**`playwright-shared` und `--isolated` sind verboten** (Max-Korrektur 11.07.2026, oberste
Priorität). Nur das Hauptprofil ist seit Monaten organisch in Gebrauch und trägt Max'
echtes Autofill und seine gespeicherten Logins für Behörden, Banken und Portale. Die
anderen Profile sind praktisch leer, dort scheitert jeder Login. Zweimal passiert, am
07.07. und 11.07.2026, beide Male bei der Arbeitsagentur, beide Male wurde das Profil
geraten statt geprüft.

**Aufgelöster Widerspruch, 11.08.2026:** `memory/playwright-profile-per-project.md`
vom 30.05.2026 verlangt das Gegenteil („niemals das Default-Profil aktiv nutzen, jedes
UI-Projekt bekommt sein eigenes"). **Diese Fassung ist überholt.** Sie löste ein anderes
Problem, nämlich gegenseitige Sperren beim parallelen Arbeiten, und opferte dafür genau
das, was seit dem 11.07. Vorrang hat: die Anmeldungen. Pro-Projekt-Profile gelten heute
nur noch in zwei Fällen: für ein zweites Konto (siehe oben) und für **Dauerbetrieb**
(`~/.playwright-profiles/repivot.me` trägt den RePivot-Autopiloten).

## Fenster und Tabs

**Vor jedem Öffnen zuerst prüfen, was schon offen ist** (`browser_tabs` mit `list`). Ein
Fenster kann von einer früheren Sitzung bewusst offen gelassen worden sein.

**Vier Klassen, die erste zutreffende gewinnt** (Volltext:
`rules/keine-artefakte-auf-max-bildschirm.md`):

| Klasse | Was | Regel |
|---|---|---|
| **0 Dauerprofil** | trägt laufenden Betrieb, Wahrheit ist `~/.claude/dauerbetrieb.json` | nie schließen, nie als Befund melden |
| **1 Dauertab** | **derzeit leer** | – |
| **2 Übergabetab** | wartet auf genau einen Klick von Max | bleibt bis `bis`, **mit Markierung UND Übergabesatz** |
| **3 Arbeitstab** | alles andere | sofort schließen, wenn der Schritt fertig ist |

**Jede Aufgabe öffnet einen neuen TAB, nie ein neues Fenster** (Max-Direktive 13.08.2026,
sie hebt „eigenes Fenster pro Aufgabe" auf): `browser_tabs` mit `action: new`, und niemals
eine zweite Browser-Instanz, solange eine passende läuft.

**Innerhalb einer Aufgabe wird nicht zwischen Einzelschritten geschlossen.** Erst wenn die
ganze Aufgabe fertig ist, nicht der Einzelschritt.

### Dauerdienste: Wahrheit ist die Datei, nicht diese Seite

| Profil | Dienst | Port | Zustand |
|---|---|---|---|
| `dauerbetrieb` | **WhatsApp Business** | 9223 | Dauerbetrieb, Wächter stellt ihn wieder her |
| `repivot.me` | RePivot-Autopilot | 9222 | pausiert seit 13.08.2026 |

```bash
powershell -File ~/.claude/bin/dauerbetrieb.ps1 -NurPruefen   # meldet nur
powershell -File ~/.claude/bin/dauerbetrieb.ps1               # stellt her
```

#### Nach jedem Neustart entsteht ein Leseauftrag

**Herstellen ist nicht Nutzen** (Max, 14.08.2026,
`rules/dauerbetrieb-heisst-lesen-nicht-nur-laufen.md`). Macht der Wächter einen Kanal neu
auf, hat der Kanal ungelesene Verläufe, und ein offener Kanal, den niemand liest, ist von
außen dasselbe wie ein geschlossener, nur teurer: Die Zeile darüber meldet „ok".

Der Wächter stößt das selbst an, von Hand braucht es nur den Abschluss:

```bash
python ~/.claude/bin/dauerbetrieb-leseauftrag.py offen      # Exit 1, wenn einer offen ist
python ~/.claude/bin/dauerbetrieb-leseauftrag.py erledigt --dienst whatsapp \
    --befund "10 Verlaeufe, 2 neu: Meier fragt nach Termin, Ruth hat abgesagt"
```

Gelesen wird mit dem fertigen Werkzeug, nicht mit handgeschriebenem JavaScript:

```bash
python ~/.claude/bin/whatsapp-verlaeufe.py               # letzte 10 Verläufe als JSON
python ~/.claude/bin/whatsapp-verlaeufe.py --chat "Ehrensberger" --nachrichten 20
python ~/.claude/bin/whatsapp-verlaeufe.py --dom         # Rückfallweg
```

**Es liest das Datenmodell, nicht den Bildschirm.** `window.require` ist im Tab
verfügbar, damit stehen `id.fromMe` (die Richtung), `unreadCount`, der Nachrichtentyp
und die Länge einer Sprachnachricht direkt zur Verfügung. **Es öffnet dabei keinen
Verlauf und schickt deshalb keine Lesebestätigung** — der frühere Bildschirmweg musste
jeden Verlauf öffnen und meldete damit zehn Menschen, jemand habe gelesen, obwohl nur
eine Maschine hingesehen hat.

**Modulnamen sind keine API.** Bricht das Modell, sagt das Werkzeug das und fällt nicht
von selbst auf `--dom` zurück, denn der Rückfallweg kostet eben jene Bestätigungen. Die
gemessene Fassung steht als `whatsapp_version` in der Ausgabe, damit ein Bruch datierbar
ist. Details und Modultabelle: `memory/dauerbetrieb-fenster-lesen.md`.

**Zwei Felder in `dauerbetrieb.json` steuern das**, und ihr Unterschied ist der Kern:
`lesbar` sagt, ob hier jemand hineinschreiben kann (ein Autopilot kann es nicht),
`leser` nennt das Projekt, das die Verläufe liest. Das ist bewusst nicht
`verantwortlich`: Der Zugang gehört werkstatt, der Inhalt dem Projekt, das den Kanal
fachlich führt, bei WhatsApp Business also erfolgsfahrplan.

Der Auftrag geht als Pool-Post an den `leser` **und** bleibt in
`state/dauerbetrieb-leseauftraege.json` offen stehen, bis ihn jemand mit einem Befund
schließt. Beides zusammen, weil eine gelesene Pool-Nachricht nach dem nächsten `/clear`
nirgends mehr steht. Stürzt der Kanal wiederholt ab, kommt trotzdem nur alle sechs
Stunden eine Erinnerung: Eine Meldung im Fünf-Minuten-Takt wird ignoriert, und dann ist
sie schlechter als keine. `bin/verantwortung-pruefen.py --dienste` zeigt offene Aufträge
neben dem Laufzustand.

**Der Befund ist eine Aussage, keine Zahl.** „Zehn Verläufe geprüft" wird abgewiesen.

**Ein weiterer Kanal kommt als Tab ins bestehende Profil** (`"profil": "dauerbetrieb"`,
gleicher Port), nicht in ein eigenes. Ein eigenes Profil bekommt nur, was zwingend getrennt
sein muss: ein zweites Konto beim selben Dienst, oder ein Betrieb mit eigenem Zeitplan.
Kleinanzeigen ist seit dem 12.08.2026 stillgelegt, eingemottet in `dauerbetrieb.json`: Es
wird *bearbeitet*, nicht nur *gesichtet*, und braucht dafür ohnehin ein MCP-Fenster.

### Markieren: nur mit dem Werkzeug, und `--tab` ist der bessere Weg

```bash
# EMPFOHLEN seit 14.08.2026: merkt sich die Identitaet des Tabs, nicht seinen Inhalt
python ~/.claude/bin/uebergabe-tab.py merken --tab "my\.fyrst\.de" \
    --wofuer "Max prueft die vorbereitete Ueberweisung und sendet sie ab"

# der alte Weg, weiterhin gueltig: ein Muster auf Titel oder URL
python ~/.claude/bin/uebergabe-tab.py merken --titel "(?i)visiotalent" \
    --wofuer "Max nimmt das Videointerview auf, Frist heute"

python ~/.claude/bin/uebergabe-tab.py liste
python ~/.claude/bin/uebergabe-tab.py entfernen --titel "(?i)visiotalent"
python ~/.claude/bin/uebergabe-tab.py entfernen --tab-id <ID aus der Liste>
```

**Ein Übergabetab ohne Eintrag in `~/.claude/state/uebergabe-tabs.json` stirbt**, und zwar
beim nächsten Antwortende durch den Stop-Hook, auch durch den einer fremden Sitzung.

**Vor dem Übergabetab steht eine Frage, die ihn oft ausschließt: Kann der Zustand, den ich
erzeuge, den Ort überleben, an dem ich ihn erzeuge?** Bei einem angemeldeten Fremdsystem
lautet die Antwort meistens nein, und zwar aus einer Zange heraus: Die Anmeldungen liegen
im **Hauptprofil**, dessen MCP-Fenster mit der Verbindung stirbt. Das **Dauerprofil** auf
Port 9223 überlebt, trägt aber keine Anmeldung, weil dort jeder Login scheitert (siehe
Serverwahl oben). Ein ausgefülltes Formular kann deshalb nicht von Claude zu Max wandern.

Gemessen am 22.08.2026 bei der Einrichtung eines Google-Ads-Verwaltungskontos: Formular
vorbereitet, Max sollte nur noch das reCAPTCHA setzen, neun Minuten später stand der Tab
auf `about:blank` und das Konto unverändert. **Wo ein reCAPTCHA oder ein anderer Bot-Schutz
im Weg steht, ist die Aufgabe ohnehin nicht teilbar**: Dann macht Max den ganzen Vorgang in
seinem eigenen Browser, und Claude liefert die Angaben zum Abtippen. Fall:
`maxone-pilots/irrtuemer/irrtum-021.md`.

**Der Unterschied zwischen den beiden Ankern, und er kostet Vorgänge:**

| | `--tab` (Identität) | `--titel` (Muster) |
|---|---|---|
| Navigation **innerhalb** eines Vorgangs (Bank, Unterseite) | überlebt | überlebt, wenn das Muster in der Adresse steht |
| Navigation **weg** vom Ziel (Bank → Rechnung, im selben Tab) | **überlebt** | **stirbt** |
| Browser-Neustart | stirbt (Tab ist ohnehin weg) | überlebt |
| ein Vorgang über mehrere Tabs | je Tab einer nötig | ein Muster reicht |

**Nimm `--tab`, wenn Max in genau diesem einen Tab etwas vorbereitet hat** (Formular,
Überweisung, Bewerbung). **Nimm `--titel`, wenn ein Vorgang mehrere Tabs oder mehrere
Fenster berührt** oder wenn der Tab erst noch entstehen soll: `--tab` braucht ihn offen.

**`--tab` bricht ab, wenn mehrere Tabs passen**, und listet sie. Das ist Absicht: Ein falsch
gemerkter Tab fällt erst auf, wenn der richtige weg ist.

**Das Muster bei `--titel` ist ein Regex und wird gegen Titel UND URL geprüft** (seit
13.08.2026, nur tab-genau über CDP; auf Fensterebene gibt es keine URL). **Nimm das Wort,
das die Navigation überlebt, und das steht fast immer in der Adresse.** Ohne `--bis` gilt
der Schutz bis zum Arbeitstagsende um 04:00.

**Warum es `--tab` gibt** (`werkstatt/BUGS.md` F-21): Am 14.08.2026 um 10:05 fiel ein
korrekt markierter Tab, weil er von `my.fyrst.de` auf `accounts.hetzner.com` navigierte. Er
war der letzte Tab seines Fensters und nahm es mit, samt vorbereiteter Überweisung. Die
CDP-`targetId` überlebt so einen Wechsel, gemessen an einem Tab, der Titel und URL
vollständig tauschte und seine Identität behielt.

**Von Hand in die Datei schreiben ist ein Fehler**, auch vorsichtig: Sie hat viele
Schreiber, und ohne Sperre gehen bei acht gleichzeitigen drei von acht Markern verloren
(`werkstatt/BUGS.md` F-9). **Nie mit PowerShell:** `ConvertTo-Json` wickelt ein Array in
`{"value":[…],"Count":n}`, der Hook liest danach null Muster, und jeder Schutz ist weg, auch
der fremder Sitzungen.

### Wann der Schließ-Hook läuft, und was dann fällt

| Wann | Modus | Was fällt |
|---|---|---|
| `SessionStart` | `--nur-leere` | nur Fenster ohne Inhalt (Titel leer oder `about:blank`) |
| `Stop`, nach jeder fertigen Antwort | `--nur-markierte` | **alles**, außer es steht irgendein Marker, dann gar nichts |
| `SessionEnd` | `--ausser-dauertabs` | alles außer Klasse 0 und gültig markierten Tabs |

Getroffen wird ausschließlich `chrome.exe` mit `--user-data-dir` auf `.playwright-profiles`
oder `.playwright-mcp-profile`. **Vor jedem scharfen Aufräumlauf ein Trockenlauf:**

```bash
bash ~/.claude/hooks/playwright-close.sh --nur-markierte --trockenlauf
```

## Tab-Herkunft: wer hat diesen Tab geöffnet

Die CDP-Tabliste liefert nur `id`, `title`, `url` und `type`, also **kein Herkunftsfeld**.
Der Schließ-Hook kann deshalb nicht sehen, ob ein Tab von dieser Session stammt oder von
einer Nachbarsession, die auf Max' Klick wartet. Genau daran gingen am 12. und 13.08.2026
Vorgänge verloren (`werkstatt/BUGS.md` F-15, F-16).

**Rückblickend** beantwortet das seit dem 12.08.2026 `bin/browser-forensik.py` aus den
Session-JSONL, in denen Claude Code jeden Tool-Aufruf mitschreibt.

**Laufend** schreibt seit dem 13.08.2026 ein PostToolUse-Hook mit, wer einen Tab öffnet:

```bash
python ~/.claude/hooks/tab-herkunft.py     # als Hook registriert, nicht von Hand rufen
cat ~/.claude/state/tab-herkunft.ndjson    # eine Zeile je Öffnung
```

Matcher `mcp__.*__browser_(navigate|tabs)`, registriert in `settings/base.json`, gilt damit
auf beiden Geräten. Protokolliert werden Zeit, Session, Projekt, URL und MCP-Server, gedeckelt
auf 400 Zeilen. **Als Hook und nicht als Schritt in meinem Ablauf**, weil eine Annahme über
mein Verhalten keine Absicherung ist; **nicht aus den JSONL**, weil ein Scan darüber Sekunden
kostet und der Schließ-Hook nach jeder Antwort läuft.

**Der Matcher ist belegt** (13.08.2026, 17:15): sieben Zeilen aus zwei fremden Sessions,
darunter echte `navigate`-Aufrufe ohne Probemodus. Der Probemarker ist damit entfernt.

### Was der Schließ-Hook daraus macht (seit 13.08.2026, `BUGS.md` F-19)

**Ein Tab, dessen HOST in keiner Protokollzeile steht, hat keine Session geöffnet, gehört
also Max und bleibt stehen.** Das ist die dritte Klasse neben „markiert" und „Arbeitstab",
und ohne sie fiel alles Unbekannte in die Restklasse, die geräumt wird. Dreimal am
13.08.2026 hat das Max' eigenen Kleinanzeigen-Tab gekostet.

Drei Dinge, die man beim Anfassen wissen muss:

- **Verglichen wird der Host, nicht die volle Adresse.** Ein Vorgang navigiert (das
  DAK-Postfach stand an einem Nachmittag unter drei Adressen). Bei Gleichheitsvergleich
  gälte nach dem ersten Klick jeder Tab als fremd, und ein Schutz, der alles schützt, lässt
  die Fensterzahl wieder wachsen.
- **Die Klammer:** Ist die erste Protokollzeile jünger als der Browserstart, kann das
  Protokoll über ältere Tabs dieses Fensters nichts sagen, und die Prüfung fällt aus. Ohne
  sie wäre der Hook nach der Einführung lautlos wirkungslos gewesen.
- **Sie kann nur behalten, nie schließen.** Ein Tab, der ohne sie gefallen wäre, fällt
  schlimmstenfalls weiter.

Testbar über `CLAUDE_TAB_HERKUNFT=<pfad>` mit `-NurProfil` und eigener `-MarkerDatei`, wie
`CLAUDE_DAUERBETRIEB` es für die Dienstliste vormacht. **Ein `about:blank`-Tab hat keinen
Host und fällt weiter**, das ist Absicht.

**Das Schließ-Protokoll trägt seit demselben Tag `session`**, also welcher Hook geschlossen
hat. Vorher war das nur über Transkript-Zeitstempel zu erschließen.

## Werkzeugwahl: Node oder Browser

Der häufigste Denkfehler, und er kostet jedes Mal einen ganzen Block:

| Werkzeug | läuft wo | `document` da? |
|---|---|---|
| `browser_evaluate` | **im Browser** | ja |
| `browser_run_code_unsafe` | **im Node-Prozess** des Servers | **nein** |

**Regel:** Reines DOM-Lesen immer mit `browser_evaluate`. Nur wenn echte `page`-Aktionen
nötig sind (Klick, Navigation, mehrstufige Locator), `run_code_unsafe`, und dort **jeden**
DOM-Zugriff in `page.evaluate(…)`, `page.$eval` oder `page.$$eval` kapseln. Ein einziges
freies `document.body.innerText` im Node-Teil bricht den gesamten Block ab
(`ReferenceError`), auch wenn die Aktionen davor schon gelaufen sind.

## Einen Wert abfragen, ohne Playwright anzufassen: `bin/cdp.py`

Für die häufigste Prüfung an einer ausgelieferten Seite (Tab auf, einen Wert lesen, Tab zu)
braucht es keinen MCP-Server. Chrome hört auf denselben Debug-Ports, die schon in
`dauerbetrieb.json` stehen, und `bin/cdp.py` spricht sie direkt an:

```bash
python ~/.claude/bin/cdp.py tabs                       # was auf 9222 und 9223 offen ist
python ~/.claude/bin/cdp.py fragen --tab 8899 --js "document.title"
python ~/.claude/bin/cdp.py fragen --url http://127.0.0.1:8899/index.html \
    --js "JSON.stringify({takt: window.__reloadTakt, karten: document.querySelectorAll('section').length})"
```

**Der Unterschied zwischen `--url` und `--tab` ist der Besitz.** `--url` öffnet einen
eigenen Tab und schließt ihn wieder, auch wenn der Ausdruck scheitert. `--tab` sucht einen
bestehenden per URL- oder Titel-Teil und lässt ihn stehen, denn er gehört jemand anderem,
oft Max. Nur `--offen-lassen` hält einen selbst geöffneten Tab, und dann sagt das Werkzeug
den Schließbefehl dazu.

**Wann trotzdem Playwright:** sobald geklickt, getippt oder auf ein Element gewartet werden
muss. `cdp.py` fragt einen Wert ab, es bedient nichts.

**Zwei Fallen, beide gemessen:** `/json/new` verlangt **PUT**, POST antwortet 405. Und
`--warten` ist mit einer Sekunde vorbelegt, weil eine frisch geöffnete Seite ihr Skript noch
nicht ausgeführt hat; ein Wert, den es erst setzt, wäre sonst schlicht `undefined`, und das
sieht wie ein Befund aus.

## Bekannte Fehlerbilder

**Ein Tab verschwindet, obwohl das Fenster lebt.** Nicht der Schließ-Hook, der kann nur
ganze Fenster treffen. Was bleibt, ist der geteilte MCP-Server: ein `browser_close` oder
ein Server-Neustart einer Nachbarsitzung. „Steht als Dauertab offen" ist deshalb keine
Zusicherung, sondern eine Momentaufnahme, die jeder Durchgang neu prüfen muss.
(`werkstatt/BUGS.md` F-5)

**Playwright-Server stapeln sich.** Sie räumen nur am Ende ihrer eigenen Sitzung ab; am
06.08.2026 liefen 36 aus sechs Sitzungen gleichzeitig. Der `node`-Prozess des MCP-Servers
wird **nie** beendet, er gehört Claude Code.

**Eine lokale HTML-Datei lässt sich nicht ansehen**, Playwright blockt `file:`. Einen
kleinen Server davorstellen; dessen Prozess heißt `python3.13`, ein Kill auf `python.exe`
trifft ihn nicht.

> **Und der eigene Serverstart scheitert still, wenn der Port schon belegt ist**
> (14.08.2026). `python -m http.server 8899` mit `>/dev/null 2>&1` verschluckt das
> „Address already in use", der folgende `curl` antwortet trotzdem, und man hält den
> **fremden** Server für den eigenen. Aufgefallen an einem fremden `<title>Heute</title>`;
> ein Kill hätte die Nachbarsession getroffen. **Also nach dem Start prüfen, ob wirklich
> die eigene Seite antwortet**, nicht nur, ob irgendetwas antwortet. Beendet wird über den
> Port, nie über den Prozessnamen:
>
> ```powershell
> Get-NetTCPConnection -LocalPort 8931 -State Listen |
>   ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -Confirm:$false }
> ```

**Autofill lässt sich nicht transplantieren.** Seit Chrome 127 sind Passwörter mit
App-Bound Encryption zweifach DPAPI-gewickelt und werden über einen SYSTEM-Dienst
entschlüsselt. Datei-Kopie zwischen Profilen, externer CDP-Chrome und `--isolated` sind
deshalb technisch aussichtslos, nicht nur schwierig. Cookies teilen geht über Playwrights
`storageState`, weil dort bereits entschlüsselte Werte exportiert werden.

**„Browser is already in use for … .playwright-mcp-profile, use --isolated".** Eine andere
Sitzung hält das Hauptprofil, und der eigene MCP-Server kommt an den laufenden Browser gar
nicht heran, auch nicht für ein `browser_tabs list`. Der Rat in der Meldung ist für Max'
Arbeit **kein gültiger Weg** (`--isolated` und `playwright-shared` sind gesperrt), und die
fremde Sitzung wird nie abgeräumt. Was hilft: `bash ~/.claude/hooks/playwright-close.sh
--nur-markierte --trockenlauf` zeigt ohne Eingriff, wer dort arbeitet, und danach entscheidet
man zwischen warten und einem Weg ohne Browser. `[B: 11.08.2026, das Hauptprofil hielt einen
Kleinanzeigen-Tab einer Nachbarsitzung]`

**Headless-Chrome ist KEIN Ersatz, um eine Seite anzusehen.** Der naheliegende Ausweg
(`chrome.exe --headless=new --screenshot` mit Wegwerf-Profil) scheitert an drei Stellen
zugleich, alle am 11.08.2026 an `griddone.de` gemessen: `--window-size=390` rendert das
**Desktop**-Layout in 390 Pixel und lässt es überlaufen, weil `<meta viewport>` nur auf
echten Mobilgeräten greift; `--screenshot` liefert nur das Viewport, nie die ganze Seite;
und eine Sektion, die per Scroll-Trigger einblendet, bleibt nach einem eingebauten
`scrollTo` **leer weiß** im Bild. Für den Blick auf eine bestimmte Stelle taugt das nicht.
Wer wirklich sehen muss, wartet auf das Hauptprofil.

**Die Fensterfarbe ist der maxone-Akzent `#e8630a`**, damit Max ein Automationsfenster von
seinem eigenen Chrome unterscheidet. Chrome speichert sie in `<profil>/Default/Preferences`
als signed 32-bit ARGB, `#e8630a` mit Alpha ist **`-1547510`**, Felder `browser.theme.user_color`
und `user_color2`, bei bestehenden Profilen zusätzlich unter `account_values`. **Chrome muss
beim Schreiben beendet sein.** Ein neu angelegtes Profil ist wieder nicht orange, die Farbe
wird also im selben Zug gesetzt.

## Grenzen, die nicht verhandelt werden

**Subagenten fassen den Browser nicht an** (Max, 28.07.2026). Sie teilen Browser und Profil
mit der Hauptsitzung und reißen deren angemeldeten Tab mit. Rechercheaufträge werden auf
`curl` festgelegt, mit ausdrücklichem Browser-Verbot im Prompt. Was ein Agent trotzdem
hinterlässt, räumt die Hauptsitzung.

**Max' eigener Chrome wird nie bedient** (`rules/nie-max-eigenen-browser-bedienen.md`),
weder ferngesteuert noch beendet noch neu gestartet. Erlaubt ist reines Lesen auf
Dateiebene.

**windows-mcp bleibt unangetastet, sobald Playwright der bessere Weg ist** (Max,
26.07.2026). Fehlt für Playwright eine Anmeldung, wird sie hergestellt, statt auszuweichen.

**Im Automationsfenster kann Max keine neuen Fenster, Tabs, Vorschau-PDFs oder
Dateidialoge öffnen.** In-Page tippen und klicken geht. Braucht ein menschlicher Schritt
mehr, wird er in Max' eigenen Browser ausgelagert.

**Fremde Sitzungen werden nie eigenmächtig beendet.**

## Nachweise

- Profil-Korrektur: Max 11.07.2026, nach dem zweiten gescheiterten BA-Login.
- Widerspruch der beiden Memories: Bestandsaufnahme 11.08.2026,
  `python ~/.claude/bin/handbuch-luecken.py playwright` (1041 Fundstellen, 291 Dateien).
- App-Bound Encryption: [Chrome-App-Bound-Encryption-Decryption/RESEARCH.md](https://github.com/xaitax/Chrome-App-Bound-Encryption-Decryption/blob/main/docs/RESEARCH.md),
  [chromium os_crypt/app_bound_encryption_win.cc](https://github.com/chromium/chromium/blob/main/chrome/browser/os_crypt/app_bound_encryption_win.cc).
- Tab-Verlust trotz lebendem Fenster: `werkstatt/BUGS.md` F-5, gemessen 11.08.2026 09:20.
- Fensterfarbe in 25 Profilen gesetzt: 10.08.2026.
