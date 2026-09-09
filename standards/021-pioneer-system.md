# 021: Pioneer-System

**Status:** active
**Seit:** 2026-05-19, Geltungsbereich erweitert 2026-09-09
**Gilt für:** **jedes Projekt.** Referenz-Implementierung: vanfree

> **Max-Direktive vom 09.09.2026, und sie ändert den Geltungsbereich dieses Standards:**
> „Es ist Bestandteil jeden Projektes. Jedes Projekt, was begonnen wird, soll ein
> Pioneersystem führen. Allein aus dem Grund, um möglichst früh und schnell eine Community
> zu bilden."
>
> Bis dahin stand hier „vanfree (Referenz-Implementierung); übertragbar auf andere
> maxone-Projekte", und der Standard las sich wie die Beschreibung eines Produkts. **Er ist
> stattdessen eine Startpflicht:** Ein neues Projekt bekommt sein Pioneer-System, bevor es
> Nutzer hat, weil eine Community sich am Anfang bildet oder gar nicht.

## Konzept

Das Pioneer-System ist ein limitiertes Early-Adopter-Programm: eine feste Anzahl
nummerierter Slots, ein endlicher Puls-Pool und eine öffentliche Leaderboard-Wall. Es
erzeugt Dringlichkeit (feste Obergrenze) und Transparenz (öffentliche Profile).

> Kernprinzip: **Feste Menge, öffentliche Reihenfolge, permanenter Status.**

---

## Konstanten: immer aus einem server-sicheren Modul

```ts
// lib/pioneer/pool.ts  (kein 'use client'!)
export const PIONEER_POOL_TOTAL = 21_000   // maximale Pulse insgesamt
export const PIONEER_MAX_SLOTS  = 50       // maximale Slot-Anzahl
```

**Verboten:** Konstanten aus einem `'use client'`-File in einem Server Component
importieren. Das macht den Wert auf dem Server `undefined` → ICU-Interpolation schlägt fehl
→ der Raw-Key wird gerendert (z.B. `Pioneers.slotsUsed`).

```ts
// ❌ Server Component importiert aus 'use client' File
import { PIONEER_MAX_SLOTS } from '@/components/PioneerCounter'

// ✅ Server Component importiert aus plain TS-Modul
import { PIONEER_MAX_SLOTS } from '@/lib/pioneer/pool'
```

Client Components dürfen weiterhin aus `@/components/PioneerCounter` importieren.

---

## Datenmodell

| Tabelle / View | Zweck |
|---|---|
| `pioneer_subscribers` | Anmeldungen (E-Mail, Slot-Nummer, Bestätigung) |
| `pioneer_scores` | Einzelne Puls-Events pro Pioneer und Quelle |
| `pioneer_leaderboard` | View: aggregiert Scores, berechnet Rang + `display_name` |
| `pioneer_milestones` | Erst-Events je Pioneer, `unique (subscriber_id, key)` |

### Puls-Quellen und Punkte

| `source` | Punkte | Beschreibung |
|---|---|---|
| `early_slot` | 1-50 | Je früher der Slot, desto mehr |
| `profile_photo` | 20 | Profilfoto hochgeladen + verifiziert |
| `feedback` | 35 | Feedback eingereicht |
| `bug_report` | 15 | Bug-Report eingereicht |
| `feature_implemented` | 30 | Feature-Request umgesetzt |
| `referral` | 25 | Erfolgreiche Einladung |

---

## Pioneer-Stufen (Tiers)

Stufen basieren auf dem **Eintrittsdatum (`confirmed_at`)**, niemals auf der Slot-Nummer,
niemals auf Pulse. Stufen sind permanent.

> **Regel:** `getTier(slot)` ist verboten. `pioneer_tier` wird im Leaderboard-View aus der
> `confirmed_at`-Reihenfolge berechnet und vom Frontend direkt gelesen.
>
> **Trennung:** `users.tier` ist das **Zugangs-Tier** (Subscription-Level:
> `'founding' | 'lifetime' | ...`). Alle Pioneers bekommen `users.tier = 'founding'`
> (höchster Zugang). Das Pioneer-Badge-Tier (`pioneer_tier`) ist davon völlig unabhängig und
> liegt ausschließlich im Leaderboard-View.

| Stufe | Eintrittposition | Farbe / Border-Klasse |
|---|---|---|
| Founding | 1-10 bestätigt | `text-primary / border-primary/30` |
| Early | 11-25 bestätigt | `text-foreground / border-border` |
| Pioneer | 26-50 bestätigt | `text-muted-foreground / border-border` |

**Ranking** (Leaderboard-Position #1, #2, …) wird **ausschließlich nach Pulse** bewertet:
```sql
RANK() OVER (ORDER BY total_pulse DESC, confirmed_at ASC)
```
Tier und Ranking sind unabhängig voneinander.

---

## Routen und Sitemap

| Route | Sichtbarkeit | Beschreibung |
|---|---|---|
| `/pioneer` | öffentlich | Signup-Seite, Slot-Counter, Vision |
| `/pioneer/confirm` | token-gated | E-Mail-Bestätigung via Token |
| `/pioneer/profile` | token-gated | Profil-Bearbeitung nach Bestätigung |
| `/pioneers` | öffentlich | Leaderboard-Wall (Podest + Tabelle) |
| `/pioneers/[slot]` | öffentlich | Individuelles Pioneer-Profil |

Pioneer-Profile (`/pioneers/[slot]`) werden dynamisch aus der DB in die Sitemap aufgenommen
(`pioneer_subscribers`, `confirmed = true`, `slot_number` nicht NULL, nach `slot_number`
sortiert). Priorität `0.5`, `changeFrequency: 'weekly'`.

---

## Deutsch: Puls (Singular) / Pulse (Plural)

| Kontext | Korrekt | Falsch |
|---|---|---|
| Einzelner Punkt | „1 Puls" | „1 Pulse" |
| Mehrere Punkte | „50 Pulse" | „50 Puls" |
| Komposita (Wortstamm = Singular) | „Puls-Pool", „Puls-Stand", „Puls-Aktivität" | „Pulse-Pool" |
| Singular mit Artikel | „Jeder Puls ist…" | „Jeder Pulse…" |

Für dynamische Mengen, die 1 sein können, ICU-Plural in `de.json`:

```json
"someKey": "{n, plural, one {# Puls} other {# Pulse}}"
```

Hardcodierte Beträge ≥ 2 (z.B. `+15 Pulse`) benötigen kein ICU-Plural.

---

## Erst-Event-Feier (Achievement-Celebration)

Erste-X-Aktionen werden mit einem kurzen visuellen Moment gefeiert. **Die Detection ist
server-seitig über einen UNIQUE-Constraint abgesichert, niemals über `localStorage`.**

### UX-Tiers (pro Projekt konfigurierbar)

| Tier | Stil | Default-Projekte |
|---|---|---|
| **A, Vollfeier** | Konfetti + Toast | vanfree, snapflow, plansey, maxone.one |
| **B, Toast-only** | Toast ohne Konfetti | stadtlahnflow |
| **C, Stille Notification** | Server-seitig geloggt, kein UI-Event | voltfair, kitchen-station |

Das Tier wird pro Projekt einmal in `lib/pioneer/config.ts` festgelegt, **NICHT pro Event**:
Konsistenz innerhalb eines Projekts hat Vorrang.

### Event-Keys

| Event-Key | Trigger | Pulse | Broadcast |
|---|---|---|---|
| `first_slot` | `/pioneer/confirm` erfolgreich (Slot belegt) | 1-50 | ja, bei Milestone-Slots |
| `first_feedback` | erstes `feedback`-Puls-Event | 35 | nein |
| `first_bug_report` | erstes `bug_report`-Puls-Event | 15 | nein |
| `first_feature` | erstes `feature_implemented`-Puls-Event | 30 | nein |
| `first_referral` | erste bestätigte Einladung (Inviter) | 25 | nein |

**Milestone-Broadcast** (öffentlich auf der `/pioneers`-Wall): Slot-Eintritte bei
**#1, #10, #25, #50** zusätzlich als globales Event. Konfetti feuert bei allen aktiven
Besuchern der Leaderboard-Seite, dazu ein permanenter Eintrag im Wall-Header („#10 erreicht,
Early-Stufe voll"). Umsetzung via Supabase Realtime auf `pioneer_milestones`.

### Die fünf Regeln der Feier

- **Server-only Detection.** Niemals `localStorage` als First-Time-Quelle, ein
  Geräte-Wechsel würde Replay erlauben.
- **Einmal pro Pioneer-Key.** Der UNIQUE-Constraint ist die einzige Wahrheit. Ein
  Doppel-Trigger löst `23505` aus, was als „schon gefeiert" gilt (kein Fehler, kein Replay).
  Keine zusätzliche Prüfung im Application-Code, die divergieren kann.
- **`disableForReducedMotion` ist Pflicht in jedem `confetti()`-Call.** Niemand soll
  Konfetti-Spam erleben, der das nicht will.
- **Kein Sound, kein Lottie.** Der Minimalismus ist Absicht: kurzer visueller Moment, dann
  weiterarbeiten.
- **Queue, nicht parallel.** Sind mehrere Milestones gleichzeitig pending (Slot-Eintritt
  plus sofortiges Feedback), wird sequenziell gefeiert, nicht überlagert.

Der Puls-Insert und `markPioneerMilestone()` laufen **in derselben Transaktion**, damit ein
gescheiterter Puls-Insert kein „first" markiert.

**Die Umsetzung im Detail** (SQL für `pioneer_milestones`, der Server-Helper, die
Client-Queue, das Konfetti-Snippet, die Toast-Copy, das Realtime-Abo und die Avatar-Größen
der Leaderboard-Tabelle) steht im Wiki: `wiki/pioneer/umsetzung.md`.

---

## Audit-Checks

```bash
# 0. Kein getTier(slot)-Pattern — Tier immer aus DB lesen
grep -rn "getTier(" app/   # sollte leer sein

# 1. Keine 'use client'-Konstanten in Server Components
grep -rn "PIONEER_MAX_SLOTS\|PIONEER_POOL_TOTAL" app/ \
  | grep -v "use client\|PioneerCounter\|node_modules" \
  | grep "PioneerCounter"   # sollte leer sein für Server Components

# 2. Keine compound "Pulse-" in de.json
grep "Pulse-" messages/de.json   # sollte leer sein

# 3. Keine hardcoded >Pulse< (Einheits-Label) in JSX — t('tablePulse') verwenden
grep ">Pulse<" app/   # sollte leer sein

# 4. Konfetti respektiert reduced-motion in JEDEM Call
grep -rn "confetti({" app/ lib/ components/ \
  | grep -v "disableForReducedMotion"   # sollte leer sein

# 5. Keine localStorage-First-Time-Detection (muss server-seitig sein)
grep -rn "localStorage" app/ lib/ \
  | grep -iE "first|seen|milestone|celebrated"   # sollte leer sein

# 6. UNIQUE-Constraint auf pioneer_milestones vorhanden
psql -c "\d pioneer_milestones" | grep -i "subscriber_id, key"   # sollte UNIQUE zeigen
```

## Verwandte Standards

- [009-geheimnisse-und-tls.md](009-geheimnisse-und-tls.md), Supabase-Zugangsdaten
- [025-ssot-und-versionsmarker.md](025-ssot-und-versionsmarker.md), Konstanten aus
  server-sicheren Modulen statt Hardcode
- [019-marke-und-sprache.md](019-marke-und-sprache.md), Schreibweise und Ton der Toast-Copy
