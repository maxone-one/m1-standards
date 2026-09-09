# Standards

Jede Regel als eigene `NNN-name.md`, mit Status, Datum und Begründung. Format nahe am
ADR-Stil, nachvollziehbar WARUM eine Regel existiert.

## Die Blockordnung (Neuschnitt 09.09.2026)

**Nummern werden nicht mehr fortlaufend vergeben, sondern in ihrem Themenblock.** Neues geht
in den Block, dem es gehört: entweder als Abschnitt in eine bestehende Nummer oder auf die
freie Nummer des Blocks. **Hinten anhängen gibt es nicht mehr, weil hinten kein Platz ist,
sondern nur noch in der Mitte.**

| Block | Nummern | frei |
|---|---|---|
| A · Betrieb und Auslieferung | 001-005 | — |
| B · Netz und Domains | 006-008 | **008** |
| C · Sicherheit | 009-013 | **013** |
| D · Daten und Zugang | 014-016 | **016** |
| E · Oberfläche, Marke und Community | 017-021 | — |
| F · Ablauf und Qualität | 022-026 | — |
| G · Die Projektakte | 027-030 | **030** |
| H · Dienste, Kosten, Recht | 031-033 | — |

**Cap-Regel: maximal 33 Standards.** Aktuell **29 belegt, 4 frei**. Die Zahl wird nicht
getippt, sondern gemessen: `python3 scripts/standards-zaehlen.py`. Vor dem Neuschnitt stand
hier „33 Standards, 0 freie Slots", während es 34 waren; die Zeile war zuletzt am 27.08.
angefasst worden und niemand hat nachgezählt.

**Wie ein Verweis aussieht:** als Link auf den Dateinamen
(`[023-gates-und-review.md](023-gates-und-review.md)`), nicht als nackte Nummer im Fließtext.
Ein Dateiname bricht sichtbar, wenn die Datei wandert; eine Zahl zeigt stumm auf etwas
anderes. Beim Neuschnitt fanden sich Verweise auf „Standard 044" (existierte nie) und auf
„018 (Bundle-Drift)", das seit einer früheren Umnummerierung `auth-db` heißt.

---

## Index

**A · Betrieb und Auslieferung**
- [001-deploy.md](001-deploy.md), Blue/Green + kein Prod-Build + Deploy-Pipeline + Warmup
- [002-server-ordnung.md](002-server-ordnung.md), Pfade, Container-Namen, Netze, HANDOFF.md auf dem Server
- [003-container-sicherheit.md](003-container-sicherheit.md), Container-Misconfig-Audit + Disk-Guard
- [004-zentrale-infrastruktur.md](004-zentrale-infrastruktur.md), Zentrale Dienste, selfhosted n8n, Zustellgarantien, ein Downloadkanal
- [005-geplante-laeufe.md](005-geplante-laeufe.md), Routinen nur auf Heartbeat-Plattform, nie in IDE- oder Claude-Sitzungen

**B · Netz und Domains**
- [006-domain-politik.md](006-domain-politik.md), Neue Infrastruktur auf `.one`, nie `.studio`
- [007-zertifikate-und-dns.md](007-zertifikate-und-dns.md), DNS auf eigenen Server, TLS-Cert gültig, LE-Issuer
- *008 frei, für Netz und Domains*

**C · Sicherheit**
- [009-geheimnisse-und-tls.md](009-geheimnisse-und-tls.md), Zentraler Secrets-Store + TLS via DNS-01
- [010-sicherheits-scans.md](010-sicherheits-scans.md), Secret-Scan (gitleaks) + Static-Analysis (Semgrep OWASP)
- [011-llm-sicherheit.md](011-llm-sicherheit.md), Direct und Indirect Injection, Agent-Rechte, Approval-Queue
- [012-live-audits.md](012-live-audits.md), DSGVO-Tracker-Audit + Bundle-Drift-Audit
- *013 frei, für Sicherheit*

**D · Daten und Zugang**
- [014-auth-und-db-trennung.md](014-auth-und-db-trennung.md), Supabase SSR Auth, eine DB pro Projekt, Zugriffsrechte
- [015-rls-policy-nennt-ihre-rolle.md](015-rls-policy-nennt-ihre-rolle.md), Jede RLS-Policy nennt ihre Rolle mit `TO`
- *016 frei, für Daten und Zugang*

**E · Oberfläche, Marke und Community**
- [017-pflichtbausteine-oberflaeche.md](017-pflichtbausteine-oberflaeche.md), Impressum, Credits, Widget, Footer, Layout-Qualität, Design-first
- [018-admin-oberflaeche.md](018-admin-oberflaeche.md), Dashboard-Layout + DevPanel + App-Launcher
- [019-marke-und-sprache.md](019-marke-und-sprache.md), Wahrhaftige Unterschrift, echte Umlaute, Schreibstil
- [020-bilder.md](020-bilder.md), Verarbeitungs-Pipeline + Herstellerquellen für Logos und Produktbilder
- [021-pioneer-system.md](021-pioneer-system.md), **Jedes Projekt führt eines**: limitierte Slots, Puls-Pool, Leaderboard

**F · Ablauf und Qualität**
- [022-tests-und-code-qualitaet.md](022-tests-und-code-qualitaet.md), Test-First + Code-Health-Budget
- [023-gates-und-review.md](023-gates-und-review.md), Gate 1 bis 3, Bau-Reihenfolge und Takt, Pentest-Light, Re-Review
- [024-stack-und-plattform.md](024-stack-und-plattform.md), Stack-Whitelist, Plattform-Blacklist, Self-Hosted-First
- [025-ssot-und-versionsmarker.md](025-ssot-und-versionsmarker.md), Version-Marker, Cron-Dedup, SSoT, kein Hardcode
- [026-projekt-koordination.md](026-projekt-koordination.md), Spec-Archiv, Dep-Currency, Cross-Project-Broadcast, was ins Repo gehört

**G · Die Projektakte**
- [027-projektakte.md](027-projektakte.md), `docs/INDEX.md` als Einstiegspunkt
- [028-konzept-und-entscheidungen.md](028-konzept-und-entscheidungen.md), CONCEPT.md, das lebende Projekt-Brain, DECISIONS.md
- [029-plan-und-fehlerregister.md](029-plan-und-fehlerregister.md), PLAN.md + BUGS.md + Cross-Project-Bugmuster
- *030 frei, für die Projektakte*

**H · Dienste, Kosten, Recht**
- [031-mail.md](031-mail.md), Gateway-Pflicht, Mail-Architektur, Passwort-Sync
- [032-kosten-caps.md](032-kosten-caps.md), Drei Verteidigungslinien gegen Kostenüberraschungen
- [033-compliance-lebenszyklus.md](033-compliance-lebenszyklus.md), Sunset-Prozess + AVV/DPA-Registry

---

## Umleitung: wo die alten Nummern geblieben sind

**Rund 655 Dateien in allen Projekten verweisen auf die alten Nummern.** Sie werden nicht auf
Vorrat umgeschrieben, sondern beim nächsten Anfassen des jeweiligen Projekts. Diese Tabelle
löst jeden alten Verweis auf.

| alt | neu | | alt | neu |
|---|---|---|---|---|
| 001 deploy | 001 | | 018 auth-db | 014 |
| 002 secrets-tls | 009 | | 019 cost-caps | 032 |
| 003 tests-quality | 022 | | 020 brand-communication | 019 |
| 004 handoff-md | 002 (B) | | 021 project-coordination | 026 |
| 005 paths-naming | 002 (A) | | 022 ssot-version | 025 |
| 006 domain-policy | 006 | | 023 admin-ui | 018 |
| 007 required-ui | 017 | | 024 plan-tracker | 029 (A) |
| 008 gates-review | 023 | | 025 bug-registry | 029 (B) |
| 009 compliance | 033 | | 026 pioneer-system | 021 |
| 010 stack-platform | 024 | | 027 image-pipeline | 020 (A) |
| 011 live-domain-audit | 012 | | 028 brevo-api-outreach | → Wiki |
| 012 cert-dns-reality | 007 | | 029 concept-reference | 028 (A/B) |
| 013 security-scanning | 010 | | 030 manufacturer-assets | 020 (B) |
| 014 llm-security | 011 | | 031 decisions-md | 028 (C) |
| 015 container-safety | 003 | | 032 docs-index | 027 |
| 016 mail | 031 | | 033 central-infrastructure | 004 |
| 017 routine-platform | 005 | | 034 rls-policy | 015 |

**Der Gateway-Abschnitt hieß 016-C und heißt jetzt 031-A.** Wer einen Verweis auf „016-C"
findet, meint die Mail-Gateway-Pflicht.

---

## Pflicht-Dateien pro Projekt (alle auf einmal anlegen)

| Datei | Ort | Standard |
|---|---|---|
| `CONCEPT.md` | Repo-Root | 028 |
| `PLAN.md` | Repo-Root | 029 |
| `BUGS.md` | Repo-Root | 029 |
| `HANDOFF.md` | `/opt/<projekt>/` auf dem Server | 002 |
| `docs/DECISIONS.md` | `docs/` | 028 (nur wenn ein PRD existiert) |

Fehlt eine, werden alle auf einmal angelegt, nicht nur die fehlende.

## Propagations-Regel (2026-05-30)

Wenn in einem Projekt eine neue Regel entsteht (Vorfall, Direktive, Erfahrung):

1. **Standard anlegen oder erweitern**, hier in maxone-standards (Blockordnung beachten)
2. **Alle anderen Projekte nachrüsten**, sofort, nicht „beim nächsten Touch"
3. **Broadcast anlegen**, wenn Drift-Risiko besteht
   ([026-projekt-koordination.md](026-projekt-koordination.md) C)

Projektlokal = temporär. In Standards = permanent und projektübergreifend.

## Format einer Regel

```markdown
# NNN: Titel

**Status:** active | deprecated | proposed
**Seit:** YYYY-MM-DD
**Gilt für:** alle Projekte | nur Kundenprojekte | ...

## Regel / Inhalt
## Warum
## Wie anwenden
## Audit
```

Bei mehreren Themen in einer Datei: Inhalt-Übersicht als erstes, dann `## A:`, `## B:` etc.

## Cross-Links: Wiki und Standards

**Regel:** Hat ein Standard ein komplexes narratives Thema (Vorfalls-Geschichte,
Betriebswissen, Nachschlagedaten), gehört der Kontext ins Wiki, der Standard verlinkt
dorthin. Das Wiki verlinkt zurück zum Standard als Pflicht-Spec.

| Standard | Wiki-Seite |
|---|---|
| 014-auth-und-db-trennung | `wiki/auth/supabase-ssr-setup.md` |
| 017-pflichtbausteine-oberflaeche | `wiki/design/brief-checkliste.md` |
| 020-bilder | `wiki/bilder/hersteller-bezugsquellen.md`, `~/.claude/wiki/brand/visual-style.md` |
| 021-pioneer-system | `wiki/pioneer/umsetzung.md` |
| 004-zentrale-infrastruktur | `wiki/integrationen/zustellgarantien.md` |
| 031-mail | `wiki/integrationen/brevo-outreach-im-gateway.md`, `~/.claude/wiki/maxone-mail-pilot/INDEX.md` |

## Externe Recherche

- [`../research/2026-04-28-github-similar-projects.md`](../research/2026-04-28-github-similar-projects.md),
  ossf/scorecard, garak, promptfoo, trivy, OWASP-Top-10-LLM
