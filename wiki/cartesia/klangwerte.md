# Cartesias Klangwerte: `emotion`, und warum ein Tippfehler darin nie auffällt

Ausgelagert am 22.08.2026 aus `INDEX.md`, weil der Zusatz sie auf 11,85 KB gebracht hätte.
Der geltende Satz steht dort unter „CAR-03", die Ausführung hier.

## Der Befund, gemessen

Derselbe Satz „Guten Tag.", MP3 mit fester Bitrate, also ist die Bytezahl die Sprechdauer.
Gegen `api.cartesia.ai/tts/bytes`, Modell `sonic-3`, Stimme Marlene, `Cartesia-Version:
2025-04-16`:

| `generation_config` | Antwort | Bytes |
|---|---|---|
| gar keines | HTTP 200 | 13.419 |
| `{"emotion": "Sympathetic"}` | HTTP 200 | **20.107** |
| `{"emotion": "VoelligerUnsinn"}` | HTTP 200 | **13.419** |
| `{"emotion": "VoelligerUnsinn"}` unter `2024-11-13` | HTTP 200 | 13.419 |

**Zwei Dinge auf einmal.** Erstens wirkt `emotion` deutlich, hier 50 Prozent mehr
Sprechzeit bei einem Zweiwortsatz. Zweitens, und das ist der teure Teil: **Ein ungültiger
Wert wird wortlos verworfen.** Kein Fehler, keine Warnung, kein Feld in der Antwort, das
davon erzählt. Die Aufnahme ist Byte für Byte dieselbe wie ohne jede Emotion.

**Warum das schlimmer ist als eine Fehlermeldung.** Ein Aufruf, der scheitert, wird
bemerkt. Ein Aufruf, der still das Falsche tut, wird geglaubt: Die Stimme klingt neutral,
das sieht nach einer Geschmacksfrage aus, und niemand sucht den Buchstabendreher. Dieselbe
Bauform wie bei der API-Version eine Zeile darüber, und es ist der zweite stille Verwerfer
in derselben Schnittstelle.

## Der Typ heißt `TTSVoiceEmotion`

Nicht `Emotion`, obwohl im Quelltext des Plugins beides zu lesen scheint. 59 Werte, ein
`Literal` in `livekit/plugins/cartesia/models.py`, laut Kommentar dort auf dem Stand vom
2025-10-24.

**„Empathetic" ist nicht darunter.** Wer Empathie meint, findet am nächsten:
`Sympathetic`, `Affectionate`, `Content`, `Calm`, `Trust`, `Grateful`, `Peaceful`,
`Serene`. Die Liste trägt auch das Gegenteil (`Angry`, `Sarcastic`, `Bored`), es lohnt
also der Blick, bevor geraten wird.

**Das Plugin nimmt eine Liste und liest daraus genau das erste Element:**

```python
if opts.emotion:
    generation_config["emotion"] = opts.emotion[0]
```

Ein zweiter Wert ist damit nicht falsch, sondern wirkungslos, und auch das meldet niemand.

## Der Schutz: gegen die echte Liste prüfen, nie gegen eine Kopie

```python
import typing
from livekit.plugins.cartesia import models

werte = set(typing.get_args(models.TTSVoiceEmotion))
assert EMOTION in werte
```

**Eine abgeschriebene Werteliste im eigenen Test wäre eine zweite Wahrheit** und würde
beim nächsten Paket-Update genau dann falsch, wenn niemand hinsieht. Und der Test darf
sich **nicht selbst überspringen**, wenn er den Typ nicht findet: Der erste Wurf in Vera
fragte nach `Emotion`, fand nichts, sprang mit `pytest.skip` heraus und sah grün aus.
Das ist die Bauform aus `vera/BUGS.md` BUG-010. Verschwindet der Typ, ist das ein Befund.

Vorbild: `vera/tests/test_stimme.py`.

## Wer einen Klangwert setzt, muss seine Konserven daran hängen

Ein Projekt mit vorproduzierten Ansagen hat nach einer Klangänderung zwei Stimmen: die
live gesprochenen Sätze in der neuen Grundstimmung, die eingefrorenen in der alten. Für
den Anrufer ist das ein Sprecherinnenwechsel mitten im Gespräch.

**Die Abhilfe ist dieselbe wie beim Aussprachewörterbuch:** Der Klangwert geht in die
Kennung, unter der die Aufnahme liegt. Ändert er sich, zeigt der Pfad ins Leere, und der
Dienst fällt auf Live-Synthese zurück, statt eine überholte Aufnahme abzuspielen. Kostet
Latenz statt Wahrheit. Umgesetzt in `vera/agent/ansage.py::konservenkennung`.

**Eine Lücke bleibt und ist dort offen:** In die Kennung geht die **Kennung** des
Aussprachewörterbuchs ein, nicht sein **Inhalt**. Wer einen Eintrag ändert, ohne ein neues
Wörterbuch anzulegen, entwertet damit keine einzige Konserve.

> **NACHGETRAGEN am 23.08.2026: Die Lücke ist nicht theoretisch, sie hat einen Weg.** Als
> dieser Absatz am 22.08. entstand, war „einen Eintrag ändern, ohne ein neues Wörterbuch
> anzulegen" ein gedachter Fall; die damals bekannten Endpunkte waren `GET`, `POST` und
> `DELETE`. Es gibt aber `PATCH /pronunciation-dicts/{id}`, und er tut exakt das. Damit
> ist aus einer notierten Lücke ein benutzbarer Fehlweg geworden: **CAR-04**, ausführlich
> in [`woerterbuch.md`](woerterbuch.md).
>
> **Und das ist die Lehre über den Fall hinaus.** Eine Lücke, die man kennt, aber für
> unerreichbar hält, wird notiert und nicht verriegelt. Sie wird erreichbar, sobald jemand
> die passende Schnittstelle findet, und dann sucht niemand mehr in den Notizen, sondern
> alle im Code. **Wer eine Lücke beschreibt, ohne den Weg dorthin zu kennen, hat sie nicht
> ausgeschlossen, sondern nur noch nicht gefunden.**

## Was der `speed`-Irrtum die Projekte gekostet hat

Bis zum 22.08.2026 stand im `INDEX.md` „Der Regler geht nur nach oben" mit dem Schlusssatz
„Wer eine Ausgabe langsamer braucht, bekommt sie von Cartesia nicht". Die Messung dahinter
war richtig gefahren und benutzte die **Strings** `slow` und `slowest`, die bei `sonic-3`
nicht gelten; ein String löst dort `ValueError("speed must be a float for sonic-3")` aus.

**Die Folge stand ein halbes Projekt weiter.** In `vera` trug `TODO.md` Punkt 14 („Vera
liest zu schnell zurück") daraufhin die Zeile „Cartesia lässt sich nicht langsamer
stellen", und der Punkt wechselte die Richtung auf „Struktur statt Synthese", also auf
einen Umbau des Gesprächsablaufs mit zusätzlichen Gesprächsrunden. **Der Regler lag die
ganze Zeit da**, ein Float zwischen 0,6 und 2,0 im `generation_config`.

*Dieselbe Bauform wie bei der Lautschrift:* Aus „so wie ich es versucht habe, ging es
nicht" wurde „es geht nicht", und dieser Satz stand danach als geprüfte Tatsache da. **Ein
Negativbefund über einen Parameter, dessen Typ man nicht am Quelltext geprüft hat, misst
die Verwerfung und nicht den Regler.**
