# Hersteller-Bezugsquellen: Logo- und Produktbild-URLs

**Herkunft:** Bis zum 09.09.2026 stand das hier im Standard `030-manufacturer-assets.md`.
Beim Neuschnitt der Standards ist es hierher gewandert, **ohne dass ein Wert entfallen ist**.
Der Grund: Das sind Nachschlagedaten, die veralten, sobald ein Hersteller seine Seite umbaut.
Ein Standard setzt eine Regel, diese Seite liefert die Adressen dazu.

**Die Regel steht in** [`standards/020-bilder.md`](../../standards/020-bilder.md) **Abschnitt B**:
Logos und Produktbilder werden nicht geraten, nicht generiert und nicht hot-linked, sondern
über die dort festgelegte Bezugsreihenfolge geholt.

**Stand der Angaben: 2026-05-30.** Wer eine URL hier benutzt und sie antwortet nicht mehr
wie beschrieben, korrigiert die Zeile im selben Zug.

## Logos: bekannte stabile URLs

| Hersteller | Logo-URL |
|---|---|
| Theben | `https://www.theben.de/themes/theben/images/logo--theben.svg` |
| MDT | `https://www.mdt.de/_assets/2d7a0a9f7bf302f23c5f91c8fc495140/Images/MDT_Logo.svg` |
| Gira | `https://www.gira.de/img/logo.svg` |
| Zennio | `https://www.zennio.com/wp-content/uploads/2026/05/zennio-logo-1.svg` |

Presseseiten als Einstieg: Theben `theben.de/the-company-en-gb/topical-themes/press/`,
MDT `mdt.de/downloads/`.

**Website-Inspektion mit Playwright**, wenn keine Presseseite greift:

```js
// Logos im Header der Hersteller-Website finden
const imgs = Array.from(document.querySelectorAll('img'));
imgs.filter(img => /logo/i.test(img.src + img.alt + img.className))
  .map(img => ({ src: img.src, w: img.naturalWidth, h: img.naturalHeight }));
```

## Produktbilder: URL-Muster je Hersteller

**Theben**
- Produktseiten-URL: `https://www.theben.de/en/<name-slug>-<order-number>`
- Beispiel: `https://www.theben.de/en/dmg-2-t-knx-4930270`
- Bild-CDN: `https://www.theben.de/ocsmedia/optimized/<size>/<filename>.webp`
- `data-zoom` = `1080x1080`-Variante, `data-srcset` = `480x480`
- Slug-Formel: Produktname → lowercase, Leerzeichen → `-`, Sonderzeichen entfernen

**MDT**
- Produktseiten-URL: `https://www.mdt.de/en/products/product-detail/<kategorie>/<unterkategorie>/<slug>.html`
- Bild-CDN: `https://www.mdt.de/_assets/…/Images/<filename>` (Pfad via page inspection)

**Jung**
- Katalog-URL: `https://www.jung-group.com/de-DE/Katalog/KNX/Produkte/`
- Produktseiten-URL: `https://www.jung-group.com/de-DE/p/<name-slug>/<SKU>`
- **Bild-URL vollständig vorhersagbar:**
  `https://www.jung-group.com/downloads/catalogue/images/280x280_webp/JUNG_{SKU_NODASH}.webp`
- `{SKU_NODASH}` = SKU ohne Bindestriche (`1701-SE` → `JUNG_1701SE.webp`)
- **Kein Scraping nötig**, die Bild-URL ist aus der SKU allein berechenbar

**Gira**
- Produktseiten-URL: `https://www.gira.de/produkte/<kategorie>/<bestell-nr>`
- Bild-CDN: `https://www.gira.de/media/<path>`

**Zennio**
- Listing-Seiten: `https://www.zennio.com/products/knx/<kategorie>/`
- Alle Produkt-Thumbnails direkt als `<img src>` sichtbar (WordPress, kein Lazy-Loading)
- Bild-CDN: `https://www.zennio.com/wp-content/uploads/<year>/<month>/<filename>.png`
- Dateiname-Muster: `{ORDER_NUMBER}_{Produktname}_370x361.png`

**Hager**
- Produktseiten-URL: `https://hager.com/de/katalog/produkt/<sku-slug>`
- JSON-LD `Product.image[0]` = Hauptbild auf `assets.hager.com`
- Bild-CDN: `https://assets.hager.com/step-content/P/{hash}/11/std.lang.all/{SKU}.webp`
- **Der Preis im JSON-LD ist immer 0**, Hager zeigt keine Endkundenpreise

## JSON-LD auslesen (bevorzugter Weg)

```js
const p = Array.from(document.querySelectorAll('script[type="application/ld+json"]'))
  .map(s => { try { return JSON.parse(s.textContent); } catch { return null; } })
  .find(d => d?.['@type'] === 'Product');
// p.image[0] = Haupt-Produktbild, p.sku = interne SKU, p.description = Beschreibung
```

## Batch-Ablauf

```bash
# 1. Produkte ohne Bild abfragen
ssh prod "docker exec vanfree-db psql -U postgres -d postgres -c \
  \"SELECT order_number, name FROM catalog_products WHERE status='approved' AND image_url IS NULL LIMIT 50;\""

# 2. Playwright-Script: Hersteller-Produkte batch-scrapen
# scripts/scrape-<hersteller>-images.mjs (Node 18+ fetch)
# - Slug aus name ableiten, URL bauen, page.goto, data-zoom extrahieren
# - Output: <hersteller>-images-{date}.json  { order_number: string, image_url: string }[]

# 3. DB-Update
# UPDATE catalog_products SET image_url = <url> WHERE order_number = <order>;
```
