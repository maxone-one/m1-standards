---
title: CopyQ, Max' Zwischenablage
description: Verlauf lesen und befuellen per CLI, die Windows-Fallen, Einstellungen, Fehlerbilder
---

# CopyQ, Max' Zwischenablage

Seit dem 12.08.2026 ersetzt CopyQ den Windows-Zwischenablageverlauf. **Der Grund war
nicht die Länge, sondern der Zugang:** Max wörtlich, „der entscheidende Faktor für mich
war, dass du mitlesen kannst". Windows' eigener Verlauf ist für eine Session unsichtbar,
CopyQ hat eine vollwertige Kommandozeile.

## Das Bedienbare zuerst

**Immer über den Wrapper**, nie direkt über `copyq.exe` (der Grund steht unter Fallen):

```bash
python ~/.claude/bin/ablage.py                    # die letzten 15 Einträge
python ~/.claude/bin/ablage.py liste 40
python ~/.claude/bin/ablage.py lies 3             # Eintrag 3 im Volltext
python ~/.claude/bin/ablage.py suche "Rechnung"
python ~/.claude/bin/ablage.py setze "Text"       # in die Zwischenablage legen
python ~/.claude/bin/ablage.py merke "Text"       # ablegen OHNE die Ablage zu ändern
python ~/.claude/bin/ablage.py tabs
python ~/.claude/bin/ablage.py --tab Diktate liste
```

**`setze` gegen `merke` ist der Unterschied, der zählt.** `setze` überschreibt, was Max
gerade kopiert hat, und das ist ein Eingriff in seine laufende Arbeit. `merke` legt nur
ab. Im Zweifel `merke`.

**Für Max am Rechner:** `Win+V` oder `Strg+Umschalt+V`. Beide Kürzel liegen auf demselben
Befehl „Verlauf anzeigen". `[?]` Ob Windows `Win+V` wirklich durchlässt, kann nur Max
prüfen, das System reserviert diese Kombination für seinen eigenen Verlauf. Klappt sie
nicht, ist `Strg+Umschalt+V` der sichere Weg.

## Windows-Fallen, alle am 12.08.2026 gemessen

**1. `copyq.exe` schreibt nichts in die Konsole.** Es ist als GUI-Anwendung gelinkt.
`copyq read 0` liefert deshalb **leer statt eines Fehlers**, und wer das nicht weiß, hält
eine volle Ablage für leer. Ausgabe gibt es nur über Umleitung in eine Datei:

```bash
copyq.exe --version > out.txt 2>&1; cat out.txt
```

Ein `copyq.com` (die Konsolen-Variante älterer Versionen) **gibt es in v16.0.0 nicht
mehr**. Der Wrapper nimmt einem das ab.

**2. Es liegt nicht in `C:\Program Files\CopyQ`.** Der winget-Installer legt es nach
`%LOCALAPPDATA%\Programs\CopyQ`. Der Program-Files-Pfad ist geraten und war am 12.08.
der erste Fehlversuch.

**3. Ohne laufenden Server antwortet gar nichts.** Die Meldung lautet „Es kann keine
Verbindung zum Server hergestellt werden". Start ohne Fenster:

```bash
"$LOCALAPPDATA/Programs/CopyQ/copyq.exe" --start-server &
```

**Der Server, den der Installer startet, überlebt nicht.** winget führt die Installation
erhöht aus, und der Prozess geht mit dieser Sitzung. Nach jeder Neuinstallation also
einmal selbst starten, sonst ist der erste CLI-Aufruf tot.

**4. Umlaute brauchen erzwungenes UTF-8.** Python fällt sonst auf cp1252 zurück und Max'
Diktattext kommt als Fragezeichen an. Im Wrapper erledigt (`reconfigure(encoding="utf-8")`).

**5. Kein `\n` in Skripten, die über Bash gehen.** Die Shell frisst es, CopyQ bekommt einen
Zeilenumbruch mitten im String und meldet `SyntaxError: Expected token )`. Skripte über
eine Datei und `eval -- "$(cat datei.js)"` schicken.

## Was eingestellt ist

| Einstellung | Wert | warum |
|---|---|---|
| `maxitems` | 10000 | Windows kann 25, das war der Anlass |
| `autostart` | true | `copyq.lnk` im Autostart-Ordner, geprüft |
| `check_clipboard` | true | Standard, sonst fängt es gar nichts |
| `clipboard_notification_lines` | 0 | kein Popup bei jedem Kopieren, siehe `keine-artefakte-auf-max-bildschirm.md` |
| globales Kürzel | `meta+v`, `ctrl+shift+v` | Befehl „Verlauf anzeigen" |

Ändern per `copyq config <name> <wert>`, alle 192 Optionen zeigt `copyq config`.

**Der Windows-Verlauf läuft bewusst weiter** (`EnableClipboardHistory=1`, Dienst
`cbdhsvc_*`). Er ist die Rückfallebene, solange nicht geklärt ist, ob `Win+V` bei CopyQ
ankommt. Erst danach entscheiden, ob er abgeschaltet wird, und das ist Max' Entscheidung.

## Duplikate lösen sich von selbst

**Gemessen:** vier Kopiervorgänge, dreimal derselbe Text, danach **zwei** Einträge im
Verlauf. CopyQ schiebt eine Wiederholung nach oben, statt sie zu stapeln. Max' Beobachtung
doppelter Einträge im Windows-Verlauf ist damit strukturell erledigt, unabhängig von jedem
Filter.

## Der Wispr-Flow-Filter, noch offen

**Der Stand:** Wispr Flow tippt nicht, es legt den diktierten Text in die Zwischenablage
und drückt Strg+V. In `AppData\Roaming\Wispr Flow\config.json` gibt es keinen Schalter,
das abzustellen (192 Schlüssel geprüft, nur `polishAutoPaste`). Die Diktate landen also
zwangsläufig im Verlauf.

**Warum noch kein Filter steht:** CopyQ filtert über `application/x-copyq-owner-window-title`,
also den Titel des Fensters, aus dem kopiert wurde. Beim Einfügen durch Wispr Flow ist das
aktive Fenster aber das **Ziel** (VS Code, der Browser), nicht Wispr Flow. Ein Filter auf
den Fenstertitel würde also das Falsche treffen. `[?]` Welche Formate ein echter
Wispr-Eintrag trägt, ist noch nicht gemessen; ein per PowerShell gesetzter Eintrag trug nur
`text/plain`.

**Der nächste Schritt** ist eine Messung an einem echten Diktat, nicht ein geratener
Filter:

```bash
python - <<'PY'
import sys; sys.path.insert(0, '/c/Users/max/.claude/bin'); import ablage
print(ablage.js("var i = getItem(0); var o = []; for (var k in i) o.push(k); print(o.join('\\n'));"))
PY
```

Trägt der Eintrag ein unterscheidbares Merkmal, wandern Diktate per Automatic Command in
einen eigenen Tab (`tab: 'Diktate'`), statt verworfen zu werden: Die Haupt-Ablage bleibt
sauber und der Text ist trotzdem noch da.

## Nachweise

- **CopyQ 16.0.0**, installiert am 12.08.2026, 11:00 Uhr, `winget install hluk.CopyQ`,
  Qt 6.10.2, MSVC, `has-global-shortcuts: 1`.
- **Herausgeber** Lukas Holecek (`hluk`), GitHub seit 2008, 12.116 Sterne, 584 Forks,
  GPL-3.0, letzter Push 03.08.2026, Releases im Vier- bis Sechs-Wochen-Takt.
- **Windows-Grenze 25 Einträge**, 4 MB je Eintrag, Löschung beim Neustart außer
  Angepinntes: [Microsoft Support](https://support.microsoft.com/en-us/windows/clipboard-in-windows-c436501e-985d-1c8d-97ea-fe46ddf338c6).
  Kein Registry-Schalter, Microsoft nennt selbst keinen Weg zur Erhöhung.
- **Fehlerseite:** `https://copyq.readthedocs.io/en/latest/command-basics.html` ist ein
  geratener Pfad und liefert 404. Richtig sind
  [command-line.html](https://copyq.readthedocs.io/en/latest/command-line.html) und
  [writing-commands-and-adding-functionality.html](https://copyq.readthedocs.io/en/latest/writing-commands-and-adding-functionality.html).
- **Ditto** wurde geprüft und verworfen: nur Startparameter statt CLI, damit für eine
  Session nicht bedienbar. Dazu gemeldete Aussetzer der Ausschlussliste bei Store-Apps
  und Browser-Erweiterungen.
