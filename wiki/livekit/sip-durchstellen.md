---
title: Durchstellen und Dazuholen, die zwei SIP-Verfahren
description: Warum Weitergeben und Verbinden technisch zwei Dinge sind, welches davon ein Protokoll uebrig laesst, und die vier Bausteine im Paket 1.6.10
---

# Durchstellen: zwei Verfahren, und nur eines laesst ein Protokoll uebrig

**Umgangssprachlich sind „durchstellen" und „verbinden" dasselbe, technisch sind es zwei
Verfahren mit einem entscheidenden Unterschied: Bei dem einen ist der Agent danach nicht
mehr im Gespraech.** Wer ein Gespraechsprotokoll braucht, hat damit nur noch eine Wahl.

Gemessen am installierten `livekit-agents 1.6.10` und an der offiziellen Doku, beides am
25.08.2026.

## Der Unterschied in einem Satz je Verfahren

| | Weitergeben (cold) | Dazuholen (warm) |
|---|---|---|
| SIP-Mechanik | `REFER` durch den Trunk zum Anbieter | zweiter ausgehender Teilnehmer, dann verschoben |
| Der Anrufer | **verlaesst den Raum, die Sitzung endet** | bleibt im Raum |
| Der Agent | ist raus | bleibt, solange er will |
| Protokoll danach | **keines mehr** | laeuft weiter |
| Kosten | enden mit dem Transfer | Zweitanruf **plus** weiterlaufende Raumminuten |

**„The caller leaves the LiveKit room, ending the session"** steht woertlich in der Doku
zum cold transfer `[B: docs.livekit.io/sip/transfer-cold/, 25.08.2026]`. Das ist keine
Nebenwirkung, das ist der Zweck: Die Leitung wandert weg, die Vermittlung faellt heraus.

## Die vier Bausteine, am Paket nachgemessen

Alle vier existieren in 1.6.10, keiner musste nachgeruestet werden
`[B: eigener Aufruf gegen `livekit.api` im laufenden Abbild, 25.08.2026]`.

| Baustein | Felder | Wofuer |
|---|---|---|
| `TransferSIPParticipantRequest` | `room_name`, `participant_identity`, `transfer_to`, `play_dialtone`, `ringing_timeout`, `headers` | Weitergeben. `transfer_to` nimmt `tel:+49…` oder `sip:user@host` |
| `CreateSIPParticipantRequest` | u. a. `sip_call_to`, `room_name`, `participant_identity`, `wait_until_answered`, `play_ringtone`, `max_call_duration` | Den Zweiten anrufen und in **einen benannten Raum** legen |
| `MoveParticipantRequest` | `room`, `identity`, `destination_room` | Einen Teilnehmer von einem Raum in einen anderen schieben |
| `RoomService.move_participant()` | | Der Aufruf dazu, neben `forward_participant()` |

## LiveKits eigenes Muster, und warum es NICHT direkt in den Anrufer-Raum waehlt

Der naheliegende Bau waere, den Zweiten sofort in den Raum des Anrufers zu waehlen. Die
offizielle Anleitung tut das ausdruecklich nicht `[B: docs.livekit.io/sip/transfer-warm/]`:

1. Der Anrufer sitzt mit dem Agenten im **Gespraechsraum**.
2. `create_sip_participant(..., room_name=beratungsraum, wait_until_answered=True)` ruft den
   Zweiten in einen **eigenen Beratungsraum**. Dort bekommt er die Vorgeschichte, ohne dass
   der Anrufer mithoert.
3. `move_participant()` schiebt ihn danach in den Gespraechsraum.
4. Der Agent stellt ihn vor und kann sich dann selbst aus dem Raum nehmen.

**Der Beratungsraum ist der ganze Punkt und kein Umweg.** Er ist der Ort, an dem man ueber
den Anrufer spricht, waehrend der Anrufer wartet. Wer ihn weglaesst, hat kein Verfahren
weniger, sondern eine Ansage mehr, die der Anrufer hoeren wird.

**Der Preis dieses Musters, ebenfalls in der Doku:** Waehrend der Beratung ist der Agent
nicht im Beratungsraum, dieser Teil steht also **nicht** im Protokoll.

## Was daraus fuer einen Telefonassistenten folgt

**Wer „verbinden und trotzdem protokollieren" verspricht, muss den warmen Weg nehmen**,
und dann laufen zwei Kostenstellen weiter: der ausgehende Anruf beim Anbieter und die
Raumminuten, solange der Agent sitzt. Beim kalten Weg endet beides sofort.

**Und es entsteht eine Grenze, die es vorher nicht gab:** Ein Agent, der im Raum bleibt,
hoert ein Gespraech mit, das ihm nicht gehoert. Wo Vertrauliches besprochen werden kann
(bei maxone.one: Forderungen, Verfahren, SCHUTZ-05), braucht das Mithoeren einen Schalter,
den der Mensch im Gespraech bedienen kann. Technisch ist dieser Schalter dasselbe
`move_participant()`, nur mit dem Agenten als Ziel.

**Der Hinweis auf das Mithoeren gehoert in den Moment des Verbindens, nicht in die
Begruessung.** Ein Hinweis, den jemand vier Minuten vorher hoert, ist bis dahin eine
Belastung ohne Anlass und im entscheidenden Moment vergessen (Max-Entscheid 19.08.2026).

## Der Pruefsatz

**Zwei Namen fuer dieselbe Sache im Alltag heissen nicht, dass es technisch eine Sache
ist.** „Durchstellen" und „verbinden" unterscheiden sich hier in genau der Eigenschaft, an
der die ganze Anforderung haengt. Wer die Begriffe gleichsetzt und dann baut, baut mit
Wahrscheinlichkeit ein Halbes das falsche Verfahren, und merkt es erst, wenn das erste
Protokoll leer bleibt.

*Anlass: Vera, TODO 24. Dort stand seit dem 19.08.2026 als `[A:]` markierte Annahme, ein
ausgehender SIP-Teilnehmer lasse sich per API in einen bestehenden Raum legen, mit dem
Zusatz „am Paket 1.6.10 noch nicht nachgemessen". Die Annahme stimmt, der Weg dorthin ist
aber ein anderer als gedacht, und der Beratungsraum wurde von niemandem mitgedacht.*
