# LiveKit Cloud Agents: einen Agenten dort betreiben, wo LiveKit ist

Gemessen am 19.08.2026 beim Umzug von Veras Agent von einem eigenen Hetzner-Host zu
LiveKit Cloud, CLI `lk` 2.18.2, Paket `livekit-agents` 1.6.10. Jede Regel hier ist am
laufenden System belegt, nicht aus einem Blog.

## LKC-01: Ein fertiges Abbild hochzuladen geht nur im Enterprise-Tarif

`lk agent create --image meinabbild:tag` und `--image-tar` existieren, sind aber laut
Doku dem Enterprise-Tarif vorbehalten
`[B: docs.livekit.io/agents/ops/deployment/builds/, gelesen 19.08.2026]`. Auf dem
Build-Tarif **baut LiveKit selbst**, aus dem Dockerfile im übergebenen Arbeitsverzeichnis.

**Für Häuser mit der Regel „Build immer lokal" ist das kein Bruch**, sondern ein anderer
Fall: Die Regel zielt darauf, nicht auf dem eigenen Produktionsserver zu bauen. Hier baut
der Anbieter sein eigenes Laufzeitartefakt, und daran führt kein Weg vorbei.

## LKC-02: Das Dockerfile muss in der Wurzel des Arbeitsverzeichnisses liegen

`lk agent create [working-dir]` sucht dort `Dockerfile`. **Einen Pfad dafür kennt die CLI
nicht** (`lk agent create --help`, 2.18.2). Wer sein Abbild sonst unter `deploy/` führt,
braucht eine zweite Datei in der Wurzel.

Die Doku verlangt dabei ausdrücklich einen **festen `CMD`, der den Agenten direkt
startet**, ohne Wrapper und ohne Hintergrundstart, plus einen unprivilegierten Nutzer und
keine Zugangsdaten im Abbild. Ein `CMD`, das etwas anderes startet (etwa einen
Web-Zugang aus demselben Repo), fällt nicht auf: Der Container läuft, nur registriert sich
nie ein Worker.

## LKC-03: `--region` ist im nicht-interaktiven Lauf Pflicht

Ohne Angabe fragt die CLI nach; mit `-y` bricht sie ab und nennt die Auswahl:
**`us-east`, `eu-central`, `ap-south`** `[B: eigener Lauf, 19.08.2026]`. Für deutsche
Anrufer ist `eu-central` die Wahl, und sie gehört zur Datenbank passend gelegt.

## LKC-04: Zugangsdaten kommen über `--secrets-file`, eine Zeile je `KEY=VALUE`

```bash
lk agent create --region eu-central --secrets-file /pfad/geheim.env -y .
lk agent deploy --secrets-file /pfad/geheim.env .
```

Die Datei wird **nicht** von einer Shell gelesen, ein `&` im Wert (typisch für
Postgres-DSNs mit Verbindungsparametern) ist also unkritisch. Genau das ist beim Sourcen
in einer Shell die klassische Falle: Der Wert bricht am `&` ab, die Variable bleibt leer,
und es gibt keinen Fehler.

## LKC-05: Der Agentenname entscheidet, ob überhaupt ein Anruf ankommt, und er kommt aus dem Code

**Das ist die Stelle, an der ein Umzug lautlos scheitert.** Ein Worker, der sich ohne
`agent_name` registriert, wird von einer Dispatch-Regel automatisch in **jeden** neuen
Raum geholt. Ein Worker mit Namen braucht expliziten Dispatch, und eine Regel ohne
Agent-Eintrag holt ihn nie.

**Gemessen: Der Cloud-Agent übernimmt, was der Code sagt.** Bei einem Agenten, der über
`@server.rtc_session()` ohne Namen läuft, steht im Log des Deployments
`"registered worker", "agent_name": ""` `[B: lk agent logs, 19.08.2026]`. Das Deployment
selbst zwingt keinen Namen auf.

**Der billige Gegentest, ohne Telefon und ohne Anrufer:**

```bash
lk room create pruefung-dispatch
lk room participants list pruefung-dispatch    # -> agent-AJ_… (ACTIVE)
lk room delete pruefung-dispatch
```

Steht der Agent binnen Sekunden im Raum, greift der automatische Dispatch. Kostet eine
angefangene Agent-Session-Minute und erzeugt ein Gesprächsprotokoll, weil der Agent seine
Begrüßung spricht.

> **Korrektur vom 19.08.2026, 17:5x: So allein reicht der Gegentest nicht.** Bei einer
> Wiederholung blieb der Agent aus, und im Log stand dafür **kein** `received job
> request`, während beim echten Anruf derselben Stunde genau diese Zeile stand. **Ein
> leerer Raum löst keinen Job aus, der Beitritt eines Teilnehmers tut es.** Die Doku sagt
> dazu nichts: „When `agent_name` is not set, an agent is automatically dispatched to each
> new room" nennt kein Ereignis `[B: docs.livekit.io/agents/worker/agent-dispatch/,
> gelesen 19.08.2026]`.
>
> **Der belastbare Gegentest tritt deshalb selbst bei**, mit einem Zugangstoken ohne
> Sende- und Empfangsrecht:
>
> ```python
> zugang = (api.AccessToken().with_identity("wache")
>           .with_grants(api.VideoGrants(room_join=True, room=raum,
>                                        can_publish=False, can_subscribe=False)).to_jwt())
> await rtc.Room().connect(wss_adresse, zugang)   # legt den Raum zugleich an
> ```
>
> So gemessen war der Agent nach **3,2 Sekunden** im Raum. Der Weg misst außerdem mehr:
> nicht nur, dass ein Worker registriert ist, sondern dass für einen neuen Raum wirklich
> ein **Job-Prozess** entsteht. Genau dort riss es am 19.08.2026 um 16:01, während jede
> andere Anzeige grün stand.

## LKC-10: Ein wiederkehrender Erreichbarkeitstest braucht einen eigenen Zweig im Agenten

Der Test aus LKC-05 ist als einmalige Probe gedacht. Wer ihn zur Wache macht, muss den
Agenten unterscheiden lassen, sonst bezahlt jede Messung mit einer Spur in den echten
Daten: In `vera` hat der Umzugstest ein Gesprächsprotokoll geschrieben, auf der
öffentlichen Testseite mitgezählt und eine gesprochene Begrüßung erzeugt, die niemand
gehört hat.

**Die Grenze gehört an den Raumnamen**, weil sie dann ohne mitgeführten Zustand
ablesbar ist: Ein Präfix (`wache-`) führt in einen Zweig, der **vor** dem Aufbau der
Session steht, `ctx.connect()` aufruft, ein paar Sekunden stehen bleibt und wieder geht.
Kein Sprachmodell, keine Stimme, keine Erkennung, keine Protokollierung. Umgekehrt gilt:
Ein Raum ohne lesbaren Namen ist **kein** Wachraum, sonst verliert ein echtes Gespräch im
Fehlerfall seine Aufzeichnung.

**Und der Zweig braucht `ctx.connect()` ausgeschrieben.** Ein Job betritt seinen Raum
nicht von selbst; die Verbindung hängt sonst an `session.start()`, das sie über die
Raum-Ein-/Ausgabe anstößt `[B: voice/agent_session.py:1044 und job.py:596, Paket 1.6.10]`.
Fehlt die Zeile, meldet die Wache „nicht erreichbar", obwohl der Job-Prozess einwandfrei
entstanden ist.

## LKC-06: `lk agent logs` folgt dem Strom und ist keine verlässliche Quelle

Der Befehl hat kein `--no-follow`; ohne `timeout` hängt er. Und er greift auf den
Container-Endpunkt der Cluster-Node durch, was fehlschlagen kann, ohne dass am Agenten
etwas ist:

```
failed to copy logs: failed to stream logs: Get "https://10.62.5.2:10250/containerLogs/…":
net/http: TLS handshake timeout
```

**Belegt am 19.08.2026**, während der Agent nachweislich lief. Wer den Zustand wissen
will, nimmt `lk agent status` (Replicas, CPU, Speicher, `Last Observed`) oder die eigene
Datenspur des Agenten, etwa seine Protokolltabelle. Für einen einmaligen Blick:

```bash
timeout 45 lk agent logs > logs.txt 2>&1
```

## LKC-07: `custom load_threshold is not supported when hosting on Cloud`

Eine gesetzte Lastschwelle im eigenen Code wird beim Cloud-Betrieb verworfen, mit genau
dieser Warnung beim Start. Kein Fehler: Die Kapazitätssteuerung übernimmt die Plattform.
Wer die Schwelle für einen eigenen Host gesetzt hat, lässt sie stehen, sie stört nicht.

## LKC-08: `lk` braucht kein Cloud-Login, aber dann die drei Werte am Aufruf

Ohne `lk cloud auth` meldet jeder Befehl `no projects configured`. Mit
`--url`, `--api-key` und `--api-secret` (oder denselben Namen als Umgebungsvariablen)
arbeitet die CLI vollständig, inklusive `agent create`, `deploy` und `status`. Das ist der
Weg für automatisierte Läufe ohne Browser-Anmeldung.

`lk agent create` legt dabei eine `livekit.toml` im Arbeitsverzeichnis an, die nur
`[project].subdomain` und `[agent].id` trägt. Sie gehört ins Repo, sie ist Architektur und
kein Geheimnis.

## LKC-09: Das Anlegen ist zugleich die Guthabenprobe

Der Build-Tarif blockiert bei leerem Guthaben, statt weiterzurechnen. Es gibt **keinen
Weg, den Kontostand über CLI oder API zu lesen**, nur die Kontoseite im Browser. **Der
Versuch selbst ist deshalb die belastbarste Messung**: Läuft `lk agent create` durch, war
Guthaben da. Am 19.08.2026 hat genau das eine Blockade aufgelöst, die einen halben Tag auf
das Ablesen einer Zahl gewartet hatte.

## Fehlerseiten, damit sie niemand ein zweites Mal aufruft

| Adresse | Antwort | Stattdessen |
|---|---|---|
| `docs.livekit.io/agents/ops/deployment/deploying/` | HTTP 404 | `…/deployment/builds/` für Dockerfile-Anforderungen |
| `docs.livekit.io/agents/ops/deployment/custom/` | 200, aber nur Selbst-Hosting | trägt nichts zu `lk agent`, `livekit.toml` oder Dispatch bei |

Beide am 19.08.2026 abgerufen, die erste geraten aus der Übersichtsseite.
