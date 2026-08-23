---
title: An Cartesias TTS messen
description: Warum der WAV-Header keine Länge trägt, wie man die Dauer richtig rechnet, und warum ein einzelner Lauf nichts sagt
---

# An Cartesias TTS messen

Ausgelagert aus dem [`INDEX.md`](INDEX.md) am 23.08.2026, als es über 11 KB wuchs. Es
braucht nur, wer wirklich misst.

## Der WAV-Header trägt keine Länge

`/tts/bytes` liefert gestreamtes WAV, in dem die Rahmenzahl ein Platzhalter ist.
`wave.getnframes()` gab in der ersten Messung **48695 Sekunden** zurück. Richtig ist die
Rechnung über die Rohbytes:

```python
sekunden = (len(rohdaten) - 44) / (abtastrate * 2)   # 16 Bit Mono
```

Beim Speichern über `wave` verschwindet das Problem, weil der Header dabei neu gesetzt
wird. **Nur die direkte Messung an der Antwort ist betroffen**, und das ist die
unangenehme Bauform: Wer zwischendurch speichert, sieht den Fehler nie und hält die
Methode für geprüft.

## Netto gegen brutto prüfen

Ob eine längere Datei mehr Sprache oder nur mehr Stille am Ende enthält, ist an der Dauer
allein nicht zu sehen. Erst der Vergleich mit der Nettodauer (Stille unter einem Prozent
der Spitze abgeschnitten) trägt eine Aussage. Bei Cartesia liegen beide bis auf Hundertstel
gleich, es ist echtes Sprechen.

## Ein einzelner Lauf sagt nichts

Dieselbe Eingabe schwankt zwischen zwei Generierungen um **bis zu 15 Prozent**, bei
identischem Text von 15,48 auf 20,37 Sekunden. Deshalb gilt für jede Messung an dieser
API: **mindestens drei Läufe, und der Median, nicht der Mittelwert.**

Die Folge daraus ist größer als die Messvorschrift: **Ein Hebel, der kleiner ist als die
Streuung, ist keiner, auf den man sich verlassen kann.** Wer „langsamer" zusichern muss,
baut die Pause in den Ablauf, nicht in den Text.

**Und dieselbe Streuung macht jede eingefrorene Aufnahme zu einer Stichprobe.** Eine
Tonkonserve hält genau eine Ziehung fest, während live gesprochene Sätze sich über ein
Gespräch ausmitteln. Wer Konserven mehrfach zieht und die langsamste behält, wählt dabei
**nach Länge** aus, und niemand hört dabei hin: Eine Ziehung mit falscher Aussprache wird
eingefroren, wenn sie zufällig die langsamste war.
