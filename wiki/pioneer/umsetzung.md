# Pioneer-System: die Umsetzung im Detail

**Herkunft:** Bis zum 09.09.2026 stand das hier im Standard `026-pioneer-system.md`, der
damit 15,1 KB wog und die Größengrenze riss. Beim Neuschnitt ist der Ausführungsteil
hierher gewandert, **ohne dass eine Zeile entfallen ist**.

**Die Regel steht in** [`standards/021-pioneer-system.md`](../../standards/021-pioneer-system.md).
Dort steht auch die Max-Direktive vom 09.09.2026, nach der **jedes** Projekt ein
Pioneer-System führt. Hier stehen nur die Bausteine, mit denen man es baut.

**Stand der Angaben: 2026-05-20.**

## Datenmodell der Erst-Events

```sql
create table pioneer_milestones (
  id uuid primary key default gen_random_uuid(),
  subscriber_id uuid references pioneer_subscribers(id) on delete cascade,
  key text not null,                  -- 'first_slot' | 'first_feedback' | ...
  seen_at timestamptz,                -- NULL = pending, sonst dismissed
  broadcast boolean not null default false,
  created_at timestamptz not null default now(),
  unique (subscriber_id, key)         -- ein Event pro Pioneer-Key
);
```

Der UNIQUE-Constraint ist die einzige Wahrheit. Doppel-Trigger lösen `23505` aus, was als
„schon gefeiert" interpretiert wird (kein Fehler, kein Replay).

## Server-Helper

```ts
// lib/pioneer/milestones.ts
import type { SupabaseClient } from '@supabase/supabase-js'

export type PioneerEvent =
  | 'first_slot' | 'first_feedback' | 'first_bug_report'
  | 'first_feature' | 'first_referral'

export async function markPioneerMilestone(
  subscriberId: string,
  key: PioneerEvent,
  admin: SupabaseClient,
): Promise<boolean> {
  const { error } = await admin
    .from('pioneer_milestones')
    .insert({ subscriber_id: subscriberId, key })
  if (error?.code === '23505') return false // schon gefeiert
  if (error) { console.error('[pioneer] milestone:', error.message); return false }
  return true
}
```

Aufruf direkt nach dem Puls-Event innerhalb derselben Transaktion oder RPC, damit ein
gescheiterter Puls-Insert kein „first" markiert.

## Client-Komponente

Eine `<PioneerConfettiQueue>` in `app/(pioneer)/layout.tsx` pollt
`/api/pioneer/milestones/pending`, feuert sequentiell und dismissed via `POST { ids: [...] }`
(setzt `seen_at`).

`fireConfetti()` folgt dem SLF-Pattern: 1500 ms zwei-seitiger Side-Burst plus zentraler
Burst mit 80 Partikeln. **Pflicht:** `disableForReducedMotion: true` in jedem
`confetti()`-Call.

```ts
import confetti from 'canvas-confetti'

function fireConfetti() {
  const duration = 1500
  const end = Date.now() + duration
  const colors = ['#3b82f6', '#f59e0b', '#10b981', '#ec4899']
  ;(function frame() {
    confetti({ particleCount: 4, angle: 60,  spread: 70, origin: { x: 0, y: 0.7 }, colors, disableForReducedMotion: true })
    confetti({ particleCount: 4, angle: 120, spread: 70, origin: { x: 1, y: 0.7 }, colors, disableForReducedMotion: true })
    if (Date.now() < end) requestAnimationFrame(frame)
  })()
  confetti({ particleCount: 80, spread: 100, origin: { x: 0.5, y: 0.5 }, colors, disableForReducedMotion: true })
}
```

## Milestone-Broadcast über Realtime

```ts
// nur auf /pioneers
const channel = supabase.channel('pioneer-milestones')
  .on('postgres_changes',
      { event: 'INSERT', schema: 'public', table: 'pioneer_milestones',
        filter: 'broadcast=eq.true' },
      (payload) => { fireConfetti(); showWallBanner(payload.new) })
  .subscribe()
```

Der Server setzt `broadcast=true` bei Slot-Insert auf #1/#10/#25/#50.

## Toast-Copy (de.json)

```json
"milestones": {
  "first_slot":     { "title": "Slot #{slot} ist deiner!",        "body": "Willkommen im Pioneer-Kreis — du gehörst zu den ersten {n}." },
  "first_feedback": { "title": "Erstes Feedback!",                "body": "Danke — dein Eindruck formt das Produkt." },
  "first_bug_report":{ "title": "Erster Bug gemeldet!",           "body": "Jeder gefundene Bug spart anderen Nerven." },
  "first_feature":  { "title": "Dein Feature ist live!",          "body": "Du hast etwas vorgeschlagen, das jetzt im Produkt steht." },
  "first_referral": { "title": "Erste Einladung angekommen!",     "body": "Dein Pioneer-Kreis wächst — {name} ist dabei." },
  "milestoneSlot":  { "title": "#{slot} erreicht!",               "body": "{tier}-Stufe ist voll. Konfetti für alle." }
}
```

Das Toast-Wording folgt der maxone-Stimme: kurz, warm, ohne Marketing-Pathos.

## ICU-Plural: weitere Beispiele

```json
"totalPulse":   "{total, plural, one {# Puls vergeben} other {# Pulse vergeben}}",
"profileMetaDesc": "{name} ist Pioneer #{slot} bei venfree.de — {pulse, plural, one {# Puls} other {# Pulse}}.",
"successMsg":   "+{points, plural, one {# Puls} other {# Pulse}} an {label} vergeben"
```

## Avatar-Größen in der Leaderboard-Tabelle

Avatar-Container in Tabellenzeilen nutzen `self-stretch` plus `fill`-Modus, damit das Bild
die volle Zeilenhöhe ohne Leerraum ausfüllt:

```tsx
// 'xl'-Größe: stretcht auf Zeilenhöhe, rounded-xl statt rounded-full
<div className="w-14 self-stretch relative rounded-xl overflow-hidden border border-border shrink-0 min-h-14">
    <Image src={url} alt={name} fill className="object-cover" unoptimized />
</div>
```

Der umschließende `<Link>` braucht `items-stretch` statt `items-start`.

## Die drei Ist-Realisierungen (Stand 2026-05-20, nicht normativ)

| Projekt | UX-Stil | Tabelle | Datei |
|---|---|---|---|
| SLF | Konfetti + Toast (volle Feier) | `member_milestones` mit `seen_at` | `FirstTimeConfetti.tsx`, `lib/milestones.ts` |
| vanfree | Grüner Checkmark (mittlere Feier) | keine (Detection über `pioneer_scores` Count, race-anfällig) | `pioneer/profile/page.tsx` |
| voltfair | Stilles Form-Feedback (keine Feier) | keine (Detection über `pioneer_scores` Count, manuell) | `app/actions/pioneer-review.ts` |

Quellen-Vergleich der Ist-Implementierungen: `briefings/pioneer-achievement-convergence.md`.
Die Snippets auf dieser Seite sind das Zielbild, nicht der Ist-Zustand aller Projekte.
