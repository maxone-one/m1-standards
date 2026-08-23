---
title: Das Aussprachewörterbuch pflegen
description: Warum ein PATCH auf ein Wörterbuch gefährlicher ist als ein neues, wie die API antwortet, und was ohne Login lesbar ist
---

# Das Aussprachewörterbuch pflegen

Die Syntax der Lautschrift, die Ganzwort-Regel und die Groß-/Kleinschreibung stehen im
[`INDEX.md`](INDEX.md). Hier steht, was beim **Ändern** eines Wörterbuchs gilt.

## CAR-04 — Ein PATCH erhält die Kennung, und genau das ist die Falle

Cartesia kennt vier Wege auf `/pronunciation-dicts`:

```
GET     /pronunciation-dicts          Liste, siehe unten
POST    /pronunciation-dicts          neues Wörterbuch, neue Kennung
PATCH   /pronunciation-dicts/{id}     Inhalt tauschen, Kennung BLEIBT
DELETE  /pronunciation-dicts/{id}
```

`PATCH` sieht nach dem sauberen Weg aus: ein Eintrag ändert sich, das Wörterbuch bleibt
dasselbe, keine Kennung muss irgendwo nachgezogen werden. **Wer vorgenerierte Tonkonserven
hält, für den ist es der gefährlichste Aufruf der ganzen API.**

Der Grund ist eine Asymmetrie, die man nur sieht, wenn man beide Seiten zugleich ansieht:
Eine Konserve wird üblicherweise unter einem Fingerabdruck aus Text, Stimme, Modell und
**Wörterbuchkennung** abgelegt. Der **Inhalt** des Wörterbuchs steckt in diesem
Fingerabdruck nicht, denn ihn kennt man beim Ablegen gar nicht ohne einen zusätzlichen
Abruf. Nach einem `PATCH` gilt deshalb beides zugleich: Live gesprochene Sätze tragen die
neue Aussprache, jede Konserve die alte. **Beide sind gültig, keine Zahl ändert sich, und
kein Test schlägt an.**

**Die Regel: Ändere ein Wörterbuch, indem du ein neues anlegst.** Die neue Kennung
entwertet jede Konserve, sie wird beim nächsten Lauf neu gezogen, und der teurere Weg ist
hier der einzige, der sich selbst prüft. Ein `PATCH` gehört nur dorthin, wo es keine
abgeleiteten Artefakte gibt.

*Verallgemeinert, weit über Cartesia hinaus:* **Wenn ein Cache an der Kennung einer
fremden Ressource hängt und nicht an ihrem Inhalt, dann ist jede Änderung, die die Kennung
erhält, eine stille Änderung.** Die bequeme Schnittstelle ist genau die, die den Cache
nicht mitnimmt.

## CAR-05 — Hören lässt sich eine Lautschrift nur über ein Wegwerf-Wörterbuch

Für einen **Textersatz** gibt es die Abkürzung: Ein geplanter Eintrag `Mail` → `Meil`
klingt exakt so wie ein Text, in dem von vornherein `Meil` steht. Man kann also probieren,
ohne das laufende Wörterbuch anzufassen, und das ist wichtig, weil ein Eintrag sofort auf
jeden echten Anrufer wirkt.

**Für Lautschrift gilt die Abkürzung nicht.** Die `<<...>>`-Syntax wird im Feld
`pronunciation` ausgewertet und nicht im gesprochenen Text; wer sie in den Transcript
schreibt, misst etwas anderes als das, was er einbauen will. Der Weg ist ein
Wegwerf-Wörterbuch je Kandidat, eine Probe damit, und Löschen im `finally`.

Ein Wörterbuch kostet nichts, aber liegengebliebene sammeln sich unter Namen an, die wie
das echte aussehen. Sie brauchen deshalb ein erkennbares Namenspräfix und einen
Aufräumweg, der **an der Kennung** prüft, welches das produktive ist, nicht am Namen.

## Wie die Liste antwortet, und warum das beim Aufräumen zählt

```json
{ "data": [ { "id": "pdict_123", "name": "Acme", "items": [...] } ],
  "has_more": false, "next_page": null }
```

Cursor-Paginierung über `starting_after` beziehungsweise `ending_before`. Ein Eintrag trägt
`text` und `pronunciation`; `alias` ist dasselbe Feld, die API spiegelt den Wert in beide.

**Zwei Fallen für den Code, der diese Liste löscht.** Erstens: `has_more` wirklich folgen.
Wer nur die erste Seite nimmt, meldet einen sauberen Lauf und lässt Reste liegen.
Zweitens, und das ist die unangenehmere: **Ein Rückfall der Bauart „wenn kein `data`-Feld
da ist, wird die Antwort selbst die Liste sein" darf hier nicht stehen.** Über ein fremdes
Objekt zu iterieren liefert seine Schlüssel, und daraus werden Löschbefehle über Namen,
die niemand vergeben hat. Bei unverstandener Antwort ist **nicht nachgesehen** die richtige
Antwort, und sie muss sich vom Ergebnis **nichts gefunden** unterscheiden: verschiedene
Rückgabewerte, verschiedene Meldung. Sonst sieht ein blinder Lauf aus wie ein sauberer.

## Was ohne Login lesbar ist, und was nicht

Im `INDEX.md` stand bis zum 23.08.2026 pauschal, `docs.cartesia.ai` leite auf einen Login
um und sei nicht abrufbar. **Das gilt nur für die Guides.** Nachgemessen:

| Pfad | Abruf ohne Login |
|---|---|
| `/api-reference/...` | **geht**, mit vollständigem Schema und Beispielen |
| `/build-with-cartesia/capability-guides/...` | 307 auf `play.cartesia.ai/docs-auth-login` |

**Die API-Referenz ist damit eine harte Quelle, die vier Tage lang als unerreichbar galt.**
Ein Negativbefund ist immer nur so breit wie der Versuch, aus dem er stammt, und hier
stammte er aus einem Guide-Pfad.

**Nebenbefund, ungeprüft `[?]`:** Die Referenz nennt als aktuelle `Cartesia-Version`
`2026-08-14`. Im Einsatz ist `2025-04-16`, gemessen und ausreichend für `generation_config`
(CAR-01). Ein Wechsel ist nicht nötig und ungemessen; wer ihn erwägt, misst vorher.

## Was die Annahme gekostet hat

Drei Kunstschreibweisen im Vera-Projekt standen auf der Annahme, es gebe keine Lautschrift:
`maxone` → `Mex Sown`, `Vera` → `Wera`, und ein geplantes `Mailadresse` → `Meyladresse`.
Max hat sie am 18.08.2026 aus **zwanzig Hörproben** ausgewählt und beim letzten gesagt, was
sie sind: ein Trick. Zwanzig Hörproben sind zwanzig Minuten seiner Zeit, und sie wären mit
einem Blick in die Referenz nicht nötig gewesen. Dazu ein Tag mit einem ungeklärten
`[?]`-Verdacht über `anmaxone.work`, den die Ganzwort-Regel in einem Satz erklärt.

**Und die Rechnung war am 18.08. nicht abgeschlossen.** Als die Annahme fiel, wurde nur der
Eintrag nachgezogen, den danach jemand angefasst hat. `maxone` → `Mex Sown` blieb stehen,
und „Mex" spricht sich „Meks". Fünf Tage und **fünf Meldungen** später war das BUG-064 im
Vera-Projekt, wobei vier Anläufe am falschen Eintrag drehten, weil der Nutzer den Vornamen
meldete und nicht den Markennamen.

**Die verallgemeinerbare Lehre ist nicht „lies die Doku".** Sie lautet: **Wenn eine Annahme
fällt, fällt sie für jeden Wert, der auf ihr steht, und nicht nur für den, der gerade offen
ist.** Ein Bestand, der nur bei einem Anbieter liegt und im eigenen Repo nicht sichtbar ist,
wird bei so einer Korrektur zuverlässig übersehen. Er braucht ein Werkzeug, das ihn
anzeigt, sonst ist er ein blinder Fleck mit Wirkung auf jeden Anrufer.
