---
topic: tablet-ops
scope: kitchen-station
last_updated: 2026-05-11
---

# Tablet-Operations

## Hardware

| Position | Wert |
|----------|------|
| Modell | Lenovo IdeaTab TB336FU, 11", 8 GB RAM, 128 GB |
| Android | 15 |
| IP (fest) | 192.168.178.51 (Fritzbox) |
| ADB-Port | wechselt, aktuell in `1-Click/config.txt` |
| ADB-Tool | `C:\Users\max\adb\adb.exe` |
| Standort | Viktoria From, Wetzlar |
| Lautsprecher | Soundcore Motion 300, mit Tablet gekoppelt |

## ADB-Cheat-Sheet

```powershell
# Über mDNS/WiFi connect (Tablet muss auf demselben WLAN sein wie der ausführende Rechner)
C:\Users\max\adb\adb.exe devices

# Falls Verbindung verloren — port wieder herstellen
C:\Users\max\adb\adb.exe connect 192.168.178.51:<PORT-aus-config.txt>

# Welche Pakete sind installiert
C:\Users\max\adb\adb.exe shell pm list packages

# Welche App ist gerade vorn
C:\Users\max\adb\adb.exe shell dumpsys activity activities | grep topResumedActivity

# Kiosk-App-Infos
C:\Users\max\adb\adb.exe shell dumpsys package com.maxone.kiosk | grep -E "versionName|lastUpdateTime|installerPackageName"

# APK pullen (für Reverse-Engineering)
C:\Users\max\adb\adb.exe shell pm path com.maxone.kiosk
C:\Users\max\adb\adb.exe pull /data/app/<pfad>/base.apk ./kiosk.apk

# App-Cache/Daten leeren (NICHT pm clear ohne Not — verliert localStorage der Web-App!)
C:\Users\max\adb\adb.exe shell pm clear com.maxone.kiosk     # ZERSTÖRT WebView-State

# Permissions für Kiosk-App setzen (nach Neuinstall)
C:\Users\max\adb\adb.exe shell pm grant com.maxone.kiosk android.permission.SYSTEM_ALERT_WINDOW
C:\Users\max\adb\adb.exe shell pm grant com.maxone.kiosk android.permission.RECORD_AUDIO

# Screenshot ZIEHEN (immer zweistufig — PowerShell-Pipe zerstört Binär)
C:\Users\max\adb\adb.exe shell screencap -p /sdcard/screen.png
C:\Users\max\adb\adb.exe pull /sdcard/screen.png .

# Tablet rebooten
C:\Users\max\adb\adb.exe reboot
```

## Bloatware-Whitelist (NIEMALS entfernen)

```
com.android.*
com.google.*
android.*
com.lenovo.penservice    # Stift-Unterstützung für Viktoria
com.lenovo.pen.*
com.maxone.kiosk         # die Kiosk-App selbst (klar)
```

## Bereits entfernte Pakete (25 Stück, dokumentiert)

```
com.lenovo.lsf.device         com.lenovo.tab_extreme        com.tblenovo.tabpushout
com.lenovo.ue.device          com.lenovo.idea_tab           com.tblenovo.setup
com.lenovo.screensaver        com.lenovo.screensplit        com.lenovo.ota
com.dolby.daxservice          com.lenovo.EngineeringCode    com.tblenovo.setup.overlay
com.lenovo.appdaily           com.lenovo.ocpl               com.lenovo.weathercenter
com.tblenovo.lenovowhatsnew   com.lenovo.tbengine           com.opera.preinstall
com.lenovo.lenovoprivacy      com.opera.browser             com.tblenovo.ue.config
com.lenovo.dsa                com.lenovo.lsf                com.tblenovo.center
```

(Quelle: `docs/archive/bootstrap-2026/PRD.md` § 7. `com.lenovo.penservice` wurde versehentlich entfernt und via `pm install-existing` wiederhergestellt → daher in der Whitelist.)

## Setup-Script (`1-Click/setup.ps1`)

Aktueller Stand (nach 2026-05-11-Cleanup): ADB-Connect + Bloatware-Entfernung + Personalisierung. **Installiert NICHT mehr Fully Kiosk** (verbannt 2026-03-30). Endet mit Check, ob `com.maxone.kiosk` installiert ist; wenn nicht, Hinweis "APK manuell aufspielen (APK-Quelle bei Max)".

## Screenshot-Workflow (User-Direktive)

**IMMER zweistufig:** `screencap` → `pull`. **NIE** `adb shell screencap -p | Out-File` (PowerShell-Pipe zerstört Binärdaten).

## Tablet-Reset / Neu-Aufsetzen

Falls Tablet komplett neu aufgesetzt werden muss:
1. ADB-Connect herstellen (siehe oben)
2. `1-Click/setup.ps1` laufen lassen — Bloatware + Personalisierung
3. **Manuell**: `com.maxone.kiosk` APK aufspielen → `adb install kiosk.apk` (APK liegt bei Max; Source verloren — siehe [custom-kiosk-app](custom-kiosk-app.md))
4. Permissions setzen (`pm grant com.maxone.kiosk android.permission.SYSTEM_ALERT_WINDOW` etc.)
5. **DeviceOwner setzen** (falls Self-Update-Service je aktiviert wird): `adb shell dpm set-device-owner com.maxone.kiosk/.AdminReceiver` — nur möglich solange keine Accounts auf dem Gerät registriert sind!
6. Tablet rebooten → Kiosk übernimmt automatisch beim Boot

## Wake-Word / Voice

Web-App nutzt **Web Speech API** (SpeechRecognition + speechSynthesis). Voraussetzung: `RECORD_AUDIO`-Permission für die Kiosk-App, weil WebView die Permission vom Host-Container braucht.

Frühere `fully.*`-API-Calls für Speech (Bootstrap-Phase) sind seit 2026-05-11 entfernt. Wenn Speech nicht funktioniert:
1. Permission prüfen: `adb shell dumpsys package com.maxone.kiosk | grep RECORD_AUDIO`
2. Chrome-Origin-Trial sicherstellen (Web Speech API ist in Chromium-WebView nicht überall stabil)
3. Bei Bedarf Picovoice oder Vosk als nativer Wake-Word-Engine — wäre aber neue Kiosk-APK-Version (Source verloren)

## Quellen

- Bootstrap-PRD § 8 (ADB-Cheat-Sheet, verschlankt)
- Memory `feedback_adb_screencap.md` (Screenshot-Workflow)
- ADB-Live-Output 2026-05-11
