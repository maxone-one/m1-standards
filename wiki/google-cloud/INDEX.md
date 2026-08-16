# Google Cloud: welcher Zugang hängt an welchem Projekt

Die eine Seite, die beantwortet: **Wenn ein Google-Zugang ausfällt, welches Cloud-Projekt
ist schuld, und ist der Ausfall breiter als er aussieht?**

Angelegt am 16.08.2026, weil dieselbe Frage innerhalb von vier Wochen dreimal von vorn
recherchiert wurde (21.07. von maxone.one, 16.08. von vera, 16.08. von werkstatt). Die
Antwort lag jedes Mal in einem fremden Repo, das niemand zu dieser Frage öffnet.

## Die Landkarte

Ein Google-Cloud-Projekt trägt den OAuth-Client. Stirbt das Projekt, stirbt der Client, und
mit ihm **jeder** Token-Refresh, der darüber läuft. Wer wissen will, was ein Ausfall
mitreißt, liest diese Spalte.

| Zugang | Cloud-Projekt | Wo die Zugangsdaten liegen | Stand 16.08.2026 |
|---|---|---|---|
| **gdrive-MCP** (Drive **und Kalender**) | `maxone-claude-drive` (Nr. 1049589896635) | `~/.secrets/google-oauth-client.json` | läuft `[B: listCalendars gab 10 Kalender]` |
| **gmail-MCP** und der Postfach-Digest auf maxone-prod | `snapflow-487500` (Nr. 1094971923698) | `~/.gmail-mcp/credentials.json`, auf prod `/opt/secrets/google-ops/token.json` | läuft `[B: gmail_get_profile, 13.043 Mails]` |
| **google-tasks-MCP** | Token ohne Projektangabe, `~/.secrets/google-tasks-token.json` | ebenda | läuft `[B: list_tasklists gab 13 Listen]` |
| **gdrive-sa** (Dienstkonto) | `vybora-488006` | `~/.secrets/google-service-account.json` | vorhanden, Projekt schläft |
| **Terminbuchung auf maxone.one** | `maxone-kalender` | `/opt/maxone-v2/.env`, `/opt/secrets/maxone/keys.env` | seit 21.07.2026 `[B: maxone.one BUGS.md F-43]` |
| **Vera (Kalender)** | `maxone-vera` | `/opt/secrets/maxone-vera/keys.env` | seit 16.08.2026 `[B: vera/docs/google-zugang.md]` |

**Kein einziger produktiver Zugang hängt an einem gesperrten Projekt** `[B: alle vier
lokalen MCP am 16.08.2026 live aufgerufen, alle antworten]`.

## Was gesperrt ist, und warum es niemanden mehr trifft

**Gesperrt sind drei Projekte:** `maxone-calendar`, `Antigravity`
(`gen-lang-client-0467187016`, aus Google AI Studio entstanden) und `Stadt Lahn Fluss`
(`my-project-1470437330941`).

**Der Grund ist Zahlung, nicht Richtlinie.** Sie hängen alle drei am Rechnungskonto
`01B2C1-F1C055-940E3D` („maxone.one"), und das ist geschlossen und gesperrt: 71,51 EUR
offen, Visa endend 1619 dreimal abgelehnt (31.05., 30.06., 21.07.2026) `[B:
erfolgsfahrplan/.planning/GLAEUBIGER-SSoT.csv Nr. 34, Cloud Console 16.08.2026]`. Die
Konsole blendet daneben ein Banner „Mehrere Ihrer Projekte verstoßen möglicherweise gegen
unsere Richtlinie zur zulässigen Verwendung" ein. **Das führt in die Irre**, die Sperrseite
des Projekts nennt ausdrücklich das Rechnungskonto.

**An diesem Rechnungskonto hängen genau diese drei Projekte, sonst nichts** `[B:
/billing/01B2C1-F1C055-940E3D/manage, 16.08.2026]`.

**Und es gibt kein aktives Rechnungskonto mehr** `[B: /billing mit Filter „Status: Aktiv"
zeigt keine Zeile, 16.08.2026]`. Alle tragenden Projekte laufen ohne eines, im kostenlosen
Kontingent. Damit ist dieser Ausfallweg strukturell zu: Ein Zahlungsproblem kann sie nicht
sperren, weil kein Zahlungsweg an ihnen hängt.

**Die Sperre wurde am 21.07.2026 umgangen, nicht behoben.** Statt das Rechnungskonto zu
klären, entstand `maxone-kalender` als Ersatz ohne Rechnungskonto. Die 71,51 EUR stehen
weiter als Gläubiger Nr. 34.

## Die drei Fallen, alle drei schon eingetreten

**1. Veröffentlichungsstatus „Test" ist eine Wochenfrist, keine Einstellung.** Google
verwirft in diesem Status jeden Refresh-Token nach sieben Tagen, unabhängig von der
Nutzung. Der Zugang stirbt planmäßig und lautlos. **Vor dem ersten Verbinden prüfen, ob das
Projekt in Produktion steht.** Traf `snapflow-487500` am 21.07.2026 `[B: maxone.one BUGS.md
F-47]`.

Der Warnbildschirm „Google hat diese App nicht überprüft" bleibt auch in Produktion stehen,
solange keine Verifizierung beantragt ist. Das ist ein anderes Thema und stört nicht.

**2. Ein Rechnungskonto an einem Projekt ist eine Sperrgefahr.** Calendar API, Drive API,
Gmail API und OAuth sind kostenlos. Wer trotzdem ein Rechnungskonto verknüpft, holt sich
dessen Zahlungsprobleme ins Projekt. **Neue Projekte grundsätzlich ohne anlegen.**

**3. Ein gesperrtes Projekt meldet sich nicht, es antwortet nur irgendwann nicht mehr.**
Der Ausfall der Terminbuchung fiel erst auf, als eine echte Kundin einen belegten Termin
buchte. Das Fehlerbild im Log ist `401 disabled_client`, „The OAuth client was disabled."

## Wie man einen Ausfall in zwei Minuten einordnet

1. **Den Zugang direkt aufrufen** (MCP-Werkzeug, `curl` mit dem Token). Das ist die härteste
   Quelle, sie schlägt jede Konsolenanzeige.
2. **Projekt aus der Client-ID lesen**, die Zahl vor dem ersten Bindestrich ist die
   Projektnummer: `python -c "import json;d=json.load(open(PFAD));print((d.get('installed') or d).get('project_id'))"`.
3. **In der Tabelle oben nachsehen, wer sonst an diesem Projekt hängt.** Ein Ausfall ist
   fast nie auf einen Dienst beschränkt.
4. **`disabled_client` heißt Projekt tot**, `insufficientPermissions` heißt fehlender
   Scope, `token revoked` heißt Test-Status oder entzogene Zustimmung. Drei verschiedene
   Ursachen, drei verschiedene Reparaturen.

## Offen

- **`maxone-vera` existiert zweimal:** `maxone-vera` in der Organisation `karastoni-org`
  und `maxone-vera-505718` ohne Organisation, letzterer nie benutzt `[B:
  cloud-resource-manager, 16.08.2026]`. Vermutlich ein Fehlversuch beim Anlegen. Gehört
  `vera`, gemeldet am 16.08.2026.
- **Die 71,51 EUR** liegen als Gläubiger Nr. 34 bei `erfolgsfahrplan`. Solange sie offen
  sind, bleiben die drei Projekte gesperrt und kein neues Projekt darf ein Rechnungskonto
  bekommen.

Verwandt: `maxone.one/BUGS.md` F-43 und F-47 (die beiden Ausfälle im Detail),
`vera/docs/google-zugang.md` (Einrichtung eines neuen Zugangs, Schritt für Schritt).
