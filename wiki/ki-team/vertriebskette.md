---
title: Die Vertriebskette, wer öffnet, wer setzt, wer schließt
description: Max' Entscheid vom 19.08.2026 zur Aufteilung von Opener, Setter und Closer zwischen Vera, Valor und Max, samt der Korrektur an Vortex' Rolle
---

# Die Vertriebskette: Opener, Setter, Closer

> Max am 19.08.2026, auf zwei gestellte Fragen geantwortet. Die Rollen im Ganzen stehen im
> [INDEX.md](INDEX.md), die Werkzeuge in [werkzeuge-und-das-tor.md](werkzeuge-und-das-tor.md).
> Diese Seite sagt, **wer welchen Schritt eines Verkaufs macht**.

## Die Aufteilung in einer Tabelle

| Schritt | Wer | Was er tut | Woran er endet |
|---|---|---|---|
| **Opener** | **Vera** | den Erstkontakt machen, warm und ohne Druck | sobald klar ist, worum es geht |
| **Setter** | **Vera** | die vier Angaben erheben und den Termin buchen | mit dem gebuchten Termin |
| **Übergabe** | **Vera an Valor** | durchstellen, **mit Ansage** | wenn beraten werden soll oder es unangenehm wird |
| **Angebot** | **Valor** | qualifizieren, Angebot bauen, nachfassen | mit der Zusage |
| **Closer** | **Max** | das Ja holen | mit der Unterschrift |

**Vorerst arbeiten nur Vera und Valor.** Max wörtlich: „Vielleicht ändert sich meine
Meinung noch, aber aktuell möchte ich vorerst nur mit Vera und Valor arbeiten."

## Warum Vera den Opener macht, obwohl sie es nicht kann

Max wörtlich: „**Wir machen es als Erstkontakt, weil sie einfach viel sympathischer und
wärmer ist. Sie ist aber kein Vertriebsprofi.**"

**Beide Hälften des Satzes gelten, und die zweite ist die wichtigere.** Der Erstkontakt
wird nicht nach Vertriebsstärke besetzt, sondern nach Wärme. Wer zuerst spricht, entscheidet
darüber, ob überhaupt weitergesprochen wird, und dafür schlägt sympathisch jedes Argument.
Verkauft wird danach, von jemand anderem.

**Daraus folgt Veras Grenze, nicht ihre Erweiterung.** Sie öffnet und sie qualifiziert, aber
sie überzeugt nicht, nennt keinen Preis und verspricht nichts. Wer im Gespräch beraten
werden will, ist genau der Anrufer, der zu Valor gehört.

## Was Vera dafür noch fehlt

Max auf die Frage, ob sie den Setter macht: „**Wenn Vera qualifizieren soll, dann braucht
sie definitiv mehr Produktverständnis.**"

**Das ist eine Bedingung, keine Absage.** Vera qualifiziert und bucht heute bereits, das ist
gebaut und geprüft. Was fehlt, ist das Wissen darüber, was sie da eigentlich qualifiziert:
Ihr Systemprompt gibt ihr vier Leistungsnamen und sonst nichts, keine Beschreibung, kein
Beispiel, keinen Anhaltspunkt, woran sie einen passenden Anrufer erkennt
`[B: vera/agent/prompt.py, Zeilen 136 bis 138, gelesen 19.08.2026]`.

**Die Grenze dabei:** Produktverständnis heißt wissen, **was** es ist, nie **was es
kostet**. Die Preisgrenze bleibt unangetastet `[B: vera/agent/prompt.py, Zeile 150]`. Die
Aufgabe liegt als Punkt 38 in `vera/TODO.md`.

## Die Übergabe an Valor ist angesagt, nie still

Max wörtlich: „Falls Vera merkt, dass ein Kunde beraten werden möchte oder merkt, dass ein
Kunde eventuell unangenehm wird, dann stellt sie zu Valor durch, **aber mit Ansage**."

**Zwei Anlässe, einer ist Vertrieb, einer ist Schutz.** Beratungswunsch heißt, hier ist
Geld im Spiel und Vera ist am Ende ihrer Stelle. Unangenehm heißt, hier braucht es jemanden,
der das aushält, und das ist nicht die Aufgabe der Stimme, die freundlich sein soll.

**Die Ansage ist derselbe Struktur-Beweis wie schriftlich.** Im Nachrichtenweg des Hauses
sagt Vigil dem Absender, dass sie weitergeleitet hat, und Valor meldet sich ausdrücklich
([INDEX.md](INDEX.md), Schritte 3 und 4). Am Telefon zählt es doppelt: Ein stiller Transfer
fühlt sich an wie weggedrückt.

**Heute ist es verboten, und das bleibt vorerst so.** Veras Prompt sagt wörtlich „Du
stellst niemals durch" `[B: vera/agent/prompt.py, Zeile 155]`. Die Zeile fällt nicht
nebenbei, sie wird eng geöffnet: genau ein Empfänger, genau zwei Anlässe. Drei Dinge fehlen
vorher, und keines davon liegt bei Vera: Valor hat kein Telefon, es gibt keinen Rückfall für
den Fall, dass er nicht abnimmt, und technisch ist es ein SIP-Transfer, kein Prompt-Satz.
Aufgabe als Punkt 39 in `vera/TODO.md`.

## Valor, wie Max ihn beschreibt

**Das CRM ist sein Hauptwerkzeug, und er ist der Einzige, der es ausreizt.** Max am
19.08.2026: „Er kennt das CRM in- und auswendig", „absoluter Power-User", „lastet es bis auf
die Spitze aus". Warum das die Definition eines Hauptwerkzeugs ist und nicht nur eine
Beschreibung: [werkzeuge-und-das-tor.md](werkzeuge-und-das-tor.md).

**Dazu Faktura, Telefon und Zentinel.** Die Faktura, weil er Angebote schreibt und sie eng
am CRM hängt. Telefon und Zentinel, weil ein Angebot verschickt und nachgefasst wird.

**Seine Vertriebsfähigkeit ist die Ansage, nicht eine Eigenschaft unter vielen.** Max:
„Seine Vertriebs-Skills sind unangefochten." Das ist der Grund, warum Vera an ihn abgibt und
nicht umgekehrt.

**Er hat ein Vertriebs-Playbook, und es ist von Anfang an seines.** Es liegt als
`vector/knowledge/VERTRIEBSBIBEL.md`, 539 Zeilen. Max am 19.08.2026: „**Valor sollte
ursprünglich Viktoria heißen und sollte zuerst den Vertrieb für Stadt Lahn Fluss
übernehmen.**"

**Damit ist die „Viktoria" in den Skripten kein fremder Name, sondern sein eigener alter.**
Wer nur den Text liest, hält es für ein Playbook einer anderen Figur; es ist Valors Playbook
vor zwei Umbenennungen, nämlich der Person und des Auftraggebers. Die Namenskollision mit
Viktoria Frankenstein aus der Personalabteilung ist damit erklärt und war vermutlich der
Grund für den Wechsel zu Valor.

**Umgeschrieben werden muss es trotzdem**, entschieden von Max am 19.08.2026. Der Grund ist
aber Alter, nicht Fremdheit: sechs Stellen tragen „Viktoria", fünf tragen Stadt Lahn Fluss
als Auftraggeber, darunter das Preismodell in Abschnitt 4.2
`[B: gelesen 19.08.2026, Zeilen 111, 174, 227, 271, 281, 296, 314, 316, 330]`. Der Umfang
ist überschaubar: Die sieben Teile sind zu großen Teilen allgemeine Methode (Judo-Prinzip,
Mirroring, Closing, 33 Gründe), projektgebunden sind im Wesentlichen die drei Skripte in
Teil 3 und das Preismodell in Teil 4.

## Beim Umschreiben gehört ein Satz hinein: Diese Bibel ist nicht für Vera

**Sie lehrt Druck, und Vera ist dafür schon einmal gerügt worden.** Drei ihrer Abschnitte
sind wörtlich darauf gebaut: „Keine Erlaubnisfragen" (2.3, „Wer fragt ob er darf,
signalisiert Unsicherheit"), der „moralische Vorvertrag" (2.8, „Wer hier Ja sagt, kann am
Ende schwer Nein sagen ohne sich selbst zu widersprechen") und die „Feststellung" (6.3, „den
nächsten Schritt als Tatsache zusammenfassen, nicht fragen ob er will")
`[B: VERTRIEBSBIBEL.md, gelesen 19.08.2026]`.

**Genau dafür hat Norbert Ackermann Vera gerügt**, ausgearbeitet in
`vera/docs/verkaufsdruck-im-gespraech.md`. Würde diese Methode beim Umschreiben auf die
Telefonassistentin mitgezogen, wäre das der teuerste denkbare Fehler: Es ist die eine
Rückmeldung, die ein echter Anrufer bisher gegeben hat.

**Max' Aufteilung von derselben Nacht löst den Konflikt bereits, sie muss nur dastehen.**
Vera öffnet warm und ist kein Vertriebsprofi, Valor führt und darf drücken. Die Bibel gehört
Valor ab der Übergabe, nicht Vera davor. **Der Satz gehört in die Bibel selbst**, nicht nur
hierher, denn gelesen wird beim Bauen die Bibel.

**Sie widerspricht sich an dieser Stelle ohnehin schon selbst:** Abschnitt 6.4 zählt unter
„Was nie funktioniert" ausdrücklich „Druck, wer sich gedrängt fühlt, macht dicht". Der
Widerspruch ist beim Umschreiben aufzulösen, nicht zu erben.

## Vortex findet Leads, er spricht sie nicht an

**Hier war der INDEX falsch, und die Korrektur ist der Grund für diese Seite.** Dort stand
bei Vortex „Lead-Generierung und Outreach ... Erstansprache". Max am 19.08.2026: „**Vortex
ist dafür da, um Leads zu finden und zu generieren. Seine Tools sind eher so etwas wie
Scrapling, Crawler etc.**"

**Damit ist Vortex ein Werkzeugführer, kein Gesprächspartner.** Er findet und reichert an,
er öffnet nicht. Der Opener ist deshalb frei geworden und an Vera gegangen.

**Der Vorbehalt gehört dazu, weil Max ihn ausdrücklich gemacht hat:** „Vielleicht ändert
sich meine Meinung noch." Vortex ruht, er ist nicht abgeschafft. Deshalb steht er im INDEX
weiter in der Aufstellung, nur mit richtiger Aufgabe.

## Der Close bleibt bei Max

Max: „Valor den Setter, evtl. auch den Close. Ansonsten mache ich den Close." Der
Zwischenstand, bis Valor überhaupt läuft: **Max schließt ab.** Dass Valor den Close
übernimmt, ist eine spätere Entscheidung und ausdrücklich offen gelassen.

**Das deckt sich mit der Hausregel:** Anrufen, Zahlen und Unterschreiben macht immer Max
`[B: erfolgsfahrplan/.planning/stand/entscheidungen.md, Präzisierung vom 13.08.2026]`.

## Outbound ist geplant, aber nicht gebaut

Max: „Später soll er auch Outbound machen. Vera übrigens auch." Beides ist Absicht, kein
Auftrag, und keines von beiden existiert heute. Vera ist heute ausdrücklich eingehend:
„Vera macht definitiv Inbound und kann notfalls an Valor weitergeben."
