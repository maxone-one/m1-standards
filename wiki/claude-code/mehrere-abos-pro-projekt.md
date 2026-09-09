---
title: Mehrere Claude-Abos, eines je Projekt
description: "Wie in parallel offenen VS-Code-Fenstern gleichzeitig verschiedene Claude-Abos laufen: das Kundenabo nur im Kundenprojekt, Max' eigenes ueberall sonst, ohne Aus- und Einloggen und ohne dass ein Wechsel global durchschlaegt"
---

# Mehrere Claude-Abos, eines je Projekt

**Wozu diese Seite:** Der Anlass ist Kundenarbeit. Grundvoraussetzung bei Max ist, dass der
Kunde fuer sein Projekt ein **eigens dafuer gekauftes** Claude-Abo mitbringt, nicht sein
persoenliches. Dieses Abo darf ausschliesslich in seinem Projekt laufen, waehrend in den
drei bis vier parallel offenen eigenen Projekten weiter Max' Abo zieht. Bei zwei Kunden
sind das **drei Abos gleichzeitig**, in gleichzeitig offenen VS-Code-Fenstern.

**Die harte Anforderung:** Ein Abo-Wechsel in einem Fenster darf die anderen Fenster nicht
erreichen. Genau das ist der Normalfall, wenn man es falsch macht, denn `/logout` und
`/login` in der Extension wirken auf den einen global hinterlegten Zugang.

**Der Kunde liefert die Lizenz, sonst nichts** [B: Max, 06.09.2026]. Es geht nicht um
Zugriff auf Kundensysteme und nicht um dessen Verbindungen: Die Arbeitsumgebung bleibt
Max' eigene, Werkzeuge werden lokal nachinstalliert. Am Kundenkonto haengen keine
Verbindungen, und es sollen auch keine daran haengen.

---

## 1. Der Weg, der traegt: `CLAUDE_CONFIG_DIR` je VS-Code-Profil

**Zugangsdaten kommen ausschliesslich aus der Prozessumgebung, nie aus einer Settings-Datei
des Projekts.** Das ist am 06.09.2026 gemessen worden, siehe Abschnitt 2. Daraus folgt der
einzige Weg, der im VS-Code-Panel funktioniert:

`claudeCode.environmentVariables` setzt echte Umgebungsvariablen des Claude-Prozesses
[B: `extension.js` 2.1.261]. Die Einstellung traegt `scope: machine`
[B: `package.json` der Extension], laesst sich also **nicht** in `.vscode/settings.json`
eines Projekts setzen, wohl aber je **VS-Code-Profil**.

**Profile sind ordnergebunden, und ein Profil traegt beliebig viele Ordner**
[B: [VS Code: Profiles](https://code.visualstudio.com/docs/configure/profiles)]:
*„When you create or select a profile, it is associated with the current folder or
workspace. Whenever you open that folder, the workspace's profile becomes active."* Die
Zuordnungen stehen im Profiles-Editor unter **Folders & Workspaces**, zuruecksetzen laesst
sie `Developer: Reset Workspace Profiles Associations`.

**Profile bilden damit Abos ab, nicht Projekte.** Bei zwei Kunden sind es drei Profile,
nicht fuenf:

| Profil | `CLAUDE_CONFIG_DIR` | Ordner |
|---|---|---|
| Eigen (Default) | `~/.claude` | alle eigenen Projekte |
| Kunde A | `~/.claude-kunde-a` | nur dessen Ordner |
| Kunde B | `~/.claude-kunde-b` | nur dessen Ordner |

Je Profil in den Benutzereinstellungen:

```json
"claudeCode.environmentVariables": [
  { "name": "CLAUDE_CONFIG_DIR", "value": "/home/max/.claude-kunde-a" }
]
```

Im neuen Verzeichnis meldet man sich einmal mit dem Kundenabo an. Das geteilte Gehirn holt
man per Symlink dazu — `skills`, `commands`, `agents` — und verlinkt **nicht** `projects/`,
`memory/`, `.credentials.json`, `.claude.json`.

### Die Alternative ohne Profile: ein Wrapper, der nach Pfad entscheidet

`claudeCode.claudeProcessWrapper` ist ebenfalls machine-scoped, aber es ist **eine einzige
globale Einstellung**: ein Skript, das anhand des Arbeitsverzeichnisses das richtige
`CLAUDE_CONFIG_DIR` exportiert und dann das echte Binary aufruft. Die Extension uebergibt
den Binary-Pfad als Argument und die Umgebung mit [B: `extension.js`, Funktion `t$$`]:

```js
if (Q) return { pathToClaudeCodeExecutable: Q, executableArgs: X ? [X] : [], env: J };
```

Damit entfaellt die Profil-Vervielfaeltigung und die offene Frage aus Abschnitt 5. **Ob der
Wrapper mit dem Workspace als `cwd` startet, ist noch nicht gemessen** — der Code legt es
nahe, beweist es aber nicht.

---

## 2. Warum die verbreiteten Loesungen hier keine sind

Die Netzrecherche vom 06.09.2026 findet vier Muster. **Drei davon sind Terminal-Loesungen
und damit hier wertlos**, weil Max ausschliesslich im VS-Code-Panel arbeitet
([[max-nutzt-claude-nur-im-vs-code-panel]]):

| Muster | Was es tut | Warum es hier ausscheidet |
|---|---|---|
| Aliases + `CLAUDE_CONFIG_DIR` | zwei Konfigverzeichnisse, per Shell-Alias gewaehlt | nur Terminal |
| [aimux](https://github.com/Digital-Threads/aimux) | „ein Gehirn, zwei Geldbeutel": Skills symlinked, Auth isoliert | nur Terminal; kann dafuer Claude, Codex und Gemini nebeneinander |
| [claude-swap](https://github.com/realiti4/claude-swap) | rotiert den Schluesselbund-Eintrag selbst | wirkt auch in der Extension, aber **sequenziell** statt parallel |
| Token je Projekt | siehe oben | **traegt** |

**Zur Abo-Rotation eine Warnung:** claude-swap und aimux werben mit automatischem Wechsel
bei Rate-Limits. Zwei eigene bezahlte Abos parallel zu nutzen ist eine Sache,
Kontenrotation gezielt zum Umgehen von Limits eine andere. Vor dem Einschalten an
Anthropics Nutzungsbedingungen pruefen.

---

## 3. Was gemessen ist, gegen das, was im Netz steht

**Die verbreitete Behauptung „`CLAUDE_CONFIG_DIR` isoliert auf macOS nicht, weil die
Zugangsdaten im Schluesselbund liegen" ist veraltet.** Sie steht in mehreren Blogs und
klingt plausibel. Gemessen am Extension-Bundle 2.1.261 [B: `extension.js`, 06.09.2026]:

```js
z = Q ? "" : `-${sha256(configDir).substring(0,8)}`
return `Claude Code${OAUTH_FILE_SUFFIX}${z}`
```

**Der Schluesselbund-Eintrag wird aus einem Hash des Konfigverzeichnisses benannt.** Ist
`CLAUDE_CONFIG_DIR` nicht gesetzt, bleibt der Suffix leer und es entsteht der schlichte
Eintrag `Claude Code-credentials`; auf dem Mac Mini war am 06.09.2026 genau dieser eine
vorhanden. Ist die Variable gesetzt, entsteht ein anderer Eintrag. Die Doku sagt dasselbe:
*„keys the macOS Keychain entry to that directory too, so a session with a different
`CLAUDE_CONFIG_DIR` reads a different entry."*

Ablageort je Plattform [B: Authentication, „Credential management"]:

| Plattform | Wo der Zugang liegt |
|---|---|
| Linux (NUC) | `<CLAUDE_CONFIG_DIR>/.credentials.json`, Modus 0600 |
| macOS | Schluesselbund, Eintrag am Konfigverzeichnis gehasht; faellt auf die Datei zurueck, wenn der Bund nicht schreibbar ist |
| Windows | `%USERPROFILE%\.claude\.credentials.json` |

**Auf dem NUC ist der Fall also der einfachere**, weil dort ohne Schluesselbund gearbeitet
wird.

**Die Extension ignoriert `CLAUDE_CONFIG_DIR` nicht**, anders als es
[Issue #55621](https://github.com/anthropics/claude-code/issues/55621) nahelegt. Sie baut
die Umgebung des Claude-Prozesses so [B: `extension.js`, 06.09.2026]:

```js
let J = P1("environmentVariables"), Q = {...process.env};
for (let X of J) if (X.name) Q[X.name] = X.value || "";
Q.CLAUDE_CODE_ENTRYPOINT = "claude-vscode";
```

---

## 4. Der Weg, der NICHT traegt: ein Token je Projekt

> **KORREKTUR 06.09.2026, wenige Stunden nach dem Anlegen dieser Seite.** Hier stand als
> Hauptempfehlung, ein `CLAUDE_CODE_OAUTH_TOKEN` in die projektlokale
> `.claude/settings.local.json` zu legen. Die Herleitung war sauber und trotzdem falsch:
> Die Anmelde-Rangfolge stellt das Token ueber den `/login`-Zugang, der `env`-Schluessel
> gilt laut Settings-Referenz auf „Any file", und beides stimmt auch. **Gemessen wurde es
> erst danach, und die Messung hat es widerlegt.**

Vier Laeufe mit `claude auth status` (2.1.261, liest Settings ohne Trust-Dialog und ohne
Modellaufruf) [B: 06.09.2026, Mac Mini]:

| Woher die Variable kam | Was gemessen wurde |
|---|---|
| Projekt-Settings, harmlose `DRIFT_PROBE_A` | **wirkt** — ein Bash-Unterprozess der Sitzung gibt `projekt-env-wirkt` aus |
| Projekt-Settings, `CLAUDE_CODE_OAUTH_TOKEN` | **wirkt nicht** — `authMethod` bleibt `claude.ai`, Konto unveraendert |
| Shell-Umgebung, dasselbe Token | **wirkt** — `authMethod` springt auf `oauth_token`, Konto- und Abo-Felder verschwinden |
| Shell-Umgebung, `CLAUDE_CONFIG_DIR` | **eigener Zugang** — `loggedIn: false`, `authMethod: none` |

**Die dritte Zeile ist die Kalibrierung und macht den Befund erst belastbar.** Ohne sie
haette die zweite Zeile auch heissen koennen, dass `auth status` fuer Env-Variablen
schlicht blind ist. Sie ist es nicht.

**Der Schluss:** Der `env`-Block aus Projekt-Settings wirkt, aber **Credential-Variablen
sind gezielt herausgefiltert**. Das passt zu der Menge sensibler Variablen, die das Bundle
fuehrt (`ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, `CLAUDE_CODE_OAUTH_TOKEN` und die
Provider-Schluessel), und zu der bereits dokumentierten Sperre bei `sandbox.*`: *„Only
honored from user, managed/policy, or CLI (`--settings`) settings — project settings
(`.claude/settings.json` and `.claude/settings.local.json`) are ignored."*

**Das ist kein Fehler, sondern Absicht.** Ein Repo, das seine eigene Abrechnung setzen
duerfte, waere ein Einfallstor: Es genuegte, eine Datei mitzuliefern, und fremde Anfragen
liefen ueber ein fremdes Konto. Wer diesen Weg in Zukunft wieder vorschlaegt, misst ihn
bitte mit den vier Zeilen oben nach, statt der Rangfolgen-Logik zu glauben.

## 5. Was offen war, und wie es ausging

**Die Annahme, die die Konstruktion aus Abschnitt 1 trägt, ist gemessen, und sie hält**
[B: NUC, 09.09.2026, 10:52]. Im Profil `Fallnavigator` gesetzt, danach drei Fenster
gleichzeitig offen:

| Fenster | Claude-Prozess | Konfigverzeichnis |
|---|---|---|
| fallnavigator | PID 116666 | `/home/max/.claude-fallnavigator` |
| werkstatt | PID 39871 | keine Variable, also `~/.claude` |
| tagesplaner | PID 13620 | keine Variable, also `~/.claude` |

Abgelesen an `/proc/<pid>/environ`, also an der Prozessumgebung selbst und nicht an einer
Anzeige im Panel. **Machine-scoped Einstellungen werden je Profil gespeichert und wirken
auch nur dort.** Der Wrapper aus Abschnitt 1 wird für diesen Zweck nicht gebraucht.

## 6. Einrichtung auf dem NUC, der Reihe nach

Linux, Benutzer `max`, Projekte unter `/home/max/Projekte/`. Die Schritte 1 bis 5 gelten je
Kunde; Schritt 0 einmal.

### Schritt 0: entfällt seit dem 09.09.2026

Hier stand eine Probe, solange Abschnitt 5 offen war. Sie ist gelaufen, der Weg trägt.
**Der Stolperstein liegt woanders, und zwar in Schritt 2.**

### Schritt 1: Konfigverzeichnis fuer den Kunden, mit geteiltem Gehirn

```bash
KUNDE=kunde-a
NEU="$HOME/.claude-$KUNDE"
mkdir -p "$NEU"

# geteilt: das Werkzeug. Aenderungen wirken sofort in allen Abos.
for teil in skills commands agents rules plugins memory CLAUDE.md; do
  [ -e "$HOME/.claude/$teil" ] && ln -sfn "$HOME/.claude/$teil" "$NEU/$teil"
done

# eigenstaendig: Einstellungen als Kopie, damit sie abweichen duerfen
cp -n "$HOME/.claude/settings.json" "$NEU/settings.json" 2>/dev/null

ls -la "$NEU"
```

**Was bewusst NICHT verlinkt wird:** `projects/` (die Sitzungsverlaeufe),
`.credentials.json` (der Zugang) und `.claude.json` (traegt die MCP-Konfiguration samt
`oauthAccount`). Genau diese drei sollen je Abo eigene sein — das ist der Zweck der Uebung.

### Schritt 2: Profil anlegen und den Kundenordner daran binden

Kundenordner oeffnen, dann **Profiles → New Profile**, Namen wie das Abo.

> **KORREKTUR 09.09.2026.** Hier stand, die Bindung entstehe dabei von selbst. **Sie tut es
> nicht.** Das Profil wird angelegt, der Ordner bleibt am Default-Profil hängen, und das
> Fenster liest weiter die eigenen Einstellungen: Claude nimmt also Max' Abo, ohne dass
> irgendwo ein Fehler erscheint. Gemessen an `profileAssociations` in
> `~/.config/Code/User/globalStorage/storage.json`, wo der Workspace nach dem Anlegen
> weiterhin auf `__default__profile__` zeigte.

**Die Bindung schreibt erst der Wechsel ins Profil.** Am schnellsten von der Befehlszeile,
und der Befehl erledigt Anlegen, Binden und Neuladen in einem:

```bash
code --profile "Fallnavigator" /home/max/Projekte/fallnavigator/fallnavigator.code-workspace
```

Kontrolle im Profiles-Editor unter **Folders & Workspaces**, härter in derselben
`storage.json`: Dort muss neben dem Workspace die Profil-ID stehen, nicht
`__default__profile__`.

**Ein Profil traegt beliebig viele Ordner.** Kommt spaeter ein zweiter Ordner desselben
Kunden dazu, oeffnest du ihn und waehlst dasselbe Profil — kein neues anlegen.

### Schritt 3: das Konfigverzeichnis im Profil setzen

Im **neuen Profil**, Benutzereinstellungen (nicht Workspace, dort wirkt es nicht):

```json
"claudeCode.environmentVariables": [
  { "name": "CLAUDE_CONFIG_DIR", "value": "/home/max/.claude-kunde-a" }
]
```

Danach das Fenster neu laden (`Developer: Reload Window`), sonst laeuft der alte
Claude-Prozess weiter.

### Schritt 4: mit dem Kundenabo anmelden

Im Kundenfenster `/login`. Der Zugang landet in `~/.claude-kunde-a/.credentials.json`
(Linux, Modus 0600) und ist von deinem eigenen vollstaendig getrennt.

### Schritt 5: nachweisen, nicht annehmen

**Im Panel:** `/status` im Kundenfenster zeigt Konto und Organisation des Kunden, `/status`
in einem eigenen Projekt weiter deins. **Beide Fenster gleichzeitig offen pruefen**, denn
genau das ist die Anforderung.

**Vom Terminal aus**, falls du es hart gegenpruefen willst:

```bash
CLAUDE_CONFIG_DIR=$HOME/.claude-kunde-a claude auth status   # Kundenkonto
claude auth status                                            # dein Konto
```

Beide Ausgaben tragen `email` und `subscriptionType`. Stehen dort zwei verschiedene
Konten, ist die Trennung belegt.

### Die Peacock-Farbe nicht vergessen

Kundenprojekte bekommen eine unverwechselbare Farbe. Der Mechanismus stimmt dann, und der
Blick bestaetigt es — dieselbe Logik wie ueberall sonst.

## Was am Kundenabo anders ist

Weil im Kundenverzeichnis ein echter `/login` steht und kein Token, hat das Kundenabo den
**vollen Funktionsumfang**, einschliesslich claude.ai-Connectors und Remote Control. Nur
sind dort keine Verbindungen eingerichtet, weil das Konto eigens gekauft wurde — fuer den
hier beschriebenen Fall ist das folgenlos, die Arbeitsumgebung bleibt Max' eigene und
Werkzeuge werden lokal nachinstalliert.

**Getrennt sind ausserdem die Sitzungsverlaeufe**, weil `projects/` im jeweiligen
Konfigverzeichnis liegt. Bei Kundenarbeit ist das der richtige Zustand und kein Verlust.

---

**Siehe auch:** [vscode/INDEX.md](../vscode/INDEX.md) fuer Fenster und Profile als
Editor-Thema. Die Naht-Regel weist diesen Text hierher: Es ist ein Claude-Problem, das
zufaellig in VS Code auftritt.
