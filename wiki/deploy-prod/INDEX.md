# Deploy und Betrieb auf maxone-prod: Bedienhandbuch

Angelegt am 11.08.2026 nach einer Bestandsaufnahme: Bedienwissen zu **Docker auf Prod** lag
an 334 Stellen in 141 Dateien, zu **Traefik** an 454 Stellen in 141 Dateien, dazu 669
Stellen zum Server selbst. Nichts davon war ein Handbuch, alles waren Bruchstücke in
Projekt-`BUGS.md` und Memories von zwölf verschiedenen Projekten. Gemessen mit
`python ~/.claude/bin/handbuch-luecken.py`.

**Das Bedienbare steht oben, die Nachweise stehen unten.** Alles in den ersten Abschnitten
wurde am 11.08.2026 zwischen 14:08 und 14:22 gegen den echten Server ausgeführt, sofern
nicht ausdrücklich anders vermerkt.

Das Gegenstück ist [inventories/servers](../inventories/topics/servers.md): Dort steht,
**was** es gibt (Adressen, Zugänge, Tabellen). Hier steht, **wie** man es bedient.

---

## Der Zugang

```bash
ssh -o BatchMode=yes -o StrictHostKeyChecking=accept-new -i ~/.ssh/id_ed25519 root@128.140.40.235
```

**Immer aus Git-Bash, nie über PowerShell im Hintergrund.** Windows-OpenSSH führt ein
eigenes `known_hosts`; ein Hostkey-Prompt blockiert dann nicht-interaktiv und hängt ohne
jede Ausgabe. Einmal 107 Minuten gekostet [B: venfree, 27.06.2026].

**Ein Login, alle Aufgaben.** Vor dem Verbinden sammeln, was auf dem Server zu erledigen
ist, und alles in einem Lauf abarbeiten.

---

## Die fünf Handgriffe

### 1. Was läuft gerade

```bash
docker ps --filter "name=blue" --filter "name=green" --format "{{.Names}}\t{{.Status}}" | sort
docker ps -q | wc -l
```

Am 11.08.2026: **89 laufende Container**, davon 21 in Blue/Green-Slots, 8 gestoppte.

### 2. Welcher Slot ist aktiv

**Nie raten, nie dem Handoff glauben, nie fest eintippen.** Der aktive Slot wechselt bei
jedem Deploy, und er ist projektweise verschieden: Am 11.08.2026 standen 15 Projekte auf
`blue` und 6 auf `green`.

```bash
docker ps --filter "name=venfree-app" --format "{{.Names}}\t{{.Status}}"
```

Manche Projekte führen zusätzlich eine Slot-Datei, die ihr `deploy.sh` schreibt:

```bash
cat /opt/maxone-v2/.active-slot     # -> green
```

**Die Datei ist die Absicht, `docker ps` ist die Wahrheit.** Bei Abweichung gewinnt
`docker ps`. Am 11.08.2026 stimmten beide überein.

### 3. Deployen

**Der Build läuft nie auf diesem Server.** Er hat 7,6 GB Speicher, davon waren am
11.08.2026 nur 1,6 GB verfügbar; ein Next.js-Build zieht 4 bis 8 GB und reißt alle anderen
Container mit. Elf OOM-Ereignisse stehen im Kernel-Log.

Der Pfad, in dieser Reihenfolge (aus den vorhandenen `deploy.sh` und der venfree-Historie
übernommen, in diesem Lauf **nicht** ausgeführt, weil ein echter Deploy dazu nötig wäre):

```bash
# 1. lokal bauen, mit allen Build-Args, sonst sind sie im Image leer
docker build --build-arg BUILD_ID="$(git rev-parse --short HEAD)" -t <projekt>-app:latest .

# 2. transferieren
docker save <projekt>-app:latest | gzip | \
  ssh -i ~/.ssh/id_ed25519 root@128.140.40.235 "gunzip | docker load"

# 3. auf dem Server: Blue/Green über das projekteigene Skript
ssh -i ~/.ssh/id_ed25519 root@128.140.40.235 "cd /opt/<projekt> && bash deploy.sh"

# 4. Pflicht danach, siehe Handgriff 4
ssh ... "/usr/local/bin/traefik-probe-fix.sh https://<domain>/"
```

**Docker Desktop baut anders als Prod.** Der lokale Rechner nutzt den containerd-Store und
erzeugt OCI-Manifest-Listen mit Attestations; Prod läuft Docker 27 mit klassischem
overlay2-Store und lädt die nicht sauber. Deshalb einmal flach re-exportieren:

```bash
docker buildx build --provenance=false --sbom=false --platform linux/amd64 --load -t <projekt>-app:latest .
```

Was ein `deploy.sh` tun muss, steht in Standard 001 und ist in `/opt/maxone-v2/deploy.sh`
vorbildlich umgesetzt: Slot ermitteln, neuen Slot hochfahren, auf `healthy` warten (Timeout
60 s), **alle öffentlichen Routen prewarmen**, erst dann umschalten, alten Slot `stop` **und**
`rm`. Das `rm` ist nicht kosmetisch: Bleibt der alte Slot nur gestoppt, routet Traefik nach
einem Re-Up auf beide gleichzeitig, und die Domain antwortet zufällig mal alt, mal neu
[B: maxone.one BUGS.md, 06.05.2026].

### 4. Wenn eine Seite nicht antwortet

**Zuerst dieser eine Befehl, bevor irgendetwas anderes untersucht wird.** In 95 Prozent der
Fälle ist es der Traefik-Backend-Cache: Der Container hat beim Recreate eine neue IP
bekommen, Traefik hält die alte. Der TLS-Handshake klappt dann, der HTTP-Stream öffnet, und
die Antwort kommt nie.

```bash
ssh ... "/usr/local/bin/traefik-probe-fix.sh https://venfree.de/ https://www.venfree.de/"
```

Das Skript probt jede URL, und **nur bei 000, 502 oder 504** startet es Traefik neu und probt
danach erneut. Es ist damit gefahrlos aufzurufen, auch wenn alles gesund ist. Bestätigte
Fälle: slf-kong am 27.04. und 06.05.2026, vector-blue am 19.04.2026.

**Direkt nach einem Slot-Wechsel kann `curl -I` (HEAD) 502 zeigen, während `curl` (GET) 200
liefert.** Erst beides prüfen, dann urteilen.

Ein zweiter Wächter tut dasselbe von außen und ungefragt: `watchdog-healer` auf
maxone-watchdog (167.235.226.129) probt acht öffentliche Adressen alle 30 Sekunden und
startet Traefik nach zwei aufeinanderfolgenden Fehlschlägen selbst neu, mit 600 Sekunden
Sperrfrist und Telegram-Meldung. Sein SSH-Schlüssel darf auf maxone-prod nichts außer genau
diesem Neustart.

### 5. Wenn die Platte voll läuft

```bash
df -h /                                    # am 11.08.2026: 101G von 150G, 70 Prozent
docker builder prune -af                   # NIE mit --until=, das war die Ursache 18.05.2026
docker image prune -a --filter "until=72h" --force
```

Zwei Wächter laufen bereits von selbst: `/opt/_ops/docker-cleanup.sh` alle vier Stunden per
`/etc/cron.d/docker-cleanup`, und `/opt/disk-guard.sh` alle zehn Minuten, der ab 80 Prozent
Belegung von sich aus aufräumt. Beide am 11.08.2026 vorhanden und eingetragen.

---

## Die Landkarte

### Es gibt ZWEI Traefik-Netze, und das ist kein Fehler

| Netz | angelegt | Container | wer hängt drin |
|---|---|---|---|
| `coolify` | 06.02.2026 | 31 | die Altbestände: Supabase-Stacks, Stalwart, vector, slf, viktoria, zentinel |
| `maxone-public` | 05.07.2026 | 37 | alles Neuere: die vier maxone-Domains, venfree, snapflow, repivot, n8n, vaultwarden |

**Traefik hängt in beiden.** Ein Container wird nur gefunden, wenn er im selben Netz liegt
wie Traefik **und** sein Label `traefik.docker.network` genau dieses Netz nennt. Am
11.08.2026 labelten 23 Container `coolify` und 25 `maxone-public`.

**Für ein neues Projekt ist `maxone-public` das richtige Netz.** Der Name `coolify` stammt
von einer Plattform, die längst abgeschafft ist, und wird nur noch aus Bestandsgründen
geführt.

> **OFFENER BEFUND vom 11.08.2026, gemeldet an maxone.one:**
> `/opt/traefik/docker-compose.yml` kennt **nur `coolify`**. Die Verbindung zu
> `maxone-public` besteht ausschließlich am laufenden Container und ist nirgends
> festgeschrieben. Ein `docker compose up -d --force-recreate` in `/opt/traefik` erzeugt
> deshalb einen Traefik, der 25 Dienste nicht mehr sieht, darunter venfree.de, alle vier
> maxone-Domains, snapflow, stadtpunkt, vaultwarden und karastelev. **Vor jedem Anfassen
> von Traefik zuerst prüfen**, ob die Compose-Datei inzwischen beide Netze führt:
> ```bash
> grep -c maxone-public /opt/traefik/docker-compose.yml    # 0 heisst: die Falle steht noch
> ```

### Wo was liegt

| Was | Ort |
|---|---|
| Projekt-Stacks | `/opt/<projekt>/docker-compose.yml`, dazu `deploy.sh` (20 Projekte haben eins) |
| Secrets | `/opt/secrets/<projekt>/keys.env`, global `/opt/secrets/global/` |
| Traefik | `/opt/traefik/`, statische Konfiguration in der Compose-Kommandozeile, dynamische unter `dynamic/` mit `watch=true` |
| Zertifikate | `/opt/traefik/acme.json`, 1,2 MB, letzte Änderung 07.08.2026 |
| Helfer | `/usr/local/bin/traefik-probe-fix.sh`, `/usr/local/bin/watchdog-restart-traefik.sh` |
| Aufräumer | `/opt/disk-guard.sh`, `/opt/_ops/docker-cleanup.sh` (Symlink ins vector-Repo) |

**Der Verzeichnisname ist nicht der Projektname.** Bei venfree liegt die App in
`/opt/venfree/`, während `/opt/vanfree/` nur den Datenbank-Stack hält. Wer die Pfade aus
einem alten Handoff übernimmt, deployt ins Leere.

### Wie Traefik konfiguriert ist

Feste Punkte aus der laufenden Kommandozeile [B: `/opt/traefik/docker-compose.yml`, gelesen
11.08.2026]: Weiterleitung von HTTP auf HTTPS auf Ebene des Einstiegspunkts, HTTP/3 aktiv,
`security-headers@file` als Middleware auf allen HTTPS-Verkehr, Zertifikate über
**DNS-01 bei INWX** (`certificatesresolvers.letsencrypt`), Docker-Anbieter mit
`exposedbydefault=false`, Dashboard und API abgeschaltet, Speichergrenze 256 MB.

`exposedbydefault=false` heißt: **ohne `traefik.enable=true` am Container passiert nichts.**

---

## Bekannte Fehlerbilder

| Symptom | Ursache | Handgriff |
|---|---|---|
| TLS klappt, GET läuft ins Leere, curl-Timeout | Traefik hält die alte Container-IP | `traefik-probe-fix.sh <url>` |
| Alles 404, Traefik meldet sich gesund | Traefik zu alt für die Docker-API (v3.3 spricht 1.24, Docker 29 verlangt 1.40) | Traefik auf v3.6 oder neuer. `DOCKER_API_VERSION` als Umgebungsvariable hilft **nicht**, Traefik setzt sie selbst |
| Eine Domain antwortet abwechselnd alt und neu | alter Slot nur gestoppt statt entfernt, Traefik routet auf beide | alten Slot `docker rm`, im `deploy.sh` `stop` **und** `rm` |
| Erster Besucher sieht eine Sekunden lange weiße Seite | kein Prewarm vor dem Umschalten | `deploy.sh` um den Prewarm-Block ergänzen (Standard 001 D) |
| Healthcheck schlägt fehl, CI rollt gesunden Container zurück | Healthcheck zeigt auf eine SSR-Seite, die länger braucht als das Timeout | Endpunkt auf `/api/health` oder `/api/version` legen, nie auf `/` |
| Container startet, stirbt, startet | abgelaufenes Zertifikat oder fehlende Umgebungsvariable im Startpfad | `docker logs <container> --tail 50`, dann Zertifikat und `env_file` prüfen |
| Build bricht ab oder der Server wird langsam | jemand baut auf Prod | sofort abbrechen, lokal bauen, `docker save \| ssh \| docker load` |
| Platte voll, alles antwortet nicht mehr | BuildKit-Cache eines self-hosted Runners | `docker builder prune -af` ohne `--until=` |
| Container mit Exit-Code 137 | vom Kernel wegen Speichermangel getötet | `mem_limit:` im Compose setzen, Ursache im Speicherverbrauch suchen |

**Diagnose in dieser Reihenfolge**, weil jede Stufe billiger ist als die nächste:

```bash
/usr/local/bin/traefik-probe-fix.sh https://<domain>/   # 1. der Standardfall
docker ps --filter "name=<projekt>"                     # 2. läuft der Slot überhaupt
docker logs traefik --since 1h 2>&1 | grep -iE "error"  # 3. sagt Traefik etwas
docker logs <container> --tail 50                       # 4. sagt die Anwendung etwas
free -h; df -h /                                        # 5. ist die Maschine am Ende
```

Am 11.08.2026 meldete Traefik in der letzten Stunde **null** Fehlerzeilen.

---

## Die Grenzen, die nicht verhandelt werden

1. **Kein Build auf Prod.** Kein `docker build`, kein `docker compose up --build`, kein
   `npm run build`. Das schließt den self-hosted Runner ein, der auf derselben Maschine
   lebt.
2. **Kein `docker run`.** Immer `docker compose`, sonst entsteht ein Container ohne
   `restart:`, der den nächsten Neustart nicht überlebt. Der Stalwart-Vorfall vom
   24.03.2026 ist genau das.
3. **Rückfragepflicht bei Datenbank-Migration, Schema-Änderung und Secret-Rotation.**
   Zero-Downtime-Deploys darf ich eigenständig fahren.
4. **Nach jedem Recreate die Traefik-Probe**, ohne Ausnahme.
5. **Nichts von Hand am laufenden Container ändern**, was nicht in der Compose-Datei steht.
   Der Netz-Befund oben zeigt, was daraus wird: ein Zustand, der beim nächsten regulären
   Befehl lautlos verschwindet.
6. **Der Hetzner-Altpreis darf nicht verspielt werden.** Kein Rescale in irgendeine
   Richtung, auch nicht für eine Lastspitze. Stattdessen einen zweiten Server danebenstellen.

---

## Nachweise

Alles Folgende wurde am 11.08.2026 zwischen 14:08 und 14:22 auf maxone-prod ausgeführt.

| Was | Ergebnis |
|---|---|
| `hostname`, `uptime` | maxone-prod, 14 Tage 19 Stunden |
| `docker --version` | 27.0.3 (build 7d4bcd8) |
| `docker compose version` | v5.0.2 |
| Traefik-Abbild und Zustand | `traefik:v3.6`, laufend seit 27.07.2026 16:54 UTC |
| `docker ps -q \| wc -l` | 89 laufend, 8 beendet |
| Blue/Green-Slots | 21, davon 15 blue und 6 green |
| `df -h /` | 150 GB, 101 GB belegt, 70 Prozent |
| `free -h` | 7,6 GB gesamt, 1,6 GB verfügbar |
| OOM-Ereignisse im Kernel-Log | 11 |
| Netz `coolify` | angelegt 06.02.2026, 31 Container |
| Netz `maxone-public` | angelegt 05.07.2026, 37 Container |
| `grep -c maxone-public /opt/traefik/docker-compose.yml` | **0** (der offene Befund oben) |
| Traefik-Fehlerzeilen der letzten Stunde | 0 |
| `/usr/local/bin/traefik-probe-fix.sh` | vorhanden, 741 Bytes, 06.05.2026 |
| `/opt/disk-guard.sh`, `/opt/_ops/docker-cleanup.sh` | beide vorhanden und im Cron eingetragen |
| `deploy.sh`-Bestand unter `/opt/*/` | 20 Projekte |

**Nicht in diesem Lauf ausgeführt und darum als übernommen gekennzeichnet:** der
Deploy-Pfad selbst (Handgriff 3), weil er ein echtes Deploy voraussetzt. Seine Quellen sind
Standard 001, `/opt/maxone-v2/deploy.sh` (gelesen), die venfree-Deploy-Memory vom 27.06.2026
und die Stadt-Lahn-Flow-Memory zum lokalen Bauen.

### Woher das verstreute Wissen kam

Zusammengezogen aus: Standard 001 (Deploy) und 015 (Container Safety),
`memory/reference-traefik-braucht-neue-docker-api.md`,
`stadt-lahn-flow/feedback_traefik_backend_cache.md` und `reference_traefik_auto_heal.md`,
`venfree/reference_manual_deploy_path.md`, `stadt-lahn-flow/workflow_local_docker_deploy.md`,
den `BUGS.md` von voltfair.de (35 Traefik-Stellen), maxone.one (16) und Zentinel, sowie der
laufenden Maschine selbst.

**Zwei Widersprüche, die dabei aufgefallen sind:**

1. **Standard 001 D nennt im Warmup-Muster das Netz `coolify` fest** (`docker network
   disconnect coolify …`). Für die 25 Dienste an `maxone-public` ist das falsch und würde
   wirkungslos durchlaufen. Der Netzname gehört als Variable ins `deploy.sh`, nicht fest in
   die Anleitung. Gemeldet, nicht eigenmächtig geändert, weil der Standard maxone.one gehört.
2. **`venfree/reference_manual_deploy_path.md` beschreibt oben einen Build auf der
   Runner-Box** und korrigiert sich erst im Nachtrag vom 27.06.2026 selbst auf „lokal bauen".
   Wer nur den oberen Teil liest, baut auf Prod. Hier gilt ausschließlich der Nachtrag.
