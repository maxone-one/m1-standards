# 017: Pflichtbausteine jeder Oberfläche (Impressum · Credits · Widget · Footer · Layout · Design-first)

**Status:** active
**Seit:** etabliert 2026-04-27, One-Liner-Pattern 2026-05-20
**Gilt für:** alle Customer-facing Projekte mit Impressum-Pflicht

## Inhalt

- [A] Impressum aus zentraler API
- [B] Credits aus zentraler API
- [C] Vector-Chat-Widget
- [D] Footer-Standard
- [E] Keine Scrollbalken (Layout-Qualität) + kein Mobile-Overflow (E.2)
- [F] Design-first-Validierung vor dem Bau (nie blind bauen)

---

## A: Impressum aus zentraler API

Das Impressum aller Projekte kommt aus der zentralen API:
```
https://panel.maxone.one/functions/v1/impressum
```

Niemals hardcoded. Cache: `{ next: { revalidate: 3600 } }`.

**Rechtslage (Stand 2026-05-16):** DDG §5 (ersetzt TMG seit 14.05.2024). Impressum muss HTML
sein, max. 2 Klicks erreichbar. Niemals PDF.

**Pflicht-Fallback:** bei API-Ausfall lokale Kopie zeigen, niemals "Impressum nicht
verfügbar".

**Pflicht-Felder:** `legal_name`, `street/zip/city`, `email`, `vat_id`/`w_id_nr`/`tax_id`.
Bei GmbH/UG/AG zusätzlich: `register_court`, `register_number`, `legal_form`.

**Die Kontaktadresse im Impressum ist IMMER `impressum@<property-domain>`** (Max-Direktive
04.08.2026), nie die allgemeine Kontaktadresse der Property und nie eine persönliche. Also
`impressum@griddone.de`, nicht `hallo@griddone.de`. Grund: Die Adresse steht öffentlich in
einem Pflichtdokument, wird abgegriffen und landet auf Listen; ein eigener Empfänger hält
das vom Arbeitspostfach fern und lässt sich getrennt filtern, ohne dass eine gesetzlich
verlangte Erreichbarkeit leidet.

**Vor dem Veröffentlichen ist die Adresse als zustellbar zu belegen, nicht anzunehmen.** Sie
liegt als Alias auf dem Stalwart-Principal der Property (Konvention `<dienst>@<domain>`).
Belegt wird per SMTP-Probe gegen `mail.maxone.one:25` mit `RCPT TO:<impressum@…>`: `250`
heißt zustellbar, `550 5.1.2 Mailbox does not exist` heißt, der Alias fehlt oder ist noch
nicht übernommen. **Ein Impressum mit nicht zustellbarer Kontaktadresse verfehlt §5 DDG.**

**Nach dem Anlegen eines Alias über die Stalwart-Management-API ist `GET /api/reload`
Pflicht.** Ohne den Reload steht die Adresse zwar im Principal, SMTP weist sie aber weiter
mit `550` ab, weil der Verzeichnis-Cache noch die alte Adressliste hält (belegt am
04.08.2026 an `impressum@griddone.de`).

**Die Stammdaten leben nicht nur im Impressum.** Die Datenschutzerklärung nennt denselben
Verantwortlichen mit Anschrift (Art. 13 DSGVO), teils auch der Footer. Jede dieser Stellen
bekommt dieselbe API-Anbindung und dieselben Element-IDs, sonst driftet sie gegen das
Impressum, sobald sich eine Anschrift ändert, und niemand merkt es.

**Statischer §36-VSBG-Block** (MUSS in jedem Impressum, kommt nicht aus API):
```html
<h2>Verbraucherschlichtung</h2>
<p>Wir sind nicht verpflichtet und nicht bereit, an Streitbeilegungsverfahren
vor einer Verbraucherschlichtungsstelle teilzunehmen.</p>
```

**Verboten:** ODR-Link (`ec.europa.eu/consumers/odr`), abmahnfähig seit 20.07.2025
(Plattform abgeschaltet). Auf `panel.maxone.studio` referenzieren (deprecated seit
2026-04-16). §5 TMG erwähnen, nur §5 DDG oder gar keinen Gesetzesverweis.

---

## B: Credits aus zentraler API

Jedes Projekt hat eine `/credits`-Route, die aus `https://maxone.one/api/credits/<slug>`
bezieht. Slug = Projekt-Name aus `registry/projects.yml`.

**Pflicht-Inhalt der `/credits`-Seite:** Studio-Info + CTA zu maxone.one, Tech-Stack (aus
API), Werte/Über-uns (aus `credits_global`), Link zu Impressum/Datenschutz.

---

## C: Vector-Chat-Widget

Jedes Customer-facing Projekt bindet das Widget über den Auto-Loader ein, **eine Zeile**,
nichts weiter:

```html
<script src="https://agent.maxone.one/widget/embed.js" async></script>
```

Am Ende von `<body>` oder im `<head>` mit `async`. Der Loader kümmert sich um Preconnect,
Preload, Widget-Script und `<vector-chat>`-Tag.

**Default-Hide-Liste** (eingebaut): `/impressum, /datenschutz, /agb, /widerruf, /privacy,
/imprint, /terms`. Override via `data-hide-on` (ersetzen), `data-hide-on-extra` (ergänzen)
oder `data-instance` (Persona manuell).

**Niemals:** Alte URL `agent.maxone.studio` (tot). Nur Widget-Script ohne
`<vector-chat>`-Tag (stiller Fehlschlag). Vector mit Restriction-Attributen einschränken
(`disabled` etc.), **Vector ist überall derselbe Vector**.

---

## D: Footer-Standard

Jedes Customer-facing Projekt hat einen Footer. Variante einmalig pro Projekt wählen, nie
mischen:

| Variante | Wann |
|---|---|
| **Mega** | Vollwertige Produkte mit Marketing-Seiten |
| **Slim** | Web-Apps, interne Tools, Platzhalter |

**Mega, Pflicht-Spalten:** 1. Brand & Kurz-Info (inkl. "Gehostet in Deutschland") · 2-4.
Navigation · letzte Spalte: Rechtliches (`/impressum`, `/datenschutz`, ggf. AGB)

**Mega Bottom-Bar:** `© <Jahr>` (dynamisch) · "Entwickelt von
[maxone](https://maxone.one)" · Version-Marker (`v: <BUILD_ID.slice(0,8)>` als Link auf
GitHub-Commit, siehe [025-ssot-und-versionsmarker.md](025-ssot-und-versionsmarker.md))

**Slim (einzeilig):**
```
© 2026 ProjektName · Impressum · Datenschutz · Entwickelt von maxone.one · v: abc12345
```

**Hide-Logik:** Footer nicht auf `/admin/*`, `/dashboard/*`, `/portal/*`, `/onboarding/*`,
Print.

**Attribution:** "Entwickelt von maxone.one" bei B2B-Projekten. "Ein Projekt von maxone.one",
wenn die Verbindung Marketing-Wert hat. **Die Marke wird IMMER voll ausgeschrieben**
(Max, 06.08.2026): nie das nackte "maxone", nie "Maxone" oder "MaxOne". Bis zu dieser
Korrektur stand hier zweimal die verkuerzte Form und hat sie in Projekte verteilt. NIEMALS
"maxone studio" (Wortmarke tot seit 2026-05-12).

**Skelette:** [`templates/footer/`](../templates/footer/), `Footer.tsx`, `FooterSlim.tsx`,
`GlobalFooter.tsx`, `Footer.svelte`, `FooterSlim.svelte`.

---

## E: Keine Scrollbalken (Layout-Qualität)

Ein Scrollbalken ist ein UI-Defektsignal, kein neutrales Bedienelement. Er bedeutet, dass zu
viel Inhalt auf zu wenig Platz gepackt oder der vorhandene Platz nicht effizient genutzt
wurde. Wo ein Scrollbalken erscheint, wurde das Layout nicht zu Ende gedacht.

**Regel:** Layouts so bauen, dass kein Scrollbalken entsteht. Dichte, mehrspaltige
Anordnung statt langer einspaltiger Listen (Grid statt Liste), kompakte Zeilen, vorhandenen
Platz bewusst ausnutzen. Bei viel Inhalt zuerst die Informationsdichte erhöhen (mehrspaltig,
gruppiert, klappbar), bevor überhaupt gescrollt wird.

**Pflicht-Check:** Vor jedem "fertig" bei UI-Arbeit prüfen, ob irgendwo ein Scrollbalken
entsteht. Wenn ja, ist die UI nicht fertig, sondern muss verdichtet werden. Diese Prüfung
gehört fest in den Verifikationsschritt jeder Frontend-Aufgabe. Direktive Max, mehrfach
gesagt, verbindlich ab 2026-06-09.

### E.2: Kein horizontaler Überlauf auf Mobile (schwimmende Layouts)

Schwimmende Layouts sind ein No-Go. Jede Seite MUSS bei Handy-Breite (Viewport <= 375px,
getestet bei 360 UND 320) ohne horizontalen Scroll und ohne seitliches Driften
funktionieren. Mobil wird mit dem Daumen bedient, jedes horizontale Überlaufen fällt sofort
auf. Laut Max der Default-Fehler bei KI-gebauten Seiten, muss aufhören.

**Häufigste Wurzel + Fix:**
- Responsive Grids: `grid-template-columns: repeat(auto-fit, minmax(min(Npx, 100%), 1fr))`,
  NIE `minmax(Npx, 1fr)`. Die feste Min-Breite kann sonst auf schmalen Screens nicht
  schrumpfen, die Spalte wird breiter als der Viewport.
- `* { min-width: 0; }` (Grid/Flex-Kinder überlaufen sonst via min-content).
- `img, video, svg, table { max-width: 100%; }`. Kein `100vw` (enthält die Scrollbar-Breite).
- Backstop: `html, body { overflow-x: hidden; }`, aber nur als Netz, die Wurzel muss trotzdem
  stimmen (sonst kaschiert es den Bug).
- SSoT-/Inline-JS, das Grids setzt: dieselbe `minmax(min(...,100%),...)`-Regel.

**Pflicht-Check (Playwright, Mobile-Viewport, nach Scroll bis unten):**
```js
const vw = document.documentElement.clientWidth;
const offenders = [...document.querySelectorAll('*')]
  .filter(el => { const r = el.getBoundingClientRect(); return r.right > vw + 1 || r.left < -1; });
// MUSS gelten: document.documentElement.scrollWidth <= vw  UND  offenders.length === 0
```
`getBoundingClientRect` deckt echten Überlauf auch unter `overflow-x:hidden` auf, also nicht
nur `scrollWidth` prüfen. Vorfall: maxone-Landingpages schwammen (`minmax(420px,1fr)`-Karten),
2026-06-24.

---

## F: Design-first-Validierung vor dem Bau

**Regel (Max-Direktive 2026-07-01, imperativ):** Jedes neue Projekt und jede neue
kundenseitige Oberfläche wird zuerst über ein visuelles Design-/Prototyping-Tool validiert,
bevor Produktionscode entsteht. **Niemals blind bauen.** Bestehende Projekte werden
retroaktiv nachgezogen (design-validiert und angeglichen), priorisiert nach Kundennähe und
UX-Wichtigkeit.

**Werkzeuge (gleichwertig, nach Kontext wählen):** **Claude Design** (claude.ai/design), Sync
zum Code über `/design-sync`, kein Zeichenlimit im Brief. **Figma Make / Figma-MCP**
(design-to-code und code-to-design), Prompt-Limit 2000 Zeichen, also verdichten. **Framer**
oder ähnliche visuelle Tools.

**Ablauf (Gate, verankert im CONCEPT → PLAN → Code-Fluss,
[023-gates-und-review.md](023-gates-und-review.md) und
[028-konzept-und-entscheidungen.md](028-konzept-und-entscheidungen.md)):**
1. Kern-Screens als Design/Prototyp erzeugen.
2. Prüfen: Optik, Flow, selbsterklärend, mobil, Vertrauen (Abschnitte A-E oben).
3. Erst nach OK bauen.

**Die Brief-Checkliste** (die neun Dimensionen, die ein Design-Werkzeug abfragt und die ein
guter Brief vorwegnimmt: Deliverable, Viewport-Priorität, Interaktivitätsgrad, Varianten,
Typografie-Richtung, Datenrealismus, Preisdarstellung, Domänen-Referenz, Look-Vorbild) und
die Werkzeug-Details zum Stack stehen im Wiki: `wiki/design/brief-checkliste.md`. **Eine
fremde Marke wird darin nie genannt**, der gewünschte Effekt wird neutral beschrieben
([019-marke-und-sprache.md](019-marke-und-sprache.md)).

---

## Audit

`scripts/audit.mjs` prüft pro Projekt:

| Prüfung | FAIL | WARN |
|---|---|---|
| **Impressum** | `ec.europa.eu/consumers/odr` im Code oder im Live-HTML (abmahnfähig) | `.studio`-Referenz; `Verbraucherschlichtung` bzw. §36-Block fehlt |
| **Credits** | `/credits`-Route fehlt oder ruft `maxone.one/api/credits/` nicht auf | — |
| **Widget** | `vector-chat.js` ohne `<vector-chat>`-Tag | `agent.maxone.studio` |
| **Footer** | Komponente fehlt (`Footer.{tsx,svelte,astro,vue}`) | kein Link auf `/impressum`, `/datenschutz` oder `maxone.one`; hardcodiertes Jahr statt `new Date().getFullYear()` |

Der Version-Marker im Footer wird über
[025-ssot-und-versionsmarker.md](025-ssot-und-versionsmarker.md) geprüft.

**Layout-Qualität (E) ist nicht statisch prüfbar**, ein Scrollbalken ist viewport- und
laufzeitabhängig. Deshalb ist der manuelle Review-Gate Pflicht: bei UI-Arbeit visuell auf
den üblichen Viewports prüfen, dass kein ungewollter Scrollcontainer entsteht. Optionaler
Heuristik-WARN: lange einspaltige `.map()`-Listen in Übersichts-Views ohne Grid-Wrapper als
Verdichtungs-Kandidaten melden.
