# Standard 033: Zentrale Infrastruktur: Bauen statt melden

**Status:** aktiv  
**Erstellt:** 2026-06-01  
**Gilt für:** alle maxone.one-Projekte

---

## Prinzip

Wenn ein Tool, MCP-Server, Crawler, Enricher oder Outreacher eine Funktion nicht kann: bauen, nicht melden. "Das geht leider nicht" ist keine Antwort.

Jede neue Funktion entsteht im zentralen Dienst und profitiert allen Projekten sofort. Dezentrale Einzellösungen sind verboten.

---

## Zentrale Dienste

| Dienst | URL | Zweck |
|--------|-----|-------|
| Crawler | https://crawler.maxone.one | Lead-Discovery, Stellensuche, Inbox-Checks, Web-Scraping |
| Enricher | https://enricher.maxone.one | Website-Email-Enrichment, Datenanreicherung |
| Outreacher | https://outreach.maxone.one | E-Mail-Sequenzen, Outbound (Sende-Engine, sendet über das Gateway) |
| Mail-Gateway | https://mail.maxone.one | EINZIGER Engpass für allen ausgehenden Mailverkehr (tx + outreach), fail-closed + Consent + append-only Audit. Einziger Halter der Provider-Keys. Spec: Standard 016-C. |
| n8n (Automatisierung) | selfhosted auf maxone-prod | No-Code-/Workflow-Automatisierung + Webhook-Orchestrierung, projektübergreifender Hub. Kein gehostetes SaaS (Zapier/Make). |
| Downloadkanal | https://github.com/maxone-one/downloads | EINZIGE Auslieferung fertiger Dateien an Menschen (Installer, Pakete, Vorlagen), für alle Projekte zusammen. Details siehe unten. |

Alle drei sind API-first und von KI bedienbar. Neue Fähigkeiten werden als neue Job-Typen, Sources oder Worker eingebaut, nicht als Einzelskripte in Projekten.

---

## No-Code-Automatisierung: selfhosted n8n, nie Zapier/Make

Alle No-Code-/Workflow-Automatisierung und Webhook-Orchestrierung läuft über **selfhosted n8n** (auf maxone-prod), nie über Zapier, Make oder ein anderes gehostetes SaaS. Grund: Datenhoheit, selfhosted-Linie, keine laufenden Fremdkosten, "Code für KI, von KI". Analog zur Tool-Wahl-Logik Mollie-nie-Stripe und Claude-CLI-nie-Anthropic-API.

- n8n ist der **projektübergreifende Automatisierungs-Hub**: jedes Projekt (snapflow, venfree, alle maxone-Properties) hängt seine Webhooks dort ein, statt je Projekt einen eigenen SaaS-Connector.
- Eigene Dienste bleiben **toolagnostisch**: sie sprechen Standard-HTTP/JSON und senden signierte Webhooks (HMAC). n8n konsumiert sie nativ, der Dienst weiß nichts von n8n, kein Vendor-Lock-in.
- Optionaler Ein-Klick-Komfort je Dienst: eine eigene n8n-Community-Node oder ein fertiges Workflow-Template (analog zu einem WordPress-Plugin), nie eine harte Kopplung.

---

## Eine Kette ist erst gebaut, wenn sie zustellt

**Eine Automatisierung, die den Normalfall schafft, ist kein System, sondern eine Demo.**
Jede Kette zwischen zwei Diensten, ob n8n-Workflow, Webhook-Empfaenger oder eigener
Worker, hat die folgenden sieben Punkte, bevor sie an echten Daten haengt. Keiner davon
ist optional, und keiner laesst sich spaeter guenstig nachruesten.

**1. Idempotenzschluessel, und der ist der wichtigste.** Webhooks werden mehrfach
zugestellt, das ist die Zusage der meisten Anbieter (at-least-once), kein Fehler. Jede
eingehende Nachricht traegt einen stabilen Schluessel des Absenders, der Empfaenger legt
ihn ab und verwirft den zweiten Treffer. Ohne das steht derselbe Lead dreimal im CRM und
dieselbe Rechnung zweimal beim Kunden.

**2. Wiederholung mit wachsendem Abstand und Streuung.** Ein Fehlschlag wird wiederholt,
nicht verworfen, mit verdoppeltem Abstand und einem Zufallsanteil, damit nicht alle
Wiederholungen gleichzeitig auf denselben Dienst treffen. Endlich, mit Obergrenze.

**3. Fehlerschlange MIT Rueckweg.** Was nach der letzten Wiederholung uebrig bleibt,
faellt in eine Fehlerschlange. Zu ihr gehoert der Knopf, der die Eintraege wieder
einspielt, samt der Frage, wer ihn drueckt. Eine Fehlerschlange ohne Rueckweg ist ein
Muelleimer mit Zeitstempel.

**4. Alarm statt Log.** Ein Log liest man erst, wenn man schon weiss, dass etwas kaputt
ist. Jede Kette hat eine Schwelle mit einem Wecker dran (Fehlerschlange nicht leer,
Durchsatz unter dem Erwartungswert, letzter Erfolg aelter als X). Ohne Alarm merkt man
den Ausfall daran, dass der Kunde anruft.

**5. Signatur eingehender Webhooks, mit Zeitfenster.** HMAC-Pruefung gegen ein Geheimnis
je Absender, dazu ein Zeitstempel im Signaturumfang und ein enges Fenster, sonst laesst
sich eine einmal mitgeschnittene gueltige Nachricht beliebig oft nachspielen.

**6. Schema-Pruefung an beiden Enden.** Eingang und Ausgang, nicht nur Eingang. Ein
Feld, das der Partner still umbenennt, faellt sonst erst drei Wochen spaeter auf, als
Luecke in der Auswertung.

**7. Eine Korrelations-ID durch die ganze Kette.** Eine Kennung, die vom ersten Aufruf
bis zum letzten Schritt mitlaeuft und in jedem Log-Eintrag steht. Ohne sie ist die Frage
"wo genau ist dieser eine Lead geblieben" nicht beantwortbar, sondern nur erratbar.

**Ausdruecklich NICHT Pflicht: der Circuit-Breaker.** Er schuetzt einen ueberlasteten
Dienst vor einem Anrufer, der ihn totrennt, und loest damit ein Problem, das bei unseren
Mengen nicht existiert. Wer ihn ohne gemessenen Anlass einbaut, hat ein Fachwort
eingebaut, keine Verbesserung. Punkt 2 und 3 decken den Fall ab, den es hier gibt.

Herkunft und die ausfuehrliche Begruendung: `maxone-standards/wiki/integrationen/zustellgarantien.md`

---

## Build-not-Flag-Regel

Wenn eine Aufgabe nicht erledigt werden kann weil etwas fehlt:

1. Welcher zentrale Dienst ist der richtige Ort dafür?
2. Welcher Job-Type / Worker / Source fehlt?
3. Bauen, deployen, danach die ursprüngliche Aufgabe ausführen.

**Priorität:** Erweiterung vor Neubau. Bestehenden Worker anpassen bevor ein neuer entsteht. Neubau nur wenn Scope grundlegend anders ist (anderes Datenmodell, andere Queue, andere Auth).

---

## Cross-Project-Profit

Jede Erweiterung wird dokumentiert und sofort auf bestehende Projekte angewendet wenn sie profitieren können. Broadcast via Standard 021-C (Cross-Project).

Beispiele bereits umgesetzter Erweiterungen:
- `jobsearch` Job-Type im Crawler: findet offene Stellen, prüft ob noch offen, speichert in `job_listings`-Tabelle
- `inboxcheck` Job-Type (geplant): prüft Plattform-Postfächer (freelancermap, malt, gulp)

---

## Fremder Kunde = Referenz, Eigengebrauch = Tenant-Flag

**Ein zentraler Dienst wird immer für den fremden Kunden gebaut, nie für den Eigengebrauch.** Der fremde Kunde ist die Referenz und das Zielbild. Der eigene Gebrauch (maxone selbst als Nutzer eines Dienstes) ist nur ein **Tenant-Flag** auf demselben Pfad, niemals ein zweiter Codepfad und niemals eine Abkürzung, die zur Architektur wird.

Konkret: braucht der Eigengebrauch eine Sonderbehandlung (z.B. „meine eigenen Leads sind sofort akzeptiert, ohne Bezahlvorgang"), wird das als Tenant-Konfiguration gelöst (`auto_approve=true`), die im normalen Kundenpfad einfach einen Schritt überspringt. Der Kundenpfad bleibt der einzige Pfad.

Begründung: sobald der Eigengebrauch einen eigenen, kürzeren Codeweg bekommt, verrottet der Kundenpfad ungetestet, und die Dogfooding-Abkürzung wird versehentlich zur Produktrealität. Wer für den Kunden baut und sich selbst als Tenant behandelt, testet den Kundenpfad bei jeder eigenen Nutzung mit.

Anwendungsfall (Lead-Liefer-Produkt, 2026-07): Kunde bestellt Leads, bekommt sie pseudonymisiert, akzeptiert pro Lead (Mollie-Abrechnung). Der Eigengebrauch (GridDone) ist ein Tenant mit `auto_approve`, dessen Karten sofort als akzeptiert gelten, ohne Abrechnungsereignis, auf demselben Auslieferungs-Codepfad. Konzept: `maxone-enricher/LEAD-CRM-ZIELBILD.md`.

---

## Ein Downloadkanal für alle Projekte

**Jede Datei, die ein Mensch herunterladen soll, wird über `maxone-one/downloads` ausgeliefert**, nie über ein eigenes Repository je Projekt und nie über einen eigenen Server. Max-Entscheid vom 25.08.2026.

Der Grund ist derselbe wie bei jedem anderen zentralen Dienst, hat hier aber eine zweite Seite: Von rund neunzig Repositories unter `maxone-one` sind zwei öffentlich. Ein Release-Anhang in einem privaten Repository ist nicht öffentlich abrufbar, wer den Link anklickt bekommt einen 404. Ein gemeinsames Download-Repository ist damit die einzige Stelle, die überhaupt öffentlich sein muss, während jeder Quelltext privat bleibt.

**Die Dateien liegen in den Releases, nie im Git-Verzeichnis.** Eine Datei im Verzeichnis lädt jeder Klon in voller Größe mit, in jeder je veröffentlichten Fassung, für immer. Die Grenzen unterscheiden sich um Größenordnungen ([GitHub-Doku](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)):

| | Release-Anhang | Datei im Verzeichnis |
|---|---|---|
| je Datei | 2 GiB | 100 MiB, Warnung ab 50 MiB |
| Gesamtgröße | unbegrenzt | unter 1 GB empfohlen, 5 GB Obergrenze |
| Bandbreite | unbegrenzt | entfällt |

**Das Tag trägt das Projekt: `<projekt>-v<version>`**, also `beo-v0.1.0`. Ohne Präfix ist in einem gemeinsamen Repository nicht erkennbar, wozu ein Release gehört. Jeder Anhang trägt Projekt, Version und Plattform im Dateinamen, weil er nach dem Herunterladen in einem fremden Ordner zwischen hundert anderen Dateien liegt.

**`releases/latest` ist hier verboten.** Der Dauerlink zeigt auf das jüngste Release *irgendeines* Projekts im Repository. Wer ihn für Beo einbaut, liefert nach dem nächsten Vera-Release einen 404 aus. Eine Seite holt sich stattdessen `https://api.github.com/repos/maxone-one/downloads/releases` und nimmt den ersten Treffer ihres Tag-Präfixes; sie bekommt damit Version und Dateinamen gleich mit.

---

## Verbot

- Eigener Crawler-Code in Projekten (kein `fetch` + loop + Regex statt Crawler-API)
- Eigener Enricher-Code (kein manuelles WHOIS/Scraping statt Enricher-API)
- Eigene Outreach-Skripte (kein direktes Brevo-Call statt Outreacher-API)
- No-Code-/Automatisierungs-SaaS (Zapier, Make, IFTTT o.ä.) für Workflow-/Webhook-Orchestrierung. Stattdessen selfhosted n8n auf maxone-prod.
- **Direkter Mail-Provider-Aufruf aus IRGENDEINEM Repo** (Brevo, SMTP, SendGrid, Mailgun, SES …). Aller Mailversand läuft über das Gateway `mail.maxone.one`, Provider-Keys nur dort. Spec: Standard 016-C.
- **Eigenes Download- oder Release-Repository je Projekt.** Auslieferung an Menschen läuft ausschließlich über `maxone-one/downloads`. Ebenso verboten: eine Binärdatei im Git-Verzeichnis statt als Release-Anhang, und `releases/latest` als Dauerlink.
- Begründung "das geht nicht" ohne vorherigen Bauversuch
