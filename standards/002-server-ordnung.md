# 002: Server-Ordnung (Pfade · Container-Namen · Netze · HANDOFF auf dem Server)

**Status:** active
**Seit:** etabliert, formalisiert 2026-04-27, zusammengeführt 2026-09-09
**Gilt für:** alle Projekte

> **Herkunft:** Diese Nummer führt zusammen, was bis zum 09.09.2026 als `005-paths-naming.md`
> und `004-handoff-md.md` getrennt lag. Beide beantworten dieselbe Frage: **Wo liegt was auf
> dem Server, und wie heißt es?** Kein Satz ist dabei entfallen.

## Inhalt

- [A] Pfade, Container-Namen, Domains, Netze
- [B] HANDOFF.md auf dem Server

---

## A: Pfade, Container-Namen, Domains, Netze

Konsistente Pfade und Container-Namen über alle Projekte hinweg.

**Warum:** Wenn jedes Projekt seine eigenen Konventionen hat (`/srv/foo`, `/var/app/bar`,
`/opt/baz/code`), dann muss jeder Befehl projekt-spezifisch nachgeschlagen werden. Ein
konsistentes Schema macht Cross-Projekt-Operationen (Audits, Backups, Updates) trivial.

**Server-Pfade:**
- `/opt/<projekt>/`, Code, docker-compose.yml, .env
- `/opt/<projekt>/HANDOFF.md`, Briefing (Abschnitt B)
- `/opt/secrets/<projekt>/keys.env`, Secrets (siehe [009-geheimnisse-und-tls.md](009-geheimnisse-und-tls.md))
- `/opt/backups/<projekt>/`, Lokale Backups vor DB-Restore

**Lokale Pfade:**
- `/home/max/Projekte/<projekt>/`, Repo-Root
- `/home/max/Projekte/<projekt>/<projekt>.code-workspace`, Workspace

> **Der lokale Pfad hat sich geändert, die Regel nicht.** Bis zum Umstieg auf Ubuntu
> (gemessen am 02.09.2026 an `/etc/os-release`: Ubuntu 26.04.1 LTS) lautete er
> `c:\Users\max\Projects\<projekt>\`. Wer in älteren Standards, Skripten oder Registry-Feldern
> (`path_local`) noch den Windows-Pfad findet, hat einen historischen Stand vor sich, keinen
> zweiten gültigen Ort.

**Container-Namen:**
- Single: `<projekt>-app`
- Blue/Green: `<projekt>-app-blue`, `<projekt>-app-green`
- DB: `<projekt>-db` (wenn projekt-eigene DB)
- Supabase-Stack: `<projekt>-{auth,rest,kong,storage}`
- Hilfs-Container: `<projekt>-redis`, `<projekt>-worker`, etc.

**Domains:**
- Eigene Brand → eigene Domain (`maxone.one`, `voltfair.de`)
- Subprojekte → `<name>.maxone.one` (DNS-Record einzeln, kein Wildcard)
- Niemals neue Resourcen auf `maxone.studio` (siehe [006-domain-politik.md](006-domain-politik.md))

**Docker-Netzwerke (2026-07-06):**
- Schema `<scope>-<tier>`.
- Geteiltes Edge-Netz (Traefik-Routing, alle Container): `maxone-public`. Ein einziges Netz, kein Splitting pro Projekt (Traefik-Routing-Komplexität ohne Nutzen).
- Privates Projekt-Netz (DB/interne Services): `<projekt>-private`, ersetzt bisher compose-autogenerierte Namen (`<projekt>_<projekt>-internal` o.ä.).
- Ersetzt das verwaiste Coolify-Relikt-Netz `coolify` (Alt-Alias-Kollisionen zwischen Kundenprojekten, siehe Vorfall 2026-06-05). Rollout welle-weise, kein Big-Bang: Welle 1 bei `maxone-sign` bereits umgesetzt, Rest der Plattform folgt opportunistisch bei nächstem Anfassen des jeweiligen Projekts.

---

## B: HANDOFF.md auf dem Server

Jedes Projekt hat unter `/opt/<projekt>/HANDOFF.md` ein Briefing-Dokument mit aktuellem
Stand, Architektur und projekt-spezifischen Regeln. Vor jeder Arbeit am Projekt: erst
HANDOFF lesen.

**Warum:** Bei 11+ Projekten kann man den Stand nicht im Kopf behalten. Wenn die Wahrheit
nur in Container-Configs und Code verstreut liegt, dauert Onboarding (Claude oder Mensch)
jedes Mal lange und es passieren Fehler durch falsche Annahmen.

Vor Arbeit:
```bash
ssh -i ~/.ssh/id_ed25519 root@<server> "cat /opt/<projekt>/HANDOFF.md"
```

Inhalt (siehe `templates/HANDOFF.md` als Skelett):
- **Stand:** Letzter Deploy, aktive Probleme, offene TODOs
- **Architektur:** Tech-Stack, Container, Datenbank, Reverse Proxy
- **Domains:** Live-Domains, Aliase, DNS-Status
- **Secrets:** Welche Keys liegen im Store, Rotations-History
- **Deploy:** Wie deployen (Blue/Green-Swap-Befehl, CI-Workflow-Name)
- **Tests:** Smoke-Befehl, Unit-Befehl, Test-URL für Staging
- **Bekannte Eigenheiten:** Was ist nicht offensichtlich aus Code/Configs

---

## Audit

`scripts/audit.mjs` prüft:

**Pfade und Namen (A):**
- Container-Namen matchen Schema (`<projekt>-app(-blue|-green)?`)
- Server-Pfad existiert: `/opt/<projekt>/`
- Lokal: `<projekt>.code-workspace` im Repo-Root existiert

**HANDOFF (B), per SSH:**
- Existenz `/opt/<projekt>/HANDOFF.md`
- Letzte Änderung (älter als 30 Tage → Warnung)
