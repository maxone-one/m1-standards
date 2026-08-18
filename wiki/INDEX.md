---
title: maxone wiki
description: Zentraler Einstieg in alle Wiki-Scopes
---

# maxone wiki

Narratives Betriebswissen und Domain-Kontext für Claude-Sessions. Ergänzt die maxone-standards (Regeln) und die Memory-Einträge (Feedback/Projekte).

**Faustregel:** Standards sagen WAS Pflicht ist. Die maxone wiki sagt WARUM und WIE es in der Praxis funktioniert.

> **Committet wird hier in `maxone-standards`, nicht in `~/.claude`.** Dieser Baum liegt
> physisch unter `maxone-standards/wiki/` und ist nur per Junction als
> `~/.claude/maxone-wiki/` erreichbar. Ein `git add` aus `~/.claude` heraus findet die
> Änderung deshalb nicht und der Commit läuft ins Leere, ohne Fehlermeldung (passiert am
> 14.08.2026). Und weil dort mehrere Sessions schreiben: **nur die eigene Datei adden**, nie
> `git add -A`.

## Scopes

| Scope | Thema | Wann lesen |
|---|---|---|
| [inventories](inventories/INDEX.md) | Server, Runner, Telegram, Brevo-Accounts, Mail-Aliases | Bei "wo / wer / welche ID / welcher Server" |
| [maxone-mail-pilot](maxone-mail-pilot/INDEX.md) | Stalwart, Brevo, Zentinel, JMAP, Vorfälle | Bei allen Mail-Fragen |
| [brand](brand/INDEX.md) | Visual Style, Image Pipeline, EXIF | Bei Bild-Prompts, Design, Fotografie |
| [pioneers](pioneers/INDEX.md) | Pioneer-System, Slots, Puls, Leaderboard | Bei Arbeit am Pioneer-Feature |
| [kitchen-station](kitchen-station/INDEX.md) | Kiosk-App, Android, Tablet-Ops | Bei Arbeit an kitchen-station |
| [paperclip](paperclip/INDEX.md) | Paperclip-Architektur und Ops | Bei Arbeit mit Paperclip |
| [meta-plattform](meta-plattform/INDEX.md) | Facebook, Instagram, Business Suite: Konten, Stimmen, Zielpfade, Rechte | Vor jedem Griff an Seiten, Werbekonten oder Portfolios |
| [playwright](playwright/INDEX.md) | Serverwahl, Profillage, Tab-Klassen, Node gegen Browser, Fehlerbilder | Vor jedem Browserschritt, besonders vor dem Öffnen oder Schließen |
| [claude-code](claude-code/INDEX.md) | Was automatisch lädt, Hooks, Skills, Berechtigungen, Sessions und Pool, Fehlerbilder, Grenzen | Vor jedem Griff an Hooks, Skills, `settings.json` oder Kontext, und bei „warum fragt er schon wieder" |
| [vscode](vscode/INDEX.md) | Fenster abfragen und öffnen, die drei Zustandsebenen, bekannte Fehlerbilder | Vor jedem `code`-Aufruf und bei „warum ist das Fenster weg" |
| [copyq](copyq/INDEX.md) | Max' Zwischenablage lesen und befüllen, `bin/ablage.py`, die Windows-Fallen | Wenn du wissen willst, was Max gerade kopiert hat, oder ihm etwas hinlegen sollst |
| [deploy-prod](deploy-prod/INDEX.md) | Deploy auf maxone-prod: Blue/Green, die zwei Traefik-Netze, Traefik-Probe, Platz schaffen, Fehlerbilder | Vor jedem Deploy, vor jedem Griff an Traefik, und bei „die Seite antwortet nicht" |
| [google-cloud](google-cloud/INDEX.md) | Welcher Google-Zugang haengt an welchem Cloud-Projekt, was gesperrt ist und warum, die drei Fallen | Wenn ein Google-Zugang ausfaellt, und vor jedem neuen Cloud-Projekt |
| [conventions](conventions/INDEX.md) | Umgebungs-Terminologie, Cross-Cutting Concepts | Bei terminologischen Fragen |
| [livekit](livekit/INDEX.md) | Sprachagenten: `RunContext`, Unterbrechungen, die verschluckte Folgeantwort, Wartesignal, Vorgaben | Vor jedem Griff an einen LiveKit-Agenten, und bei „der Agent schweigt nach dem Werkzeug" |
| [cartesia](cartesia/INDEX.md) | Sprachsynthese: das Aussprachewoerterbuch (Lautschrift-Syntax, nur ganze Woerter), Sprechgeschwindigkeit, zwei Messfallen | Bevor eine Aussprache geaendert wird, bei „sie spricht zu schnell", und vor jeder Messung an dieser API |
| [vanfree](vanfree/INDEX.md) | vanfree Projektkontext | Bei Arbeit an vanfree |
