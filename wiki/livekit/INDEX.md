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

## Wo die Belege stehen

Die Faelle, aus denen diese Regeln stammen, die vier bereits behobenen
Community-Fehler und die genauen Quellstellen im installierten Paket stehen in
[`vorfaelle-und-nachweise.md`](vorfaelle-und-nachweise.md). **Hier steht nur, was man
wissen muss, bevor man baut.**
