# LiveKit Agents: Bedienhandbuch

Angelegt am 18.08.2026 auf Max' Auftrag (TODO 12 im Projekt `vera`), wörtlich: „LiveKit ist ein
sehr großes Projekt mit sehr viel Bekanntheit und einer sehr großen Community. Ich frage mich
überhaupt, warum wir all diese Bugs gehabt haben." Die ehrliche Antwort steht unten unter
„Was uns das gekostet hat": drei von einundzwanzig Defekten in Vera hätte ein Blick hierher
verhindert, und es waren die teuersten.

**Gelesen wurde der installierte Quellcode von `livekit-agents 1.6.10`**, nicht ein Blog und
nicht ein Tutorial. Der Code ist die härteste Quelle, und er widerspricht der Doku an mehreren
Stellen, weil die Doku älter ist.

**Das Bedienbare steht oben, die Nachweise stehen unten.**

## Das Wichtigste in drei Sätzen

Ein Werkzeug bekommt als erstes Argument einen `RunContext`, und dieser Kontext ist kein
Beiwerk, sondern trägt fast alles, was man sonst von Hand nachbaut: Sitzungsgedächtnis,
Wartesignal, Zwischenmeldung und den Schutz vor Unterbrechung. Wird der Agent unterbrochen,
während ein Werkzeug läuft, dann **verschluckt das Framework die Folgeantwort** und der
Anrufer hört Stille. Und was der Agent im selben Zug sagt, in dem er ein Werkzeug aufruft,
ist für das Modell in der nächsten Runde nur bedingt vorhanden.

## Der `RunContext`, das meistübersehene Bauteil

Jedes `@function_tool` bekommt ihn und die meisten Projekte nutzen nur den Namen.

| Was | Wofür | Warum man es sonst falsch baut |
|---|---|---|
| `context.userdata` | Sitzungsgedächtnis über mehrere Werkzeugaufrufe hinweg | Sonst muss das Modell Maschinenwerte aus seinen eigenen gesprochenen Sätzen rekonstruieren, und dabei rät es |
| `context.disallow_interruptions()` | Sperrt die Unterbrechung für genau diesen Aufruf | **Der einzige harte Schutz gegen die verschluckte Folgeantwort**, siehe unten |
| `context.with_filler(...)` | Sagt etwas, während das Werkzeug rechnet | Ein Wartesignal muss nicht gebaut werden, es ist da |
| `context.update(...)` | Zwischenmeldung mitten im Werkzeug, das Modell bekommt das Wort zurück | Sonst schweigt der Agent, bis das Werkzeug ganz fertig ist |
| `context.wait_for_playout()` | Wartet, bis der Satz vor diesem Werkzeug zu Ende gesprochen ist | |
| `context.foreground()` | Hält das Wort, während interaktive Arbeit läuft | |

`userdata` wird an der Sitzung gesetzt und ist typisiert:

```python
session = AgentSession[MeinZustand](userdata=MeinZustand(), ...)

@function_tool
async def werkzeug(context: RunContext[MeinZustand]) -> str:
    context.userdata.zuletzt_angeboten = [...]   # überlebt bis zum nächsten Aufruf
```

Ohne `userdata=` am Konstruktor wirft der Zugriff `ValueError: AgentSession userdata is not set`.
Ein Modul-global wäre der naheliegende Irrweg und ist falsch, sobald zwei Gespräche gleichzeitig
laufen.

## Die Stille nach dem Werkzeug, und warum sie kein Fehler von uns war

**Das Fehlerbild:** Der Agent kündigt etwas an („Moment, ich schaue nach"), das Werkzeug läuft
durch und liefert sein Ergebnis, und dann sagt der Agent nichts mehr. Keine Fehlermeldung, keine
Latenz, einfach Stille, bis der Mensch von sich aus wieder spricht.

**Die Wurzel steht wörtlich im Framework**, `voice/agent_activity.py` in 1.6.10:

```python
if speech_handle.interrupted:
    await utils.aio.cancel_and_wait(exe_task)
    # ... Ergebnisse werden gesichert ...
    return                       # <- und hier ist die Antwort weg

# und weiter unten:
if fnc_executed_ev._reply_required and not speech_handle.interrupted:
    ...   # nur hier entsteht die Folgeantwort
```

Wird der Sprechvorgang unterbrochen, während das Werkzeug läuft, sichert das Framework das
Ergebnis brav in den Verlauf und **erzeugt keine Antwort daraus**. Das Ergebnis liegt fertig
vor und wird nie ausgesprochen.

**Woran man es im Protokoll erkennt, ohne zu raten:** Der Agentenzustand geht nach dem
Werkzeugstart auf `listening` statt auf `thinking`. Der Code entscheidet das eine Zeile vorher
an derselben Bedingung. Steht dort `listening`, war es eine Unterbrechung.

**Warum das am Telefon dauernd passiert:** Die Voreinstellung ist `min_duration: 0.5` Sekunden
und `min_words: 0`. Ein halbsekündiges Geräusch ohne ein einziges erkanntes Wort reicht also,
um den Agenten zu unterbrechen. Am Telefon, mit Leitungsrauschen und Nebengeräuschen, ist das
viel zu empfindlich.

**Die drei Gegenmittel, in dieser Reihenfolge:**

1. `context.disallow_interruptions()` als erste Zeile jedes Werkzeugs, dessen Ergebnis
   ausgesprochen werden muss. Das ist der harte Riegel.
2. `interruption: {"min_words": 2}` in `turn_handling`, damit ein Geräusch keine Unterbrechung
   mehr ist, ein echter Einwurf aber schon.
3. Auf das Ereignis `agent_false_interruption` hören. Es trägt `resumed: bool`; steht dort
   `False`, ist der Agent verstummt und kommt von allein nicht zurück. Das ist der Rettungsanker,
   an dem ein `generate_reply()` gehört.

## Die Optionen, die man kennen muss

Alles Alte (`min_interruption_duration`, `resume_false_interruption`, `min_endpointing_delay`,
`preemptive_generation`, `turn_detection` als eigene Argumente) ist seit 1.6 **veraltet** und
gehört in ein einziges `turn_handling`. Wer die alten Namen benutzt, bekommt eine Warnung und
nicht immer das erwartete Verhalten.

```python
AgentSession(
    turn_handling={
        "endpointing": {"min_delay": 0.5, "max_delay": 3.0},
        "interruption": {"min_words": 2, "min_duration": 0.5},
        "preemptive_generation": {"enabled": True},
    },
    max_tool_steps=3,
)
```

Die Voreinstellungen, gelesen in `voice/turn.py`:

| Einstellung | Vorgabe | Bemerkung |
|---|---|---|
| `interruption.min_duration` | 0,5 s | am Telefon zu empfindlich |
| `interruption.min_words` | 0 | **kein Wort nötig**, reines Stimmsignal genügt |
| `interruption.resume_false_interruption` | `True` | nimmt den Satz wieder auf, nicht aber die Werkzeugantwort |
| `interruption.false_interruption_timeout` | 2,0 s | |
| `interruption.backchannel_boundary` | (1,0, 1,0) | „mhm" am Satzanfang und Satzende unterdrückt |
| `endpointing.min_delay` | 0,5 s | |
| `preemptive_generation.enabled` | `True` | rechnet vor, bevor der Zug bestätigt ist |
| `max_tool_steps` | 3 | danach erzwungen `tool_choice="none"` |

## Was ein Werkzeug zurückgeben darf

Der Rückgabewert ist eine **Meldung an das Modell**, kein Text für den Menschen. Wer dort einen
blanken Satz zurückgibt, bekommt genau den Fehler, der Vera am 17.08.2026 einen Termin
bestätigen ließ, den es nicht gab: Ein erfolgreicher Rücklauf sieht dann aus wie ein
erfolgreicher Vorgang. **Jede Rückgabe nennt zuerst den Zustand, dann erst den Satz.**

Zwei Ausnahmen für Fehlerfälle:

- `raise ToolError("...")` gibt dem Modell den Text als Fehlerkontext, es darf darauf antworten.
- `raise StopResponse()` beendet den Zug ohne jede Antwort. Nur nehmen, wenn Schweigen richtig
  ist.

Es gilt weiter: `reply_required` wird auf `fnc_out is not None` gesetzt. Ein Werkzeug, das `None`
zurückgibt, löst also **nie** eine Folgeantwort aus.

## Der Ton während des Nachdenkens

Der `BackgroundAudioPlayer` bringt fertige Schleifen mit, unter anderem `HOLD_MUSIC`,
`KEYBOARD_TYPING` und drei Raumklänge. Für ein Wartesignal während eines langsamen Werkzeugs ist
aber `context.with_filler(...)` das genauere Mittel, denn es feuert erst, wenn die Sitzung
wirklich `delay` Sekunden still war, und `interval=None` sorgt dafür, dass es höchstens einmal
kommt.

```python
async with context.with_filler("Einen Moment, ich sehe im Kalender nach.", delay=1.5):
    ergebnis = await langsame_arbeit()
```

Der entscheidende Unterschied zu einer Ankündigung durch das Modell: Dieser Satz kommt aus dem
Code, er kommt nur wenn es wirklich dauert, und er kann nicht dazu führen, dass das Modell
seinen Zug nach der Ankündigung für beendet hält.

## Zwei Regeln über das Werkzeug hinaus, beide am 19.08.2026 teuer gelernt

**Ein Werkzeug ohne Argumente kann keine Frage beantworten, die Argumente braucht, und das
Modell erfindet dann die Antwort.** In Vera nahm `termine_vorschlagen` keine Parameter, es
lieferte immer nur die nächsten zwei freien Plätze. Nannte ein Anrufer selbst einen
Zeitpunkt, gab es keinen Weg, ihn zu prüfen. Das Modell hat daraufhin fünfmal „Moment, ich
schau mal kurz nach" gesagt, kein Werkzeug aufgerufen und fünfmal eine Absage erfunden.

Der Fehler sieht im Protokoll aus wie eine Prompt-Schwäche und ist keine. **Prüfsatz: Wenn
das Modell etwas behauptet, was ein Werkzeug messen müsste, sieh zuerst nach, ob es dafür
überhaupt ein Werkzeug mit den nötigen Argumenten gibt.** Ein Prompt-Satz behebt eine
fehlende Fähigkeit nie, er verlagert die Erfindung nur an eine andere Stelle.

**Ein Systemprompt muss den heutigen Tag nennen, sonst ist jede relative Zeitangabe
geraten.** Das Sprachmodell kennt das Datum nicht, und keine der Bibliotheken setzt es von
sich aus ein. Ohne diese Zeile kann es „morgen", „Freitag" oder „nächste Woche" nicht in
ein Datum auflösen und damit auch kein Werkzeug damit aufrufen. In Vera stand der
Systemprompt drei Tage lang vollständig statisch da, und zwei Defekte hingen daran.

Der Prompt wird deshalb je Gespräch gebaut, nicht einmal als Konstante:

```python
def systemprompt(jetzt: datetime) -> str:
    return f"Heute ist {tag_als_text(jetzt.date())}.\n{SYSTEMPROMPT}"
```

Der Zeitpunkt wird **übergeben und nicht in der Funktion geholt**, sonst ist der Prompt nur
an dem Tag prüfbar, an dem der Test gerade läuft.

**Und wenn das Modell doch einen Zeitpunkt bilden muss, gib ihm kein Feld für eine
Zeitzone.** Ein ISO-Zeitstempel als Werkzeugargument lädt den Fehler ein: In Vera schrieb
das Modell `2026-08-20T13:00:00Z`, also die Ortszeit als UTC, und der Anrufer bekam einen
Termin zwei Stunden später. Zwei getrennte Felder für Datum und Uhrzeit, beide festgelegt
als Ortszeit, machen denselben Fehler bauartbedingt unmöglich.

## Wer anruft: die Nummer des SIP-Anrufers

**Das SDK kennt sie nicht, der Server setzt sie**, deshalb findet ein Grep über das Paket
keinen einzigen SIP-Attributnamen. Erkannt wird der Anrufer an
`rtc.ParticipantKind.PARTICIPANT_KIND_SIP`, die Nummer steht in seinen `attributes` und
zusätzlich im Raumnamen. **Jede Quelle wird gegen dieselbe Plausibilitätsprüfung gehalten,
keine wird geraten**, und liefert keine etwas, ist None die richtige Antwort statt eines
Näherungswerts.

Ausführlich, mit Code und dem Prüfsatz gegen die nie verdrahtete Prüfung:
[`sip-anrufer.md`](sip-anrufer.md).

## Den Agenten bei LiveKit Cloud betreiben statt auf eigenem Blech

Zehn Regeln zum Deployen mit `lk agent create` und `lk agent deploy`, gemessen am
19.08.2026 beim Umzug von Veras Agent: warum LiveKit selbst baut (ein fertiges Abbild
darf nur Enterprise hochladen), wo das Dockerfile liegen muss, wie Zugangsdaten
hereinkommen, und **die eine Stelle, an der ein Umzug lautlos scheitert**, nämlich der
Agentenname und der automatische Dispatch. Dazu zwei Fehlerseiten der offiziellen Doku
und der Gegentest ohne Telefon: **Er muss dem Raum selbst beitreten**, denn ein leerer
Raum löst keinen Job aus, und als wiederkehrende Wache braucht er einen eigenen Zweig im
Agenten (LKC-10), sonst schreibt jede Messung in die echten Daten.

[`cloud-agents.md`](cloud-agents.md).

## Fünf Regeln zu Ton, Unterbrechung und eingehendem SIP

> Die Überschrift hieß bis zum 23.08.2026 „Zwei Regeln zum Testen mit echtem Ton", da
> standen aber längst vier darunter. Eine Zählung in einer Überschrift altert mit jedem
> Zusatz und stimmt genau bis zum nächsten.

### LK-20 — Das eingebaute Test-Framework kennt keinen Ton, für Audio gibt es `lk room join --publish`
`AgentSession`-Tests laufen **ausdrücklich im Textmodus** („The test framework and agent
simulations both run in text mode"), und für die volle Audiokette verweist die Doku auf
Fremdanbieter (Bluejay, Cekura, Coval, Hamming). Wer eine Aufnahme durch die echte Kette
schicken will, braucht sie nicht: `lk room join --publish datei.ogg --exit-after-publish`
spielt eine Tonspur als Teilnehmer in einen Raum. Formate: `.ogg` (Opus), `.h264`, `.ivf`,
auch aus einem Socket.
*Lehre:* Vera, TODO 56. Die Messstrecke für Sprachverständlichkeit unter Lärm wäre sonst als
Eigenbau entstanden.

### LK-21 — Die adaptive Unterbrechungserkennung geht bei LiveKit Cloud VON SELBST an
`_resolve_interruption_detection()` schaltet den `AdaptiveInterruptionDetector` ein, sobald
`is_hosted()` gilt, und das prüft nur, ob `LIVEKIT_REMOTE_EOT_URL` gesetzt ist — LiveKit
Cloud setzt sie selbst. **Wer den Schalter als Lösung einbaut, legt womöglich einen um, der
längst steht.** Woran man es am Protokoll erkennt: Das Ereignis `overlapping_speech` samt
`total_duration` entsteht an genau einer Stelle im Paket, nämlich in diesem Erkenner, und
wird nur weitergereicht, wenn er aktiv ist. Voraussetzung sind eine STT mit
`aligned_transcript` und Streaming (Deepgram erfüllt beides) sowie eine VAD. Für Agenten bei
LiveKit Cloud ist der Dienst **gebührenfrei**, selbst gehostet 40.000 Anfragen im Monat. Die
Die eigentlichen Regler heißen `threshold` und `min_interruption_duration` (Vorgabe 50 ms),
**und über die Session sind sie nicht erreichbar**: `mode` ist ein
`Literal["adaptive","vad"]`, und `_resolve_interruption_detection()` baut den Detector ohne
ein einziges Argument. Nur `update_options()` auf der fertigen Instanz ändert sie.
*Lehre:* Vera, BUG-051. Der Erkenner lief die ganze Zeit, ohne in einer Zeile Code
vorzukommen. **Setz `mode` ausdrücklich** — nicht um ihn einzuschalten, sondern damit das
Verhalten dir gehört und nicht der Umgebung des Anbieters.

### LK-22 — `total_duration` im `overlapping_speech` ist eine LATENZ, keine Dauer
Wörtlich im Paket: „RTT (Round Trip Time) time taken to perform the inference"
(`inference/interruption.py:104`), gerechnet über den Zeitstempel, den der Client selbst
beim Absenden in den 8-Byte-Kopf packt. Werte um 30 bis 60 ms sind eine **gute
Antwortzeit** und sehen nur aus wie kurze Störgeräusche. Die Dauer der Überlappung steht
unter `detection_delay`, die Sicherheit des Erkenners unter `probability`.
*Lehre:* Vera, 22.08.2026. Diese eine Fehllesung trug eine ganze Nacht Diagnose, stand in
vier Wahrheitsquellen und begründete eine Aufgabe, die es nie gab. **Verallgemeinert: Bevor
eine Zahl aus einem fremden System eine Handlung trägt, lies ihre Definition im Quelltext.
Ein Feldname beschreibt keine Größe, er beschreibt eine Hoffnung.**

### LK-23 — Bei eingehendem SIP darf der Agent sprechen, BEVOR der Rückweg zum Anrufer offen ist
Das Track-Abo und der offene Medienweg sind **zwei verschiedene Zeitpunkte**, und dazwischen
liegen 200 OK plus ACK. In `pkg/sip/inbound.go` steht der Ausgang zunächst auf
`mp.DisableOut()`, mit dem Kommentar der Entwickler `// disabled until we send 200`. Erst
danach kommen Raumbeitritt, `publishTrack()` und `waitSubscribe()`; das `200 OK` und das
Warten auf das ACK über UDP folgen **danach**, und erst dann `EnableOut()`. Die Agentenseite
wartet aber nur auf das Abo: `_ParticipantAudioOutput.capture_frame()` hängt an
`wait_for_subscription()` (`voice/room_io/_output.py`, Zeilen 79 bis 106).
**Was in diesem Fenster gesprochen wird, ist weg — es wird verworfen, nicht gepuffert.** Der
Anrufer hört den Satz mitten drin beginnen. LiveKit benennt das im eigenen Quelltext: „If
the delay kicks in earlier than the caller is ready, they might miss some audio packets."
Der einzige Wert, der den offenen Rückweg anzeigt, ist `sip.callStatus == "active"`.
**Es gibt dafür keine offizielle Empfehlung**, und das Telefonie-Beispiel der Doku ruft die
Begrüßung ohne jedes Warten direkt nach `session.start` auf.
*Nicht zu verwechseln:* Der „preconnect audio buffer" puffert das **Mikrofon des Nutzers**
im Browser und hat mit dieser Richtung nichts zu tun. `ctx.wait_for_participant()` hilft
ebenfalls nicht, es kehrt sofort zurück, wenn der Teilnehmer schon da ist — bei einem
eingehenden Anruf immer.
*Lehre:* Vera, BUG-033, **viermal gemeldet, bevor die Ursache belegt war.** Der Grund für
die Zähigkeit ist verallgemeinerbar: **Der Schaden lag hinter der letzten Stelle, die
protokolliert.** Agentenseitig sah jeder dieser Anrufe fehlerfrei aus, die ganze Ansage
stand im Verlauf. **Wenn ein Symptom nur der Mensch am anderen Ende sieht, ist mehr
Hinsehen im eigenen Log kein Weg zur Ursache.**

> **KORREKTURVERMERK vom 23.08.2026, und er betrifft nicht den Befund, sondern seine
> Anwendung.** Alles oben bleibt gemessen und richtig. Aber der Satz „der einzige Wert,
> der den offenen Rückweg anzeigt, ist `sip.callStatus == "active"`" steht hier **direkt
> unter** der Reihenfolge, in der `waitSubscribe()` vorkommt, und beide zusammen ergeben
> eine Falle, die vier Tage niemand gesehen hat. Wer daraus „warte auf `active`, dann
> sprich" macht und **vor** dem Start seiner Session wartet, baut einen Zirkel: siehe
> LK-24. Diese Regel sagt, **dass** man warten muss, LK-24 sagt, **wo**.

### LK-24 — Eingehend wird `sip.callStatus` erst `active`, NACHDEM der Agent seine Spur publiziert hat
Ein eingehender Anruf ohne Pin durchläuft in `pkg/sip/inbound.go` diese Reihenfolge, und
der Kommentar der Entwickler nennt sie wörtlich: „For dispatches without pin, we first
wait for LK participant to become available, and also for at least one track
subscription."

```go
if !pinPrompt {
    if ok, err := c.waitSubscribe(ctx, disp.RingingTimeout); !ok { return err }
    if ok, err := acceptCall(answerData); !ok { return err }   // hier erst das 200 OK
}
c.setStatus(CallActive)
```

**`waitSubscribe()` steht vor `acceptCall()` steht vor `setStatus(CallActive)`.** Die
einzige Spur, die der SIP-Teilnehmer abonnieren kann, ist die des Agenten. Daraus folgt
hart: **Ein Agent, der auf `active` wartet, bevor er publiziert, wartet auf eine
Bedingung, die nur sein eigenes Publizieren herstellt.** Eingehend ist dieser Zustand
nicht erreichbar, der Code läuft immer in seine eigene Zeitgrenze, und was wie ein
Randfall aussieht, ist der einzig mögliche Verlauf.

**Woran man es im Betrieb erkennt, und es sieht nach vier verschiedenen Fehlern aus:** Im
Log steht bei eingehenden Anrufen **nie** `active`, immer `ringing`. Ein Wartewert ist in
Wahrheit eine feste Pause, denn er läuft jedes Mal aus. In LiveKits Sessions-Ansicht
stehen Agent und Anrufer beide unter *Subscribers* und **keiner** unter *Publishers*. Und
der Anrufer hört durchgehend Freiton, weil ohne `acceptCall()` nie ein `200 OK` rausgeht,
während der Anbieter den Anruf als „abgebrochen, 00:00:00" führt.

*Der Fix ist die Reihenfolge, nicht die Bedingung:* Session starten, Spur publizieren,
**dann** auf `active` warten, dann sprechen. Das Fenster aus LK-23 bleibt real und muss
weiter abgewartet werden, es liegt nur später, als man denkt.

*Lehre:* Vera, BUG-062, **der schwerste Defekt des Projekts, und er hat echte Anrufe
gekostet.** Verallgemeinert, weit über LiveKit hinaus: **Bevor du auf ein Signal aus einem
fremden System wartest, sieh nach, wodurch es entsteht.** Steht die eigene Handlung in
seiner Entstehungskette, ist das Warten kein Riegel, sondern eine Verklemmung. Sie
verrät sich nie durch einen Fehler, sondern nur dadurch, dass die Zeitgrenze **immer**
greift, und eine Zeitgrenze, die immer greift, ist keine Sicherung mehr, sondern der
Normalweg.

### LK-25 — NIEMALS `lk agent update-secrets --overwrite` benutzen, um EINEN Wert zu ersetzen
**Der Flag-Name sagt das Gegenteil dessen, was er tut.** Ohne ihn gilt: „By default, the CLI
adds or updates the provided secrets, while leaving other existing secrets as-is." Mit ihm:
„To delete all existing secrets and replace them with the provided secrets"
`[B: docs.livekit.io/deploy/agents/secrets, gelesen 24.08.2026]`. Wer einen einzelnen
Schlüssel „überschreiben" will und deshalb `--overwrite` setzt, **löscht alle anderen**. Bei
`maxone-vera` wären das acht von neun gewesen, darunter Deepgram, Cartesia und die Datenbank.
*Lehre:* 24.08.2026, `vera/BUGS.md` BUG-070. Richtig ist der Aufruf **ohne** das Flag, danach
`lk agent secrets` gegenlesen: Genau eine Zeile darf ein neues `Updated At` tragen.

### LK-26 — NIEMALS annehmen, der Cloud-Agent lese denselben Secret-Store wie die Container
**Er hält eine eigene Kopie, und sie altert getrennt.** Auf `maxone-prod` kommen die Werte aus
`/opt/secrets/maxone-vera/keys.env` über `env_file`; der LiveKit-Cloud-Agent trägt sie als
**Agent-Secrets**, einmal beim Einrichten dorthin kopiert. Eine Erneuerung im Store erreicht
ihn **nie**, und nichts meldet das.
*Lehre:* 24.08.2026, BUG-070. Nach dem Erneuern des Google-Tokens meldete der Hintergrunddienst
`200 lebt`, während der Agent noch den toten Token vom 19.08. hielt — also genau der Dienst,
der am Telefon bucht. **Zwei Orte, zwei Handgriffe:** `docker compose up -d --force-recreate`
**und** `lk agent update-secrets`. Dasselbe gilt für jeden anderen Schlüssel, den beide teilen.

## Wo die Belege stehen

Die Faelle, aus denen diese Regeln stammen, die vier bereits behobenen
Community-Fehler und die genauen Quellstellen im installierten Paket stehen in
[`vorfaelle-und-nachweise.md`](vorfaelle-und-nachweise.md). **Hier steht nur, was man
wissen muss, bevor man baut.**
