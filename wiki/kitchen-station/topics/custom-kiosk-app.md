---
topic: custom-kiosk-app
scope: kitchen-station
last_updated: 2026-05-11
---

# Custom-Kiosk-App `com.maxone.kiosk`

## Status (Stand 2026-05-11)

- **Installiert:** auf Tablet 192.168.178.51 (Lenovo IdeaTab TB336FU)
- **Version:** v1.0.0, versionCode=1
- **Installiert am:** 2026-03-30 11:54:35 (Update 13:17:55 selbiger Tag)
- **Signature:** SHA-256 `8344ad3b` (alte Signing-Identity, Source-Konsistent zum verloren gegangenen Build)
- **Foreground-Activity:** `com.maxone.kiosk/.MainActivity` (verifiziert via `dumpsys activity activities`)
- **Installer:** `null` → ADB-Sideload (nicht Play Store, nicht F-Droid)
- **APK-Größe:** ~7.6 MB
- **APK-Pfad auf Tablet:** `/data/app/~~v_fex5OHyscNJWawI7Il0A==/com.maxone.kiosk-vDSq70pOIxPBz3-xHoSfng==/base.apk`

## Was die App tut (rekonstruiert aus Bibliotheken im APK + Verhalten)

- **WebView-Kiosk** — startet beim Boot, lädt `kitchen.maxone.one`, zeigt sie fullscreen, blockt Home/Back-Buttons
- **SSH-Funktionalität** — APK enthält `jBCrypt` + `JZlib` Bibliotheken → reverse-SSH-Tunnel oder ähnliches (vermutlich für Remote-Wartung)
- **Auto-Reload-Integration** — Web-App pollt `/version.txt`, bei Mismatch `location.href` Cache-Buster — Kiosk leitet das durch ohne Eingriff
- **Permissions auf Tablet** (siehe [tablet-ops](tablet-ops.md)): braucht u.a. `SYSTEM_ALERT_WINDOW`, `RECORD_AUDIO`, `MODIFY_AUDIO_SETTINGS`, evtl. DeviceAdmin

## SOURCE-CODE STATUS: VERLOREN

> Original-Source der v1.0.0 lag auf **Vika's Notebook** in Wetzlar und ist verloren gegangen.
> Quelle: Commit-Body `0842b9d` (Repo `maxone-one/kitchen-station`, 2026-05-11 14:17).

**Was nicht existiert:**
- Kein GitHub-Repo (`maxone-one`, `maxone-studio-org`, `karastoni`, `maxone-studio` alle leer für "kiosk")
- Keine lokale Source-Dir auf NUC (`C:\Users\max\Projects\` — kein android/kiosk Verzeichnis)
- Kein Source auf maxone-prod, voltfair-cli
- Keine andere Backup-Spur

**Was existiert (Spuren):**
- Installierter APK auf Tablet (siehe Pfad oben) — kann mit `adb pull` extrahiert werden
- Commit `0842b9d` enthielt einen **Rebuild-Versuch** in `android-kiosk/` (Kotlin, AGP 8.2.2) — dieser wurde in Commit `a1d22db` wieder gelöscht (irrtümlich, mit Hallu-Begründung "Tablet runs Fully Kiosk"). Wiederherstellbar via `git revert a1d22db` ODER `git checkout 0842b9d -- android-kiosk/ .github/workflows/android-kiosk.yml`.

### Rebuild-Inhalt von Commit `0842b9d` (zur Referenz)

```
android-kiosk/
├── app/build.gradle.kts
├── app/proguard-rules.pro
├── app/src/main/AndroidManifest.xml
├── app/src/main/java/com/maxone/kiosk/
│   ├── AdminReceiver.kt           ← DeviceAdmin policies
│   ├── BootReceiver.kt            ← Auto-launch nach BOOT_COMPLETED
│   ├── KioskApplication.kt
│   ├── MainActivity.kt            ← WebView, landscape-lock
│   ├── SshTunnelService.kt        ← Foreground-Service für Reverse-SSH
│   └── update/
│       ├── ApkInstaller.kt
│       ├── InstallStatusReceiver.kt
│       ├── SelfUpdaterService.kt  ← Polls /kiosk-version.json alle 5min
│       └── UpdateChecker.kt
├── app/src/main/res/values/strings.xml
├── app/src/main/res/values/themes.xml
├── app/src/main/res/xml/device_admin.xml
├── app/src/main/res/xml/network_security_config.xml
├── app/src/main/res/xml/provider_paths.xml
├── build.gradle.kts
├── gradle.properties
└── settings.gradle.kts
+ .github/workflows/android-kiosk.yml  (GHA build on ubuntu-latest)
```

**Neue Signing-Identity im Rebuild** (NICHT identisch zur installierten APK):
```
SHA-256 05:F6:B7:A0:1A:41:21:DF:A2:0E:B1:62:45:50:32:D6:12:FD:F6:36:F1:C8:F3:E2:79:CF:02:45:0A:4A:BB:FC
```
Master-Copy des Keystore: `/opt/secrets/kitchen-station/` auf maxone-prod (referenziert im Commit).

## Update-Pfad (geplant, nie aktiviert)

Der Rebuild hatte `SelfUpdaterService` der `kitchen.maxone.one/kiosk-version.json` alle 5 min pollt, APK SHA-256 verifiziert, via `PackageInstaller` silent installiert (braucht DeviceOwner-Status — einmaliges `adb shell dpm set-device-owner com.maxone.kiosk/.AdminReceiver` während Install).

**Aktuell auf dem Tablet:** kein OTA-Update-Mechanismus aktiv. Wenn die Kiosk-App selbst aktualisiert werden muss → neue APK per `adb install -r` aufspielen. Da Source aber verloren ist, kann derzeit keine neue Version gebaut werden.

## Wenn die App ausfällt

1. **Tablet hängt im Bootloop** → Recovery via ADB, Kiosk-App via `adb uninstall com.maxone.kiosk` deinstallieren, dann Tablet läuft mit Default-Launcher
2. **App startet aber zeigt weiße Seite** → wahrscheinlich `kitchen.maxone.one` nicht erreichbar; im WebView-Kiosk kann man kaum debuggen ohne Source/Remote-Debug
3. **Web-App-Update bricht App** → Polling im `index.html` Zeile ~2802 deaktivieren via Git-Revert auf alten Build, neu deployen

## Reverse-Engineering bei Bedarf

Wenn der echte Source rekonstruiert werden muss:
1. APK pullen: `adb pull /data/app/.../com.maxone.kiosk-*/base.apk`
2. Decompile mit `apktool d` (Resources) + `jadx-gui` (Java/Kotlin)
3. Manuell Kotlin-Projekt um den decompiled Code bauen
4. Vergleichen mit dem im Commit `0842b9d` gemachten Rebuild — vermutlich 70–90% Überlapp

## Quellen / Belege

- ADB-Output via `pm path`, `dumpsys package`, `dumpsys activity activities` (2026-05-11 17:20 lokale Zeit)
- Commit `0842b9d` (Body): "Old com.maxone.kiosk v1.0.0 source was lost (was on Vika's notebook)"
- Commit `a1d22db`: Löschung des Rebuild-Trees (Begründung war falsch — Hallu)
- APK-Bibliotheken via `unzip -l`: jBCrypt, JZlib, kotlinx_coroutines, androidx.*
