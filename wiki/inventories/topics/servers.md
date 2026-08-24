---
title: Server-Inventar
aka: [Hetzner-Cloud-Inventar, SSH-Zugaenge, maxone-prod, Stalwart-Hosts, Hetzner-Preiserhoehung, Altpreis, Rescale, Hetzner-Bibel, Serverkosten, Arm-Migration, cax31, cax41, Umverteilung]
sources:
  - C:\Users\max\.claude\CLAUDE.md (archived 2026-05-22, Zeilen 311-405)
last_updated: 2026-08-24
status: active
---

# Server-Inventar

Alle Hetzner-Cloud-Server unter Max' Kontrolle, ihre SSH-Zugaenge, Container-Aufstellung und projekt-spezifische Eigenheiten.

## SSH-Zugang

- SSH hat IMMER Vorrang vor Web-Fetch (globale Regel)
- Wenn etwas ueber SSH erledigt werden kann, SSH nutzen — nicht fragen

> **Naming-Stolperstelle:** "Vybora" ist doppelt belegt. Die **KI-Mitarbeiterin Vybora** lebt weiter und ist Teil des Agenten-Teams. Das **Vybora-IDE-Cloud-Projekt** (Server `vybora-prod`, 46.225.88.53) schlaeft seit 2026-05-02 bewusst — nicht mehr antippen.

| Server             | IP              | SSH-Key            | Befehl                                                         |
|--------------------|-----------------|--------------------|----------------------------------------------------------------|
| `maxone-prod`      | 128.140.40.235  | `~/.ssh/id_ed25519`| `ssh -i ~/.ssh/id_ed25519 root@128.140.40.235`                 |
| `maxone-watchdog`  | 167.235.226.129 | `~/.ssh/id_ed25519`| `ssh -i ~/.ssh/id_ed25519 root@167.235.226.129`                |
| `maxone-staging`   | 178.105.124.92  | `~/.ssh/id_ed25519`| `ssh -i ~/.ssh/id_ed25519 root@178.105.124.92`                 |
| ~~`voltfair-cli`~~ | ~~46.225.107.118~~ | — | **GELOESCHT 2026-08-04** (voltfair an Robert Scholter uebergeben) |
| ~~`voltfair-db`~~  | ~~46.225.168.235~~ | — | **GELOESCHT 2026-08-04** (voltfair an Robert Scholter uebergeben) |
| ~~`vybora-prod`~~  | ~~46.225.88.53~~ | — | **schlaeft seit 2026-05-02** (IDE-Cloud-Projekt pausiert; nicht antippen) |

> **voltfair ist seit dem 04.08.2026 nicht mehr Max' Infrastruktur.** Das Projekt laeuft vollstaendig auf `voltfair-prod` (46.225.15.232) in Robert Scholters eigenem Hetzner-Projekt "Voltfair.de" (ID 15471119), inklusive DNS-Zone (seit 26.07.) und Mailserver. Max hat dort weder SSH-Zugang noch einen gueltigen API-Token, nur die Admin-Rolle im Projekt. Seine beiden CPX22 wurden am 04.08. geloescht, samt primaeren IPs, das spart 16,98 € netto im Monat. Vorher gesichert nach `/opt/archiv/voltfair-{cli,db}-2026-08-04.tar.gz` auf maxone-prod. **Damit stehen nur noch drei Server in Max' Konto:** maxone-prod (`maxone-projekte`), maxone-staging und maxone-watchdog. Die Tabellen weiter unten fuehren die voltfair-Spalten noch als Vorgeschichte.

## maxone-watchdog — externer Uptime-Waechter (seit 2026-04-27)

- Hetzner Falkenstein (separate Region zu maxone-prod-Nuernberg = echter externer Probe)
- 3.7 GB RAM, 38 GB Disk, laeuft `watchdog-traefik` + `watchdog-kuma` (Uptime-Kuma 1.x)
- Erreichbar: https://watchdog.maxone.one/dashboard (DNS-01-Cert via INWX)
- 15 HTTP/Port-Probes fuer agent.maxone.one, alle Kunden-Domains, Supabase-Studio, Umami, Zensor, Mail
- **Repo:** [`maxone-one/maxone-watchdog`](https://github.com/maxone-one/maxone-watchdog) — `/opt/maxone-watchdog/` auf Server ist mit `origin/main` in sync (Drift 2026-05-11 geschlossen)
- **Push-Monitors:** drei Push-Tokens live (Watchdog-Heartbeat, Disk-Alert maxone-prod, Disk-Alert watchdog-server) — URLs in `/opt/secrets/global/sentinel.env`, vom `watchdog`-Container auf maxone-prod (umbenannt 2026-05-11, vorher `sentinel` — Namens-Clash mit Zentinel) + `docker-cleanup.sh`-Cron konsumiert

## Unterschiede zwischen Servern

| Merkmal          | maxone-prod       | maxone-staging  | maxone-watchdog | voltfair-cli     | voltfair-db   |
|------------------|-------------------|-----------------|-----------------|------------------|---------------|
| Reverse Proxy    | Traefik (eigenstdg.) | Traefik (eigenstdg.) | Traefik  | Traefik (Coolify)| keiner        |
| Orchestrierung   | **manuell**       | **manuell**     | manuell         | Coolify          | keiner        |
| Supabase         | ja (lokal)        | nein            | nein            | nein (auf DB-Svr)| ja (dediziert)|
| Mail             | Stalwart          | nein            | nein            | Stalwart         | nein          |
| GitHub Runner    | ja (Org-Level)    | **ja** (maxone-staging) | nein   | ja               | nein          |
| Kuma             | nein              | nein            | **ja**          | nein             | nein          |
| Hardware         | **cpx32** (4C/8GB) | cpx32 (4C/8GB) | **cax11** (2C/4GB) | (Hetzner)        | (Hetzner)     |

> _vybora-prod historisch: Caddy-RP, manuell orchestriert, eigene aeltere Supabase, kein Stalwart, eigener Runner. Stand 2026-05-02 abgeschaltet._

> **KORREKTUR 16.08.2026 an der Hardware-Zeile, gemessen an der Cloud-API des eigenen Kontos**
> (`/v1/servers`, aus einer Vera-Kostenrechnung heraus). Dort stand `CX41` fuer maxone-prod und
> `CX22` fuer maxone-watchdog, beides falsch. Richtig sind **cpx32** (4 Kerne, 8 GB, AMD) und
> **cax11** (2 Kerne, 4 GB, ARM). Das deckt sich mit dem Befund weiter unten, dass maxone-prod
> auf der geteilten AMD-Linie laeuft, und widerlegt die Tabelle, nicht ihn.
>
> **Stolperstein fuer jede kuenftige Abfrage: maxone-prod heisst im Hetzner-Konto
> `maxone-projekte`.** Wer nach dem Namen `maxone-prod` sucht, findet nichts.
>
> **Listenpreise am 16.08.2026, brutto im Monat:** cpx32 42,23 EUR (fsn1, hel1, nbg1),
> cax11 7,13 EUR. Das sind die aktuellen Listenpreise, **nicht zwingend die gezahlten**: Ob eine
> Maschine noch einen Altpreis traegt, zeigt nur die Rechnung im Konto (siehe Abschnitt
> "Hetzner-Altpreise" weiter unten).

## Server-Infrastruktur (maxone-prod)

- **Hostname:** `maxone-prod`
- **OS:** Ubuntu (Hetzner VPS)
- **Orchestrierung:** Manuell (Coolify komplett entfernt 2026-03-23). Traefik v3.6 eigenstaendig unter `/opt/traefik/`.
- **VECTOR Agent:** Ops-Agent (`vector-blue`/`vector-green` Container, Blue/Green) ueberwacht alle Server/Projekte, Telegram Bot + Web-Chat, Auto-Discovery
- **Kein Caddy** — alles laeuft ueber Traefik
- **Datenbank:** Supabase self-hosted (PostgreSQL, Container `supabase-db`)
- **Mail:** Stalwart Mail Server (Container `stalwart-mail`)
- **Analytics:** Umami (self-hosted)
- **Docker-Netzwerke:** `coolify` (Traefik, Name beibehalten), `supabase_default` (DB + Services)

### Wo laeuft was (Ports)

| Port  | Dienst                          |
|-------|---------------------------------|
| :80   | Traefik (HTTP → HTTPS redirect) |
| :443  | Traefik (HTTPS, alle Projekte)  |
| :3000 | Supabase Studio (intern)        |
| :8000 | Supabase Kong API Gateway       |

### Deployte Projekte auf maxone-prod (Stand: 2026-05-31)

> **Re-Compiled 2026-05-31** via `ssh ... docker ps`. Vorgängerstand 2026-04-02 listete 10 Projekt-Container; tatsächlich live sind 80 Container (≈50 Projekt + 30 Infra). Massiver Ausbau in 2 Monaten: Bewerbungs-Mikrosites, Crawler/Outreach/Enricher-Pipeline, maxone aufgesplittet in v2/pro/studio/tech/work, wired-* (3 Container), pivotin-*, viktoria, repivot Frontend+Backend gesplittet.

**maxone.one Family (alle Blue):**

| Container | Slot | Projekt | URL |
|---|---|---|---|
| `maxone-v2-blue` | Blue | maxone.one (Umbrella + Zentinel + admin/email) | https://maxone.one |
| `maxone-pro-blue` | Blue | maxone.pro (Expertise) | https://maxone.pro |
| `maxone-studio-blue` | Blue | maxone.studio (SaaS & Tools) | https://maxone.studio |
| `maxone-tech-blue` | Blue | maxone.tech (Hardware & Devices) | https://maxone.tech |
| `maxone-work-blue` | Blue | maxone.work (Dienst & Leistung) | https://maxone.work |

**Kunden-/SaaS-Projekte (Blue/Green wo angegeben):**

| Container | Slot | Projekt | URL |
|---|---|---|---|
| `slf-app-green` | Green | SLF (Stadt Lahn Fluss) | https://stadtlahnflow.de |
| `venfree-app-green` | Green | venfree | https://venfree.de |
| `viktoria-app-green` + `viktoria-identity` | Green | Viktoria From Fotografie | https://viktoria-from.de |
| `snapflow-app-blue` | Blue | snapflow.one | https://snapflow.one, https://app.snapflow.one |
| `repivot-backend-blue` + `repivot-frontend-blue` | Blue (split) | repivot.in | https://repivot.maxone.one |
| `plansey-app-green` | Green | plansey-2026 / -engaged | (DNS-Wartung) |
| `katchi-app-green` | Green | katchi | https://katchi.maxone.studio |
| `kitten-app` | Single | kitten | (intern) |
| `karastelev-app` | Single | karastelev | https://karastelev.de |
| `stadtpunkt-app-green` | Green | stadtpunkt | https://stadtpunkt.maxone.studio |
| `zrow-dashboard` | Single | zrow (Browser-Dashboard) | (intern) |
| `zensor-app` | Single | zensor | (intern) |
| `gs-lohra` | Single | Grundschule Lohra Webseite | https://grundschule-lohra.de |
| `kitchen-station-app` | Single | kitchen-station | (intern) |
| `bewerbung`, `interim-bewerbung`, `leica-bewerbung` | Single je | 3 Bewerbungs-Mikrosites | (intern) |

**Toolkit / Tooling-Apps:**

| Container | Projekt | URL/Zweck |
|---|---|---|
| `crawler-app` + `crawler-ui` + `crawler-db` | maxone-crawler (Lead-Discovery) | https://crawler.maxone.one |
| `outreach-app` + `outreach-ui` + `outreach-db` | maxone-outreach (E-Mail-Sequenzen) | https://outreach.maxone.one |
| `enricher-app` + `enricher-db` | maxone-enricher (Website-Email-Enrichment) | https://enricher.maxone.one |
| `toolkit-green` + `toolkit-db` | maxone-toolkit | (intern) |
| `schreibstudio-app` + `schreibstudio-telegram` | schreibstudio (SvelteKit + TG-Bot) | https://schreibstudio.maxone.studio |
| `umami-app-blue` (DB: `shared-db`, nicht mehr `umami-db`/gestoppt, Stand 2026-07-12) | Analytics | https://analytics.maxone.one (analytics.maxone.studio leitet per 301 dorthin) |
| `paperclip-db` | paperclip (Vision-Familie-Orchestrator) | (intern) |
| `pivotin-api` + `pivotin-db` + `pivotin-postgrest` | pivotin | (intern) |

**Agent / Sentinel / Bot:**

| Container | Slot | Zweck |
|---|---|---|
| `vector-green` + `vector-redis` + `vector-site-blue` | Green/Blue | VECTOR Agent (Ops-Agent + Web-Chat + Redis) — agent.maxone.studio |
| `watchdog` | Single | Push-Monitor (Heartbeat + Disk-Alert) — umbenannt 2026-05-11 von `sentinel` wegen Zentinel-Namens-Clash |
| `zentinel-vigil` | Single | Zentinel VIGIL (Mail-Watchdog) |
| `wired-repair` + `wired-webchat` + `wired-telegram-bot` | Single je | wired-team Family (telegram-bot zeigte 2026-05-31 Restart-Loop — beobachten) |
| `ve-api-blue` + `ve-studio-blue` + `ve-worker` | Blue | Visual Engine |
| `snappymail-viktoria` | Single | SnappyMail Web-Interface für Viktoria |

### Infrastruktur-Container

- **Traefik:** `traefik` (eigenstaendig unter `/opt/traefik/`)
- **Supabase (maxone, shared instance):** `supabase-db`, `supabase-auth`, `supabase-rest`, `supabase-kong`, `supabase-storage`, `supabase-pooler`, `supabase-edge-functions`, `realtime-dev.supabase-realtime`
- **Supabase (SLF, dedicated):** `slf-db`, `slf-auth`, `slf-rest`, `slf-kong`, `slf-storage`, `slf-crawler`
- **Supabase (vanfree, dedicated):** `vanfree-db`, `vanfree-auth`, `vanfree-rest`, `vanfree-kong`, `vanfree-storage`, `vanfree-templates`
- **Supabase (solarproof, dedicated):** `solarproof-db`, `solarproof-auth`, `solarproof-rest`, `solarproof-kong`
- **Mail:** `stalwart-mail`

Regel (Standard 018-db-isolation): 1 Projekt = 1 eigene DB-Instanz. Shared `supabase`-* nur für maxone.* Familie; SLF/vanfree/solarproof haben jeweils eigene Stacks.

### Supabase-Zugang

- Studio: DEAKTIVIERT (nicht mehr noetig — Claude steuert alles per CLI/SSH)
- API (Kong): Port 8000 intern, extern via `panel.maxone.studio`

### Server-Discovery Regel

- Bei jedem Session-Start pruefen: `ssh ... "docker ps --format '{{.Names}}'"`
- Neue Container erkennen und zuordnen
- Gestoppte/restartende Container melden
- Diese Liste ist ein Snapshot — die echte Wahrheit liegt auf dem Server

## Stalwart Mail Server

- **Instanzen:** 2 (maxone-prod + voltfair-cli)
- **Admin-User:** `admin` (Passwort: SHA-512 gehasht in Config)
- voltfair-db hat KEINE Mail-Instanz (vybora-prod ebenfalls nicht — schlaeft sowieso seit 2026-05-02)

| Server        | Container       | Fuer Projekte                                    |
|---------------|-----------------|--------------------------------------------------|
| `maxone-prod` | `stalwart-mail` | vanfree, plansey, maxone.studio                  |
| `voltfair-cli`| `stalwart-mail` | voltfair.de                                      |

## Hetzner-Tarifgenerationen: bei JEDER Neubestellung die CX-Gen3-Linie pruefen (2026-07-26)

**Der Tarifname sagt nichts ueber den Preis, die Generation tut es.** Seit Hetzners Umstellung vom 16.10.2025 unterscheiden die Tarife nicht mehr nach Hardware-Typ, sondern nach Hardware-Generation. Praktisch heisst das: Es gibt Tarife mit **identischen Eckdaten zu voellig verschiedenen Preisen**, und wer nach Gewohnheit einen CPX bestellt, zahlt schnell das Vierfache. Alle Werte am 26.07.2026 aus der Cloud-API des eigenen Kontos gezogen (`/v1/server_types`, Standort nbg1, brutto):

| Eckdaten | guenstigster Tarif | teuerster Tarif mit denselben Eckdaten | Faktor |
|---|---|---|---|
| 2 vCPU, 4 GB, 40 GB | **cx23, 6,53 €** | cax11 (Arm) 7,13 € | 1,1 |
| 4 vCPU, 8 GB, 80 GB | **cx33, 10,10 €** | cax21 (Arm) 12,48 € | 1,2 |
| 2 vCPU, 4 GB, 80 GB | cpx21 (Gen1) 11,29 € | **cpx22 (Gen2) 23,19 €** | 2,1 |
| 4 vCPU, 8 GB, 160 GB | cpx31 (Gen1) 20,81 € | **cpx32 (Gen2) 42,23 €** | 2,0 |

Die **CX-Gen3-Linie** (`cx23/33/43/53`, „Cost-Optimized", laeuft je nach Verfuegbarkeit auf Intel oder AMD) ist durchgaengig die guenstigste x86-Wahl und schlaegt sogar die Arm-CAX-Tarife. Die **CPX-Gen2-Linie** (`cpx12/22/32/42/52/62`, „Regular Performance") ist die teuerste und bietet bei gleichen Eckdaten nichts Zusaetzliches ausser neuerer Hardware. Die Gen1-Tarife (`cpx11/21/31/41/51`) tauchen in der API nur noch auf, weil das Konto solche Server haelt; fuer Neubestellungen sind sie eingestellt.

Kurios und leicht zu uebersehen: `cpx12` (1 vCPU, 2 GB, 13,67 €) ist teurer als `cx23` (2 vCPU, 4 GB, 6,53 €), also **doppelt so teuer fuer die Haelfte der Maschine**. Der im Juli 2026 als „neuer Einstiegsserver" beworbene CPX12 ist damit fuer fast jeden Zweck die schlechteste Wahl im Katalog.

**Regel:** Vor jeder Neubestellung die CX-Gen3-Zeile derselben Groesse gegenrechnen, nicht aus Gewohnheit CPX nehmen. Das gilt nur fuer NEUE Server; Bestandsserver nie deswegen rescalen, das vernichtet den Altpreis (siehe naechster Abschnitt).

> **KORREKTUR 24.08.2026: Die ganze CX-Gen3-Linie ist in Deutschland derzeit nicht bestellbar.**
> Gemessen über `/v1/server_types`, ausgewertet nach `locations[].available` statt nach dem
> bloßen Erscheinen in der Preisliste: **cx23, cx33, cx43 und cx53 stehen an allen drei
> deutschen Standorten (fsn1, nbg1, hel1) auf `available: false`.** Bestellbar sind dort nur
> die CAX-, CPX-Gen2- und CCX-Linien.
>
> Die Empfehlung oben bleibt richtig, sie läuft aber praktisch ins Leere, solange die Linie
> nicht lieferbar ist. **Die Lehre für jede Preisabfrage: Ein Tarif in der Preisliste ist noch
> kein Angebot.** `prices` enthält auch Typen, die man nicht kaufen kann; erst
> `locations[].available` sagt, ob eine Bestellung möglich ist. Wer nur nach Preis sortiert,
> empfiehlt Maschinen, die es nicht gibt.
>
> **Günstigste tatsächlich bestellbare Wahl in Deutschland am 24.08.2026** (brutto/Monat):
> 8 Kerne und 16 GB gibt es als `cax31` für 24,98 € (Arm) oder `cpx42` für 82,69 € (x86),
> 16 Kerne und 32 GB als `cax41` für 48,78 € (Arm) oder `cpx62` für 154,69 € (x86). Ohne Arm
> kostet dieselbe Maschine also gut das Dreifache.

**Anlass:** Bei der Kostenplanung fuer die voltfair-Uebergabe aufgefallen. Die beiden voltfair-CPX22 laufen auf dem Altpreis 7,99 € netto, waehrend derselbe Tarif neu 19,49 € netto kostet und ein cx33 mit doppelter CPU und doppeltem RAM nur 8,49 € netto.

## Hetzner-Altpreise: welche Aktionen den guenstigen Preis verfallen lassen (2026-07-25)

**Kernregel: Ein Bestandsserver behaelt seinen alten Preis nur, solange er unangetastet bleibt.** Hetzners Pressemitteilung zur Anpassung vom 15.06.2026 sagt "Aktuell gemietete Server bleiben von der Preisanpassung unberuehrt", die technische Doku schraenkt das aber ein: "bei bestimmten Aenderungen an Servern mit alten Preisen werden ebenfalls die neuen Preise angewendet". Wer nur die Pressemitteilung liest, haelt den Altpreis faelschlich fuer sicher.

**Abschliessende Liste aus der Cloud-FAQ:**

| Aktion | Altpreis bleibt? |
|---|---|
| Rescale, egal ob hoch ODER runter | **nein, neuer Preis** |
| Wiederherstellen eines geloeschten Servers | **nein, neuer Preis** |
| Verschieben in ein Projekt mit **anderer** Waehrung | **nein, neuer Preis** |
| Verschieben in ein Projekt mit derselben Waehrung | ja |
| Rebuild des Servers | ja |
| Server einfach weiterlaufen lassen | ja |

Quellen: <https://docs.hetzner.com/de/cloud/billing/faq> (Abschnitt "Welche Kundenaktionen fuehren bei Servern mit alten Preisen zu einer Aktualisierung des Serverpreises?") und <https://docs.hetzner.com/general/infrastructure-and-availability/price-adjustment/>, beide abgerufen 25.07.2026.

**Die teure Falle:** Ein Rescale zaehlt in BEIDE Richtungen. Wer fuer eine Lastspitze kurz hochzieht und danach wieder herunterstuft, landet dauerhaft im neuen Tarif, obwohl die Aktion sich reversibel anfuehlt. Beim CPX22 waeren das 19,49 statt 7,99 Euro im Monat, also fast das Zweieinhalbfache, dauerhaft, fuer eine Aktion von zehn Minuten.

**Handlungsregel bei der naechsten angekuendigten Preiserhoehung:**

1. **Vor dem Stichtag bestellen, was absehbar gebraucht wird.** Bestellungen, die vor dem Stichtag aufgegeben und erst danach geliefert werden, bekommen laut Doku noch die alten Preise.
2. **Ab dem Stichtag jeden Bestandsserver einfrieren.** Kein Rescale, kein Restore, kein Waehrungs-Projektwechsel, solange der Altpreis lebt. Rebuild und Umzug in derselben Waehrung sind unbedenklich.
3. **Lastspitzen nicht ueber Rescale abfangen**, sondern ueber einen zweiten Server oder einen Load Balancer daneben. Der teure Bestandsserver bleibt unberuehrt, die Zusatzkapazitaet ist wieder kuendbar.
4. **Vor jedem geplanten Rescale rechnen:** neuer Dauerpreis gegen den einmaligen Nutzen. Oft ist ein zusaetzlicher kleiner Server billiger als der dauerhafte Tarifsprung des grossen.
5. **Ausgenommen von der Anpassung 2026 waren** Webhosting, Managed Server, Serverboerse und Storage-Produkte. Bei kuenftigen Anpassungen jeweils den Geltungsbereich pruefen, nicht annehmen.

**Betroffene Maschinen:** Alle Server oben sind Hetzner-Cloud-Instanzen, die Regel gilt also fuer jede davon, projektuebergreifend. `maxone-prod` ist Instanz 120088436 in nbg1-dc3, 4 vCPU auf AMD EPYC Genoa, 8 GB RAM (geteilte AMD-Linie, CPX-Klasse), geprueft am 25.07.2026 ueber die Cloud-Metadaten `http://169.254.169.254/hetzner/v1/metadata`. Ob eine einzelne Maschine noch einen Altpreis traegt, zeigt nur die Rechnung im Hetzner-Konto.

**Anlass:** Max wurde von einer Preiserhoehung getroffen, obwohl er den Server bereits besass. Die Erklaerung steht in dieser Tabelle, die Annahme "Bestandskunden sind sicher" war falsch.

## Die Cloud-API kennt keine Preise, nur eine Preisliste (2026-08-24)

**Das Server-Objekt der Hetzner-Cloud-API hat kein einziges Preisfeld.** Gemessen an
`/v1/servers`, vollständige Feldliste je Server: `backup_window`, `created`, `id`, `image`,
`included_traffic`, `ingoing_traffic`, `iso`, `labels`, `load_balancers`, `location`, `locked`,
`name`, `outgoing_traffic`, `placement_group`, `primary_disk_size`, `private_net`, `protection`,
`public_net`, `rescue_enabled`, `server_type`, `status`, `volumes`. Kein `price`, kein `cost`,
kein `billing`.

Die einzigen Preise, die über die API erreichbar sind, hängen am **Typ** (`server_type.prices`),
nicht an der Instanz. Das ist der **Listenpreis für Neubestellungen**. Eine laufende Maschine mit
Altpreis sieht in der API exakt so aus wie eine neue mit Neupreis.

**Damit ist der Warnsatz im Abschnitt oben technisch begründet, nicht nur vorsichtig formuliert:
Was gezahlt wird, steht ausschließlich in der Rechnung.**

### Der Prüfstein, den man ohne Rechnung hat: `created`

Die Preisanpassung gilt laut Hetzner für Instanzen, die **ab dem 15.06.2026 erstellt oder
rescaled** wurden. Das Erstellungsdatum liefert die API, also lässt sich der Altpreis-Verdacht
ohne Kontozugang erhärten:

| Server | erstellt | Folge |
|---|---|---|
| `maxone-projekte` | 2026-02-06 | vor dem Stichtag, Altpreis |
| `maxone-watchdog` | 2026-04-27 | vor dem Stichtag, Altpreis |
| `maxone-staging`  | 2026-05-12 | vor dem Stichtag, Altpreis |

**Grenze der Methode, und sie ist wichtig:** `created` beweist nur die eine Hälfte. Ein späterer
Rescale hebt den Preis, und **die API führt kein Feld, das einen Rescale sichtbar macht**. Ein
Server mit altem `created` kann also trotzdem im neuen Tarif laufen. Umgekehrt gilt es hart: ein
`created` ab dem 15.06.2026 heißt sicher Neupreis.

### Gemessene Altpreise, netto je Monat (Rechnung 083000975793, Zeitraum 06/2026)

| Tarif | Altpreis | Listenpreis heute | Faktor |
|---|---|---|---|
| `cpx32` | **13,99 €** | 35,49 € | 2,5 |
| `cax11` | **4,49 €**  | 5,99 €  | 1,3 |
| `cpx22` | **7,99 €**  | 19,49 € | 2,4 |

Zwei CPX32 kosten damit zusammen 27,98 € netto, also **33,30 € brutto**, nicht die 84,47 €, die
sich aus der Preisliste ergäben. Die Rechnung trägt den Hinweis selbst: „Neue Tarife gelten für
Cloud-Instanzen, die ab dem 15. Juni 2026 erstellt oder rescaled wurden. Bestehende Instanzen
bleiben bis zum Rescaling preislich unverändert."

### Die Rechnung sagt den Preis, aber nie den Bestand

**Eine Rechnung ist immer ein abgeschlossener Vergangenheitsmonat.** Dieselbe Rechnung
083000975793 führt unter „Projekt voltfair" zwei CPX22 mit 15,98 € netto. Daraus wurde am
24.08.2026 der Schluss gezogen, Max zahle laufend für Roberts Server. **Falsch:** Der
Leistungszeitraum ist 06/2026, und die beiden Maschinen wurden am **04.08.2026 gekündigt und
gelöscht**, siehe die SSH-Tabelle oben. Voltfair läuft seither vollständig in Robert Scholters
eigenem Konto.

**Die beiden Quellen taugen also für genau je eine Frage, und für die andere nicht:**

| Frage | richtige Quelle |
|---|---|
| Was kostet eine laufende Maschine? | die letzte Rechnung |
| Welche Maschinen laufen überhaupt? | die API, `/v1/servers` |

Wer die Rechnung für den Bestand nimmt, führt gekündigte Server weiter. Wer die API für den Preis
nimmt, rechnet mit Listenpreisen. **Beide Fehler sind am selben Tag passiert, in dieselbe
Aufstellung hinein.**

### Was daraus für Upgrade-Fragen folgt

**Bei einem Bestandsserver mit Altpreis rechnet sich ein Upgrade fast nie**, weil der Vergleich
nicht Listenpreis gegen Listenpreis läuft, sondern Altpreis gegen Listenpreis. Gegen zwei CPX32
im Altpreis (33,30 € brutto) spart ein `cax31` nur 8,32 € im Monat und verlangt dafür eine
vollständige Arm-Migration; ein `cax41` kostet sogar 15,48 € mehr. **Und jedes Rescale der
Bestandsmaschine vernichtet zusätzlich die Grundlage der Rechnung.** Der richtige Hebel bei einem
vollen Server ist deshalb Umverteilung auf vorhandene Maschinen, nicht ein größerer Tarif.

### Wie teuer eine Arm-Migration von maxone-prod wirklich wäre (gemessen 2026-08-24)

Weil die Ersparnis nur über die CAX-Linie zu holen ist, wurden alle 58 Images der laufenden
Container gegen ihre Registry-Manifeste geprüft (`docker manifest inspect`, ausgeführt auf
maxone-staging, um prod nicht zu belasten):

| Ergebnis | Anzahl | Bedeutung |
|---|---|---|
| bietet `arm64` an | 22 | läuft ohne Änderung |
| **nur x86** | **0** | **kein einziger echter Blocker unter den Fremd-Images** |
| nicht abfragbar | 36 | lokal gebaut oder in ghcr ohne Anmeldung, kein Manifest abrufbar |

**Die entscheidende Zahl ist die Null.** Jedes fremde Image aus einer öffentlichen Registry, also
Supabase, Postgres, Traefik, n8n, Stalwart, Vaultwarden und die übrigen, kann Arm bereits. Die 36
nicht abfragbaren sind ausnahmslos Max' eigene, erkennbar an `:latest`, `:local` oder
`ghcr.io/maxone-one/*`, dazu elf namenlose Hash-Images.

Ihre Basis-Images sprechen dafür, dass ein Neubau billig wäre: gemessen über die Dockerfiles unter
`/opt` sind es durchgehend `node:20-alpine`, `node:22-alpine`, `node:22-slim`, `nginx:alpine`,
`python:3.12-slim` und `alpine:3.20`. **Alle diese Basen haben offizielle arm64-Varianten.** Der
Aufwand liegt damit nicht im Portieren, sondern im einmaligen Umstellen der Bau-Pipelines auf
`buildx --platform linux/arm64`.

**Trotzdem lohnt es beim heutigen Altpreis nicht**, siehe Absatz darüber. Die Messung ist für den
Tag gedacht, an dem der Altpreis ohnehin fällt, etwa nach einem erzwungenen Rescale.

### Der Fehlerfall, aus dem das hier stammt

Am 24.08.2026 wurde eine Kostenaufstellung aus `server_type.prices` gebaut und als gezahlter
Preis vorgelegt: 42,23 € je CPX32, 84,47 € für beide. Max hat widersprochen, die Rechnung gab ihm
recht. **Der Warnsatz dagegen stand zu diesem Zeitpunkt bereits in dieser Datei**, im Abschnitt
„Unterschiede zwischen Servern" vom 16.08.2026, und wurde nicht gelesen.

Zwei Ursachen, beide baulich:

1. **Die Bibel wurde nicht ausgelöst.** `~/.claude/rules/bibel-bei-anbieterarbeit.md` lädt über
   `paths:`-Frontmatter, und ihre Tabelle nennt Deepgram, LiveKit, Cartesia, Google Calendar,
   Zadarma und Fish-Audio. **Hetzner steht nicht darin**, und Serverarbeit fasst ohnehin keine
   Datei an, auf die ein Pfadmuster passen könnte. Eine Bibel, die nur bei Dateiberührung lädt,
   deckt Infrastrukturarbeit grundsätzlich nicht ab.
2. **Der Pfad in der Memory zeigt ins Leere.** `reference-hetzner-altpreis-schuetzen` verweist auf
   `~/.claude/maxone-wiki/inventories/topics/servers.md`. Auf dem NUC liegt das Wiki seit dem
   Umzug unter **`~/Projekte/maxone-standards/wiki/`**, `~/.claude/maxone-wiki` existiert nicht.

**Regel daraus:** Vor jeder Aussage über laufende Kosten wird die letzte Rechnung geöffnet, nicht
die API befragt. Die API beantwortet „was kostet so eine Maschine", nie „was zahlt Max".

## Verwandt

- Runner-Pool je Server → [[runners]]
- Mail-Architektur (Stalwart-Regeln, Brevo, Zentinel) → `~/.claude/wiki/maxone-mail-pilot/INDEX.md`
- Bibel mit allen Stalwart-Vorfaellen → `c:/Users/max/Projects/maxone.one/briefings/ZENTINEL-STALWART-BIBEL.md`
