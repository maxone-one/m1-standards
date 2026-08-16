# 008: Gates & Review (Konzept-Gate · Launch-Gate · Pentest · Re-Review)

**Status:** active
**Seit:** 2026-04-27 (erweitert 2026-04-28)
**Gilt für:** alle Projekte

## Inhalt

- [A] Gate 1: Konzept vor Code (CONCEPT.md)
- [E] Gate 2: Die erste Scheibe ist sichtbar
- [B] Gate 3: Launch-Gate (LAUNCH-REVIEW.md)
- [C] Pentest-Light (defensive Außensicht)
- [D] Re-Review-Reminder (alle 180 Tage)

---

## A: Gate 1: Konzept vor Code

Bevor die erste Code-Zeile geschrieben wird, MUSS im Repo-Root eine `CONCEPT.md` liegen. Kein Konzept → kein Code.

**Pflicht-Sektionen in `CONCEPT.md`:**
- `## Problem / Ziel`, ein Satz
- `## Nutzer`, wer (anonym/eingeloggt/zahlend?)
- `## Datenmodell`, Entitäten + Sensitivität
- `## Auth-Modell`, wer darf was lesen/schreiben (Default: niemand außer Owner)
- `## Externe Dienste`, jeder mit Verarbeitungsrolle, AVV-Status, Server-Region
- `## Threat-Model`, Top 3-5 wahrscheinlichste Schaden-Szenarien
- `## Stack-Wahl`, Framework, DB, Hosting, AI-Tool + WARUM
- `## Out of Scope`, was absichtlich NICHT gebaut wird

**Sign-Off-Format:**
```markdown
## Gate 1 — Konzept-Sign-Off
- Vorgeschlagen: Max Karastelev (@karastoni) am YYYY-MM-DD
- Gate 1: PASSIERT — Code-Bau freigegeben
- DSFA fällig (DSGVO Art. 35): ja / nein / unklar
```

Bei Konzept-Änderungen (Datenmodell, Auth-Modell, externe Dienste): CONCEPT.md updaten + neuen Gate-1-Block anhängen.

**Warum:** OWASP A04:2021 "Insecure Design" ist die Klasse die kein nachgelagertes Tool findet, fehlendes Auth-Modell, zu große Trust-Boundary, Lock-in durch proprietäre Plattform. Vibe-Coding zementiert Konzept-Lücken.

---

## E: Gate 2: Die erste Scheibe ist sichtbar

**Seit:** 2026-08-16 (Max-Direktive). Die Gate-Nummer 2 war bis dahin unbesetzt, und
die Lücke sitzt genau hier: zwischen dem freigegebenen Konzept und dem Launch.

**Bevor ein Plan ausgeführt wird, MUSS seine erste Aufgabe etwas erzeugen, das Max
öffnen und ansehen kann.** Nicht das Datenmodell, nicht die Anbindung, nicht das
Gerüst darunter. Kein Sichtbares → keine Ausführung, der Plan wird umsortiert.

**Die Prüffrage, wörtlich in den Plan:** *Was sieht Max nach dem ersten Schritt, und
wo genau?* Lautet die Antwort „noch nichts, das kommt in Phase 3", ist der Plan falsch
herum sortiert.

| zählt als sichtbar | zählt NICHT |
|---|---|
| live auf Production (stärkste Form) | eine Datei im Repo |
| eine lokal geöffnete Seite oder Oberfläche | ein grüner Testlauf |
| eine Ausgabe, ein Bild, ein Klickpfad | ein Commit, ein fertiger Plan |
| eine Attrappe mit erfundenen Daten | ein Bericht über Gebautes |

**Attrappe ist ausdrücklich erlaubt** und kein Wegwerfprodukt: Sie ist das Gerüst, in
das die echte Funktion einzieht, und sie holt die Abnahme von Wortlaut, Anordnung und
Aufbau, bevor jemand sie zweimal baut.

**Verhältnis zu Standard 001 (Langläufer zuerst anstoßen):** kein Widerspruch, sondern
die Reihenfolge innerhalb desselben ersten Schritts. (1) Langläufer anstoßen, das
kostet Minuten und läuft danach ohne uns. (2) Sichtbares bauen, während er reift, mit
Attrappe an der wartenden Stelle. (3) Alles darunter zuletzt. Wer den Langläufer als
Grund nimmt, zuerst Infrastruktur zu bauen, hat das Gate umgedreht.

**Für die Phasenplanung (GSD):** Phase 1 einer Roadmap ist immer eine vertikale Scheibe
quer durch den Stapel, nie eine Schicht. Die Bauform existiert als `gsd-mvp-phase`
(SPIDR-Schnitt); durch dieses Gate wird sie der Standard statt einer Option.

**Warum:** Was der Auftraggeber nicht sieht, kann er nicht korrigieren. Ein halber Tag
Arbeit an der falschen Sache fällt erst auf, wenn sie fertig ist, und dann ist der Tag
weg. Sichtbares früh ist kein Schaufenster, sondern die einzige Stelle, an der billig
gesteuert werden kann. Dazu: Fortschritt, den nur der Bauende sieht, ist für den
Zahlenden keiner.

**Audit:** Ein `PLAN.md`, dessen erste Aufgabe kein ansehbares Ergebnis hat, ist ein
Befund. Verhaltensfassung mit Anlass: `~/.claude/rules/erst-der-sichtbare-teil.md`.

---

## B: Gate 3: Launch-Gate (LAUNCH-REVIEW.md)

Vor `status: live` MUSS eine `LAUNCH-REVIEW.md` im Repo-Root liegen. Kein Sign-Off → kein Live-Status.

Template: [`templates/LAUNCH-REVIEW.md`](../templates/LAUNCH-REVIEW.md), Checkliste: [`checklists/013-launch-gate.md`](../checklists/013-launch-gate.md).

**Sign-Off-Format:**
```markdown
## Sign-Off
- Verantwortlich: Max Karastelev (@karastoni)
- Datum: 2026-MM-DD
- Geprüft auf: DSGVO, Auth, RLS, Test/Prod-Trennung, Dependencies
- Black-Box-Anteil KI-generiert: X %
- Bekannte Restrisiken: ...
```

**Pflicht-Bereiche:**
- Supabase: RLS auf JEDER Tabelle + Default-deny; Anon-Key manuell mit `curl` getestet; kein Service-Role-Key im Frontend
- DSGVO: Tracker-Inventar, externe Hosts, Consent-Banner, Datenschutzerklärung, AVV-Status (→ Standard 009)
- Bei Black-Box-Anteil > 20 %: zusätzlich `/code-review ultra` durchlaufen
- Lockfile committed; `npm audit` ohne Critical/High; Standards 022 + 023 PASS

Bei größeren Änderungen (neues Tracking, neue 3rd-Party-API, Schema-Migration): Re-Review mit neuem Datum-Eintrag.

**Warum:** Enrichlead 2025 (100% KI-Code, Auth nie reviewed, jeder Nutzer konnte Bezahlfeatures nutzen), Tea/Sapphos (DB-Permissions zu weit), Base44 (Plattform-Lücke), Replit-Agent (löschte Prod-DB).

---

## C: Pentest-Light

Jede Live-Domain wird automatisiert auf bekannte Vibe-Coding-Schwachstellen geprüft, ohne Anmeldedaten, ohne invasive Payloads.

**Prüft:**
- Keine versehentlich exposed Files (`.env`, `.git/`, Source-Maps)
- Keine offen zugänglichen Admin-Routen ohne Auth
- Keine offen erreichbaren Status-Endpoints ohne Auth
- Security-Header gesetzt (HSTS, X-Frame-Options, X-Content-Type-Options)

**Common-Path-Probe (HEAD-Requests, Timeout 3s):**

| Pfad | Erwartung | Severity |
|---|---|---|
| `/.env`, `/.env.local`, `/.git/HEAD`, `/backup.sql` | 404/403 | **FAIL** |
| `/server-status`, `/metrics`, `/admin` (ohne Auth) | 404/403 | **WARN** |
| `/.well-known/security.txt` | 200 gewünscht | INFO wenn fehlt |

**Header-Hygiene (1 GET auf `/`):**
- `Strict-Transport-Security` fehlt → WARN
- `X-Content-Type-Options: nosniff` fehlt → WARN
- `X-Frame-Options` fehlt → WARN
- `Server`-Header verrät Version → WARN

**Was NICHT gefunden wird:** BOLA, SSRF, RLS-Brute-Force, XSS, das ist manueller Gate-3-Scope.

---

## D: Re-Review-Reminder

Jedes Live-Projekt durchläuft alle **180 Tage** einen verkürzten Gate-3-Re-Review. Stichtag = `last_review_date` in `registry/projects.yml`.

**Re-Review-Umfang:** Audit-Lauf PASS; Section J LAUNCH-REVIEW.md; neue Tracker/Drittdienste (→ Standard 011); Bundle-Drift-Check (→ Standard 011); DNS/Cert-Check; Pentest-Light; neuer Sign-Off-Block.

**registry/projects.yml:**
```yaml
- name: stadtlahnflow
  status: live
  last_review_date: 2026-03-12
```

Nach Re-Review `last_review_date` aktualisieren + Tabellen-Eintrag in LAUNCH-REVIEW.md:
```markdown
| 2026-09-15 | Max | keine | PASS |
```

---

## Audit

`scripts/audit.mjs` prüft pro Projekt mit `status: live`:

**Gate 1:** `status: dev` ohne `CONCEPT.md` → **FAIL**; `status: live` ohne `CONCEPT.md` → WARN; Pflicht-Sektionen per Regex → WARN wenn fehlend.

**Gate 3:** `LAUNCH-REVIEW.md` fehlt → **FAIL**; Sign-Off fehlt → **FAIL**; Datum > 12 Monate → WARN.

**Pentest:** Common-Path-Probe + Header-Check (mit `--local-only` übersprungen).

**Re-Review:** `last_review_date` fehlt → FAIL; 180-269 Tage → WARN; ≥ 270 Tage → FAIL.
