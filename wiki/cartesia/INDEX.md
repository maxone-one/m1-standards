# Cartesia TTS: Bedienhandbuch

Angelegt am 18.08.2026 auf Max' Auftrag (TODO 12 im Projekt `vera`), demselben, aus dem das
LiveKit-Handbuch entstand: „vor der nächsten Arbeit die offizielle Doku durchgehen, die
häufigsten Fehler sammeln, und die Best Practices vorlegen, bevor gebaut wird."

**Der Anlass ist unangenehm und gehört an den Anfang.** Für Cartesia gab es dieses Handbuch
drei Tage lang nicht, obwohl im Projektcode drei „belegte Sackgassen" standen. **Eine davon
war keine.** Sie hat Veras Aussprache in Kunstschreibweisen gezwungen, die Max am 18.08.2026
zu Recht als „nur dich tricksen" bezeichnet hat.

**Gemessen wurde gegen die laufende API**, mit Wegwerf-Wörterbüchern, die danach gelöscht
wurden. Wo etwas aus der Doku stammt und nicht selbst nachgemessen ist, steht es dabei.

## Das Wichtigste in drei Sätzen

Das Aussprachewörterbuch **kann Lautschrift**, aber nur in einer bestimmten Syntax, und wer
sie nicht kennt, hält es für reine Textersetzung. Der Abgleich trifft **ausschließlich ganze
Wörter**, ein Eintrag `Mail` wirkt also nie in `Mailadresse`. Und die Sprechgeschwindigkeit
ist bei `sonic-3` ein **Float zwischen 0,6 und 2,0**, der in beide Richtungen wirkt, während
dieselbe Eingabe zwischen zwei Generierungen um bis zu 15 Prozent schwankt.

## Das Aussprachewörterbuch

### Lautschrift, und die Syntax ist der ganze Trick

```json
{"text": "Mailadresse", "pronunciation": "<<ˈ|m|eɪ|l|ʔ|a|d|ʁ|ɛ|s|ə>>"}
```

**Doppelte spitze Klammern außen, Phoneme mit senkrechtem Strich getrennt.** Ohne die
Klammern werden die Zeichen als Buchstaben vorgelesen, und genau das war der Befund, aus dem
im Vera-Projekt „das Wörterbuch kennt KEINE Lautschrift" wurde. Der Befund war richtig
gemessen und falsch verallgemeinert.

**Gemessen am 18.08.2026**, drei Läufe je Fall, Testwort in einem Trägersatz:

| Eintrag | Dauer |
|---|---|
| kein Eintrag, Kunstwort wird gesprochen | 1,58 s |
| Textersatz `mail` | 1,21 s |
| Lautschrift `<<m\|eɪ\|l>>` | **1,07 s** |

Die Lautschrift ist die **kürzeste** von allen. Würden die Zeichen buchstabiert, wäre sie die
mit Abstand längste. Damit ist belegt, dass die Syntax verstanden und nicht vorgelesen wird.

Neben der Lautschrift gibt es die einfachere Form, eine Aussprachehilfe in normaler Schrift
(„VAH-pee") `[B: Cartesia-Doku]`. Beide stehen im selben Feld.

**Veras aktuelles Wörterbuch seit 21.08.2026:** `pdict_JNMCWKyQvKjCSgy7cFtnt1` (davor
`pdict_CDWFi97vyNedquHH3bzgSV`). Sechs Einträge, am 22.08.2026 an der API ausgelesen:
`Karastelev` → `<<k|a|ʁ|a|s|t|ɛ|l|ə|v>>` (Max' Vorgabe: der letzte Teil klingt wie
„Television", nicht wie „Thelen"), `Max` → `<<m|a|k|s>>`, `maxone` und `Maxone` →
„Mex Sown", `vera` und `Vera` → „Wera".

> **CAR-02, gelernt am 22.08.2026 und teuer bezahlt: Ein Ausspracheproblem ist nicht immer
> ein Ausspracheproblem.** Vera sprach „Max" viermal als „Mex", und drei Anläufe drehten am
> Wörterbuch. Gemessen: Der Eintrag griff, und der Name klang isoliert sogar **ohne**
> Wörterbuch sauber. Falsch klang er nur im langen Satz, der im Ganzen **eine** Pause von
> 0,12 s trug; Cartesia verschluckte darin den Vokal. Ein Punkt statt eines Kommas gibt
> 0,56 s und behebt es, ohne ein Wort zu ändern. **Vor jedem Eintrag also erst das Wort
> allein hören.** Klingt es allein richtig, liegt es am Satz, und ein Wörterbucheintrag
> macht es nur unübersichtlicher.

### Der Abgleich trifft nur ganze Wörter

**Gemessen am 18.08.2026** mit einem Wegwerf-Wörterbuch, in dem ein Eintrag auf einen
drastisch langen Ersatz zeigte, damit das Greifen an der Aufnahmedauer sichtbar wird:

| Text | Wörterbuch | Dauer | |
|---|---|---|---|
| `Das Wort ist qzx.` | ohne | 1,65 s | Bezugspunkt |
| `Das Wort ist qzx.` | mit | **3,60 s** | greift |
| `Das Wort ist abcqzxdef.` | mit | 1,74 s | greift **nicht** |
| `Das Wort ist qzxdef.` | mit | 1,70 s | greift auch als Wortanfang **nicht** |

**Was daraus folgt, in beide Richtungen.** Ein kurzer Eintrag ist ungefährlich: `at` wirkt
nicht in `Automat`, `privat` oder `Daten`. Aber ein Eintrag für ein Grundwort deckt seine
Zusammensetzungen nicht ab: `Mail` behebt `Mailadresse` nie, es braucht das ganze Wort.

**Der Fall, an dem es im Vera-Projekt aufgefallen wäre, wenn jemand nachgesehen hätte:** Am
17.08.2026 sprach Vera `anmaxone.work` aus, weil das Sprachmodell es in einem Wort
geschrieben hatte. Der Eintrag `maxone` griff nicht, weil `maxone` darin kein eigenes Wort
ist. Das stand einen Tag lang als ungeklärter Verdacht in der Projektdoku.

### Groß- und Kleinschreibung

Der Abgleich ist **case-sensitiv**, mit einer Ausnahme: Ein kleingeschriebener Eintrag trifft
auch die am Satzanfang großgeschriebene Form. `cat` trifft `cat` und `Cat`, aber nicht `CAT`.
Das gilt auch für mehrwortige Einträge `[B: Cartesia-Doku]`.

**Praktisch heißt das:** Ein Doppeleintrag `maxone` plus `Maxone` ist überflüssig, der
kleingeschriebene reicht. Eine durchgehend große Schreibweise braucht dagegen einen eigenen.

### Reihenfolge bei mehreren Einträgen

Einträge werden der Reihe nach angewandt, und ein früherer kann einen späteren zerschneiden.
Das Doku-Beispiel ist `AI hoshino`, wo ein Eintrag für `AI` zuerst greift und die Phrase
zerlegt `[B: Cartesia-Doku]`. Bei überlappenden Einträgen also den längeren zuerst.

### Die API läuft auf einer anderen Version als das TTS

```
GET/POST/DELETE  https://api.cartesia.ai/pronunciation-dicts[/{id}]
Header:          X-API-Key, Cartesia-Version
```

**`Cartesia-Version: 2024-11-13` liefert hier 404** mit der Meldung „No API schema exists for
the requested Cartesia-Version", obwohl der TTS-Endpunkt unter genau dieser Version läuft.
Funktionierend gemessen: `2025-04-16`, `2025-06-01`, `2025-09-01` und ohne Header. Nicht
funktionierend: `2025-01-01`, `2024-06-10`.

**Wörterbücher wirken nur mit `sonic-3` oder neuer** `[B: Cartesia-Doku]`. Im TTS-Aufruf
werden sie über `pronunciation_dict_id` mitgegeben.

Ein Eintrag trägt die Felder `text`, `pronunciation` und `alias`. **`pronunciation` und
`alias` sind dasselbe Feld**, die API spiegelt den geschriebenen Wert in beide.

## Sprechgeschwindigkeit

### CAR-01: Bei sonic-3 ist `speed` eine Zahl, kein Wort

> **KORREKTUR vom 22.08.2026.** Hier stand bis heute „Der Regler geht nur nach oben" mit dem
> Schlusssatz „Wer eine Ausgabe langsamer braucht, bekommt sie von Cartesia nicht." **Das war
> falsch verallgemeinert.** Die Messung darunter benutzte die **Strings** `slow` und
> `slowest`, und die gelten bei `sonic-3` nicht. Die alte Tabelle bleibt als Beleg stehen,
> ihre Deutung fällt.
>
> **Was es die Projekte gekostet hat:** In `vera` stand daraufhin in `TODO.md` Punkt 14
> („Vera liest zu schnell zurück") die Zeile „Cartesia lässt sich nicht langsamer stellen",
> und der Punkt wechselte die Richtung auf „Struktur statt Synthese", also auf einen Umbau
> des Gesprächsablaufs. Der Regler lag die ganze Zeit da.

**Für `sonic-3` ist `speed` ein Float zwischen 0,6 und 2,0**, und er geht in ein eigenes
Objekt `generation_config`, nicht mehr in `__experimental_controls`
`[B: livekit-plugins-cartesia, tts.py, `_check_generation_config` und `_to_cartesia_options`,
Quelltext gelesen 22.08.2026]`. Ein String löst dort ausdrücklich
`ValueError("speed must be a float for sonic-3")` aus.

```json
{"model_id": "sonic-3", "generation_config": {"speed": 0.85, "emotion": "Content"}}
```

**Gemessen am 22.08.2026**, drei Läufe je Fall, identischer Satz, Stimme Marlene:

| Einstellung | Median | |
|---|---|---|
| ohne Angabe | 6,41 s | Bezugspunkt |
| `speed: 0.7` | **8,55 s** | 33 Prozent langsamer |
| `speed: 0.85` | 7,43 s | 16 Prozent langsamer |
| `speed: 1.3` | 4,88 s | 24 Prozent schneller |
| `speed: "slow"` (String) | 6,04 s | wirkungslos |

**Die Falle liegt in der API-Version, und sie ist lautlos:** `generation_config` wird erst ab
einer Version **über** `2024-11-13` gelesen. Wer wie früher `Cartesia-Version: 2024-11-13`
schickt, bekommt keinen Fehler, sondern eine Aufnahme ohne jede Wirkung. Das Plugin nutzt von
sich aus `2025-04-16`. Gegengeprobt: Ein Float als **Top-Level**-Feld `speed` wirkt auch unter
`2024-11-13` (8,41 s), das Objekt dagegen nicht.

Daneben nimmt `generation_config` `emotion` (genau **eine** aus einer festen Liste, siehe
`models.py` im Plugin) und `volume` (0,5 bis 2,0).

**Die Lehre ist die Reihenfolge:** Erst am installierten Quelltext nachsehen, welche Typen
ein Parameter annimmt, dann messen. Eine Messung über einen ungültigen Wert misst die
Verwerfung, nicht den Regler.

**CAR-03: Ein ungültiger `emotion`-Wert wird wortlos verworfen**, HTTP 200 und die
Aufnahme ohne Emotion: [klangwerte.md](klangwerte.md)



### Interpunktion ist ein Hebel, aber ein kleiner

Komma und Punkt sind die Pausenlängen der Synthese. Ein Punkt nach jedem Element statt nach
je zweien verlängerte eine buchstabierte Kette um rund 17 Prozent, Auslassungspunkte um 8.

**Und hier liegt die Falle:** Dieselbe Sprechform schwankt zwischen zwei Generierungen um bis
zu 15 Prozent, bei identischem Text von 15,48 auf 20,37 Sekunden. **Ein Hebel, der kleiner
ist als die Streuung, ist keiner, auf den man sich verlassen kann.** Wer „langsamer" zusichern
muss, baut die Pause in den Ablauf, nicht in den Text.

**Folge für jede Messung an dieser API:** Ein einzelner Lauf sagt nichts. Immer mindestens
drei, und der Median, nicht der Mittelwert.

## Zwei Fallen beim Messen

**Der WAV-Header trägt keine Länge.** `/tts/bytes` liefert gestreamtes WAV, in dem die
Rahmenzahl ein Platzhalter ist. `wave.getnframes()` gab in der ersten Messung 48695 Sekunden
zurück. Richtig ist die Rechnung über die Rohbytes:

```python
sekunden = (len(rohdaten) - 44) / (abtastrate * 2)   # 16 Bit Mono
```

Beim Speichern über `wave` verschwindet das Problem, weil der Header dabei neu gesetzt wird.
Nur die direkte Messung an der Antwort ist betroffen.

**Netto gegen brutto prüfen.** Ob eine längere Datei mehr Sprache oder nur mehr Stille am Ende
enthält, ist an der Dauer allein nicht zu sehen. Erst der Vergleich mit der Nettodauer
(Stille unter einem Prozent der Spitze abgeschnitten) trägt eine Aussage. Bei Cartesia liegen
beide bis auf Hundertstel gleich, es ist echtes Sprechen.

## Nur schriftliche Doku, kein Login

`docs.cartesia.ai` leitet auf einen Login um und ist mit einem einfachen Abruf nicht lesbar.
Was hier aus der Doku stammt, ist über die Suchmaschinen-Zusammenfassung belegt. **Die härtere
Quelle ist ohnehin die laufende API**, und alle Zahlen dieses Handbuchs stammen von dort.

## Was uns das gekostet hat

Drei Kunstschreibweisen im Vera-Projekt, die auf der Annahme standen, es gäbe keine
Lautschrift: `maxone` → `Mex Sown`, `Vera` → `Wera`, und ein geplantes `Mailadresse` →
`Meyladresse`. Max hat sie am 18.08.2026 aus zwanzig Hörproben ausgewählt und beim letzten
gesagt, was sie sind: ein Trick. **Zwanzig Hörproben sind zwanzig Minuten seiner Zeit, und
sie wären mit einem Blick in die Doku nicht nötig gewesen.**

Dazu ein Tag mit einem ungeklärten `[?]`-Verdacht über `anmaxone.work`, den die
Ganzwort-Regel in einem Satz erklärt.
