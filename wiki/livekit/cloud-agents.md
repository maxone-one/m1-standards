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

## LKC-11: `lk agent versions` nennt den Git-Commit, `status` nennt ihn nicht

**Die Frage „welcher Code spricht gerade mit Anrufern" beantwortet `status` nicht.** Er
zeigt eine Plattform-Kennung wie `xX8rvRwdMnKA`, und die sagt nichts darüber, welcher
Commit darin steckt. `versions` zeigt dieselbe Kennung **mit** einer Attributspalte:

```
Version        Production  Attributes
xX8rvRwdMnKA   ✓           {"git_branch":"main","git_commit":"8f7ff95"}
rqq3dqpxgxaT   --          {"git_branch":"main","git_commit":"ccd79d5"}
```

**Damit wird aus einer Vermutung eine Messung.** Ob ein bestimmter Fix draußen ist,
beantwortet danach `git merge-base --is-ancestor <fix> <git_commit>`, und der Rückstand
`git diff --name-only <git_commit>..HEAD -- <pfade>`.

**Warum das mehr ist als Bequemlichkeit.** Am 25.08.2026 lagen 16 Commits zwischen dem
laufenden Agenten und `HEAD`, und die Zahl las sich wie ein großer Rückstand. Unter
`agent/`, `ansagen/` und `kalender/` hatte sich davon **nichts** geändert: Der Agent war
aktuell. **Ohne die Zuordnung Version zu Commit lässt sich das nicht einmal fragen**,
und die naheliegende Ersatzrechnung über Zeitstempel führt in die Irre, weil `Deployed
At` in UTC steht und die Commit-Zeit in Ortszeit.

## LKC-12: Auf dem Build-Tarif kostet der erste Anruf 10 bis 20 Sekunden

**Produktionsagenten skalieren dort nach dem Ende aller Sitzungen auf null Repliken
herunter**, der Status heißt dann `Sleeping`. Der nächste eingehende Job weckt sie, und
das „adds 10 to 20 seconds before the agent joins the room"
`[B: docs.livekit.io/deploy/agents/managing-deployments/, gelesen 25.08.2026]`. **Auf
Ship und Scale bleiben Produktionsagenten warm**, nicht-produktive Deployments dagegen
schlafen auf jedem Tarif ein.

**Einen Schalter dagegen gibt es nicht.** Weder `lk agent update` noch `lk agent create`
kennen ein Flag für Mindest-Repliken, und `livekit.toml` trägt nur Subdomain und
Agent-Kennung. Es ist eine Tarifeigenschaft, keine Einstellung.

**Für Telefonie ist das der teuerste Satz auf dieser Seite.** Am 25.08.2026 in Vera
gemessen: kalt über 20,8 Sekunden bis zum Erscheinen, warm 1,4 Sekunden, dieselbe
Anmeldung und dasselbe Werkzeug. **Eine Erreichbarkeitsprobe mit 20 Sekunden Frist
meldet auf diesem Tarif also „tot" für einen gesunden Dienst.** Wer so eine Probe baut,
gibt ihr entweder mehr Frist oder liest `status` daneben: Steht dort nach dem
Fehlschlag `Running`, hat die Probe geweckt statt gemessen.

## Fehlerseiten, damit sie niemand ein zweites Mal aufruft

| Adresse | Antwort | Stattdessen |
|---|---|---|
| `docs.livekit.io/agents/ops/deployment/deploying/` | HTTP 404 | `…/deployment/builds/` für Dockerfile-Anforderungen |
| `docs.livekit.io/agents/ops/deployment/custom/` | 200, aber nur Selbst-Hosting | trägt nichts zu `lk agent`, `livekit.toml` oder Dispatch bei |

Beide am 19.08.2026 abgerufen, die erste geraten aus der Übersichtsseite.
