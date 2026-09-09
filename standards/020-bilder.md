# 020: Bilder (Verarbeitungs-Pipeline · Herstellerquellen)

**Status:** active
**Seit:** 2026-05-20 (Pipeline), 2026-05-30 (Herstellerquellen), zusammengeführt 2026-09-09
**Gilt für:** alle maxone-Properties; Abschnitt B zusätzlich für jedes Projekt, das
Hersteller-Logos oder Produktbilder Dritter zeigt

> **Herkunft:** Diese Nummer führt zusammen, was bis zum 09.09.2026 als
> `027-image-pipeline.md` und `030-manufacturer-assets.md` getrennt lag. Beide beantworten
> dieselbe Frage: **Wie kommt ein Bild sauber auf eine maxone-Seite?** Die zweite Nummer war
> nur entstanden, weil die erste schon vergeben war.

## Inhalt

- [A] Verarbeitungs-Pipeline für hochgeladene Bilder
- [B] Logos und Produktbilder von Drittherstellern beziehen

---

## A: Verarbeitungs-Pipeline

Jedes hochgeladene Bild auf einer maxone-Property MUSS durch eine zentrale
Verarbeitungs-Pipeline laufen, die

1. Original-EXIF/IPTC/XMP komplett strippt (Privacy + Konsistenz)
2. maxone-Brand-EXIF einschreibt (Provenance + Trust)
3. JPEG mit mozjpeg als Speicher-Format nutzt
4. Auslieferung an Browser über Next.js AVIF/WebP-Optimization

**Warum:** **Privacy**, hochgeladene Bilder enthalten GPS-Koordinaten, Geräte-IDs und
Software-Signaturen und dürfen nie public werden. **Brand-Konsistenz**, Bilder auf jeder
Property tragen dieselbe EXIF-Spur. **Performance**, AVIF reduziert LCP um 200-500 ms
gegenüber JPEG. **Recht**, der Copyright-Vermerk dokumentiert die Urheberschaft für
Stock-Site-Uploads, Backup-Recovery und externe Embed-Fälle.

### Server-seitig (Upload-Verarbeitung)

```ts
// lib/images/process-upload.ts (oder gleichwertig)
export async function processBrandImage(
  buffer: Buffer,
  options?: { width?: number; quality?: number }
): Promise<Buffer>
```

Pflicht-Verhalten: JPEG re-encode (strippt alle Original-Metadaten), optional Resize via
`width`, mozjpeg-Encoder mit Quality default 90 und min 80, EXIF schreiben via sharp
`.withExif()`:

| EXIF-Feld | Wert | EXIF-Feld | Wert |
|---|---|---|---|
| Make | `Sony` | ISOSpeedRatings | `200` |
| Model | `ILCE-7M4` | ExposureTime | `1/250` |
| LensMake | `Sony` | Artist | `Max Karastelev` |
| LensModel | `FE 24-70mm F2.8 GM II` | Copyright | `© maxone.one` |
| FocalLength | `35` | Software | `Adobe Lightroom Classic` |
| FNumber | `2.8` | | |

Der Helper MUSS an JEDER Upload-Server-Action verwendet werden. Direkter
`sharp(buffer).jpeg(...).toBuffer()` ohne EXIF-Block ist nicht erlaubt.

### Framework-Config (Next.js)

`next.config.ts` MUSS enthalten:

```ts
images: {
  formats: ["image/avif", "image/webp"],
  minimumCacheTTL: 31536000,
  // remotePatterns nach Projekt-Bedarf
},
```

`formats` steht standardmäßig nur auf `image/webp`, AVIF muss explizit aktiviert werden.
`minimumCacheTTL` steht default auf 60 s, für immutable Bild-URLs viel zu kurz; ein Jahr ist
der Industrie-Wert.

### Ausnahmen

- **User-Avatare / Bewerbungsfotos:** Strip ja, Brand-EXIF nein (semantisch falsch, das sind
  keine maxone-Bilder)
- **Logo-Uploads (Provider/Hersteller):** Strip ja, Brand-EXIF nein
- **Screenshots (Pioneer-Feedback `/melden`):** Bleibt PNG, kein Re-Encode
- **Externe URLs** (Datenblatt-PDFs, Hersteller-Logos via `remotePatterns`): Pipeline nicht
  anwendbar

---

## B: Logos und Produktbilder von Drittherstellern

Logos und Produktbilder von Drittherstellern werden **nicht geraten, nicht generiert und
nicht hot-linked** von zufälligen URLs. Sie werden systematisch bezogen: Logos über
offizielle Presseseiten oder Website-Inspektion, Produktbilder über die Hersteller-
Produktseiten per Playwright.

### Logos: Bezugsreihenfolge

1. **Pressebereich / Media Kit** (bevorzugt). Suchmuster:
   `"<Hersteller>" press media kit logo download site:<domain>`
2. **Website-Inspektion mit Playwright**, Bilder im Header nach `/logo/i` in `src`, `alt`
   oder `className` filtern und nach `naturalWidth` bewerten.
3. **Bekannte stabile URLs**, siehe Wiki-Seite unten.

**Speicherung:** SVGs lokal unter `public/logos/<slug>.svg`, **nie hot-linken**, URLs ändern
sich ohne Vorwarnung. `manufacturers.logo_url` zeigt auf den lokalen Pfad
`/logos/<slug>.svg`. Tochtergesellschaften erben das Logo der Muttergesellschaft.

### Produktbilder: Bezugsreihenfolge

1. **JSON-LD `Product`-Schema** (bevorzugt für JS-gerenderte Shops wie Hager/Magento).
   Funktioniert auch bei lazy geladenen Bildern, kein `data-src` nötig.
   `p.image[0]` ist das Hauptbild, `p.sku` die interne SKU.
2. **`data-zoom`-Attribut**, für traditionelle Produktseiten (Theben, MDT).
3. **WordPress `wp-content/uploads/`**, dort listen WP-basierte Sites (Zennio) alle
   Thumbnails direkt im Listing-Grid.
4. **Bekannte URL-Muster je Hersteller**, siehe Wiki-Seite unten.
5. **Fallback:** eibhandel.de oder knxwarehouse.com, für Produkte ohne eigene Herstellerseite.

```js
// Auf der Hersteller-Produktseite:
const img = document.querySelector('img[alt*="<Produktname>"]');
const imageUrl = img?.getAttribute('data-zoom')        // beste Qualität
              || img?.getAttribute('data-src')
              || img?.src;
```

**Speicherung, zwei Wege:** **Option A (bevorzugt)**, `image_url` in `catalog_products` zeigt
auf die Hersteller-CDN-URL, kein Storage-Aufwand und immer aktuell, dafür kann die URL sich
ändern (mit 404-Monitoring absichern,
[025-ssot-und-versionsmarker.md](025-ssot-und-versionsmarker.md)). **Option B**, Bild
herunterladen und in Supabase Storage legen, Pflicht wenn das Bild aus einem
auth-geschützten Bereich stammt oder der Hersteller Hot-Linking verbietet.
`catalog_products.image_url` ist `text NULL` und bleibt leer, wenn kein Bild gefunden wurde.

### Batch-Update

Ausgeführt wird bei Erstanlage eines neuen Herstellers, beim Quarterly-Refresh (Preise und
Bilder synchron, [026-projekt-koordination.md](026-projekt-koordination.md)) und wenn mehr
als 20 % der Produkte eines Herstellers kein `image_url` haben. Ablauf: Produkte ohne Bild
abfragen, per Playwright-Skript batch-scrapen (Output als JSON
`{ order_number, image_url }[]`), dann `UPDATE catalog_products`.

**Keine Phantoms:** Vor jedem Scraping-Lauf sicherstellen, dass die Produkte in der DB echte
Produkte sind (kein `status='rejected'`). **Ein falsches Bild ist schlimmer als kein Bild**
([029-plan-und-fehlerregister.md](029-plan-und-fehlerregister.md)).

### Rechtliches

- Logos und Produktbilder bleiben Eigentum der jeweiligen Hersteller
- Verwendung fällt unter Produktinformations-Darstellung (§ 23 UrhG, freie Benutzung für
  Abbildungen von Produkten)
- Bei Direktkontakt mit einem Hersteller (FEGA & Schmitt, Rexel etc.) explizit nach
  Bildrechten fragen
- Wasserzeichen-freie Bilder aus Pressematerial bevorzugen

**Die konkreten Hersteller-URLs, CDN-Muster und Slug-Formeln** (Theben, MDT, Jung, Gira,
Zennio, Hager) stehen im Wiki: `wiki/bilder/hersteller-bezugsquellen.md`. Sie sind
Nachschlagewissen, das sich ändert, sobald ein Hersteller seine Seite umbaut, und gehören
deshalb nicht in einen Standard.

---

## Audit

**Pipeline (A):**
1. **Upload-Helper existiert:** `grep -r "processBrandImage\|processImage" lib/images/` →
   mindestens eine Datei mit Export
2. **Kein roher sharp-jpeg-Aufruf in Server-Actions:**
   `grep -r "sharp(.*).jpeg(.*).toBuffer" app/ --include="actions.ts" --include="route.ts"`
   → 0 Treffer
3. **next.config hat AVIF + Cache:** `images.formats` enthält `image/avif` UND
   `images.minimumCacheTTL >= 31536000`
4. **EXIF-Spot-Check** (manuell, einmal pro Property): Test-Upload → `sharp(out).metadata()`
   → EXIF muss `Sony`, `Max Karastelev`, `maxone.one`, `FE 24-70` enthalten

**Herstellerquellen (B):**
```sql
SELECT slug FROM manufacturers WHERE logo_url IS NULL;                    -- Ziel: 0
SELECT manufacturer, COUNT(*) FROM catalog_products
WHERE status = 'approved' AND image_url IS NULL GROUP BY manufacturer;    -- Ziel: ≥ 80 % befüllt
```

**Implementations-Stand (A):** voltfair.de live seit 2026-05-20 (Hero-Uploads und
Ratgeber-Cover, AVIF aktiv). SLF, vanfree, snapflow und maxone.one stehen aus.

## Quellen

- Implementation-Referenz: `voltfair.de:lib/images/process-upload.ts`
- Brand-Spec: `~/.claude/wiki/brand/visual-style.md`
- Konsistenz-Prinzip: [019-marke-und-sprache.md](019-marke-und-sprache.md)
