# Pioneers — Per-Projekt-Details

## stadtlahnflow

**Credit-Einheit:** Tropfen (Singular: Tropfen) | Kontext: Fluss, Pegel
**Pool:** 21.000 Tropfen (`tropfenLimit = 21_000`)
**Status:** Produktiv, am ausgereiftesten (14 Activity-Types)

**Projektspezifische Aktivitäten (zusätzlich zum Standard):**
- Event gewinnen: 100
- Netzwerker empfehlen: 25
- Netzwerk-Anfrage senden: 5
- Netzwerk-Anfrage annehmen: 15
- RSVP für Event: 1
- Profil-Startgutschrift: projektspezifisch

**TropfenAction-Typen:** pioneer_startgutschrift, profilbild, bewertung, bug_melden,
feature_einreichen, netzwerker_empfehlen, endkunden_qualifizieren, social,
invite, recommendation, converted, interview, fallback_weiterleitung, profile_complete

**Landing Pages:**
- `/pioneers` — Leaderboard (Wall of Fame)
- `/pioneer` — Deepdive/Erklärungs-Seite

**Tiers:** Founding (1–10, Amber), Early (11–25, Blau), Pioneer (26+, Standard)

---

## voltfair

**Credit-Einheit:** Volt (Plural: Volts) | Kontext: Energie, PV
**Pool:** 21.000 Volts (`PIONEER_POOL_TOTAL = 21_000`)
**Status:** Produktiv

**Aktivitäten (nach Leaderboard-Breakdown):**
early_adopter, feedback, bug_points, referral, customer_referral, profile_photo, review

**Besonderheit:** Hat Admin-Approval-Workflow für Bug- und Feature-Einreichungen
(PioneerFeedback-System mit Freigabe vor Punkt-Vergabe).

**Landing Pages:**
- `/wall-of-fame` — Leaderboard
- `/pioneer` — Deepdive

**Tiers:** Seit 2026-05-19 hinzugefügt (vorher nur Rang-Nummer).
Founding (1–10, Amber), Early Adopter (11–25, Sky), Pioneer (26+, Slate)

**Paradox-des-Teilens-Erklärung:** "Wir sind der TÜV der PV-Branche" — voltfair
macht explizit, warum ein Fachbetrieb andere Fachbetriebe und Kunden einlädt.
Aufgeklärte Kunden kaufen gezielter und bevorzugen denjenigen der sie aufgeklärt hat.

---

## vanfree

**Credit-Einheit:** Puls (Plural: Pulse) | Kontext: Herzschlag, Lebendigkeit
**Pool:** 21.000 Pulse (`PIONEER_POOL_TOTAL = 21_000`)
**Status:** Beta/Early — minimale Implementierung, wächst noch

**Aktivitäten (6 PulseSource-Typen):**
early_slot, profile_photo, feedback, bug_report, feature_implemented, referral

**Punkt-Gewichte** (Stand 2026-05-19 — auf Standard ausgerichtet):

| Aktivität | Punkte |
|---|---|
| profile_photo | 20 |
| feedback | 35 |
| bug_report | 15 |
| feature_implemented | 30 |
| referral | 25 |

*(Vorher beta-niedrig: 5/3/8/20/15 — auf Standard angehoben 2026-05-19)*

**Landing Pages:**
- `/pioneers` — Leaderboard
- `/pioneer` — Deepdive
- `/pioneer/mein-rang` — persönlicher Rang-Dashboard

**Tiers:** Founding (1–10), Early (11–25), Pioneer (26+) — Farb-Logik wie SLF/voltfair

**Noch ausstehend:** pulse-config.ts enthält nur 3 der 5 Quellen (fehlen: profile_photo,
referral) — beim nächsten Vanfree-Sprint ergänzen.

---

## Neue Projekte

Checkliste für ein neues Pioneers-Programm:

- [ ] DB: `pioneer_subscribers`, `pioneer_scores`, `pioneer_leaderboard`-View
- [ ] Server-Logic: `awardCredits()` mit Pool-Check + Idempotenz über `ref_id`
- [ ] Kanonische Punkt-Gewichte aus `implementation.md` übernehmen
- [ ] Projektspezifisches Wording für Credit-Einheit festlegen
- [ ] `/pioneers` (Leaderboard) mit den 7 Pflicht-Sektionen aufbauen
- [ ] `/pioneer` (Deepdive) mit Erklärungs-Content + Anmeldeformular
- [ ] Tier-Badges in Profil und Leaderboard einbauen
- [ ] Credit-Breakdown in Mitgliedsprofil und Listen einbauen
