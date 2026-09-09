---
title: Mehrere Claude-Abos, die Belege
description: "Die Messungen hinter der Seite Mehrere Claude-Abos, eines je Projekt: warum die verbreiteten Terminal-Loesungen ausscheiden, warum der Schluesselbund-Einwand veraltet ist, und warum ein Token je Projekt nicht traegt"
---

# Mehrere Claude-Abos, die Belege

**Wozu diese Seite:** Sie traegt die Messungen zu
[Mehrere Claude-Abos, eines je Projekt](mehrere-abos-pro-projekt.md). Dort steht der
Ablauf, hier steht, warum er so aussieht. **Kein Satz ist gekuerzt**, die Trennung ist
allein die Groessenregel.

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
