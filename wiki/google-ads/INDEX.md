# Google Ads: Lesezugang für Claude

Die eine Seite, die beantwortet: **Wie sieht ein KI-Team-Mitglied die echten Zahlen eines
Google-Ads-Kontos, ohne dass jemand etwas ausversehen umstellt?**

Angelegt am 22.08.2026, weil das eigene Konto von maxone.one ausgewertet werden soll und
der Engpass nicht das Fachwissen ist, sondern der Zugang.

## Die Kurzfassung

Google veröffentlicht seit dem 28.04.2026 einen **eigenen MCP-Server** für die Google Ads
API: [googleads/google-ads-mcp](https://github.com/googleads/google-ads-mcp), Apache-2.0
`[B: Repo am 22.08.2026 geklont und gestartet, Commit ba47210, FastMCP 3.4.7]`.

Er ist **rein lesend**. Drei Werkzeuge, mehr gibt es nicht:

| Werkzeug | Was es tut |
|---|---|
| `list_accessible_customers` | Nennt die Kundennummern, auf die der Zugang reicht |
| `search` | Führt eine GAQL-Abfrage gegen das Konto aus, das ist der Arbeitspferd-Befehl |
| `get_resource_metadata` | Beschreibt Felder und Ressourcen, damit die Abfrage stimmt |

**Kein Werkzeug pausiert eine Kampagne, ändert ein Gebot oder rührt ein Budget an.** Das
ist der Grund für die Wahl: Änderungen an einem Werbekonto kosten Geld und wirken nach
außen. Hier erzwingt die Technik, was sonst nur eine Regel wäre.

Die gehosteten Alternativen (Pipeboard, Composio, gomarble, die Angebote auf mcpmarket)
sind bewusst verworfen: Sie leiten den Kontozugang über fremde Server und fremde
Developer-Token, mehrere kosten monatlich `[A: aus den Anbieterseiten, Stand 22.08.2026]`.

## Die Konten, Stand 22.08.2026

Abgelesen aus der Kontoauswahl in `ads.google.com` über das Playwright-Hauptprofil, Anmeldung
`karastoni@gmail.com` `[B: /nav/selectaccount, 22.08.2026, 01:37 Uhr]`. **Sechs Konten, davon
vier tot.**

| Kundennummer | Name | Stand laut Oberfläche |
|---|---|---|
| **302-397-5199** | **maxone.work** | Das einzige lebende Werbekonto. **Liefert seit 21.08.2026, 09:49 Uhr keine Anzeigen mehr**, Zahlung mit Visa 1619 abgelehnt `[B: Gmail 1a0253a57912b64f, 1a0244e8ce301106]` |
| **236-262-6976** | (ohne Namen) | **Verwaltungskonto, „Wird eingerichtet"**. Existiert, ist aber nicht fertig registriert |
| **422-387-9203** | MARKETING KERL | Aufgelöst am 20.08.2026, **300,55 EUR offen**, Zahlungsprofil 9144-5911-8784 `[B: Gmail 1a01f1eb473e0c65]` |
| **576-613-1215** | GRPTLK | Aufgelöst |
| **392-320-7913** | „keine Ahnung" | Geschlossen |
| **342-145-0047** | sonnenreich GmbH & Co. KG | Aufgelöst am 09.03.2025 `[B: Gmail 1957d9580ebbc5dd]` |

**Das Postfach taugt für diese Frage nicht.** Eine Erhebung aus Mails hatte zuvor GRPTLK als
„ruht" geführt (Google schickt Reaktivierungswerbung auch an aufgelöste Konten) und das
Verwaltungskonto ganz übersehen, weil ein Verwaltungskonto keine Anzeigen schaltet, keine
Rechnung hat und daher **so gut wie keine Mail erzeugt**. Der ganze Fall:
`maxone-pilots/irrtuemer/irrtum-020.md`.

**Fremdzugriff ist weg.** 2022 waren „CleverAds APP" (über `google@cleverads.com`) und „Plai"
als fremde Verwaltungskonten verknüpft `[B: Gmail 17f28a52bd9267f7, 17f0d8d0df46b6eb]`. Die
Verwalter-Tabelle von maxone.work ist heute **leer**
`[B: /aw/accountaccess/managers?ocid=8486141702, 22.08.2026]`. Bei den vier toten Konten ist es
gegenstandslos.

**Die Ursache ist eine einzige Karte.** Visa endend 1619 wurde dreimal für Cloud abgelehnt
und am 21.08.2026 auch für Ads. Es sind nicht mehrere Vorgänge, es ist einer. Siehe
[google-cloud/INDEX.md](../google-cloud/INDEX.md).

## Der Weg, und wer welchen Teil macht

Die Reihenfolge ist nicht beliebig. Schritt 1 kann eine Wartezeit auslösen, deshalb steht
er vorn.

### 1. Das vorhandene Verwaltungskonto fertig einrichten (Max)

**Nicht anlegen, es existiert schon:** `236-262-6976`, Status „Wird eingerichtet".

Ein einzelnes Werbekonto kommt **gar nicht erst ins API-Center**, auch nicht als
Administrator. Der Developer-Token wird auf Ebene eines Verwaltungskontos (MCC) ausgestellt
`[B: developers.google.com/google-ads/api/docs/api-policy/developer-token]`. Deshalb führt der
Weg zwingend über dieses Konto.

Die Einrichtung liegt hinter der Kontoauswahl: In `ads.google.com` das Konto `236-262-6976`
wählen, Google leitet dann auf `/aw/signup/manager`. Dort fehlen Name, Zeitzone und Währung.
Danach `maxone.work` (302-397-5199) darunter verknüpfen. Die vier toten Konten mitzunehmen
lohnt sich nur, wenn ihre alten Zahlen noch gebraucht werden.

**Die Seite braucht Zeit, und sie sieht in der Zwischenzeit aus wie kaputt.** `/aw/signup/manager`
liefert zunächst eine leere `main` und legt den Dialog „Turn off ad blockers" darüber. Nach
etwa fünf Sekunden ist das Formular da. **Der Werbeblocker-Hinweis ist irreführend:** Google
zeigt ihn in der automatisierten Umgebung auch dann, wenn gar kein Werbeblocker installiert
ist. Im Playwright-Hauptprofil liegen nur ScreenTool.io, Zoho PageSense, Zoho Books Timer und
iCloud-Lesezeichen `[B: Secure Preferences, 22.08.2026]`. Wer beim ersten Blick abbricht, hält
eine Ladezeit für eine Blockade.

Das Formular verlangt Anzeigename und primäre Verwendung, dazu Land, Zeitzone und Währung.
Google schreibt darüber: „Sie können diese Einstellungen später nicht mehr ändern." Am Ende
sitzt ein **reCAPTCHA**, und das ist die Stelle, an der Automatisierung endet. Der Rest lässt
sich vorbereiten, das Häkchen und das Absenden gehören Max.

Gewählt am 22.08.2026: Anzeigename `maxone.one`, Verwendung „Konten von anderen Nutzern
verwalten" (die breitere Wahl, weil Google Ads auch als Leistung für Kunden angeboten wird),
Deutschland, GMT+02:00, Euro.

**Dieses Formular wird nicht vorbereitet und übergeben.** Der ausgefüllte Zustand lebt nur im
Playwright-Fenster, und das überlebt die Sitzung nicht. Ein Übergabetab im Dauerprofil hilft
hier ebenfalls nicht, weil dort keine Google-Anmeldung liegt. Max füllt es in seinem eigenen
Browser aus, mit den fünf Angaben von oben. Der Fall:
`maxone-pilots/irrtuemer/irrtum-021.md`.

### 2. Developer-Token holen (Max, etwa fünf Minuten)

Im Manager-Konto unter **Werkzeuge und Einstellungen → Einrichtung → API-Center**.

Ein frischer Token startet auf **Test Account Access** und sieht damit nur Testkonten.
Gebraucht wird mindestens **Explorer Access**: 2.880 Abfragen pro Tag gegen echte Konten.
Diese Stufe gibt es erst seit Februar 2026 und Google stuft Token oft **automatisch**
hoch, ohne Antrag und ohne Wartezeit
`[B: developers.google.com/google-ads/api/docs/api-policy/access-levels]`.

Für ein einzelnes Konto reicht Explorer mit Abstand. Blockiert bleiben dort nur die
Planungsdienste (Keyword-Planer über API), Kontoverwaltung und Abrechnung. Wer die
braucht, beantragt Basic Access im selben API-Center, das hat derzeit Rückstau
`[B: ppc.land, „Google faces developer token application backlog"]`.

Der Token ist 22 Zeichen lang und gehört in den Secret-Store, nicht in eine Notiz.

### 3. Cloud-Projekt anlegen (Max, etwa fünf Minuten)

**Ein neues Projekt, kein bestehendes.** Die Versuchung, `maxone-claude-drive`
mitzubenutzen, ist falsch: Der Ads-Scope müsste dort nachträglich zugestimmt werden, und
das autorisiert Drive und Kalender mit neu. Ein laufender Zugang wird nicht für eine
Bequemlichkeit angefasst.

Drei Dinge, und die Reihenfolge zählt:

1. Projekt anlegen, Vorschlag `maxone-google-ads`, **ohne Rechnungskonto**. Warum:
   [google-cloud/INDEX.md](../google-cloud/INDEX.md), Falle 2. Die Ads API ist im
   Leseumfang kostenlos.
2. **Google Ads API aktivieren** unter APIs und Dienste.
3. OAuth-Zustimmungsbildschirm einrichten und den **Veröffentlichungsstatus auf
   „In Produktion" setzen**. Das ist die wichtigste Einstellung der ganzen Seite: Im
   Status „Test" verwirft Google jeden Refresh-Token nach sieben Tagen, lautlos und
   unabhängig von der Nutzung. Siehe [google-cloud/INDEX.md](../google-cloud/INDEX.md),
   Falle 1.
4. OAuth-Client vom Typ **Desktop** erstellen, JSON herunterladen, nach
   `~/.secrets/google-ads-client.json` legen.

Der Warnbildschirm „Google hat diese App nicht überprüft" bleibt stehen, solange keine
Verifizierung beantragt ist. Das stört nicht und ist ein anderes Thema.

### 4. Zustimmung einholen (ein Befehl, Max klickt einmal)

```
python ~/.claude/bin/google-ads-oauth.py --client-json ~/.secrets/google-ads-client.json
```

Das Skript öffnet die Zustimmungsseite, nimmt die Rückleitung auf `127.0.0.1:8765`
entgegen, tauscht den Code gegen einen Refresh-Token und legt das Ergebnis als
`~/.secrets/google-ads-adc.json` ab. **Kein Wert erscheint dabei auf dem Bildschirm.**

Es trägt `access_type=offline` und `prompt=consent`. Ohne das erste gibt es überhaupt
keinen Refresh-Token, ohne das zweite nur bei der allerersten Zustimmung. Ein zweiter Lauf
liefe sonst lautlos leer.

**Warum kein `gcloud auth application-default login`:** Das Cloud SDK ist auf dem Rechner
nicht installiert `[B: Get-Command gcloud leer, 22.08.2026]`, und es für einen einmaligen
Zustimmungsdurchlauf zu installieren wäre ein Fremdpaket für nichts. Die geschriebene
Datei trägt exakt dasselbe Format (`type: authorized_user`).

### 5. Server eintragen (Claude)

pipx ist installiert, aber `pipx.exe` liegt nicht im PATH `[B: 22.08.2026]`. Deshalb wird
der Server über `python -m pipx` gestartet:

```json
{
  "mcpServers": {
    "google-ads": {
      "command": "C:\\Users\\max\\AppData\\Local\\Microsoft\\WindowsApps\\python.exe",
      "args": ["-m", "pipx", "run", "--spec",
               "git+https://github.com/googleads/google-ads-mcp.git", "google-ads-mcp"],
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "C:\\Users\\max\\.secrets\\google-ads-adc.json",
        "GOOGLE_PROJECT_ID": "maxone-google-ads",
        "GOOGLE_ADS_DEVELOPER_TOKEN": "...",
        "GOOGLE_ADS_LOGIN_CUSTOMER_ID": "..."
      }
    }
  }
}
```

`GOOGLE_ADS_LOGIN_CUSTOMER_ID` ist die Kundennummer des **Manager-Kontos** ohne
Bindestriche. Sie fehlt in vielen Anleitungen und ist der Grund, warum der Zugriff über
ein MCC sonst mit einer Berechtigungsmeldung scheitert.

Der Eintrag gehört **nicht** in die globale Konfiguration. Google Ads braucht nicht jede
Session, sondern das Projekt, das gerade Marketing macht.

## Erste Prüfung nach dem Einrichten

Die härteste Quelle ist der Aufruf selbst, nicht die Konsolenanzeige. `list_accessible_customers`
muss die Kundennummern nennen.

Danach steht das ganze Inventar fertig bereit: [abfragen.md](abfragen.md) enthält die
sechs GAQL-Abfragen in der Reihenfolge, in der sie gefahren werden, von der Kontohierarchie
über die Fremdzugriffe bis zu den Suchbegriffen.

## Was dann ausgewertet wird

Das Strategiewissen liegt schon da und muss nicht neu recherchiert werden:
`~/.claude/marketing-skills/ads/references/google-search-playbook.md` (Intent-Leiter,
Kontostruktur, Match-Types, Negativ-Keywords, Suchbegriff-Ritual, Gebotsstrategie nach
Conversion-Volumen, PMax-Leitplanken) und `rsa-output-spec.md` für die Zeichengrenzen der
Anzeigentexte. Route dorthin: `/mkt-reichweite`.

## Offen

- `[?]` Ob der Developer-Token automatisch auf Explorer hochgestuft wird oder ein Antrag
  nötig ist, zeigt sich erst im API-Center. Beides ist vorgesehen.
- `[?]` Ob das Konto überhaupt laufende Kampagnen hat, ist ungeprüft. Ohne Zugang wäre
  jede Aussage dazu geraten.
