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

**Aufgelöster Widerspruch, 11.08.2026:** `memory/reference_playwright_profile_per_project.md`
vom 30.05.2026 verlangt das Gegenteil („niemals das Default-Profil aktiv nutzen, jedes
UI-Projekt bekommt sein eigenes"). **Diese Fassung ist überholt.** Sie löste ein anderes
Problem, nämlich gegenseitige Sperren beim parallelen Arbeiten, und opferte dafür genau
das, was seit dem 11.07. Vorrang hat: die Anmeldungen. Pro-Projekt-Profile gelten heute
nur noch in zwei Fällen: für ein zweites Konto (siehe oben) und für **Dauerbetrieb**
(`~/.playwright-profiles/repivot.me` trägt den RePivot-Autopiloten).

## Fenster und Tabs

**Vor jedem Öffnen zuerst prüfen, was schon offen ist** (`browser_tabs` mit `list`). Ein
Fenster kann von einer früheren Sitzung bewusst offen gelassen worden sein.

**Drei Klassen, die erste zutreffende gewinnt** (Volltext:
`rules/keine-artefakte-auf-max-bildschirm.md`):

| Klasse | Was | Regel |
|---|---|---|
| **0 Dauerprofil** | trägt laufenden Betrieb (`repivot.me`) | nie schließen, nie als Befund melden |
| **1 Dauertab** | WhatsApp Business, Kleinanzeigen gewerblich | bleibt offen, auch am Sitzungsende |
| **2 Übergabetab** | wartet auf genau einen Klick von Max | bleibt bis Sitzungsende, **mit Übergabesatz UND Markierung** |
| **3 Arbeitstab** | alles andere | sofort schließen, wenn der Schritt fertig ist |

**Innerhalb einer Aufgabe wird nicht zwischen Einzelschritten geschlossen.** Erst wenn die
ganze Aufgabe fertig ist, nicht der Einzelschritt.

**Ein Übergabetab ohne Eintrag in `~/.claude/state/uebergabe-tabs.json` stirbt**, und zwar
beim nächsten Antwortende durch den Stop-Hook, auch durch den einer fremden Sitzung.
Ansage und Markierung sind ein Vorgang, und die Markierung kommt zuerst:

```json
[{ "titel": "<Regex auf den Fenstertitel>", "wofuer": "<was Max dort tut>",
   "bis": "<ISO-Zeitstempel>" }]
```

Der Titel ist ein **Regex und muss die Navigation überleben**: Max klickt weiter, der Titel
ändert sich, ein exakter Treffer wäre nach dem ersten Klick tot.

**Die Markerdatei wird nie mit PowerShell geschrieben.** `ConvertTo-Json` wickelt ein Array
in `{"value":[…],"Count":n}`, der Hook liest danach null Muster, und jeder Schutz ist weg,
auch der fremder Sitzungen. Python oder `Edit`, nichts sonst.

**Vor jedem scharfen Aufräumlauf ein Trockenlauf:**

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
