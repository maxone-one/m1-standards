---
topic: architecture
scope: kitchen-station
last_updated: 2026-05-11
---

# Kitchen Station — Architektur

## Stakeholder + Infra

- **Kundin:** Viktoria From, Fotografin in Wetzlar
- **Geschäftsmodell:** 899 € Setup + 7,90 €/Monat Abo (Sponsored-Customer per CLAUDE.md — Domain + Postfach + Client von Max gestellt → Mail-Footer-Pflicht greift)
- **Server:** `maxone-prod` (128.140.40.235, Hetzner)
- **Domain:** `kitchen.maxone.one` (TLS via DNS-01 Resolver `letsencrypt`)
- **Container:** `kitchen-station-app` (single, nicht Blue/Green — internes Tool)
- **Repo:** `maxone-one/kitchen-station` (private)
- **Deploy-Pipeline:** GitHub Actions self-hosted runner `voltfair-server` (pinned via `runs-on: [self-hosted, maxone-prod]` seit 2026-05-11)

## Drei Komponenten

```
┌──────────────────────────────────────────────────────────────────┐
│  TABLET (Lenovo IdeaTab TB336FU, 192.168.178.51, Android 15)     │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  com.maxone.kiosk v1.0.0 (foreground-app, Source verloren)│  │
│  │   ├─ WebView → https://kitchen.maxone.one                 │  │
│  │   └─ (vermutlich) Reverse-SSH-Tunnel via jBCrypt+JZlib    │  │
│  └────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
                              ↓ https
┌──────────────────────────────────────────────────────────────────┐
│  TRAEFIK (maxone-prod) — TLS Termination, Routing                │
└──────────────────────────────────────────────────────────────────┘
                              ↓ http
┌──────────────────────────────────────────────────────────────────┐
│  CONTAINER kitchen-station-app (nginx:alpine, single)            │
│   ├─ /             → index.html (Vanilla HTML/CSS/JS, ~210 KB)   │
│   ├─ /face.html    → Screensaver (Rive-Animation)                │
│   ├─ /list.html    → Einkaufsliste                                │
│   ├─ /version.txt  → Build-Timestamp (Unix-Epoch)                │
│   └─ /health       → "OK"                                        │
└──────────────────────────────────────────────────────────────────┘
```

## Features der Web-App (`1-Click/index.html`)

- **Home:** Uhrzeit, Wetter (OpenWeatherMap), 3-Tage-Vorschau, Hintergrundfoto (Unsplash, täglich wechselnd), 4 Schnellzugriff-Kacheln
- **Timer:** Presets + Custom, mehrere parallel, Audio-Alarm
- **Chat:** Gemini 1.5 Flash API
- **Musik:** Spotify Web Player
- **Einkaufsliste:** lokal + Spracheingabe (Web Speech API)
- **Mehr:** YouTube, WhatsApp Web, Google Keep, Kalender, Chefkoch, Umrechner
- **Einstellungen:** API Keys, Bitcoin-Adresse, Theme, Onboarding wiederholen
- **Wake Word "Hey Küche":** Web Speech API (kein nativer Wake-Word-Engine mehr, nachdem Picovoice Eagle in v1 noch geplant war)
- **Bitcoin-Feature:** zeigt €-Wert + 7-Tage-Chart (CoinGecko), Widmung "Mit ❤️ von Max"
- **Landscape-Lock:** CSS-Hint + JS-Warning bei portrait-Orientation; Kiosk-App locked das auf Manifest-Ebene
- **Auto-Update:** Polling von `/version.txt` alle 30s → bei Mismatch Hard-Reload zu `/?v=<timestamp>`

## Auto-Update-Flow

```
CI (GHA, deploy.yml)
  └─ date +%s > 1-Click/version.txt          (1)
  └─ docker build -t kitchen-station-app:latest .
  └─ docker compose up -d                     (2)
  └─ traefik-probe-fix.sh ...                 (3)

Web-App (im WebView auf Tablet)
  └─ poll /version.txt?t=now alle 30s         (4)
  └─ wenn timestamp ≠ localStorage['ks-build-v']:
       location.href = '/?v=<new-timestamp>'  (5)
  └─ Cache Storage API caches.delete(*) für vollständige Reload
```

**Kein Banner, keine User-Interaktion** — Kiosk-Modus, niemand klickt "Neu laden".

## Was NICHT Teil der Architektur ist

- **Kein VECTOR-Widget** (Standard 011 explicit ausgenommen — internes Tool)
- **Kein Standard-Footer** (Standard 012 explicit ausgenommen — kein Customer-facing-Traffic im klassischen Sinn)
- **Kein Vector-Chat** — die Web-App hat einen eigenen Gemini-Chat statt
- **Kein Supabase** — alles localStorage, keine Backend-DB
- **Kein Auth** — single-user-tablet, kein Login

## Sponsored-Customer-Implikation

Viktoria From bekommt nicht nur das Tablet + Web-App kostenlos, sondern auch das Postfach via Stalwart + Domain via Max → die Sponsored-Customer-Footer-Regel aus globaler CLAUDE.md greift für alle ausgehenden Mails ihres Postfachs. Das ist **nicht hier** implementiert (das gehört in `maxone.one`-Repo, Edge Function `email-client/handlers/send.ts`), aber konzeptionell verlinkt.

## Server-Pfade

- **Repo lokal:** `c:\Users\max\Projects\Kitchen Station`
- **Repo Server:** `/opt/kitchen-station` (nur docker-compose.yml + Build-Context aus CI gepushed)
- **Secrets:** `/opt/secrets/kitchen-station/` (Keystore für Kiosk-APK-Rebuild, falls je gebraucht)
- **Container-Mount:** keine Volumes (statische HTML im Image)

## Quellen / Belege

- Registry: `c:/Users/max/Projects/maxone-standards/registry/projects.yml`
- Bootstrap-PRD (historisch): `docs/archive/bootstrap-2026/PRD.md`
- docker-compose.yml: aktueller Stand in Repo
- Deploy-Workflow: `.github/workflows/deploy.yml`
