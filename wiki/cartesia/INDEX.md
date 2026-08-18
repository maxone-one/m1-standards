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
lässt sich **nur nach oben** regeln, während dieselbe Eingabe zwischen zwei Generierungen um
bis zu 15 Prozent schwankt.

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

### Der Regler geht nur nach oben

**Gemessen am 18.08.2026**, drei Läufe je Einstellung, identischer Text, Stimme Marlene:

| Einstellung | Median |
|---|---|
| ohne `speed` | 7,76 s |
| `speed: "slow"` | 7,90 s |
| `speed: "fastest"` | **5,02 s** |

Dass der Parameter überhaupt ankommt, belegt die Gegenprobe nach oben. Nach unten bewegt sich
nichts: **die Vorgabe ist bereits das langsame Ende.** Wer eine Ausgabe langsamer braucht,
bekommt sie von Cartesia nicht.

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
