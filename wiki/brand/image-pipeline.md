---
name: image-pipeline
description: maxone Bild-Verarbeitungs-Pipeline — Upload-Strip + Brand-EXIF + Next.js AVIF/WebP-Auslieferung. Gilt fuer alle maxone-Properties.
metadata:
  scope: brand
---

# maxone Image Pipeline

Wie Bilder auf maxone-Properties (maxone.one, voltfair.de, vanfree.de, SLF, snapflow, vector etc.) verarbeitet und ausgeliefert werden.

## Drei Stufen

```
Upload (User/Admin)
   ↓
[1] Strip + Brand-EXIF (sharp, Server-Action)
   ↓
Supabase Storage (Quelle, JPEG, ~140-280 KB)
   ↓
[2] Next.js Image Optimization (AVIF/WebP, on-demand)
   ↓
[3] Browser-Auslieferung (best format per Accept-Header)
```

## Stufe 1 — Upload-Verarbeitung (Server-Action)

**Zentraler Helper:** `lib/images/process-upload.ts` → `processBrandImage(buffer, opts)`

Was passiert:
1. Original-Metadaten (EXIF/IPTC/XMP) werden gestrippt via JPEG re-encode
2. Optional Resize (z.B. 1200px fuer Google Discover Hero-Bilder)
3. JPEG mit mozjpeg-Encoder, q=90 default
4. Brand-EXIF wird neu eingeschrieben:

| EXIF-Feld | Wert |
|---|---|
| Make | Sony |
| Model | ILCE-7M4 (A7 IV) |
| LensModel | FE 24-70mm F2.8 GM II |
| LensMake | Sony |
| FocalLength | 35mm (fix) |
| FNumber | 2.8 |
| ISO | 200 |
| ExposureTime | 1/250s |
| Artist | Max Karastelev |
| Copyright | © maxone.one |
| Software | Adobe Lightroom Classic |

**Warum fix 35mm?** Pragmatisch — die KI waehlt im Prompt zwischen 24-70mm pro Motiv, aber im EXIF einen fixen Wert zu setzen ist konsistent und unauffaellig. 35mm ist die haeufigste Brand-Brennweite (Lifestyle, Halbportrait, Office).

**Warum Artist=Person, Copyright=Marke?** Person hinter maxone.one ist immer Max Karastelev. EXIF Artist traegt den Menschen, Copyright die Marke. Marke ist immer „maxone.one", niemals nur „maxone".

## Stufe 2 — Next.js Image Optimization

**Config:** `next.config.ts`

```ts
images: {
  formats: ["image/avif", "image/webp"],
  minimumCacheTTL: 31536000, // 1 Jahr
  remotePatterns: [{ protocol: "https", hostname: "**" }],
},
```

- AVIF zuerst (kleinste Datei), WebP als Fallback fuer aeltere Browser
- 1-Jahr-Cache fuer optimierte Bilder (Default war 60s — viel zu kurz)
- `<Image>`-Komponente in Next.js triggert das automatisch

**Wichtig:** Beim Re-Encoding durch Next.js geht das Brand-EXIF im *ausgelieferten* Bild verloren. Die Quelle in Supabase Storage behaelt es. EXIF ist Provenance-Marker fuer Backups + Stock-Sites, kein User-Browser-Feature.

## Stufe 3 — Browser-Auslieferung

Browser sendet `Accept: image/avif,image/webp,*/*`, Next.js liefert beste passende Variante:

| Format | Anteil 2026 | Groesse Hero 1920×1080 |
|---|---|---|
| AVIF | ~94% | ~90 KB |
| WebP | ~3% (AVIF-Fallback) | ~140 KB |
| JPEG | ~3% (legacy) | ~280 KB |

LCP-Gewinn durch AVIF ggue. JPEG: 200-500ms auf 4G-Verbindungen.

## SEO-Implikation

- WebP/AVIF werden seit ~2020 voll in Google Bildsuche indexiert
- LCP ist Core-Web-Vital-Ranking-Signal — AVIF hilft direkt
- EXIF ist **kein** Ranking-Signal (Google-bestaetigt)
- Bild-Provenance ist Trust-Signal fuer EEAT, aber sekundaer

## Wann diese Wiki nutzen?

- Bei neuer Bild-Upload-Funktion (welcher Helper, welche Quality)
- Bei Performance-Optimierung von Bild-Auslieferung
- Bei Fragen zu EXIF/Privacy von hochgeladenen Bildern
- Bei Stock-Site-Uploads oder Foto-Provenance-Themen

## Sources

- Implementation: [voltfair.de:lib/images/process-upload.ts](https://github.com/maxone-one/voltfair/blob/main/lib/images/process-upload.ts)
- Next.js Config: [voltfair.de:next.config.ts](https://github.com/maxone-one/voltfair/blob/main/next.config.ts)
- Brand-Visual: [[visual-style]]
- Standard: [maxone-standards/standards/027-image-pipeline.md](https://github.com/maxone-one/maxone-standards/blob/main/standards/027-image-pipeline.md)
