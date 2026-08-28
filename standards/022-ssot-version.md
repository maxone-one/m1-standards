# 022: SSoT & Version-Marker (Version-Marker · Cron-Dedup · Kein Hardcode)

**Status:** active
**Seit:** 2026-05-17
**Gilt für:** alle deploybare Web-Apps und alle Projekte

## Inhalt

- [A] Version-Marker (ENV + /api/version + Footer-Banner)
- [B] Cron-E-Mail-Dedup-Schutz
- [C] SSoT & kein Hardcode für geteilte Werte
- [D] Design Token Hierarchy (Primitive vor Semantisch)

---

## A: Version-Marker

Jedes deploybare Web-Projekt weist seinen Build an drei Stellen aus:

1. **`BUILD_ID` als ENV im Container**, Short-SHA (7-8 Zeichen). Lesbar per `docker inspect ... | grep BUILD_ID=`.
2. **`/api/version` Endpoint**, `{ "build_id": "abc1234", "deployed_at": "..." }`
3. **Sichtbarer Banner im Footer**, `v: abc1234`, klein, klickbar auf GitHub-Commit

Alle drei MÜSSEN denselben Wert tragen. Drift = manueller Server-Build = Audit-FAIL.

**Build-Pipeline:**
```yaml
- name: Build image
  run: docker build --build-arg BUILD_ID="${GITHUB_SHA::8}" -t <projekt>-app:latest .
```

```dockerfile
ARG BUILD_ID=dev
ENV BUILD_ID=${BUILD_ID}
```

**Per-Framework:**
- Next.js: `app/api/version/route.ts` mit `export const dynamic = "force-dynamic"`
- SvelteKit: `src/routes/api/version/+server.ts` mit `import { BUILD_ID } from "$env/static/private"`
- Vite/React SPA: `/version.json` bei Build erzeugen (kein API-Endpoint möglich)

**Warum:** Drift-Check braucht maschinenlesbare Wahrheit auf Prod. Vorfall 2026-05-06: Traefik routete beide Slots gleichzeitig, ohne sichtbaren Banner war "welche Version siehst du?" beim Bug-Report nicht beantwortbar.

---

## A.1: Build-Umfang, das noetigste Minimum

**Max-Direktive 06.08.2026:** *immer das noetigste Minimum, begonnen beim Versionieren; nur mehr reinnehmen, wenn es optimiert statt verschlechtert.*

Ein Build ist keine Packung, die man ganz nimmt, sondern eine Liste von Schritten, aus der ausgewaehlt wird: buendeln, verkleinern, uebersetzen, versionieren. **Pflicht ist genau einer, das Versionieren** (Abschnitt A). Jeder weitere Schritt muss sich rechtfertigen, nicht seine Abwesenheit.

**Prueffrage vor jedem zusaetzlichen Schritt:** Was wird dadurch messbar besser, und was verliere ich dafuer? Ohne klare Antwort auf beides bleibt der Schritt draussen.

**Warum das keine Bequemlichkeit ist, sondern eine Schutzregel.** Belegter Fall griddone, 06.08.2026: Dort waere Verkleinern schaedlich gewesen. Das Projekt hat keine Build-Kennung, und der einzige verlaessliche Weg, den Stand auf Produktion zu belegen, ist der byteweise Vergleich der ausgelieferten Dateien gegen den Commit. Minimierte Dateien lassen sich so nicht mehr vergleichen: der Schritt haette die Wahrheitsquelle zerstoert, die er nicht ersetzt, und das waere beim Rollout niemandem aufgefallen.

**Typische Schritte und wann sie wegfallen:**

| Schritt | faellt weg, wenn |
|---|---|
| Buendeln | der Code nicht zum Browser geht, etwa Server-Code auf Node |
| Verkleinern | die Dateien klein sind, oder ein Datei-Vergleich als Nachweis dient |
| Uebersetzen in aeltere Sprachformen | die Laufzeit modern genug ist (Node 20+, aktuelle Browser) |
| Versionieren | nie, siehe A |

---

## A.2: Die Version bleibt nicht bei der Anzeige stehen

**Max-Direktive 06.08.2026:** *Somit koennen wir nach diesem Schritt auch direkt auf die aktuelle Version pruefen, und der User kann selbst aktualisieren, sofern er noch eine alte Version sieht. Das ist immer die logische Konsequenz aus der Versionierung und muss direkt immer mitgezogen werden.*

Ein Marker, den nur ein Entwickler per `docker inspect` liest, loest die halbe Aufgabe. Die andere Haelfte sitzt im Browser des Nutzers: er kann eine veraltete Fassung sehen, ohne es zu merken, und niemand sagt es ihm. **Sobald A steht, ist die Selbstpruefung Pflicht, nicht Kuer.**

**Die drei Teile:**

1. **Die ausgelieferte Seite kennt ihre eigene Kennung.** Sie wurde damit gebaut und traegt sie mit sich, nicht nur im sichtbaren Fussbereich, sondern abfragbar im Skript.
2. **Sie fragt die aktuelle Kennung beim Server ab**, ueber `/api/version` beziehungsweise `version.json`. Mindestens beim Laden und beim Zurueckkehren in den Tab (`visibilitychange`), bei langlebigen Oberflaechen zusaetzlich in einem ruhigen Intervall.
3. **Weichen beide ab, erscheint ein dezenter Hinweis mit einem Knopf, der neu laedt.** Der Text nennt die Sache beim Namen: es gibt eine neuere Fassung.

**Kein automatisches Neuladen.** Eine Seite, die sich unter den Haenden des Nutzers erneuert, zerstoert halb ausgefuellte Eingaben. Der Nutzer entscheidet, die Seite informiert nur. Das ist zugleich die ehrliche Variante des Nudgings (Standard 020): sichtbarer Wert-Tausch, volle Wahlfreiheit.

**Anlass, belegt:** `griddone.de` liefert mit `Cache-Control: public, max-age=3600` aus. Am 06.08.2026 sah Max beim Abnehmen mehrfach die alte Fassung einer gerade ausgelieferten Seite, waehrend der Server nachweislich die neue hielt; die einzige Abhilfe war der Zuruf, mit `Strg+F5` neu zu laden. Genau diesen Zuruf soll die Seite selbst uebernehmen.

---

## B: Cron-E-Mail-Dedup-Schutz

Jeder Cron-Job der E-Mails versendet MUSS sicherstellen: Zähler wird **ausschließlich nach erfolgreichem Dedup-Write** inkrementiert.

**Pflicht-Muster:**
```typescript
const sendRes = await sendEmail(recipient, subject, template);
if (!sendRes.success) { totals.failed_send++; continue; }

const { error: insertErr } = await admin
  .from("email_sequences")
  .insert({ email: recipient, sequence_type: kind });

if (insertErr) {
  totals.failed_log++;
  continue;          // PFLICHT: kein Zähler ohne gesicherten Marker
}

totals.sent++;       // erst hier
```

**Anti-Muster (verboten):**
```typescript
if (insertErr) { logFailure(...); }
// kein continue → nächster Run sendet erneut
totals.sent++;
```

Gilt analog für Boolean-Flags (`reminder_sent_7d`, `reminder_sent_14d`).

**Logging-Konvention:** `[CronName] INSERT_LOG_FAILED { step, user_id, pg_code }`, damit VECTOR bei Drift Alarm schlagen kann.

**Warum:** 2026-05-17 in 9 Stellen in voltfair.de gefunden. Fehler-Kette: Mail versendet → DB-Insert schlägt fehl → Zähler trotzdem erhöht → kein Marker in DB → nächster Cron-Lauf sendet erneut. Stiller Fehler, kein Alert, Zähler positiv.

---

## C: SSoT & kein Hardcode

Kein Wert der in mehr als einer Datei verwendet wird, darf hardcoded im Komponentencode stehen.

| Kategorie | Kanonischer Ort |
|---|---|
| Social-Media-Links | `maxone-standards/config/social.ts` → sync → `lib/social.ts` |
| Marken-URLs | `lib/constants.ts` pro Projekt / ENV wo sinnvoll |
| Rechtliche Texte / Impressum | Zentrale API (→ Standard 007) |
| Secrets & API-Keys | `/opt/secrets/` Store (→ Standard 002) |
| Build-IDs | ENV-Injection zur Build-Zeit (→ A oben) |
| Farbpaletten / Tokens | `@theme`-Block in der globalen CSS-Datei (Tailwind v4) / CSS-Custom-Properties (→ Standard 010 C) |

**Cross-Repo-Werte:** kanonische Datei in `maxone-standards/config/<name>.ts`, Sync-Script verteilt, Projekte haben `lib/<name>.ts` (generiert, nicht manuell editiert).

**Verboten:**
```ts
// Hardcoded Social-Link im Footer
<a href="https://github.com/irgendwas">GitHub</a>
// Hardcoded Farbe inline
<div style={{ color: '#16a34a' }}>
```

---

## D: Design Token Hierarchy (Primitive vor Semantisch)

Jede Token-Datei (Tailwind `@theme`, CSS Custom Properties, `landing-styles.ts` o.ä.) MUSS zweistufig aufgebaut sein. Primitive einmal definieren, semantische Token zeigen darauf, nie auf eigene Strings.

> **Korrektur 28.08.2026:** Hier stand bis heute `tailwind.config` als kanonischer Ort der Farbpaletten. Diese Datei gibt es in Tailwind v4 nicht mehr; die Token stehen im `@theme`-Block der globalen CSS-Datei. 15 der 20 Tailwind-Projekte laufen bereits auf v4, darunter venfree, das den Standard damit korrekt erfüllt, ohne die genannte Datei zu besitzen. Ein Standard, der einen Weg nennt, den das größte Projekt verlassen hat, leitet den nächsten Bau fehl.

```ts
// RICHTIG
const P = {
  smMuted: 'text-sm text-muted-foreground',
} as const

const UI    = { caption:   P.smMuted }
const TABLE = { cellMuted: P.smMuted }
const FORM  = { hint:      P.smMuted }
```

```ts
// FALSCH — benanntes Copy-Paste, kein echter SSOT
const UI    = { caption:   'text-sm text-muted-foreground' }
const TABLE = { cellMuted: 'text-sm text-muted-foreground' }
```

**Warum:** Wenn n semantische Token denselben String direkt enthalten, erfordert eine globale Größenänderung n Edits. Semantische Namen und Namespace-Trennung lösen das nicht, sie verstecken es. Mit Primitiven reicht ein einziger Edit.

**Wann Primitive extrahieren:** sobald ein String-Wert in mehr als einem Token direkt vorkommt.

---

## Audit

**Version-Marker:**
1. Build-Pipeline setzt `BUILD_ID` als build-arg → WARN wenn fehlt
2. Dockerfile: `ARG BUILD_ID` + `ENV BUILD_ID` → WARN wenn fehlt
3. `/api/version` liefert 200 + JSON mit `build_id` → FAIL wenn 404
4. Footer enthält `v:\s*[a-f0-9]{7,8}` → WARN wenn fehlt
5. Drift zwischen ENV / Endpoint / Banner → FAIL

**Cron-Dedup:** alle `app/api/cron/**/route.ts` mit `sendEmail`:
- Dedup-Error-Block ohne `continue` vor Counter-Increment → **FAIL**

**SSoT:** Social-Links, bekannte tote Handles, hardcoded Jahre ohne `new Date().getFullYear()`, Inline-Secrets → FAIL/WARN.
