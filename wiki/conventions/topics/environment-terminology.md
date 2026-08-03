# Konventionen — Terminologie

## Definitionen (verbindlich, 2026-05-12)

| Begriff | Bedeutet | Niemals |
|---|---|---|
| **live** | Production — echte Nutzer, echter Server | Staging, lokal, dev |
| **Production** | = live | — |
| **Staging** | Dedizierter Pre-Prod-Server, gleiche Infra wie Prod, kein echter Nutzer-Traffic | "fast live", "live-ähnlich" |
| **lokal** | Entwickler-Maschine (Max' Rechner) | — |

## maxone.one — Routing-Dach (2026-06-02)

`maxone.one` ist das neutrale Dach. Alles wird darüber geroutet.
Die vier Welten darunter (Domains aktiv, Wortmarken je nach Domain-Zweck):

| Domain | Zweck |
|---|---|
| `maxone.work` | Dienst & Leistung |
| `maxone.pro` | Expertise |
| `maxone.studio` | SaaS & Tools |
| `maxone.tech` | Hardware & Devices |

## maxone.studio — Domain vs. Wortmarke

| Was | Status |
|---|---|
| Wortmarke "Studio" (z.B. "maxone-Studio", "das Studio von Max") | Tot — nie verwenden |
| Domain `maxone.studio` | Aktiv — SaaS & Tools |
| UI-Label für diesen Bereich | "SaaS & Tools" — niemals "Studio" |

## Infra-Hostname-Konvention (2026-06-02)

Schema: `{dienst}.{projekt}.maxone.one`

Beispiele: `db.venfree.maxone.one`, `api.venfree.maxone.one`, `db.vector.maxone.one`

Verboten: alte Projektnamen (`planexo-api`), Personennamen, temporäre Bezeichnungen.
Hostnamen sind langlebig — neutral halten damit sie Rebrands überdauern.
Details: Standard 006-domain-policy.

## Quelle

User-Direktive 2026-05-12: "live bedeutet ausschließlich Production. Es ist niemals Staging und es ist niemals lokal."
User-Korrektur 2026-05-12: "Studio ist nicht tot, aber es hat eine andere Bedeutung bekommen" — Domain lebt, Wortmarke bleibt tot.

## Staging-Architektur (Stand 2026-05-12)

- Zielzustand: **dedizierter Staging-Server** (Option A), eigene Traefik + Supabase + Runner-Instanz
- Aktueller Stand: noch nicht provisioniert
- Geplant für: SLF (stadtlahnflow) als erstes Projekt
- Server-Kandidat: neuer Hetzner CX32 (~9 €/Monat), Falkenstein-Region
- Prinzip: Staging wächst inkrementell — Komponenten werden nur aufgebaut wenn konkret gebraucht (Stalwart erst wenn Mail-Tests nötig)
- Trigger für echtes Staging: sobald mehrere Kunden denselben Dienst nutzen und ein Prod-Bug alle gleichzeitig trifft
