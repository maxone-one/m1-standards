---
title: KI-Team, Rollen und der Weg einer Nachricht
description: Wer im Haus wofür zuständig ist, wie eine eingehende Nachricht läuft, und welche Identität wann nach außen zeichnet
---

# Das KI-Team: Rollen, Zuständigkeiten, Nachrichtenweg

> **Die Verhaltensregel steht woanders.** Wer *darf* senden, unter welchen Bedingungen und
> was gesperrt ist: `~/.claude/rules/ki-mitarbeiter-senden-selbst.md`. Diese Seite sagt nur,
> **wer was macht**, und wird nur gelesen, wenn man es wissen muss.

Die technische Wahrheit über Adressen, Anzeigenamen und Signaturen ist die Registry
`Zentinel/supabase/functions/_shared/email-signature.ts` ab Zeile 91, nicht diese Seite.
Vierzehn Identitäten, Sammelpostfach `frankensteins@maxone.one`, Alias von
`vector@maxone.one`.

## Die drei Funktionen, damit die Zuordnung nachvollziehbar bleibt

**Marketing** macht den Markt bereit: Zielgruppe, Angebot, Preis, Positionierung. Arbeitet
auf eine Gruppe hin.

**Vertrieb** verwandelt Nachfrage in ein Geschäft. Arbeitet mit **einem** Gegenüber an
**einem** Vorgang, hat immer eine Zahl und ein Datum.

**Kommunikation** baut Verständnis und Ruf. Arbeitet auf **viele** hin, ohne einzelnen
Abschluss im Blick, und hat kein Fälligkeitsdatum.

Die Trennlinie in einem Satz: **Der Vertrieb will etwas vom anderen, die Kommunikation
will, dass der andere etwas versteht.** Praktisch: Wer den ersten Schritt macht, weil wir
etwas wollen, ist Vertrieb. Wer antwortet, weil der andere etwas will, ist Kommunikation.

## Wer wofür zuständig ist

**Die Wahrheit über die Rollen sind die System-Prompts** in
`vector/knowledge/character-prompts/PROMPT-<NAME>.md`, nicht die Signatur-Registry. Wo beide
auseinandergehen, gewinnt der System-Prompt: Er beschreibt, was der Agent tut, die Registry
beschriftet nur seine Mail.

### Nach außen, mit Kundenkontakt

| Wer | Rolle laut System-Prompt | Macht konkret |
|---|---|---|
| **Vortex** | Lead-Generierung und Outreach | Erstansprache, Kontakte finden, in die Pipeline bringen, **bis Valor übernimmt** |
| **Valor** | Vertrieb und Closing | qualifiziert, erstellt Angebote, fasst nach, „holt das Ja" |
| **Vigil** (Jill) | **Assistenz der Geschäftsführung** | Vorzimmer, Posteingang, Auftragsabwicklung, Rechnung, Mahnung, Bestandskunden |
| **Vera** | KI-Telefonassistentin, **„du bist die Stimme"** | Telefon, qualifizieren, **buchen**, nachfassen, erinnern. Zugleich verkaufbares Produkt |
| **Vantage** | CMO, „für seine Kunden sein verlängerter Arm" | Positionierung, Paket, Preis, Kampagne, **und wie das Haus klingt** |
| **Vega** | Videoproduktion | Videos für Max und für Kunden |

**Womit** jeder arbeitet, und warum alle KI-Adressen an einem einzigen Principal hängen:
[werkzeuge-und-das-tor.md](werkzeuge-und-das-tor.md) (Max, 19.08.2026).

### Nach innen, ohne Kundenkontakt

| Wer | Rolle laut System-Prompt | Besonderheit |
|---|---|---|
| **Vector** (Tor) | CEO und Orchestrator, Max' Alter Ego | nimmt jede Aufgabe zuerst entgegen und verteilt |
| **Viper** | Head of Finance, „der kälteste Kopf" | **spricht nicht einmal direkt mit Max**, nur mit Vector |
| **Vault** | Architekt, Standards-Hüter, Coach für Vybora | |
| **Vybora** | Coding, „Tochter von Vault" | |
| **Vista** | Frontend und UI/UX | |
| **Visor** | Qualitätssicherung | letzter Check vor Produktion |
| **Viktoria** | Head of HR und Fotografie, „Seele der Familie" | Zwillingsschwester der **echten** Viktoria From, das ist im Prompt sauber getrennt |

### Außerhalb der Linie

| Wer | Was |
|---|---|
| **Vox** | **freie Mitarbeiterin**, Strategic Observer. „Du löst keine Probleme, du erkennst sie." Ausdrücklich **nicht operativ**, kein festes Terrain |
| **Andreas Baulig** | **externer Unternehmensberater**, kein Mitglied. Siehe eigener Abschnitt unten |

**Merkform:** Vortex geht raus, Valor macht den Preis, Vigil führt das Büro, Vera nimmt das
Telefon, Viper rechnet nach.

## Zwei Abweichungen der Registry, entschieden am 14.08.2026

Beide sind entschieden und ausgeführt: Vigils Rollenzeile lautet „KI-Mitarbeiterin ·
Assistenz der Geschäftsführung", und Vera behält „die Stimme". Der ganze Vorgang mit
Begründung, Gegenrede und Beleg steht in
[registry-abweichungen-2026-08-14.md](registry-abweichungen-2026-08-14.md).

## Der Weg einer eingehenden Nachricht (Max-Direktive 14.08.2026, 00:08)

| Schritt | Wer | Was |
|---|---|---|
| 1 | **Vigil** | nimmt jede eingehende Nachricht an und **beantwortet sie** |
| 2 | **Vigil** | riecht es nach Auftrag: an den Vertrieb weiterleiten |
| 3 | **Vigil** | sagt dem Absender, dass sie weitergeleitet hat |
| 4 | **Valor** | meldet sich beim Kunden und übernimmt ausdrücklich |
| 5 | **Valor** | erstellt und versendet das Angebot, jedes einzeln |

**Die Ankündigung in Schritt 3 und 4 ist kein Beiwerk, sie ist der Struktur-Beweis.** Ein
stiller Absenderwechsel liest sich als Durcheinander, ein angekündigter als Haus mit
Abteilungen. Sie steht deshalb ausdrücklich in beiden Nachrichten, so wie ein Mensch es am
Telefon auch sagen würde.

**Woran etwas nach Auftrag riecht**, damit Vigil entscheiden kann statt zu raten: Eine
Leistung wird nachgefragt, ein Preis erfragt, ein Vorhaben oder Bedarf beschrieben, eine
Frist oder ein Budget genannt, oder es ist die Rückfrage auf ein laufendes Angebot.

**Kein Auftrag** sind Rückfragen zu einer Rechnung (Finanzen), Reklamationen von
Bestandskunden (Betreuung), Bewerbungen (Viktoria), Behörden und alles Private.

**Im Zweifel an den Vertrieb.** Ein Auftrag, der in der Kommunikation liegen bleibt, ist
verlorenes Geld; eine unnötige Weiterleitung kostet eine Nachricht.

## Der Vertrieb endet mit dem Abschluss (Max-Direktive 14.08.2026, 00:15)

Max wörtlich: „**Der Vertrieb kümmert sich nur um Angebote. Sobald das Projekt verkauft
wurde, ist der Vertriebler raus, und es übernimmt der Innendienst.**"

**Damit hat der Vorgang eine zweite Übergabe, und sie ist so ausdrücklich wie die erste.**
Valor führt bis zur Zusage, dann übergibt er an den Innendienst und sagt es dem Kunden.

| Phase | Wer | Ende |
|---|---|---|
| eingehend, allgemein | **Vigil** | riecht es nach Auftrag |
| Angebot bis Zusage | **Valor** | mit der Zusage |
| ab Zusage: Abwicklung | **Innendienst** | bis der Auftrag abgeschlossen und bezahlt ist |

## Was der Innendienst macht, und dass er noch niemandem gehört

Max am 14.08.2026: „**Bei der Eskalation von Mahnstufen ist Viper nicht der richtige
Ansprechpartner. Wenn ich mich recht entsinne, haben wir tatsächlich niemanden für das Thema
Büro. Entweder wir erfinden jemanden oder es übernimmt Vigil.**"

**Zum Innendienst gehört:** Auftragsbestätigung, Terminplanung und Koordination,
Rückfragen des Kunden während der Umsetzung, Lieferung und Abnahme, **Rechnungsstellung**,
**Zahlungserinnerung und Mahnstufen**, Bestandskundenbetreuung, Stammdatenpflege.

**Damit sind zwei frühere Zuordnungen widerlegt und hier korrigiert:** Das Mahnwesen liegt
**nicht** bei Viper (er rechnet nach, er treibt nicht ein), und die Rechnung geht **nicht**
vom Vertrieb raus (der ist mit der Zusage draußen).

**Die Rolle gehört Vigil, und sie war nie unbesetzt.** Nachdem ihr die falsche
Kommunikationsbeschriftung abgenommen ist, steht ihr System-Prompt genau darauf:
Assistenz der Geschäftsführung, nach außen „professionell, warm, verbindlich", nach innen
„still, wachsam, präzise, kein Drama". Eine fünfzehnte Identität ist damit hinfällig, es
braucht keinen neuen Namen und kein neues Portrait.

## Andreas Baulig ist extern und bleibt unsichtbar (Max-Direktive 14.08.2026)

Max: „Ich glaube, er sollte gar nicht ein Mitglied unseres Unternehmens sein, sondern das,
was er wirklich ist: ein externer Unternehmensberater, komplett neutral und unabhängig, auf
unser Unternehmen schauen."

**Er gehört nicht zur Familie**, und das war nie Zufall: Er heißt nicht mit V und nicht
Frankenstein. Er liegt unter `erfolgsfahrplan/mentor/` und berät Max, er vertritt ihn nicht.

**Die harte Grenze, und sie ist keine Stilfrage:** Er trägt den Namen eines echten, lebenden
Menschen. Intern seine Denkweise anzuwenden ist Max' Sache. Ihn als Mitglied des eigenen
Unternehmens zu führen wäre eine Vereinnahmung seiner Person, und sichtbar nach außen wäre
es eine Namensanmaßung mit echtem Risiko. Deshalb: **nie auf der Teamseite, nie als
Absender, nie in einem Text, den ein Dritter liest.**

**Strukturell steht er neben Vox**, der einzigen anderen Figur außerhalb der Linie: beide
beobachten, keiner von beiden ist operativ, keiner tritt nach außen auf.

## Viper ist Controlling, nicht Buchhaltung

Max am 14.08.2026: „Viper kümmert sich um die Finanzen des gesamten Unternehmens. Schaut, ob
die Preise stimmen, ob die Margen stimmen, ob die Firma schwarze Zahlen schreibt. Ist aber
nicht aktiv im Vertrieb drin."

Er prüft Preise und Margen, bewertet, ob ein Geschäft trägt, und hält den Blick auf das
Ganze. Er verhandelt nicht, macht keine Angebote, versendet keine Rechnungen und mahnt
nicht. Wo Vertrieb und Controlling aneinandergrenzen (ein Preis, der die Marge reißt), berät
er **nach innen**, gegenüber Max und dem Vertrieb, nie gegenüber dem Kunden.

## Eine bekannte Lücke

**Marketing und Kommunikation überschneiden sich ungeklärt.** Vantage und Vigil wären beide
für einen Webseitentext zuständig. Die brauchbare Grenze: Vantage entscheidet, **was**
verkauft wird und an wen, Vigil entscheidet, **wie** das Haus klingt.

## Namenskollision, vor dem ersten Außenkontakt zu klären

`viktoria@maxone.one` heißt „Viktoria Frankenstein" und kollidiert mit Max' Partnerin
Viktoria From und ihrem Projekt. Kein Blocker, aber eine Entscheidung wert, bevor diese
Identität zum ersten Mal nach außen zeichnet.
