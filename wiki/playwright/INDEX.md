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

**Ein weiterer Kanal kommt als Tab ins bestehende Profil** (`"profil": "dauerbetrieb"`,
gleicher Port), nicht in ein eigenes. Ein eigenes Profil bekommt nur, was zwingend getrennt
sein muss: ein zweites Konto beim selben Dienst, oder ein Betrieb mit eigenem Zeitplan.
Kleinanzeigen ist seit dem 12.08.2026 stillgelegt, eingemottet in `dauerbetrieb.json`: Es
wird *bearbeitet*, nicht nur *gesichtet*, und braucht dafür ohnehin ein MCP-Fenster.

### Markieren: nur mit dem Werkzeug

```bash
python ~/.claude/bin/uebergabe-tab.py merken --titel "(?i)visiotalent" \
    --wofuer "Max nimmt das Videointerview auf, Frist heute"
python ~/.claude/bin/uebergabe-tab.py liste
python ~/.claude/bin/uebergabe-tab.py entfernen --titel "(?i)visiotalent"
```

**Ein Übergabetab ohne Eintrag in `~/.claude/state/uebergabe-tabs.json` stirbt**, und zwar
beim nächsten Antwortende durch den Stop-Hook, auch durch den einer fremden Sitzung.

**Das Muster ist ein Regex und wird gegen Titel UND URL geprüft** (seit 13.08.2026, nur
tab-genau über CDP; auf Fensterebene gibt es keine URL). **Nimm das Wort, das die Navigation
überlebt, und das steht fast immer in der Adresse:** Max klickt weiter, der Titel ändert
sich. Ohne `--bis` gilt der Schutz bis zum Arbeitstagsende um 04:00.

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
