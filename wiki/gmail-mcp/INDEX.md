---
title: gmail-mcp
description: Bibel für den Gmail-Zugang über MCP. Zwei Pakete mit fast gleichem Namen, getrennte Token-Ordner, ein Anmeldebefehl, den es so nicht gibt
---

# gmail-mcp

Stand 14.09.2026, angelegt von der werkstatt-Session auf Bitte des tagesplaners, nachdem
der Kanal `gmail_karastoni` im Morgenlauf ausgefallen war.

## Anmelden, wenn der Kanal „Not authenticated“ meldet

**Das tut Max selbst**, weil sich dabei sein Browser öffnet und er das Google-Konto
wählt. Ich lege den Befehl hin, starte ihn aber nie.

Im Terminal ausführen, dann im Browser **karastoni@googlemail.com** wählen und alle
Gmail-Rechte bestätigen:

```bash
GMAIL_MCP_CONFIG_DIR=/home/max/.gmail-mcp-karastoni /home/max/.local/share/mise/installs/node/22.14.0/bin/node /home/max/.local/share/mise/installs/node/22.14.0/lib/node_modules/@dev-hitesh-gupta/gmail-mcp-server/dist/auth-cli.js
```

Fertig ist es bei der Zeile „Authentication successful! Token saved.“ Danach liegt
`/home/max/.gmail-mcp-karastoni/token.json`.

**Danach jede laufende Session neu verbinden** (`/mcp` oder Session neu starten). Eine
Session, die vor dem 14.09.2026, 12:21 gestartet ist, hat noch den alten Serverprozess mit
dem alten Ordner `~/.gmail-mcp` offen und bleibt sonst abgemeldet. `[A:]` Eine Session, die
schon mit dem neuen Ordner läuft, braucht keinen Neustart: Solange der Server noch nie
angemeldet war, liest er den Token bei jedem Werkzeugaufruf neu (`dist/index.js`,
`ensureClient`, `[B:]` am Code).

Prüfen, ob es wirkt: in einer Claude-Session `mcp__gmail__gmail_get_profile` aufrufen.

## Welcher Server was ist

| MCP-Name | Wo eingetragen | Programm | Token-Ordner |
|---|---|---|---|
| `gmail` | `~/.claude.json`, global, dazu `werkstatt/.mcp.json` und `~/.claude/manifests/mcp-servers.json` | `gmail-mcp-server`, das global installierte `@dev-hitesh-gupta/gmail-mcp-server` 1.0.0 | `~/.gmail-mcp-karastoni` über `GMAIL_MCP_CONFIG_DIR` |
| `gmail-archiv` | `~/.claude.json`, global, **nicht im Manifest** | dasselbe Programm | `~/.gmail-mcp-insolvenz` über `GMAIL_MCP_CONFIG_DIR` |
| `gmail` in Codex | `~/.codex/config.toml` | `npx -y gmail-mcp-server` mit node 24.19.0 vorn im PATH, dort liegt nichts global, also holt npx das **andere** Paket `gmail-mcp-server` 1.0.30 | `~/.gmail-mcp` |

**Getrennt seit dem 14.09.2026, Max-Entscheid.** Bis dahin lasen Claudes `gmail` und
Codex denselben Ordner `~/.gmail-mcp`, und ein Abmelden in Codex nahm Claude den Kanal mit.
Codex braucht dafür jetzt seine eigene Anmeldung.

`[B:]` Welches Programm hinter Claudes `gmail` läuft, belegt dessen Fehlermeldung im
MCP-Log: Der Wortlaut „Please run 'npm run auth' in …“ steht nur in
`@dev-hitesh-gupta/gmail-mcp-server/dist/index.js:337`.

## Bekannte Fehlerbilder

**„Not authenticated. Please run 'npm run auth' in /home/max/Projekte/<projekt>“.** Der
Pfad in der Meldung ist nur das Arbeitsverzeichnis der Session (`process.cwd()`), dort
gibt es nichts auszuführen. `npm run auth` funktioniert nur im Quell-Repo des Pakets.
Gemeint ist der Anmeldebefehl oben. `[B:]` am Paketcode.

**`gmail-mcp-server auth` aus der README tut nichts Hilfreiches.** In Version 1.0.0 zeigt
das Programm nur auf `dist/index.js`, und dort wertet nichts das Wort `auth` aus. Der
Aufruf startet den MCP-Server und wartet stumm auf Eingaben. `[B:]` `package.json` (`bin`
und `scripts.auth`) und `dist/index.js` gelesen, nicht ausgeführt.

**Der Token verschwindet, ohne dass eine Claude-Session etwas getan hat.** Das Paket 1.0.30,
das Codex startet, hat ein Werkzeug `gmail_logout`. Es löscht `token.json` in seinem Ordner
(`dist/utils/gmail-auth.js`, `resetAuth`). `[A:]` So ist es am 10.09.2026 um 19:37 passiert,
als beide noch `~/.gmail-mcp` teilten: Eine Übergabe im Pool von `tagesplaner-0000`, einem
Absender ohne Claude-Sitzung, meldet „Gmail meldet erfolgreiche Abmeldung und gelöschte
Authentifizierung“. Der Ordner wurde zur selben Minute zuletzt geändert, und in den
Claude-Transkripten vom 10.09. steht kein Abmeldeaufruf. Seit der Trennung trifft das nur
noch Codex selbst.

**`npx -y gmail-mcp-server` startet je nach node-Version ein anderes Paket.** Liegt im PATH
eine node-Version vorn, unter der das Programm nicht global installiert ist, lädt npx still
das gleichnamige Paket 1.0.30 mit anderen Werkzeugen. Deshalb ruft Claudes Eintrag das
Programm seit dem 14.09.2026 direkt auf, ohne npx.

**„Executable not found in $PATH: cmd“.** Ein Projekt trägt noch einen Windows-Aufruf
`cmd /c gmail-mcp-server` in seiner `.mcp.json`. So in `werkstatt/.mcp.json` vom 21.07. bis
14.09.2026, dort behoben.

## Grenzen

- **Die Anmeldung klickt nur Max.** Der Befehl öffnet seinen Browser, und das ist sein Raum.
- **Kein Abmelden „zum Aufräumen“.** Ein Abmelden löscht den Token, und die nächste
  Anmeldung kostet Max einen Klick.
- **`credentials.json` und `token.json` werden nie ausgegeben**, auch nicht teilweise. Wer
  den Aufbau prüfen muss, liest nur die Schlüsselnamen.

## Nachweise

- 14.09.2026, `[B:]` Paketcode gelesen: `auth.js` (Ordner, Token, Rücksprung auf
  `127.0.0.1:3000`), `auth-cli.js`, `index.js`, `package.json`, dazu 1.0.30
  `dist/utils/gmail-auth.js`.
- 14.09.2026, `[B:]` MCP-Log `~/.cache/claude-cli-nodejs/-home-max-Projekte-tagesplaner/mcp-logs-gmail/`,
  Fehler von 08:28 und 09:03 UTC.
- 14.09.2026, `[B:]` `~/.gmail-mcp` enthielt nur `credentials.json` vom 24.08., Ordner zuletzt
  geändert 10.09. 19:37. Die Clientdatei ist vom Typ `installed` mit Rücksprung
  `http://localhost:3000/oauth2callback`, Port 3000 war frei.
- 14.09.2026, 12:21, `[B:]` Trennung: `~/.gmail-mcp-karastoni` angelegt (Rechte 700), Clientdatei
  byte-gleich kopiert, `gmail` über `claude mcp remove` und `claude mcp add` neu gesetzt,
  `claude mcp get gmail` meldet verbunden mit der neuen Umgebungsvariable.
- `[?]` Die Anmeldung selbst ist noch nicht gelaufen. Ob Google den Client ohne Weiteres
  annimmt (Testmodus, Testnutzer), zeigt erst Max' Klick.
