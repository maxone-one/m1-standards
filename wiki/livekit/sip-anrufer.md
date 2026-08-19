---
title: Wer anruft, die Nummer des SIP-Anrufers
description: Woher die Rufnummer eines eingehenden SIP-Anrufers kommt, warum das SDK sie nicht kennt, und die Regel gegen den geratenen Wert
---

# Wer anruft: die Nummer des SIP-Anrufers

**Das SDK kennt sie nicht, der Server setzt sie.** Ein Grep über `livekit/agents` und
`livekit/rtc` in 1.6.10 findet **keinen einzigen** SIP-Attributnamen, weder
`sip.phoneNumber` noch eine Variante `[B: eigener Grep, 19.08.2026]`. Wer den Namen im
Paket sucht, findet nichts und schließt daraus fälschlich, es gebe die Nummer nicht.

**Was das SDK sehr wohl kennt, ist die Art des Teilnehmers:**
`rtc.ParticipantKind.PARTICIPANT_KIND_SIP`. Daran wird der Anrufer erkannt, nie am Namen
und nie an der Identität.

```python
for teilnehmer in room.remote_participants.values():
    if teilnehmer.kind == rtc.ParticipantKind.PARTICIPANT_KIND_SIP:
        nummer = teilnehmer.attributes.get("sip.phoneNumber")
```

**Die zweite, unabhängige Quelle ist der Raumname**, und sie ist oft die belegtere. Eine
Dispatch-Regel vom Typ *individual* mit Präfix legt je Anrufer einen eigenen Raum an, und
der Name trägt die Nummer: `anruf_+4917648085640_viLZMfAwTt9o`. Der Raumname steht sofort
zur Verfügung, die Attribute erst mit dem Teilnehmer.

## Die Regel: jede Quelle wird geprüft, keine geraten

Attributname, Präfix und Raumname liegen **alle drei außerhalb des eigenen Repos**. Der
Attributname steht beim Server, das Präfix in einer Dispatch-Regel beim Anbieter, und wer
dort etwas ändert, bricht eine Zerlegung lautlos.

Deshalb: mehrere Schreibweisen probieren statt einer raten, und **jeden Kandidaten gegen
dieselbe Plausibilitätsprüfung halten**, die auch für eine diktierte Nummer gilt. Liefert
keine Quelle etwas Plausibles, ist **None die richtige Antwort** und nicht ein
Näherungswert: Die Nummer landet in einer Buchung, und eine falsche ist schlechter als
keine.

Ein Nebeneffekt derselben Prüfung, der Arbeit spart: Ein Browser-Gespräch heißt
`probe-2g4c7vah` und liefert damit von selbst None, ohne dass die Funktion die
Gesprächsart kennen müsste.

## Der teuerste Teil ist keine Technik

**Prüfsatz: Wenn eine Prüfung im Trockenlauf entsteht, gehört in denselben Zug die Frage,
wer sie im Echtbetrieb aufruft.**

Der Fall dazu ist BUG-036 in `vera`. Dort war die Regel „frag nur nach einer
Rückrufnummer, wenn keine vorliegt" (GES-09) seit dem 17.08.2026 gebaut, mit elf Tests
belegt und **nie verdrahtet**: Sie entstand im Browser-Trockenlauf, wo es gar keine
Anrufernummer gibt, und ihre eigene Doku verschob die funktionale Abnahme in eine spätere
Phase. Seit dem 18.08.2026 kamen echte Anrufe, und niemand legte den Schalter um.

**Die Prüfung war grün und wirkungslos zugleich.** Der Anrufer musste seine Nummer
diktieren, obwohl der Raumname sie trug, und weil beim Diktieren nach der Vorwahl eine
Atempause fällt, entstand daraus ein zweiter Defekt: eine abgebrochene Nummer in der
Buchung (BUG-031). Max hat den sichtbaren Teil dreimal gemeldet, bevor jemand die Wurzel
sah.
