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
Max' eigene, Werkzeuge werden lokal nachinstalliert. Das schliesst den Verzicht auf
claude.ai-Connectors im Kundenabo ein und macht damit den einfachen Weg unten erst gangbar.

---

## 1. Der Weg, der traegt: ein Token je Projekt

In der Anmelde-Rangfolge steht `CLAUDE_CODE_OAUTH_TOKEN` auf **Platz 5**, der per
`/login` hinterlegte Abo-Zugang auf **Platz 7** [B: [Authentication](https://code.claude.com/docs/en/authentication),
Abschnitt „Authentication precedence"]. Ein Token schlaegt also den global angemeldeten
Account, **ohne ihn anzufassen**.

Der `env`-Block gilt laut Settings-Referenz auf **„Any file"**, also auch projektlokal
[B: [settings-reference](https://code.claude.com/docs/en/settings-reference), Eintrag `env`].
Damit reicht im Kundenprojekt eine Datei:

```json
// kundenprojekt/.claude/settings.local.json
{
  "env": {
    "CLAUDE_CODE_OAUTH_TOKEN": "<Token aus dem Abo des Kunden>"
  }
}
```

Die eigenen Projekte bleiben unberuehrt, weil dort schlicht kein Token gesetzt ist. **Ein
Wechsel kann nicht global durchschlagen**, weil die Datei nur in ihrem Ordner wirkt.

Die Rangfolge der Settings-Dateien, von stark nach schwach
[B: [settings](https://code.claude.com/docs/en/settings), „Settings precedence"]:

| Rang | Datei | Gilt fuer |
|---|---|---|
| 3 | `.claude/settings.local.json` | „You, in this one project only" |
| 4 | `.claude/settings.json` | alle im Projekt, gehoert ins Repo |
| 5 | `~/.claude/settings.json` | du, in jedem Projekt |

**Zwei Eigenschaften kommen dem Fall entgegen.** `settings.local.json` traegt Claude Code
beim ersten Schreiben selbst in die globalen Git-Excludes ein, das Token landet also nicht
im Repo. Und weil das Konfigverzeichnis dasselbe bleibt, steht im Kundenprojekt das
**volle eigene Werkzeug**: Skills, Commands, Agents, MCP-Server, Einstellungen. Nichts zu
symlinken, nichts zu duplizieren.

### Das Kundentoken holen, ohne den eigenen Zugang anzuruehren

```bash
CLAUDE_CONFIG_DIR=/tmp/kunde-a claude setup-token   # Browser-Login als Kunde
# Token erscheint im Terminal -> in settings.local.json eintragen
rm -rf /tmp/kunde-a
```

Der eigene Login liegt in einem anderen Verzeichnis und bleibt unberuehrt. Das Token gilt
**ein Jahr** [B: Authentication, „Generate a long-lived token"].

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

## 4. Ausbaustufe: VS-Code-Profile, wenn auch die Verlaeufe getrennt gehoeren

Der Weg aus Abschnitt 1 laesst die Sitzungsverlaeufe **gemeinsam** in
`~/.claude/projects/`. Fuer Max ist das richtig, es ist seine Arbeitsumgebung. Verlangt ein
Kunde je vertraglich, dass auch Transkripte getrennt liegen, fuehrt der Weg ueber getrennte
Konfigverzeichnisse plus VS-Code-Profile.

**Die Falle dabei:** `claudeCode.environmentVariables` hat `scope: machine`
[B: `package.json` der Extension 2.1.261]. VS Code filtert machine-scoped Einstellungen aus
Workspace-Settings heraus — **`.vscode/settings.json` im Projektordner wird ignoriert**.
Pro Projekt geht es so also nicht, pro Profil schon.

**Profile sind ordnergebunden, und ein Profil traegt beliebig viele Ordner**
[B: [VS Code: Profiles](https://code.visualstudio.com/docs/configure/profiles)]:
*„When you create or select a profile, it is associated with the current folder or
workspace. Whenever you open that folder, the workspace's profile becomes active."* Die
Zuordnungen stehen im Profiles-Editor unter **Folders & Workspaces**, zuruecksetzen laesst
sie `Developer: Reset Workspace Profiles Associations`.

**Profile bilden damit Abos ab, nicht Projekte:**

| Profil | `CLAUDE_CONFIG_DIR` | Ordner |
|---|---|---|
| Eigen (Default) | `~/.claude` | alle eigenen Projekte |
| Kunde A | `~/.claude-kunde-a` | nur dessen Ordner |
| Kunde B | `~/.claude-kunde-b` | nur dessen Ordner |

Bei zwei Kunden sind es **drei Profile, nicht fuenf**. Je Profil in den
Benutzereinstellungen:

```json
"claudeCode.environmentVariables": [
  { "name": "CLAUDE_CONFIG_DIR", "value": "/home/max/.claude-kunde-a" }
]
```

Das geteilte Gehirn holt man sich dann per Symlink dazu — `skills`, `commands`, `agents` —
und verlinkt **nicht** `projects/`, `memory/`, `.credentials.json`, `.claude.json`.

---

## 5. Was offen ist

**Zwei Annahmen sind noch nicht gemessen.** Beide betreffen den Fall, in dem eine
Verwechslung fremde Abrechnung bedeutet, also nicht kleinreden:

1. **Ob Credential-Variablen aus Projekt-Settings ueberhaupt angewandt werden.** Das Bundle
   fuehrt eine eigene Menge sensibler Variablen, die `ANTHROPIC_API_KEY`,
   `ANTHROPIC_AUTH_TOKEN` und `CLAUDE_CODE_OAUTH_TOKEN` zusammenfasst; ihre Durchsetzung
   liegt im CLI-Binary, nicht in `extension.js`. Fuer `sandbox.*` ist belegt, dass
   Projekt-Settings **ignoriert** werden (*„Only honored from user, managed/policy, or CLI
   settings — project settings are ignored"*). Ob dieselbe Sperre fuer Credential-Variablen
   im `env`-Block gilt, ist **nicht geklaert**. Die Settings-Doku formuliert vorsichtig,
   *„most `env` values"* wuerden nach Ordner-Freigabe wirken.
2. **Ob machine-scoped Einstellungen wirklich je Profil gespeichert werden.** Die VS-Code-Doku
   sagt es nur indirekt, ueber die Bemerkung, dass sie beim Profil-Export ausgelassen werden.

**Beides ist in wenigen Minuten empirisch zu klaeren** und sollte vor dem ersten
Kundeneinsatz geklaert sein, nicht danach.

## 6. Die Kontrolle im Betrieb

`/status` zeigt, welche Anmeldung eine Sitzung tatsaechlich benutzt: Bei aktivem Token
erscheint die `Login`-Zeile des eigenen Abos dort nicht. Das ist der Ein-Blick-Nachweis,
dass im Kundenfenster wirklich das Kundenabo zieht.

**Dazu die Farbe.** Jedes Projekt traegt ohnehin eine Peacock-Farbe; Kundenprojekte
bekommen eine unverwechselbare. Ein Mechanismus, der stimmt, plus ein Blick, der es
bestaetigt — Belege statt Vertrauen, wie ueberall sonst auch.

## Was am Kundenabo fehlt

`CLAUDE_CODE_OAUTH_TOKEN` *„can only make model requests"* [B: Authentication]: **keine
claude.ai-Connectors, kein Remote Control**. Lokale MCP-Server ueber `.mcp.json` laufen
normal. Fuer den hier beschriebenen Fall ist das folgenlos, weil das Kundenkonto neu
gekauft ist und dort ohnehin keine Verbindungen bestehen.

---

**Siehe auch:** [vscode/INDEX.md](../vscode/INDEX.md) fuer Fenster und Profile als
Editor-Thema. Die Naht-Regel weist diesen Text hierher: Es ist ein Claude-Problem, das
zufaellig in VS Code auftritt.
