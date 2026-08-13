# VS Code: Bedienhandbuch

Angelegt 11.08.2026, nachdem `code <ordner>` ein laufendes Fenster samt Claude-Session
überschrieben hatte und die Frage „steht dieses Fenster offen?" nicht beantwortbar war.
Gilt estate-weit: VS Code ist Max' einzige Arbeitsoberfläche, jedes Projekt läuft darin.

**Das Bedienbare steht oben, die Nachweise stehen unten.**

## Abgrenzung: hier steht der Editor, nicht Claude Code

Entschieden am 11.08.2026 auf Max' Frage, ob beides in ein Handbuch gehört. **Getrennt**,
und die Messung war eindeutig: Claude-Code-Bedienwissen liegt an **1.229 Stellen** im
Bestand, reines VS-Code-Wissen an **56**. Zusammengelegt entstünde kein VS-Code-Handbuch
mit Claude-Anhang, sondern das Gegenteil. Dazu läuft Claude Code auch als CLI, im Web und
im Desktop; VS Code ist nur eine seiner Oberflächen.

| Frage | Handbuch |
|---|---|
| Fenster, Workspaces, Zustände, Erweiterungen, Project Manager | **hier** |
| Hooks, Skills, Commands, `settings.json`, Berechtigungen, Kontext, Pool | Claude Code (noch nicht gebaut) |
| **Die Naht**: Anmelde-Abbruch, Sessions-Picker, Reload nach Extension-Update, `statusLine` im Panel | **Claude Code**, denn es sind Claude-Probleme, die zufällig in VS Code auftreten |

Solange das Claude-Code-Handbuch fehlt, steht der Anmelde-Abbruch weiter unten hier und
zieht beim Bau um.

## Fenster: die drei Sätze, die man wirklich braucht

| Aufgabe | Befehl | Falle |
|---|---|---|
| Welche Fenster sind offen? | `code --status`, Zeilen `window [N] (Titel)` | dauert 2,7 s |
| Neues Fenster öffnen | `code --new-window <ordner>` | **ohne `--new-window` wird das aktive Fenster überschrieben** |
| Offenes Fenster nach vorn | vorher mit `--status` prüfen, sonst gar nicht öffnen | VS Code holt nicht von selbst nach vorn |

**`code <ordner>` ohne Flag ist gefährlich.** Ist der Ordner nirgends offen, lädt VS Code
ihn in das zuletzt aktive Fenster und wirft dessen Inhalt hinaus, samt der Claude-Session,
die dort lief. Gemessen am 11.08.2026: PID 18648 wechselte von „werkstatt (Workspace)" auf
„repivot.me", ohne Warnung, ohne zweites Fenster.

**`code --status` ist die einzige belastbare Fensterliste**, und zwar aus zwei Gründen:

- Die Prozessliste trägt `MainWindowTitle` nur für **einen** Prozess. Bei drei offenen
  Fenstern nennt `Get-Process Code` genau einen Titel, die anderen fehlen komplett.
- Die Kommandozeile (`Win32_Process.CommandLine`) enthält den Ordner nur beim allerersten
  Fenster. Später geöffnete tragen ihn nirgends.

Auswertbar mit:

```bash
code --status 2>/dev/null | grep -oE "window \[[0-9]+\] \(.*\)"
```

Im Estate benutzt von `~/.claude/bin/pool.py` (`offene_fenstertitel`, `fenster_steht`).

**Ein Fenster wird nie per `Stop-Process -Force` geschlossen.** VS Code zeigt beim nächsten
Start „The window terminated unexpectedly (reason: 'crashed')" und bietet an, die Sitzung
wiederherzustellen. Am 11.08.2026 einmal passiert und Max hat zu Recht gefragt, was das
soll.

## Wo VS Code seine Zustände speichert: drei Ebenen

Das ist die Antwort auf „aber die Workspace-Datei speichert doch die Zustände" (Max,
11.08.2026). Sie stimmt zur Hälfte, und die Trennung ist scharf.

| Ebene | Ort | Was dort liegt |
|---|---|---|
| **Global** | `%APPDATA%\Code\User\globalStorage\state.vscdb` | **Reihenfolge** der Leisten-Symbole, Anheftung, zuletzt geöffnete Ordner |
| **Pro Workspace** | `%APPDATA%\Code\User\workspaceStorage\<hash>\state.vscdb` | **Sichtbarkeit** je Ansicht, aktives Panel, offene Editoren, Baumzustände |
| **`.code-workspace`** | im Projektordner, versioniert | nur `folders` und `settings` (bei Max: Peacock-Farben). **Kein UI-Zustand** |

**Belegt am 11.08.2026:** Der Schlüssel `workbench.auxiliarybar.pinnedPanels` (mit den
`order`-Werten) steht in **0 von 107** Workspace-Speichern, also rein global. Der
Workspace führt daneben `workbench.auxiliarybar.viewContainersWorkspaceState`, und der
trägt ausschließlich `visible: true/false`, keine Reihenfolge.

**Merksatz: Wer wo steht, ist global. Wer überhaupt zu sehen ist, hängt am Workspace.**

**Ein Projekt hat oft ZWEI Workspace-Speicher**, einen für den Ordner und einen für die
`.code-workspace`-Datei, mit verschiedenen Hashes. Wer den falschen liest, misst einen
Zustand, den Max nie sieht. Zuordnung steht je Ordner in `workspace.json`.

**Schreiben nur bei beendetem VS Code.** Es hält den Zustand im Speicher und schreibt ihn
beim Beenden zurück, eine Änderung im laufenden Betrieb ist spätestens dann weg.

### Claude vor Copilot in der rechten Leiste

Werkzeug: `python ~/.claude/bin/vscode-claude-nach-vorn.py` (weigert sich, solange
`Code.exe` läuft, legt vorher eine Sicherung an). Schneller geht es per Maus: Symbol
greifen und nach links ziehen, das wirkt sofort und gilt danach in jedem Fenster.

Ausgangslage am 11.08.2026: `workbench.panel.chat` (Copilot) auf `order` 1, das
Claude-Panel auf 101.

## Projektfarben: zwei Orte, und welcher gilt, hängt am Öffnungsweg

Die Farbe, an der Max seine drei gleichzeitig offenen Fenster unterscheidet, kann an zwei
Stellen stehen, und **welche gilt, ist keine Eigenschaft des Projekts, sondern des
Öffnungswegs**:

| Datei | gilt, wenn geöffnet wird über |
|---|---|
| `<projekt>/<name>.code-workspace` | Projektmanager, „zuletzt geöffnet", Doppelklick auf die Datei |
| `<projekt>/.vscode/settings.json` | `code <ordner>`, also auch **jedes vom Pool geweckte Fenster** (`pool.py` ruft `code --new-window <ordner>`) |

`workbench.colorCustomizations` ist eine **fensterweite** Einstellung. Ist eine
Workspace-Datei geöffnet, gewinnt deren `settings`-Block, und die Ordner-Fassung bleibt
wirkungslos. **Belegt am lebenden Fenster** (13.08.2026): `Zentinel` zeigte `#acca21` aus
seiner Workspace-Datei, während `.vscode/settings.json` `#ba4f08` trug. 46 der 78 Projekte
haben eine Workspace-Datei.

**Folge: Dasselbe Projekt kann in zwei Farben erscheinen**, je nachdem wer es geöffnet hat.
Genau das macht die Unterscheidung kaputt, für die die Farben da sind.

```bash
python ~/.claude/bin/projektfarbe.py <projekt> "#rrggbb"   # setzt BEIDE Orte
python ~/.claude/bin/projektfarbe.py --pruefen             # nur Befunde und Kontraste
python ~/.claude/bin/projektfarbe.py --spiegeln            # Trockenlauf des Abgleichs
python ~/.claude/bin/projektfarbe.py --spiegeln --scharf
python ~/.claude/bin/projektfarbe.py --schrift <projekt>…  # nur die Schrift lesbar machen
```

`--schrift` dreht ausschließlich Vordergrundfarben auf den lesbareren Kandidaten, **keine
einzige Hintergrundfarbe wird angefasst**, das Fenster behält seine Farbe. Angefasst wird
nur, was unter 4.5:1 liegt. Der Alpha-Anhang (`…99`) gehört zur Deckkraft und bleibt.
**Ohne Projektnamen läuft es über alle**, und das ist selten gewollt: Es findet auch
winzige Nebenelemente in Projekten, deren Hauptfarbe stimmt.

**Beide Dateien oder keine.** Ist eine davon in einem fremden Repo versioniert, bleibt auch
die andere unangetastet. Nur eine zu ändern hieße, die Divergenz neu zu erzeugen, gegen die
das ganze Werkzeug gebaut ist.

`--spiegeln` **kopiert** den wirksamen Satz in die andere Datei, statt ihn neu abzuleiten:
Neu berechnen würde auch Abzeichen, Schrift und Hover der bereits sichtbaren Fassung
ändern, und das Ziel ist, dass sich am gewohnten Bild möglichst wenig ändert. Ist die
Zieldatei in einem **fremden** Repo versioniert, fasst das Werkzeug sie nicht an, sondern
meldet sie: Eine Änderung dort wäre ein uncommitteter Stand, den eine fremde Session
erklären müsste.

**Peacock ist deinstalliert** (13.08.2026) und wird nicht vermisst: Es war ein Generator,
kein Anzeiger. VS Code liest die Farbwerte selbst, sie bleiben ohne die Erweiterung stehen.
Was fehlte, war allein die Fähigkeit, einem neuen Projekt eine Farbe zu geben, und das ist
das Werkzeug oben.

**Das neue Design schluckt die Farben nicht.** `workbench.experimental.modernUI` existiert
in 1.133.0 mit `default: false` und `experiment: {mode: "auto"}`, wird also gestaffelt
ausgerollt, ohne in den Einstellungen zu stehen. Titelleiste, Aktivitätsleiste und
Statusbalken tragen ihre Farben weiterhin (gemessen am Fenster, dazu Max am 13.08.2026:
„Die Farben sind von Peacock geblieben"). Die Sorge, es brauche eine Ersatz-Unterscheidung,
hat sich damit erledigt.

## Bekannte Fehlerbilder

**„Claude ist abgemeldet", meist morgens.** Nicht die Geräte-Replikation, sondern ein
offener Fehler der Erweiterung: Die Erneuerung des Zugangs scheitert beim Start
(`refresh failed`), obwohl der Refresh-Token noch Wochen gültig ist. Verschärft durch
mehrere gleichzeitig startende Fenster. Vier GitHub-Meldungen dazu sind geschlossen, drei
davon von einem Staleness-Bot ohne Fix. Details:
`~/.claude/projects/…/memory/woechentliche-abmeldung-ist-ein-extension-fehler.md`.

**Die VS-Code-Logs rotieren bei rund 4,5 MB.** Ein `grep` über ältere Startordner misst
deshalb nicht, ob ein Fehler auftrat, sondern nur, ob die Zeile noch in der Datei steht.
Häufigkeiten sind rückwirkend nicht feststellbar.

**Project Manager: das Pfadfeld im Git-Cache heißt `fullPath`, nicht `rootPath`.** Die
`projects.json` daneben benutzt den anderen Namen. Wer blind schreibt, bekommt eine
Erfolgsmeldung und ändert nichts. Pflegeskript: `~/.claude/bin/mx-projektliste.py`, läuft
als Schritt 4c in `/driftglobal`. Nach einer Ordner-Umbenennung zeigt die Liste auf tote
Pfade, bis Max einmal „Project Manager: Refresh Projects" klickt.

**Die `.code-workspace` wird mit `Edit` angefasst, nie mit `Write`.** Sie trägt
Extension-Zustände wie die Peacock-Farbe, die ein Überschreiben verliert.

**Electron-Anwendungen aus einer Claude-Code-Shell starten nicht.** Claude Code läuft
selbst auf Electron und vererbt `ELECTRON_RUN_AS_NODE=1`, wodurch jede Electron-App als
reines Node läuft und Chromium-Argumente verwirft. Abhilfe: `env -u ELECTRON_RUN_AS_NODE`
davorsetzen. Betrifft Chrome, VS Code, Signal, Discord, Obsidian.

## Grenzen, die nicht verhandelt werden

**Max' eigener Chrome wird nie ferngesteuert** (`rules/nie-max-eigenen-browser-bedienen.md`).
Sinngemäß gilt für VS Code: Fenster werden nicht ungefragt beendet, neu gestartet oder mit
fremdem Inhalt überladen. Es ist seine laufende Arbeitsumgebung, in der parallel Sitzungen
und Formulare leben.

**Höchstens drei Projektfenster gleichzeitig** (Max, 11.08.2026). Durchgesetzt vom Pool,
der bei vollem Haus auf eine Weckliste setzt statt zu öffnen. Gezählt werden Projekte,
nicht Fenster.

## Nachweise

- Fenster-Ersetzung ohne `--new-window`: eigene Messung 11.08.2026, PID 18648, Titelwechsel
  „werkstatt (Workspace)" → „repivot.me", Korrektur im selben Zug.
- `MainWindowTitle` nur für einen Prozess: `Get-Process Code | Where MainWindowTitle`
  lieferte eine Zeile, während `code --status` drei Fenster führte.
- `pinnedPanels` rein global: Scan über alle 107 Verzeichnisse in `workspaceStorage`,
  0 Treffer.
- Version zum Zeitpunkt der Aufnahme: Code 1.132.0, Commit `df53daab`, 04.08.2026.
