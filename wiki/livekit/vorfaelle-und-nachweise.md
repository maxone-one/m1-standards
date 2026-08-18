# LiveKit Agents: Vorfälle und Nachweise

Ausgelagert aus [`INDEX.md`](INDEX.md) am 19.08.2026, als das Handbuch mit zwei neuen
Regeln über die 11-KB-Grenze wuchs. **Die Trennung ist die vorgesehene:** Der `INDEX.md`
trägt das Bedienbare, also was jemand wissen muss, bevor er etwas baut. Hier stehen die
Belege dafür und die Fälle, aus denen die Regeln stammen. Wer bauen will, braucht diese
Datei nicht; wer eine Regel anzweifelt, findet hier ihren Grund.

## Was uns das gekostet hat

Von einundzwanzig Defekten im Projekt `vera` wären drei durch das Handbuch verhindert
worden, und es waren die teuersten:

- **BUG-011**, die Tonspur wurde nie an ein Audio-Element gehängt. Steht wörtlich in der
  Anleitung unter „Receiving tracks".
- **Der Klon-Zwang bei `createAudioAnalyser`**: Ohne `cloneTrack: true` liefert Chrome für
  eine ferne Spur dauerhaft Nullen. Ein Pegelbalken zeigt dann ewig Stille.
- **BUG-007**, Verstummen beim Zwischenergebnis der Erkennung. Bekanntes Muster, und das
  Framework meldet den Fall selbst über `user_transcription_timeout`.

Die anderen achtzehn hätte keine LiveKit-Recherche verhindert: leere Guthaben beim
Stimmanbieter, eigene Testfehler, Prompt-Verhalten und die Betriebsbauform.

**Nachtrag vom 19.08.2026, BUG-023**, und er ist die Ausnahme zu diesem Muster: Vera
behauptete fünfmal eine Kalenderprüfung und rief kein Werkzeug auf. Kein Blick in dieses
Handbuch hätte das verhindert, denn die Wurzel lag im eigenen Entwurf, nämlich in einem
Werkzeug ohne Argumente und einem Systemprompt ohne Datum. **Die Lehre daraus steht
trotzdem im `INDEX.md`**, weil sie für jedes Agentenprojekt gilt und nicht für dieses eine.

## Vier gemeldete Fehler der Community, alle vier in 1.6.10 bereits behoben

Wer eines dieser Fehlerbilder sieht, sucht die Ursache **nicht** bei LiveKit, sondern bei
sich. Alle vier sind geschlossen und der Fix steht im installierten Code.

| Nummer | Fehlerbild |
|---|---|
| [#3702](https://github.com/livekit/agents/issues/3702) | Werkzeugergebnisse gingen bei Unterbrechung verloren, Werkzeuge liefen doppelt |
| [#3407](https://github.com/livekit/agents/issues/3407) | Ein Satz neben einem Werkzeugaufruf fehlte im Verlauf, das Modell wiederholte ihn |
| [#5009](https://github.com/livekit/agents/issues/5009) | Keine Schlussantwort, wenn `max_tool_steps` erreicht war |
| [#5150](https://github.com/livekit/agents/issues/5150) | Übergabe an einen anderen Agenten scheiterte bei parallelen Werkzeugaufrufen |

**Die verschluckte Folgeantwort nach Unterbrechung ist davon nicht abgedeckt und steht
offen.** Sie ist der Grund für die Regel, `disallow_interruptions()` als erste Zeile jedes
Werkzeugs zu setzen, dessen Ergebnis ausgesprochen werden muss.

## Nachweise

Alles im `INDEX.md` ist am 18.08.2026 im installierten Paket gelesen, Fassung
`livekit-agents 1.6.10` `[B: site-packages/livekit/agents]`. Die Stellen:

| Was | Wo |
|---|---|
| alle Vorgaben zu `turn_handling` | `voice/turn.py` |
| die Werkzeugschleife und die verschluckte Antwort | `voice/agent_activity.py`, Zeilen 3467 bis 3565 |
| der `RunContext` | `voice/events.py`, Zeile 45 folgende |
| `reply_required` | `voice/generation.py`, Zeile 1038 |
| `ToolError` und `StopResponse` | `llm/tool_context.py` |
| die mitgelieferten Klänge | `voice/background_audio.py` |

Die Originaldoku liegt persistent in [`doku/`](doku/), damit eine spätere Änderung an
LiveKits Seiten hier auffällt statt unbemerkt zu bleiben. `bin/doku-drift.py` meldet das.
