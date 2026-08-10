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
| Zweitfaktor privat | Authenticator-App (TOTP), kein Mail- oder SMS-Weg angeboten | Anmeldung 10.08.2026 |
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
| `business.facebook.com/latest/settings/pages?asset_id=1278546548674819` | „Invalid ID. Die angegebene ID ist nicht (und war noch nie) gültig." | Die Kennung stammt aus einem Irrtum, siehe unten |
| `business.facebook.com/latest/settings/pages?asset_id=61592772701568` | „Leider ist dieser Inhalt derzeit nicht verfügbar" | Seite gehört keinem Portfolio an |
| `facebook.com/110234024435075` | „Dieser Inhalt ist momentan nicht verfügbar" | Seite ist deaktiviert, nur über ihr Portfolio erreichbar |

## Der eigentliche Blocker: das Konto darf gerade nichts schreiben

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
scheitern. Bleibt die Sperre, ist der Einspruch über das Business-Support-Center ein
Langläufer und gehört sofort angestoßen.

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

## Korrektur eines Irrtums aus dem Handoff

Der Handoff vom 07.08.2026 führte für die Seite GridDone zwei Kennungen:
„Profil-Kennung 61592772701568" und „Asset-Kennung 1278546548674819". **Die zweite
ist bei Meta nie gültig gewesen**, die Business Suite lehnt sie mit „Invalid ID" ab.
Gültig ist allein 61592772701568.

## Kennungen

| Objekt | Kennung |
|---|---|
| Portfolio „Proleads" (das echte, trägt alles) | 1693993127556558 |
| Portfolio „Max K" (fast leer) | 644805094242070 |
| Seite GridDone | 61592772701568 |
| Seite Xenio DACH - Smart Home (deaktiviert) | 110234024435075 |
| Seite Die Autarken | 100095155003279 |
| Seite HOCHZEITSNEST | 113126068776326 |
