---
purpose: Wiki-Scope für kitchen-station — Kiosk-Tablet-App für Viktoria From (Wetzlar)
last_updated: 2026-05-11
---

# Wiki — Kitchen Station

**Was ist Kitchen Station?** Tablet-Dashboard für die Küche. Lenovo IdeaTab 11", läuft seit 2026-04-20 produktiv unter `kitchen.maxone.one`. Erste (und derzeit einzige) Kundin: Viktoria From, Fotografin in Wetzlar — Tablet als Geburtstagsgeschenk von Max.

**Zwei-Schichten-Architektur:**
1. **Web-App** — `kitchen.maxone.one`, single HTML-Datei (`1-Click/index.html`), Repo `maxone-one/kitchen-station`. Vanilla HTML/CSS/JS, keine Frameworks. Hier liegt die Funktionalität: Home/Timer/Chat/Musik/Einkaufsliste/Settings, Rive-Screensaver, Wake Word, Auto-Update-Polling.
2. **Kiosk-Launcher** — Android-App `com.maxone.kiosk` v1.0.0, läuft als foreground-app auf dem Tablet, lädt `kitchen.maxone.one` per WebView. **Source verloren** (siehe [custom-kiosk-app](topics/custom-kiosk-app.md)).

## Topics

- [custom-kiosk-app.md](topics/custom-kiosk-app.md) — Die `com.maxone.kiosk` Android-App: Status, was bekannt ist, was verloren ist, Rebuild-Spuren
- [architecture.md](topics/architecture.md) — Web-App + Kiosk + Auto-Update + Tablet, wie alles zusammenhängt
- [tablet-ops.md](topics/tablet-ops.md) — Tablet-Operations: ADB, Paket-Whitelist, Bloatware, Setup-Script
- [bugs.md](bugs.md) — **Bug-Protokoll** (Referenzliste): bekannte Bugs mit Root-Cause, Fix, Commit, Wiedererkennung

## Wann diese Wiki nutzen

| Frage | Topic |
|-------|-------|
| "Wo ist der Source für die Kiosk-App?" | [custom-kiosk-app](topics/custom-kiosk-app.md) |
| "Wie kommt ein Update aufs Tablet?" | [architecture](topics/architecture.md) |
| "Welche Pakete dürfen NIE entfernt werden?" | [tablet-ops](topics/tablet-ops.md) |
| "Wie aktualisiere ich die Kiosk-APK?" | [custom-kiosk-app](topics/custom-kiosk-app.md) → "Update-Pfad" |
| "Wer ist die Kundin, welcher Server?" | [architecture](topics/architecture.md) → "Stakeholder + Infra" |
| "Dieser Bug schon mal vorgekommen?" | **[bugs.md](bugs.md) — immer zuerst nachschlagen!** |

## Verwandte Dokumente

- **Bootstrap-PRD** (historisch, retroaktiv annotiert): `c:/Users/max/Projects/Kitchen Station/docs/archive/bootstrap-2026/PRD.md`
- **Project-Level CLAUDE.md**: `c:/Users/max/Projects/Kitchen Station/CLAUDE.md`
- **Registry-Eintrag**: `c:/Users/max/Projects/maxone-standards/registry/projects.yml` (kitchen-station)

## Bei Konflikt

Standards (in `maxone-standards/standards/`) gewinnen immer. Diese Wiki ist narrative Beschreibung des Ist-Zustands, kein normativer Standard.
