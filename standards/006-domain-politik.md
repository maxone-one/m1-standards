# 006: Domain-Policy: Technik auf .one, Inhalt in die Welten

**Status:** active
**Seit:** 2026-04-16, Zuschnitt neu gefasst 2026-08-16 (Max-Direktive)
**Gilt für:** alle Domains, Subdomains und Inhalte

## Regel

**Technische Ressourcen** (Subdomains, Mail-Sender, DNS-Records, OAuth-Apps,
Service-URLs, Doku-Links) werden auf `maxone.one` angelegt, nie auf
`maxone.studio`.

**Inhalte für Menschen** wohnen in den Welten, jeder Inhalt an genau einer
Adresse. Welche Welt wofür zuständig ist, steht unten im Abschnitt „Der
Zuschnitt".

> **KORREKTUR 16.08.2026:** Bis hierher stand „**alle** neuen Resourcen … nie auf
> `maxone.studio`", ohne Unterscheidung zwischen Technik und Inhalt. Der Satz
> stammt aus der Zeit, als `*.maxone.studio` gerade abgeschaltet worden war, und
> war damals richtig. Er verbietet in dieser Fassung aber auch das, was seit dem
> 02.06.2026 in derselben Datei als Zweck von `maxone.studio` steht: SaaS und
> Tools. Max hat den Widerspruch am 16.08.2026 aufgelöst, indem er die Galerie
> ausdrücklich dort verortet hat. Der Broadcast
> `BCAST-2026-04-22-domain-studio-to-one.md` bleibt gültig, er betraf die
> Infrastruktur, und die zieht nicht zurück.

## Warum die Technik auf .one bleibt, und zwar für immer

`*.maxone.studio` ist seit 2026-04-16 produktiv abgeschaltet, alle Traefik-Router
auf maxone-prod laufen auf `*.maxone.one`. User-Direktive damals: „alles auf .one,
nie wieder .studio (vorerst nicht)."

Der tiefere Grund, von Max am 16.08.2026 nachgeliefert: Der Umzug von `.studio`
auf eine andere Domain hat damals sämtliche Routen zerrissen und eine Menge Fehler
erzeugt. Seine Lehre daraus, wörtlich: „`one` wird ein für alle Mal die globale
Route für alles sein. Damit der Stack niemals mehr bricht."

**Die verallgemeinerte Fassung, die auch für jedes künftige Projekt gilt:** Die
Adresse, unter der etwas technisch läuft, ist nie dieselbe wie die, unter der
geworben wird. Die erste muss für immer stabil bleiben, die zweite darf sich
jederzeit ändern. Wer beides zusammenlegt, kann seine Marke nicht mehr ändern,
ohne seinen Stack zu brechen. In der Fachsprache ist `.one` damit eine
**Indirektionsschicht**, also eine Zwischenebene, die zwei Dinge entkoppelt, die
sonst aneinanderkleben.

## Ausnahme

`mail.maxone.studio` + `autoconfig.maxone.studio` bleiben aktiv (Stalwart
Mail-Server, MX/SPF/DKIM/Autoconfig-Clients). Migration ist invasiv und
separat zu planen, nicht in dieser Regel umfasst.

## Wie anwenden

Bei neuen Subdomains auf `*.maxone.one`:
- Vorher prüfen: existiert DNS-A-Record? (Kein Wildcard auf `*.maxone.one`!)
- Jeder Subdomain einzeln. Ohne DNS kein SSL-Cert von Lets Encrypt.

## Infra-Hostname-Gesetz (2026-06-02)

Infrastruktur-Subdomains immer neutral nach Schema:

```
{dienst}.{projekt}.maxone.one
```

Beispiele:
- `db.venfree.maxone.one` (Supabase/Postgres für venfree)
- `api.venfree.maxone.one` (REST-API für venfree)
- `db.vector.maxone.one` (VECTOR-Datenbank)
- `mail.maxone.one` (Zentraler Mailserver)

**Verboten:** Projektnamen als Hostnamen die nicht mehr gelten (`altprojekt-api`),
Personennamen, Marketing-Namen, temporäre Bezeichnungen.

**Warum:** Hostnamen sind langlebig. Sie überdauern Rebrands, Team-Wechsel und
Projekt-Renames. Ein neutrales Schema verhindert dass interne Infra-URLs in
Logs, Zertifikaten und DNS-Records den alten Projektnamen festigen.

## Der Zuschnitt (2026-06-02, ausformuliert und entschieden 2026-08-16)

`maxone.one` ist das neutrale Routing-Dach für alle Systeme. Getrennt wird nach
**Rolle**, nicht nach Zielgruppe: Ein Produkt darf auf mehreren Domains
erscheinen, aber jede Domain hat genau eine Aufgabe.

| Domain | Rolle | Was dort wohnt |
|---|---|---|
| `maxone.one` | Wurzel und Auffangnetz | Internes Routing, Impressum, Datenschutz, Kontakt, ein schlanker Verteiler in die Welten, und alles ohne feste Zuweisung |
| `maxone.work` | Der Außenauftritt | Dienst und Leistung, das Team unter `/team`, Blog, `/meine-geschichte`, die Mailadressen der KI-Mitarbeiter |
| `maxone.studio` | Die Galerie | Werkzeuge, SaaS, eigene Projekte. Hier werden Produkte vorgestellt, auch solche, die anderswo betrieben werden |
| `maxone.pro` | Die Beweis-Domain | Fachartikel und der Selbststudium-Nachweis. Sie belegt Können, sie verkauft nichts |
| `maxone.tech` | Hardware | Gadgets, Kitchen Station, Wearables |

**Die Marke bleibt `maxone.one`**, in jedem Text, jeder Signatur und jedem
Impressum, auch wenn der Kunde immer auf `maxone.work` landet. Max am 16.08.2026:
Das Dach behält den Namen, unter anderem wegen `max@maxone.one`.

**`.one` ist ausdrücklich auch das Auffangnetz** (Max, 16.08.2026): „Genau das ist
der Zusatznutzen von One. Alles umleiten, was keine feste Zuweisung hat. Das
letzte Sicherheitsnetz." Deshalb bleibt `giving.maxone.one` dort, wo es ist, und
`maxone.giving` wird nicht gekauft.

### Ein Inhalt, eine Heimatadresse

Was auf mehreren Welten sichtbar sein soll, hat trotzdem **genau eine**
Heimatadresse. Alles andere leitet dauerhaft dorthin um (301), oder es trägt einen
Kanonisierungs-Hinweis (`<link rel="canonical">`) auf die Heimat.

**Warum diese Zeile hier steht:** Am 16.08.2026 lagen dieselben acht Blogbeiträge
gleichzeitig auf `.work`, `.pro` und `.studio`, `/meine-geschichte` auf drei
Welten, `/tools/voice` auf drei Welten, und das Team doppelt auf
`maxone.work/mitarbeiter` und `maxone.pro/team`. Suchmaschinen entscheiden dann
selbst, welche Fassung sie zeigen und welche sie abwerten. Der Zustand war seit
dem 25.07.2026 in `maxone.one/.planning/REDIRECT-MAP-dach-legacy.md` als offener
Konflikt dokumentiert und nicht behoben.

### Konsequenzen

- **Mehr Domains kosten mehr als Pflege, sie kosten Aufmerksamkeit.** Wer drei
  sichtbare Domains bespielt, teilt Auffindbarkeit und Vertrauen durch drei. Das
  ist ausdrücklich akzeptiert, weil die Rollen verschieden sind, aber es ist kein
  freier Zug.
- **Jede sichtbare Welt braucht ihre Rechtsseiten**, notfalls per Verweis auf
  `maxone.one`. Stand 16.08.2026 haben `.pro` und `.tech` keine eigenen und
  verweisen dorthin, das ist zulässig.
- **Eine Domain ohne Inhalt ist billiger als eine halbfertige.** Registriert
  lassen und leer ist besser, als eine Welt aufzumachen, für die es nichts zu
  zeigen gibt.

## Verify-before-assert: Domain-/DNS-Fakten (HART, 2026-07-12)

Über Domains, DNS und Registrare wird **keine Tatsache aus dem Gedächtnis oder
aus einem halb gelesenen Roh-Feld behauptet**. Lieber fünfmal an der Quelle
nachschauen, als einmal eine falsche Aussage tätigen (Max-Direktive nach einem
Preis-Fehler: eine gTLD als „8,50 €/Jahr" statt korrekt „8,50 €/Monat"
angegeben, also das Zwölffache verrechnet).

Gilt insbesondere für:

- **Preis UND Abrechnungszeitraum:** eine Zahl aus einer Registrar-API oder
  einem Panel nie ohne die Einheit übernehmen. Ist der Betrag pro **Monat** oder
  pro **Jahr**? Ist es Neuregistrierung, Verlängerung oder ein Aktionspreis?
  Betrag und Zeitraum zusammen am maßgeblichen Ort (Domain Offensive fürs
  Kaufen, INWX/`domain.check` nur als Indikator) prüfen, bevor eine Zahl genannt
  oder in ein Doc geschrieben wird. Premium-/gTLDs (`.partners`, `.exchange`,
  `.club` …) sind oft ein Vielfaches teurer als Standard-`.de`.
- **Verfügbarkeit:** „frei/vergeben" immer live per `domain.check` belegen, nie
  aus Erinnerung.
- **DNS-Records, TTLs, Nameserver:** am lebenden Zonen-Stand (INWX API) prüfen,
  nie aus einem alten Doc zitieren.

Ungeprüft → konditional formulieren („laut INWX-Rohwert, Einheit noch zu
bestätigen") oder gar nicht behaupten. Ein genannter Domain-Preis ohne
verifizierten Zeitraum ist ein Fehler, kein Schätzwert.

## Audit

`scripts/audit.mjs` prüft:
- `registry/projects.yml`: keine `domain: *.maxone.studio` (außer mail/autoconfig)
- `docker-compose.yml` aller Projekte: keine Traefik-Hosts auf `.maxone.studio`
- Infra-Hostnamen folgen Schema `{dienst}.{projekt}.maxone.one`
