# Meta-Plattform: Bedienhandbuch (Facebook, Instagram, Business Suite)

Angelegt 10.08.2026. Gilt estate-weit, nicht nur für ein Projekt: Dieselben Konten
tragen GridDone, Voltfair, Plansey, Stadt Land Solar, snapflow, Stadt Lahn Flow und
Elektro Piechocki.

**Das Bedienbare steht oben, die Nachweise stehen unten.**

## Die Kontenlage in einem Blick

| Was | Wert | Beleg |
|---|---|---|
| Gewerbliches Facebook-Konto | `max.karastelev.business`, Kennung **100002368008924** | `/me` leitet dorthin, 10.08.2026 |
| Hinterlegte Adressen | `karastoni@googlemail.com`, `fb@karastelev.de` | Kontenzentrale, 10.08.2026 |
| Playwright-Profil dafür | `playwright` (`C:\Users\max\.playwright-mcp-profile`) | Max-Direktive 10.08.2026 |
| Privates Facebook-Konto | `max@karastelev.de`, Kennung **100021983952708** | Anmeldung 10.08.2026, 21:21 Uhr |
| Zweitfaktor privat | Authenticator-App (TOTP), kein Mail- oder SMS-Weg angeboten. **Nur Max kommt an diesen Code** | Anmeldung 10.08.2026 |
| Zweitfaktor gewerblich | seit 10.08.2026 aktiv. Bestätigungscodes gehen an `karastoni@googlemail.com`, also **ohne Max erreichbar** | Aktivierung 10.08.2026, 22:11 |
| Playwright-Profil dafür | `playwright-privat` (`.playwright-mcp-profile-2`) | Max-Direktive 10.08.2026 |
| Seiten am gewerblichen Konto | **22** | Kontenzentrale, 10.08.2026 |
| Instagram am selben Konto | `getsnapflow`, `plansey_bride`, `griddone.de`, `venfree.de` | Kontenzentrale, 10.08.2026 |

**Die beiden Konten werden nie im selben Browserprofil geöffnet.** Sonst vermischen
sich die Sitzungen und überdauern nicht. Das gewerbliche gehört ins Hauptprofil, das
private in `playwright-privat`.

## Was bei einer Erstanmeldung passiert

Ein Konto, das zum ersten Mal in einem frischen Browserprofil angemeldet wird, kommt
zwar in den Feed, aber **die Business Suite bleibt rund 15 Minuten gesperrt**:
„Dieser Vorgang ist momentan nicht möglich. Wir führen zusätzliche Überprüfungen für
dieses neue Gerät durch." Das ist eine normale Prüfung, kein Kontoproblem, und sie
läuft von selbst ab.

**Konsequenz für die Planung:** Ein neues Profil wird angemeldet, bevor es gebraucht
wird, nicht wenn es gebraucht wird. Dieselbe Bewegung wie bei jedem anderen
Langläufer.

## Zielpfade, die tragen

| Zweck | Adresse |
|---|---|
| Aktives Profil feststellen | `facebook.com/me` (leitet auf die gerade aktive Stimme, **nicht** zwingend auf das Konto) |
| Alle Profile und Seiten | Kontenzentrale `accountscenter.facebook.com/profiles` |
| Seitenliste | `facebook.com/pages/?category=your_pages` |
| Kontoprobleme und Sperren | `facebook.com/accountquality` (leitet ins Business-Support-Center) |
| Portfolio-Einstellungen | `business.facebook.com/latest/settings/pages?business_id=<PORTFOLIO_ID>` |
| Seite deaktivieren, offline nehmen, löschen | `facebook.com/deactivate_delete_account/` **in der Stimme der Seite** |

## Die Stimme entscheidet über alles

Facebook führt die „aktive Stimme" (persönliches Profil oder eine Seite)
**serverseitig**, nicht mehr im Cookie. Der frühere `i_user`-Cookie existiert nicht
mehr; `c_user` trägt immer das echte Konto.

**Konsequenz: Vor jeder Handlung die Stimme prüfen.** Dieselbe Adresse
(`/settings/`, `/deactivate_delete_account/`) meint je nach Stimme die Seite oder
**Max' persönliches Konto**. In der Konto-Stimme führt derselbe Weg zur Löschung
seines Kontos.

Erkennungsmerkmale der Seiten-Stimme: Der Seitenkopf zeigt
„Professional-Dashboard" statt „Dashboard", der Benachrichtigungszähler im
Seitentitel verschwindet, und jeder Dialogtext spricht von „dieser Facebook-Seite".

**Wechseln:** Profilbild oben rechts (`div[aria-label="Dein Profil"]`), dann der
Eintrag mit dem sprechenden Kennzeichen `[aria-label="Zu <Name> wechseln"]`. Das ist
der einzige stabile Selektor, siehe unten.

## Bedienfallen bei der Automatisierung

- **Synthetische Klicks (`el.click()` per JavaScript) greifen bei Facebook nicht.**
  React hört auf echte Zeigerereignisse. Immer `browser_click` verwenden.
- **`:text-is()` findet Facebook-Schaltflächen nicht**, weil der Text in
  verschachtelten `span`-Elementen liegt. Stattdessen über `aria-label` gehen:
  `div[role="button"][aria-label="Weiter"] >> nth=N`.
- **Markierungen per `setAttribute` überleben nicht.** React ersetzt das Element
  zwischen zwei Aufrufen, ein danach gesetzter Selektor greift ins Leere.
- **Ein „Overlay", das Klicks abfängt, ist oft der gesuchte Dialog selbst.** Vor dem
  Wegräumen prüfen: `document.querySelector('div.__fb-light-mode.xshlqvt').innerText`.
- **Niemals `browser_snapshot` auf ein Passwortfeld.** Der Snapshot gibt den Feldwert
  im Klartext aus. Am 10.08.2026 ist so ein Passwort ins Sitzungsprotokoll geraten.

## Fehlerseiten, damit sie niemand zweimal probiert

| Adresse | Ergebnis | Stattdessen |
|---|---|---|
| `facebook.com/profile/<SEITEN_ID>/settings/?tab=your_facebook_information` | HTTP 404 | `facebook.com/settings/` in der Seiten-Stimme |
| `business.facebook.com/latest/settings/pages?asset_id=1278546548674819` | „Invalid ID. Die angegebene ID ist nicht (und war noch nie) gültig." | Die Kennung ist echt, nur kein Portfolio-Asset, siehe unten |
| `facebook.com/accountquality` als Statusprüfung | „Keine Konto- oder Assetprobleme", obwohl das Konto eingeschränkt ist | `business-support-home/?landing_page=overview`, dort steht der echte Status |
| `business.facebook.com/latest/settings/pages?asset_id=61592772701568` | „Leider ist dieser Inhalt derzeit nicht verfügbar" | Seite gehört keinem Portfolio an |
| `facebook.com/110234024435075` | „Dieser Inhalt ist momentan nicht verfügbar" | Seite ist deaktiviert, nur über ihr Portfolio erreichbar |

## Der eigentliche Blocker: die zweistufige Authentifizierung fehlt, seit 16.01.2021

**GELÖST am 10.08.2026, 22:01 Uhr. Meta nennt die Ursache selbst, im Klartext:**

> „Konto eingeschränkt • **16.01.2021** — Du bist nicht berechtigt, für deine
> Business-Portfolios Werbung zu schalten oder Business-Assets zu verwalten, **da du
> die zweistufige Authentifizierung nicht nutzt**."

Fundstelle: `facebook.com/business-support-home/100002368008924/`, also die
**Detailseite des Kontos**, nicht die Startseite des Support-Centers.

Die dort gelisteten Einschränkungen decken jede einzelne Ablehnung dieses Abends ab:

| Einschränkung laut Meta | Was daran gescheitert ist |
|---|---|
| Kann keine Werbeassets oder **Personen für Unternehmen verwalten** | die sechs abgelehnten Asset-Zuweisungen |
| Kann keine **Werbeanzeigen erstellen oder schalten** | die gesamte Phase 7 wäre hier aufgeschlagen |
| Kann keine Werbekonten verwenden oder verwalten | Werbekonten aufräumen, BusOffensive zuweisen |

**Kein Verstoß, kein Einspruch, kein Langläufer.** Es ist ein Schalter, und der Weg
dorthin steht auf derselben Seite: „Aktiviere die zweistufige Authentifizierung, um
Zugriff zu deinen Business-Konten und Assets zu erhalten."

### Der Schalter ist umgelegt, die Sperre steht noch

**10.08.2026, 22:11 Uhr: Die zweistufige Authentifizierung ist aktiviert.** Wortlaut
der Kontenzentrale: „Zweistufige Authentifizierung aktiviert. Wir fragen nun bei jeder
Anmeldung auf einem unbekannten Gerät nach einem Anmeldecode."

**22:13 Uhr, Gegenprobe am Schreibvorgang: weiterhin abgelehnt**, wortgleich mit
„Assets können nicht zugewiesen werden. Bitte versuche es später noch einmal". Auch
der Statusblock nennt unverändert die fehlende 2FA als Grund, obwohl sie läuft.

**Meta zieht den Kontostatus also verzögert nach.** Das ist der Stand, nicht eine
Widerlegung der Diagnose. Was dagegen belegt ist und nicht mehr geprüft werden muss:
Die Ursache steht schriftlich von Meta selbst, und sie ist adressiert.

**Bemerkenswert:** Unter „Verknüpfte Geräte" stand bereits eine Authentifizierungs-App
(„My Authenticator app"), die 2FA selbst war trotzdem aus. **Eine hinterlegte
Authenticator-App belegt nicht, dass die zweistufige Authentifizierung aktiv ist.**

### Der Einrichtungsweg, für den Wiederholungsfall

1. `accountscenter.facebook.com/password_and_security/two_factor/`
2. Konto „Max Karastelev, Facebook" wählen
3. Facebook schickt einen **achtstelligen Code an `karastoni@googlemail.com`**
   (Absender `security@facebookmail.com`, Betreff „Dein Sicherheitscode lautet …").
   Der ist über den Gmail-Zugang **ohne Max erreichbar**, ein Handy braucht es nicht.
4. Code eintragen, „Weiter". Damit ist die 2FA aktiv.

**Warum das private Konto davon nicht betroffen ist:** Dort ist die zweistufige
Authentifizierung aktiv, belegt durch die Abfrage der Authenticator-App beim Öffnen
der Business Suite am 10.08. um 21:56 Uhr.

**Die Einschränkung ist über fünf Jahre alt.** Sie hat mit der Meldung vom 09.08.2026
nichts zu tun und läuft nicht von selbst ab.

### Zwei Anzeigen widersprechen sich, und die Startseite ist die falsche

| Ort | Aussage |
|---|---|
| `facebook.com/accountquality`, Startseite | „Keine Konto- oder Assetprobleme" für 30 Tage |
| `business-support-home/?landing_page=overview` | „Max Karastelev: **Konto eingeschränkt**", „Proleads: **Assets eingeschränkt**" |

Die Startseite zeigt **Verstöße gegen Werbestandards** der letzten 30 Tage, nicht den
Kontostatus. Eine leere Anzeige dort belegt gar nichts. **Der Statusweg ist immer
„Meine Konten ansehen", nie die Startseite.**

Die Portfolio-Detailseite (`business-support-home/1693993127556558/`) meldet für alle
Werbekonten, Kataloge, Datenquellen und das WhatsApp-Konto „keine Probleme". Das
Etikett „Assets eingeschränkt" spiegelt also nur den Kontostatus wider und ist kein
eigener Mangel des Portfolios.

## Wie sich die Sperre gezeigt hat (Symptome, 10.08.2026)

**Stand 10.08.2026, 21:10 Uhr.** Lesevorgänge laufen einwandfrei, **jeder
Schreibvorgang wird abgelehnt**, und zwar mit wechselnden, irreführenden Meldungen.

| Vorgang | Meldung |
|---|---|
| Seite GridDone löschen (10.08., mehrfach) | „Das von dir eingegebene Passwort ist falsch" trotz nachweislich richtigem Passwort |
| Drei Assets an das private Profil zuweisen | „Assets können nicht zugewiesen werden. Bitte versuche es später noch einmal" |
| **Ein einzelnes** Asset zuweisen | dieselbe Meldung |
| Seite ins Portfolio holen (09.08.) | „Dein Konto ist derzeit eingeschränkt. Die Durchführung dieser Handlung wurde vorübergehend für dich gesperrt" |

Der letzte Fall ist der einzige, der die Ursache beim Namen nennt. Die anderen drei
zeigen dasselbe Verhalten mit anderem Text. **Die Passwortmeldung ist damit sehr
wahrscheinlich eine Fehlanzeige**, nicht die Ursache.

Gegenprobe gelaufen: `facebook.com/accountquality` meldet „Keine Konto- oder
Assetprobleme" für die letzten 30 Tage. **Eine leere Anzeige dort schließt eine
Schreibsperre also nicht aus.**

**Was daraus folgt:** Vor jedem weiteren Versuch an Seiten, Rechten oder Portfolios
erst einen billigen Schreibtest machen, statt lange Wege zu bauen, die am Ende
scheitern. ~~Bleibt die Sperre, ist der Einspruch über das Business-Support-Center ein
Langläufer und gehört sofort angestoßen.~~

**KORREKTUR 10.08.2026, 22:01:** Der Einspruch war nie nötig, siehe oben. Die Lehre
aus dem Abend ist eine andere und sie ist teuer bezahlt: **Vier verschiedene
Fehlertexte für eine Ursache**, und der einzige, der sie benannte, kam von einer
Seite, die niemand geöffnet hatte. **Bei jeder abgelehnten Handlung zuerst den
Kontostatus lesen**, bevor die Meldung selbst gedeutet wird. Der Weg dahin sind zwei
Klicks und er steht in der Tabelle oben.

## Nachgelagerter Blocker: Seiten lassen sich nicht löschen

**Stand 10.08.2026, 20:52 Uhr.** Der Löschfluss läuft bis zum letzten Schritt und
scheitert dort an der Passwortbestätigung.

Der Dialog heißt „Bestätige, dass dies deine Seite ist" und nennt als Kontonamen
**die Seite** („GridDone"), nicht Max. Auf jedes eingegebene Passwort antwortet er
„Das von dir eingegebene Passwort ist falsch."

**Was geprüft und ausgeschlossen ist:**

- Das Passwort stimmt. Max hat es bestätigt, und es ist dasselbe, das in Chromes
  Passwortspeicher liegt (Konto `fb@karastelev.de`).
- Kein Eingabefehler. Zeichenweise getippt, Feldlänge unmittelbar vor dem Absenden
  gemessen: exakt 10 Zeichen, Anfang und Ende stimmen.
- Keine Altlast im Feld. Der Fehlertext verschwindet beim Leeren des Feldes und
  erschien nach jedem neuen Absenden erneut, der Dialog war also frisch.
- **Keine Kontoeinschränkung.** `facebook.com/accountquality` meldet für die letzten
  30 Tage „Keine Konto- oder Assetprobleme". Die Sperre vom 09.08. ist abgelaufen.
- Kein Weg über die Business Suite: Die Seite gehört keinem Portfolio an und ist dort
  deshalb unbekannt.

**Wahrscheinliche Ursache, belegt aber nicht bewiesen:** Der Dialog verlangt in der
Seiten-Stimme ein Passwort für das Seiten-Profil, und ein solches existiert nicht.
Seiten der neuen Seitenerfahrung haben eine eigene Profilkennung, aber keine eigene
Anmeldung.

**Nicht getan und warum:** Xenio wurde **nicht reaktiviert**. Die Seite ist
deaktiviert, zum Löschen müsste sie erst wieder öffentlich werden, und danach liefe
sie in dasselbe Hindernis. Eine reaktivierte tote Seite wäre schlechter als der
Ausgangszustand.

## Was die Löschung nicht blockiert

Die am 07.08. angelegte Seite **GridDone hat keinen Benutzernamen**: Ihre Adresse ist
`facebook.com/profile.php?id=61592772701568`, nicht `facebook.com/griddone`. Ein
Benutzername ist bei Meta das einzige eindeutige Merkmal, Seitennamen dürfen doppelt
vorkommen. **Die geplante Umbenennung von „Die Autarken" nach GridDone wird von ihr
also nicht behindert.**

## Eine Seite trägt zwei Kennungen, und beide sind echt

Der Handoff vom 07.08.2026 führte für die Seite GridDone zwei Kennungen:
„Profil-Kennung 61592772701568" und „Asset-Kennung 1278546548674819".

~~**Die zweite ist bei Meta nie gültig gewesen**, die Business Suite lehnt sie mit
„Invalid ID" ab. Gültig ist allein 61592772701568.~~

**KORREKTUR 10.08.2026, 22:07. Das war falsch, und zwar in beide Richtungen belegt:**

- `facebook.com/1278546548674819` **leitet auf** `profile.php?id=61592772701568`.
  Beide Kennungen meinen dieselbe Seite.
- Die Kontodetailseite des Support-Centers führt sie unter „Seiten, die von dir
  verwaltet werden" als „GridDone, ID: 1278546548674819".

**Was daraus wirklich folgt:** Eine Seite der neuen Seitenerfahrung hat eine
**Seiten-Kennung** und eine **Profil-Kennung**, und sie sind nicht austauschbar. Die
Meldung „Invalid ID. Die angegebene ID ist nicht (und war noch nie) gültig" bezog sich
allein auf den Parameter `asset_id` der Business Suite, und dort ist sie ungültig,
**weil die Seite keinem Portfolio angehört**, nicht weil es die Kennung nicht gäbe.

**Die Lehre:** Eine Fehlermeldung gilt für den Kontext, in dem sie erscheint. „Nie
gültig gewesen" aus einer Portfolio-Ansicht heißt „gehört keinem Portfolio", nicht
„existiert nicht". Vor einer solchen Aussage die Kennung einmal direkt aufrufen, das
kostet einen Aufruf.

## Kennungen

| Objekt | Kennung |
|---|---|
| Portfolio „Proleads" (das echte, trägt alles) | 1693993127556558 |
| Portfolio „Max K" (fast leer) | 644805094242070 |
| Seite GridDone (Profil-Kennung) | 61592772701568 |
| Seite GridDone (Seiten-Kennung, leitet auf die Profil-Kennung) | 1278546548674819 |
| Seite Xenio DACH - Smart Home (deaktiviert) | 110234024435075 |
| Seite Die Autarken | 100095155003279 |
| Seite HOCHZEITSNEST | 113126068776326 |
