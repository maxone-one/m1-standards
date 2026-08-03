# Pioneers — Kanonische Implementation

Dieser Artikel ist die Spec für jedes neue Projekt das ein Pioneers-Programm bekommt.
Abweichungen müssen explizit begründet werden.

## Credit-System

- **Pool:** exakt 21.000 Einheiten — unveränderlich, wie Bitcoin
- **Verteilung:** automatisch pro Aktivität, server-seitig geprüft (Pool-Check vor jedem Insert)
- **Einheit:** projektspezifisches Wording (Tropfen, Volts, Puls, …)
- **Anzeige:** im Leaderboard + im Mitglieds-Profil + in Listen/Ranking-Ansichten

## Kanonische Punkt-Gewichte

Diese Werte sind der Standard. Neue Projekte starten damit. Abweichungen → begründen.

| Aktivität | Punkte | Kategorie |
|---|---|---|
| Bewertung schreiben | 35 | Feedback |
| Feature einreichen | 30 | Beitrag |
| Empfehlung/Referral | 25 | Wachstum |
| Profilbild hochladen | 20 | Profil |
| Bug melden | 15 | Qualität |
| Endkunden qualifizieren | 10 | Wachstum |

## Kanonische Early-Slot-Formel

**Referenz-Implementation:** SLF (`stadt-lahn-flow/src/app/api/register/route.ts:255`):

```ts
const tropfen = Math.max(10, 500 - (slot - 1) * 10);
```

Slot 1 = **500**, Slot 2 = 490, … Slot 50 = 10. Mathematisch äquivalent: `(51 - slot) * 10` (vanfree-Schreibweise).

**Drift-Watch:**
- **voltfair** (`voltfair.de/app/(onboarding)/onboarding/actions.ts:~165`) nutzt `490 - 10 * position` (position = count-1) → Slot 1 = **490**. Weicht vom Standard ab. Nicht übernehmen.
- Historische User-Intention "490 + Profilbild 10 = 500" ist verworfen — Profilbild bleibt bei **20** (siehe Punkt-Gewichte oben), Slot 1 bleibt bei **500** Basis.

Onboarding-Boni (SLF-Muster, optional pro Projekt):
- Öffnungszeiten eintragen: 15
- Erster Dienst: 20
- Erste Empfehlung: 25
- Telefon hinterlegen: 30

**Grundprinzip:** Aktivitäten die der Plattform mehr bringen, werden stärker belohnt.
Bewertung (35) > Feature (30) > Empfehlung (25) > Profilbild (20) > Bug (15) > Lead (10).

## Pioneer-Tiers

Tiers basieren auf dem **Rang zum Zeitpunkt des Eintritts** (Slot-Nummer), nicht auf
der aktuellen Punktzahl. Wer früh eintritt, behält seinen Tier dauerhaft.

| Rang | Tier | Farbe | Bedeutung |
|---|---|---|---|
| 1–10 | **Founding Member** | Amber/Gold | Allererste Unterstützer |
| 11–25 | **Early Adopter** | Blau/Sky | Frühe Community |
| 26+ | **Pioneer** | Neutral/Slate | Aktive Mitglieder |

## Zwei Landing Pages

### Seite 1: Leaderboard (die Show)
URL-Muster: `/pioneers` oder `/wall-of-fame`

Sektions-Reihenfolge (Pflicht):
1. **Credit-Kontingent** — Gesamtpool (21.000) + bereits verteilt + verbleibend
2. **Podest** — Top 3 mit Medaillen (Gold/Silber/Bronze), prominent
3. **Vollständiges Ranking** — ab Rang 4, Tabelle. Details: Rang, Name, Tier-Badge, Firma, Datum, Punkte, Breakdown-Badges. **Breite vor Höhe** — lieber mehr Spalten als mehr Scrollhöhe.
4. **Punkt-Erklärungskarten** — welche Aktivität bringt wie viele Credits
5. **Tier-Stufen-Erklärung** — Founding/Early/Pioneer mit Beschreibung
6. **Aktiv verteilte Credits** — Live-Liste was gerade vergeben wird (auch in Profilen sichtbar)
7. **CTA** — Jetzt Pioneer werden

### Seite 2: Erklärungs-Deepdive
URL-Muster: `/pioneer`

Wird nach dem CTA auf Seite 1 erreicht. Erklärt tiefer:
- Was sind Pioneers genau?
- Warum lohnt es sich jetzt einzusteigen (Skarcity)?
- Das Paradox des Teilens (B2B: warum andere einladen?)
- Welche Aktivitäten zählen (vollständige Liste)
- Anmelde-Formular

## Technische Umsetzung (Muster)

```
DB-Tabellen:
  pioneer_subscribers (email, confirmed, slot_number, created_at)
  pioneer_scores (pioneer_email, source, points, ref_id, created_at)
  pioneer_leaderboard (VIEW: aggregiert Scores nach Email, berechnet rank)

Server-Logic:
  awardCredits(email, source, refId?) {
    // 1. Pioneer existiert und ist confirmed?
    // 2. Idempotenz: source+refId bereits vergeben?
    // 3. Pool-Check: used + POINTS[source] <= 21_000?
    // 4. Insert pioneer_scores
  }
```

Idempotenz über `ref_id` ist Pflicht — sonst können Aktivitäten mehrfach zählen.

## Anzeige in Profil und Listen

Die aktiv verdienten Credits (nach Quelle aufgeschlüsselt) werden überall angezeigt:
- Mitgliedsprofil (`/mitglieder/[slug]`)
- Listen-/Ranking-Ansicht
- Leaderboard Breakdown-Badges

Format: farbige Chips pro Quelle, z.B. `Bewertung 35` · `Empfehlung 25`
