# 011: Live-Domain-Audits (DSGVO-Tracker · Bundle-Drift)

**Status:** active
**Seit:** 2026-04-27
**Gilt für:** alle Projekte mit `status: live` und öffentlicher Domain

## Inhalt

- [A] DSGVO-Tracker- und Drittdienst-Audit
- [B] Bundle-Drift-Audit

---

## A: DSGVO-Tracker-Audit

Beim Initial-Load der Live-Domain dürfen KEINE personenbezogenen Daten (IP-Adresse, Cookies, Browser-Fingerprint) an Drittdienste fließen, bevor der Nutzer eingewilligt hat.

**Konkrete Pflichten:**
- **Google Fonts:** lokal via `@fontsource/*` oder self-hosted `.woff2`, niemals CDN ohne Consent
- **Tracker (GA, GTM, Facebook Pixel):** erst nach Consent laden (Consent-Mode v2 oder Consent-Banner)
- **Externe Embeds (YouTube, Vimeo, Maps):** Two-Click-Lösung oder `youtube-nocookie.com`
- **Maps:** OpenStreetMap (Leaflet/MapLibre) + self-hosted Tiles statt Google Maps

**Whitelist (kein Consent nötig):** `*.maxone.one`, eigene Subdomains, `fonts.bunny.net`, `analytics.maxone.one` (Umami self-hosted). **Die Freistellung von Umami gilt nur, solange dorthin nichts Personenbezogenes fließt**, siehe A-2.

**Warum:** DSGVO Art. 6 + TTDSG §25. LG München I (2022): Google Fonts via CDN ohne Consent = rechtswidrig, Schadensersatz pro betroffene IP. Vibe-Coding-Plattformen bauen Google Fonts standardmäßig ein.

**Manueller Check (bei Gate 3):** Webbkoll (`webbkoll.dataskydd.net`), DevTools Network-Tab vor und nach Consent-Klick.

### A-2: Kennung im Pfad, und Umami schickt sie mit (seit 12.08.2026)

**Eine Seite mit einer Kennung im Pfad darf nicht ohne Maskierung getrackt werden.** Betroffen ist jeder Pfad mit UUID, Vorgangs-, Kunden-, Auftrags- oder Rechnungsnummer, jedem Token und jedem Slug, der auf eine Person zurückführt.

**Der Grund, und er ist der eigentliche Punkt:** Es genügt nicht, das eigene Ereignis sauber zu halten. Das Umami-Skript **vervollständigt die Nutzlast selbst** und hängt `url`, `referrer` und `title` aus der laufenden Seite an, bevor es sendet. Ein `umami.track()` mit einwandfreiem Daten-Objekt überträgt die Kennung im Pfad also trotzdem, bei jedem einzelnen Ereignis, verkettbar zu einem Bewegungsprofil je Vorgang.

**Pflicht:** `data-before-send` setzen und dort Pfad **und** Referrer maskieren. Drei Fallen, die beim Bau alle drei zugeschlagen haben:

| Falle | Was passiert |
|---|---|
| Signatur `(typ, nutzlast)`, nicht `(nutzlast)` | die Funktion greift ins Leere, es wird nichts maskiert |
| `url` absolut behandelt statt als Pfad | die Maskierung trifft nie |
| falsy Rückgabewert | Umami unterdrückt das Ereignis **ganz**, die Messung fällt lautlos aus |

**Der Riegel muss die Maskierfunktion AUSFÜHREN, nicht das Attribut greppen.** Das ist die verallgemeinerbare Hälfte: Ein Test, der prüft, ob ein `data-before-send` im Markup steht, oder der nur das zweite Argument von `track()` untersucht, prüft genau den Teil, der nie das Problem war. Er macht die Lücke unsichtbar und damit überlebensfähig.

**Und die Prüfung greift am ausgelieferten Bundle, nicht am Quelltext.** Aufgefallen ist der Fehler nur, weil jemand das echte `script.js` abgerufen hat. Gleiche Bewegung wie Teil B dieses Standards.

**Die Regel über Umami hinaus:** Wo eine fremde Bibliothek die Nutzlast **vervollständigt**, reicht saubere eigene Übergabe nicht. Dann gilt die Prüfung dem, was den Rechner verlässt, nie dem, was der Aufruf übergibt. Betrifft jedes Analytics-, Fehler- und Session-Werkzeug (Sentry mit `beforeSend`, jedes Replay-Werkzeug).

**Prüffrage bei jedem Live-Audit:** Gibt es in diesem Projekt eine Seite mit einer Kennung im Pfad und einem Umami-Tag? Wenn ja, geht die Kennung heute mit, solange kein `data-before-send` läuft.

**`data-exclude-path` gibt es nicht.** Am ausgelieferten `analytics.maxone.one/script.js` erhoben (12.08.2026): Das Skript liest genau `website-id`, `host-url`, `before-send`, `tag`, `auto-track`, `do-not-track`, `exclude-search`, `exclude-hash`, `domains`, `fetch-*`. **Ein Attribut, das nicht in dieser Liste steht, wird stillschweigend ignoriert**, und ein ignoriertes Attribut sieht im Markup aus wie ein wirksamer Riegel. In `maxone.one` stand `data-exclude-path="/admin/**"` seit dem 12.05.2026 und hat nie etwas ausgeschlossen: gemessen **2.309 Admin-Aufrufe** in der Umami-Datenbank, bis zum Tag der Messung. Wer einen Pfad ausschließen will, tut das in `data-before-send`, sonst nirgends.

**Die Liste wird nicht abgeschrieben, sondern erhoben**, denn sie hängt an der laufenden Umami-Version:

```bash
curl -s https://analytics.maxone.one/script.js | grep -o '.\{60\}before-send.\{80\}'
```

*Anlass: Code-Review griddone Phase 6.2 am 12.08.2026, sechs Ereignisse unter `/vorgaenge/<UUID>`. Volltext: `griddone/.planning/phases/06.2-gefuehrter-einreichungsweg-netzbetreiber/06.2-REVIEW.md`, CR-01.*

---

## B: Bundle-Drift-Audit

Das live ausgelieferte JS/CSS-Bundle darf nicht enthalten:

- **Veraltete Hostnamen** aus Migrationen (z.B. `panel.maxone.studio`, `agent.maxone.studio`, Migration auf `.one` abgeschlossen 2026-04-16)
- **Source-Maps** in Production (`.map`-Dateien öffentlich abrufbar)
- **Plattform-Wasserzeichen** der Blacklist-Anbieter (`lovable`, `bolt.new`, `base44`, `built with v0`, `replit-agent`)
- **Dev-Hosts und Loopback-URLs** (`localhost:`, `127.0.0.1:`, `host.docker.internal`)
- **Hardkodierte Secrets oder Service-Role-Keys** im gebauten Bundle

**Build-Settings um Source-Maps zu verhindern:**
- Vite: `build.sourcemap: false`
- SvelteKit: `vite.build.sourcemap: 'hidden'` (für Sentry-Upload), nie public
- Next.js: `productionBrowserSourceMaps: false`

**Bei jeder Migration:** Build-Cache leeren (`.vite/`, `.next/cache/`), neu bauen, Audit gegen **Live-Domain** laufen lassen (nicht Repo).

**Warum, Vorfälle:**
- repivot: nach `.studio`→`.one`-Migration lud Browser weiter `panel.maxone.studio/functions/v1/impressum` wegen altem Vite-Cache
- maxone.one: 2 Wochen Source-Maps im Bundle durch `--sourcemap=true` im Prod-Build → TypeScript-Quellcode öffentlich
- Lovable/Bolt-Watermark im Bundle = verlässlicher Indikator für umgangene Verbots-Liste

---

## Audit

`scripts/audit.mjs` prüft pro Projekt mit `status: live` + Domain (mit `--local-only` übersprungen):

**Tracker (A):**
1. Fetch `https://<domain>/` mit Timeout 10s
2. HTML auf bekannte Tracker-Patterns scannen:
   - `fonts.googleapis.com`, `fonts.gstatic.com` → **WARN**
   - `google-analytics.com`, `googletagmanager.com` → **WARN**
   - `connect.facebook.net`, `facebook.com/tr` → **WARN**
   - Hotjar, Mixpanel, Segment, Amplitude, Intercom → **WARN**
   - YouTube, Vimeo, Google Maps (direkt im HTML) → **WARN**

**Bundle-Drift (B):**
1. Fetch `https://<domain>/` + bis zu 8 Assets fetchen (5s Timeout pro Asset)
2. Pro Asset scannen:
   - `*.maxone.studio` → **WARN**
   - `//# sourceMappingURL=` → **WARN**
   - `lovable`, `bolt.new`, `base44`, `built with v0`, `replit-agent` → **FAIL**
   - `localhost:`, `127.0.0.1`, `host.docker.internal` → **WARN**
   - Service-Role-Key-Pattern (`"role":"service_role"`) → **FAIL**
