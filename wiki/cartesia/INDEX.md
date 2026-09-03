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

**Gemessen am 18.08.2026**, drei Läufe je Fall: Die Lautschrift ist mit **1,07 s** die
kürzeste von allen (ohne Eintrag 1,58 s, Textersatz 1,21 s). Würden die Zeichen
buchstabiert, wäre sie die mit Abstand längste. Damit ist belegt, dass die Syntax
verstanden und nicht vorgelesen wird. Tabelle: [`messen.md`](messen.md).

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

> **NACHTRAG 04.09.2026: Der Doppeleintrag ist nicht mehr nur überflüssig, er wird
> ABGEWIESEN.** Ein `POST` mit beiden Formen antwortet mit HTTP 400 und diesem Klartext:
>
> ```
> Invalid pronunciation dictionary items: Entries "maxone" and "Maxone" would
> collide because at least one is case-insensitive
> ```
>
> **Das ist zugleich die Bestätigung der Regel darüber**, und zwar von Cartesia selbst
> statt aus der Doku gelesen: Wären die Einträge unabhängig, könnten sie nicht kollidieren.
>
> **Die teure Folge betrifft bestehende Wörterbücher, nicht neue.** Vera trug den
> Doppeleintrag seit dem 25.08.2026, angelegt mit der ausdrücklichen Begründung „ein
> zweiter Eintrag kostet nichts". Er lief weiter und wirkte, **aber derselbe Sollstand
> ließ sich nicht mehr anlegen**: Der nächste, der irgendeinen Ausspracheeintrag ändern
> wollte, wäre in einen 400er gelaufen, dessen Meldung ein ganz anderes Wort nennt als
> das, das er gerade setzen wollte. **Ein Bestand, der sich nicht reproduzieren lässt,
> meldet das nie von selbst.**
>
> *Prüfsatz daraus, über Cartesia hinaus:* Ein Datensatz, der beim Anlegen erlaubt war, ist
> deshalb nicht dauerhaft anlegbar. Wer einen Sollstand pflegt, prüft ihn gelegentlich
> gegen die API, statt nur die Abweichungen zu vergleichen.
>
> *Anlass:* Vera, 04.09.2026, beim Eintragen von `Mailadresse` (TODO 36.3).

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

### CAR-04: Ein Wörterbuch wird geändert, indem man ein neues anlegt

Es gibt `PATCH /pronunciation-dicts/{id}`, und **wer Tonkonserven hält, benutzt ihn nie.**
Eine Konserve hängt an der **Kennung** des Wörterbuchs, nicht an seinem Inhalt. Nach einem
`PATCH` spricht die Live-Synthese neu und jede Konserve weiter alt, ohne dass sich eine
Zahl ändert oder ein Test anschlägt. Ein `POST` gibt eine neue Kennung und entwertet damit
alle Konserven von selbst.

### CAR-06: Ein Lautschrift-Eintrag setzt hinter das Wort eine Pause

**310 ms gegen 60 ms**, drei Läufe mit Kontrollgruppe `[B: eigene Messung 25.08.2026,
Vera BUG-077]`. Nicht das Wörterbuch macht die Pause, sondern der Eintrag für **dieses**
Wort. **Folge:** Ein zusammengesetzter Name wie `maxone.work` braucht **einen** Eintrag
über die ganze Zeichenfolge, nie einen je Wortteil.

Dazu CAR-05 (Lautschrift nur über ein Wegwerf-Wörterbuch hörbar), die Messung zu CAR-06,
die Listen-Antwort und die zwei Fallen beim Aufräumen: [`woerterbuch.md`](woerterbuch.md).

> **NACHTRAG 01.09.2026, und er ist der eigentliche Anwendungsfall von CAR-06.** Die Regel
> stand seit dem 25.08. genau so da, und trotzdem lief die Suche nach der Ursache derselben
> Pause sechs Tage später noch einmal von vorn, über drei Messreihen hinweg. **Der Eintrag
> für `maxone` allein setzt seine Pause zwischen `maxone` und `work`, also mitten in den
> Markennamen** — 520 ms gemessen, gegen 40 ms ohne Wörterbuch. Ein Eintrag über
> `maxone work` als ganze Zeichenfolge hat sie nicht. **Wer eine Regel schreibt, die einen
> Fall vorhersagt, prüft beim nächsten Auftreten dieses Falls zuerst die eigene Bibel.**

### CAR-07 — Zwischen zwei Ziehungen schwankt nicht nur die Dauer, sondern die TONALITÄT

**Und der Unterschied ist hörbar, nicht statistisch.** Max am 01.09.2026 zu zwei Aufnahmen
desselben Satzes mit identischem Text, identischer Stimme, identischer Emotion und
identischem Wörterbuch: „Bei Messsatz 2 ist das Guten Tag freundlich, der Rest nicht. Bei
Messsatz 3 ist beides freundlicher." Und: „Beim Ersatz 3 hört es sich so an, dass sie es in
einem Atemzug sagt, wobei bei 2 sie kurz eine Pause hat und **ab da nicht so freundlich
wirkt**."

**Gemessen liegt der Unterschied in einer Pause** `[B: eigene Messung 01.09.2026, vier
Ziehungen von „Guten Tag, hier ist Vera.", Stimme Marlene]`:

| Lauf | Gesamt | innere Stille | Sprechzeit |
|---|---|---|---|
| 2 | 1,86 s | **470 ms** hinter „Guten Tag," | 1,33 s |
| 3 | 1,58 s | 50 ms | 1,53 s |

**Zwei Folgen, und die zweite ist die teurere.**

**Erstens: Der Höreindruck „freundlich" hängt an einer messbaren Größe.** Er lässt sich
also automatisieren, statt jede Aufnahme vorlegen zu müssen — gewählt wird die Ziehung mit
der geringsten Summe innerer Stille, bei Gleichstand die mit der längeren Sprechzeit.

**Zweitens: „Die längste Aufnahme behalten" ist als Auswahlregel kaputt**, auch wenn ihr
Ziel (nicht gehetzt klingen) richtig ist. **Eine Aufnahme wird vor allem durch Pausen lang,
nicht durch langsameres Sprechen.** Wer auf Gesamtdauer optimiert, wählt systematisch die
Aufnahmen mit den meisten Löchern — also genau die, die als distanziert empfunden werden.
Die Größe muss **Sprechzeit** sein, nicht Gesamtzeit.

*Lehre: Vera, BUG-053 in seiner korrigierten Fassung. Verallgemeinert über TTS hinaus:
**Bevor eine Zahl zum Auswahlkriterium wird, gehört geprüft, wodurch sie eigentlich groß
wird.** Hier war „lang" ein Sammelbegriff für zwei Dinge mit entgegengesetztem Wert.*

## Sprechgeschwindigkeit

### CAR-01: Bei sonic-3 ist `speed` eine Zahl, kein Wort

> **KORRIGIERT am 22.08.2026**, hier stand „Der Regler geht nur nach oben". Die Messung
> dahinter benutzte **Strings**, die bei `sonic-3` nicht gelten. Was der Irrtum die
> Projekte gekostet hat: [`klangwerte.md`](klangwerte.md).

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

**Der WAV-Header trägt keine Länge**, `/tts/bytes` liefert gestreamtes WAV mit einer
Platzhalter-Rahmenzahl. Und **netto gegen brutto prüfen**, sonst misst man Stille am
Dateiende als Sprechzeit. Beides mit der Rechnung und den Zahlen:
[`messen.md`](messen.md).

## Die Doku: die Referenz ist offen, die Guides sind es nicht

**Die API-Referenz unter `/api-reference/...` ist ohne Anmeldung lesbar**, die Guides sind
es nicht. Bis zum 23.08.2026 galt sie hier pauschal als gesperrt, vier Tage lang: **Ein
Negativbefund ist immer nur so breit wie der Versuch, aus dem er stammt.**

**Die härteste Quelle bleibt die laufende API**, und alle Zahlen dieses Handbuchs stammen
von dort. Die Referenz ist die zweitbeste und für Dinge, die man nicht messen kann, ohne
sie zu tun (Endpunkte, Antwortformen, Paginierung), die richtige. Die Messung dazu stand
doppelt und steht seit dem 25.08.2026 nur noch in
[`woerterbuch.md`](woerterbuch.md#was-ohne-login-lesbar-ist-und-was-nicht).

## Was uns das gekostet hat

Drei Kunstschreibweisen, zwanzig Hörproben von Max' Zeit, ein Tag mit ungeklärtem
Verdacht, fünf Tage später ein zweiter Bug aus demselben Behelf, und am 25.08.2026 ein
dritter aus dessen Lösung (CAR-06):
[`woerterbuch.md`](woerterbuch.md#was-die-annahme-gekostet-hat).
