# Kitchen-Station Bug-Protokoll

Referenzliste aller bekannten Bugs — chronologisch, mit Root-Cause und Fix.
**Vor jedem Bugfix zuerst hier nachschlagen**, ob das Problem schon bekannt ist.

---

## BUG-001 — Onboarding-Screen hängt trotz `ks-ob`-Injection im Deploy (2026-05-18)

**Symptom:** Tablet zeigt immer noch den Onboarding-Screen, obwohl `co()` mit `ks-ob`-Bypass bereits deployed ist.

**Root-Cause:** Service Worker v1 hatte die alte `/`-Response ohne `ks-ob`-Injection gecacht. Auto-Update-Navigationen zu `/?v=<ts>` wurden vom SW abgefangen und aus dem alten Cache bedient. Der neue Code kam nie an.

**Fix:** Deeplink-Trick — lädt `/callback?vN` frisch vom Server (kein SW-Cache-Eintrag für `/callback`), SW v2 installiert sich, löscht alle alten Caches.

```powershell
& "C:\Users\max\platform-tools\adb.exe" -s 192.168.178.52:37131 shell `
  "am start -n com.maxone.kiosk/.MainActivity -a android.intent.action.VIEW -d 'https://kitchen.maxone.one/callback?v=1'"
```

**Wiedererkennung:** Onboarding-Screen hängt nach Deploy — immer zuerst prüfen, ob SW alten Cache hat.

---

## BUG-002 — Wake-Word-Detektor reagiert nie auf „Hey Küche" (2026-05-18)

**Symptom:** User sagt „Hey Küche", nichts passiert. Keine Reaktion, kein Fehler sichtbar.

**Root-Cause (Stufe 1 — Fehlendes Feedback):** `catch(e){}` im `ondataavailable`-Handler hat alle Gemini-Fehler stumm geschluckt. Wurde zur Diagnose sichtbar gemacht (vbar zeigt Fehler 4s lang).

**Root-Cause (Stufe 2 — Echter Bug):** Android WebView verwendet **CBR Opus** (ca. 70kbps, ergibt ~4.390 Bytes/500ms-Chunk). Das blob-size-VAD-System (`_WWD_VOICE_BYTES`) kann CBR-Chunks nicht von Stille unterscheiden:
- Alle Chunks ≥ Schwellwert → immer als „Sprache" klassifiziert
- `_wwd.silentCount` erreicht nie `_WWD_SIL_CHUNKS`
- Gemini wird **nie** aufgerufen
- `_wwd.speechChunks` wächst ins Unendliche

**Diagnose:** Debug-Overlay (grünes Pill unten rechts, `id="wwd-dbg"`) eingefügt — zeigte `4390b V buf=18` → 18 Chunks akkumuliert, alle als „Voice" klassifiziert, nie abgesendet.

**Fix:** Blob-Size-VAD durch **3-Sekunden-Rolling-Window** ersetzt:
- `setInterval(3000)` sendet alle 3s den akkumulierten Clip an Gemini
- Kein VAD mehr nötig — funktioniert mit CBR und VBR
- Commit: `0b76485`

**Commits:**
- `c98232e` — Threshold 1500→400, audioBitsPerSecond:64000, Debug-Overlay, Error-Visibility
- `b372475` — Debug-Overlay-Font auf 14px (lesbar im Screenshot)
- `0b76485` — Rolling-Window-Rewrite (echter Fix)

**Wiedererkennung:** WWD reagiert nie → Debug-Overlay anschauen. Wenn `buf=N` immer größer wird ohne zu resetten → Gemini wird nie aufgerufen → Rolling-Window defekt.

---

## BUG-003 — Auto-Update pollt version.txt, aber Mismatch löst keinen Reload aus (2026-05-18)

**Symptom:** Nach CI-Deploy macht das Tablet keine Requests an den Server (oder sieht keinen Mismatch).

**Root-Cause:** Bei manuellem Debug wurde `version.txt` auf dem Server auf `1779199999` gebumpt. Nach erneutem Deploy setzte CI `version.txt` auf `1779119346` zurück — kleiner als die manuell gebumpte Zahl, aber das Tablet hatte `1779199999` gespeichert. Mismatch vorhanden, reload feuerte.
Bei anderen Fällen: Tablet hatte exakt die Build-ID des neuen Deploys schon in `localStorage` (weil `KS_BUILD` im neuen HTML passte) → kein Mismatch.

**Fix:** Zum Erzwingen eines Reloads: `version.txt` manuell auf `1999999999` setzen:
```powershell
ssh -i "C:\Users\max\.ssh\id_ed25519" root@128.140.40.235 `
  "echo '1999999999' | docker exec -i kitchen-station-app sh -c 'cat > /usr/share/nginx/html/version.txt'"
```
Danach wird die nächste CI-Build-ID kleiner sein → erneuter Mismatch → Reload.

**Wiedererkennung:** Tablet macht keine Requests nach Deploy → `version.txt` prüfen vs. `localStorage['ks-build-v']` auf dem Tablet.

---

## BUG-004 — `run-as com.maxone.kiosk` schlägt fehl (2026-05-18)

**Symptom:** `adb shell run-as com.maxone.kiosk` gibt Fehler zurück.

**Root-Cause:** Das APK ist nicht mit `debuggable=true` signiert. Chrome DevTools Remote Debugging für den WebView funktioniert damit ebenfalls nicht.

**Workaround:** Debug-Overlays direkt im JS-Code implementieren (`id="wwd-dbg"`) und per ADB-Screenshot auslesen.

**Wiedererkennung:** Immer wenn JS-Debugging im WebView nötig scheint → sichtbares Overlay einbauen, Screenshot ziehen.

---

## BUG-005 — GitHub Actions nutzt `ubuntu-latest` (bezahlte Minuten) statt Self-Hosted Runner

**Symptom:** CI-Kosten laufen auf, deploys schlagen fehl mit Billing-Fehler.

**Root-Cause:** Workflow hat `runs-on: ubuntu-latest` statt `[self-hosted, maxone-prod]`.

**Fix:** Alle `runs-on` in `.github/workflows/deploy.yml` auf `[self-hosted, maxone-prod]` umstellen.

**Wiedererkennung:** Bei jedem Drift-Check: `grep -rn 'runs-on: ubuntu' .github/` → sofort fixen.

---

## BUG-006 — `pm clear` und `am force-stop` für com.maxone.kiosk blockiert (2026-05-18)

**Symptom:** ADB-Befehle `pm clear` und `am force-stop` für `com.maxone.kiosk` werden verweigert.

**Root-Cause:** Device Owner ist gesetzt — schützt die Kiosk-App vor Stopp und Datenlöschung.

**Workaround:** App neu starten via Deeplink (`am start -n com.maxone.kiosk/.MainActivity -a VIEW -d 'https://...'`).

---

## BUG-007 — WWD-Fehler-Banner flackert ständig: Gemini Rate-Limit (2026-05-18)

**Symptom:** Oben ein roter Banner erscheint und verschwindet dauerhaft (~alle 4s): „You exceeded your current quota… limit: 20, model: gemini-2.5-flash, Please retry in 46s". App „flippt aus".

**Root-Cause:** Rolling-Window mit 3s-Interval = 20 RPM = exakt das Gratis-Limit von Gemini Free Tier (gemini-2.5-flash). Jeder minimale Verarbeitungs-Overhead (Netzwerk, JS-Tick) pusht drüber → 429 → Fehler-Banner 4s → nächster Call → 429 → Dauerflackern.

**Fix:** Commit `b654576`
- Interval 3000 → 5000ms (12 RPM, sicherer Abstand)
- Bei 429-Fehler: `_wwd.pauseUntil = Date.now() + 65000` → 65s Stille, Chunks verwerfen
- Debug-Overlay zeigt Countdown während Pause
- HTTP-Status im Error-String für zuverlässige 429-Erkennung

**Wiedererkennung:** Banner erscheint rhythmisch alle 4-8s mit „quota" / „exceeded" → Rate-Limit. Prüfen: Interval zu kurz, oder Key hat zu wenig Quota.

---

## BUG-008 — Gemini-Polling falsche Architektur für Wake-Word (2026-05-18)

**Symptom:** „Hey Küche" reagiert nie zuverlässig — 5-8s Latenz, Rate-Limit-Pausen, Datenschutzproblem, kein echter On-Device-VAD möglich (CBR-Codec).

**Root-Cause:** Gemini REST-API ist für Continuous Listening architektonisch falsch:
- 5s-Rolling-Window = 12 RPM → trifft Gratis-Limit bei minimalem Overhead
- Latenz 5-8s pro Erkennungsversuch — untragbar für Wake-Word-UX
- Android WebView Opus = CBR → blob-size-VAD unmöglich, Gemini wird immer gerufen
- Gesamtes Küchenaudio geht ungefilter zu Google

**Fix:** Commit `1725df4` — Android-nativer `SpeechRecognizer` (v1.4.0)
- `WakeWordDetector.kt`: kontinuierlicher SpeechRecognizer de-DE, Partial Results, Auto-Restart
- `KioskBridge.kt`: `stopWakeWord()` / `resumeWakeWord()` als JS-Interface
- `index.html`: `startWakeWordDetector()` prüft zuerst `window.kitchen.resumeWakeWord` → nativer Pfad. Gemini-Pfad bleibt als Fallback für Desktop-Browser.
- Latenz: < 1s (on-device VAD, kein Netzwerk)
- Kosten: 0 (Android-OS-API, kein externen Service)

**Wiedererkennung:** Wake-Word mit Gemini-Polling = immer dieser Bug-Cluster. Nicht nochmal versuchen.

**Fallback-Option (falls SpeechRecognizer nicht verfügbar):** Gemini Live Streaming API (WebSocket, ein persistenter Stream statt Polling).

---

## Debug-Cheatsheet

| Problem | Erste Anlaufstelle |
|---|---|
| Onboarding hängt nach Deploy | Deeplink `/callback?vN` |
| WWD reagiert nicht | Screenshot → `wwd-dbg`-Overlay lesen |
| Auto-Update feuert nicht | `version.txt` auf `1999999999` bumpen |
| JS-Fehler im WebView | `wwd-dbg`-Overlay (zeigt Fehler 4s) |
| Tablet nicht erreichbar | ADB-Port aus `tablet_heartbeat`-Tabelle lesen |
| Gemini-Fehler | Vbar blinkt kurz mit „WWD-Fehler: …" |
