---
topic: secrets-tls
last_compiled: 2026-05-02
source_count: 2
status: active
---

# Secrets & TLS

## Summary [coverage: medium -- 2 sources]

Sources span 2026-03 (Stalwart-Vorfall) bis 2026-04 (DNS-01-Direktive). Mail-fokussierter Auszug der globalen Secrets/TLS-Doku.

Alle Mail-relevanten Secrets liegen im **zentralen Secrets-Store** auf `maxone-prod` unter `/opt/secrets/<projekt>/keys.env`. Globales (Brevo API-Key, INWX-DNS-Credentials) liegt in `/opt/secrets/global/`. Die kritischste Verkettung: `SUPABASE_SERVICE_ROLE_KEY` verschlüsselt `jmap_password` in `maxone.email_accounts` (AES-GCM) — eine unüberlegte Rotation killt alle Mail-Konten gleichzeitig. Alle TLS-Zertifikate gehen seit 2026-04-22 ausschließlich über **DNS-01-Challenge via INWX**, niemals HTTP-01.

## Architecture [coverage: high -- 2 sources]

**Secrets-Hierarchie** (alle auf `maxone-prod`, Permissions 700/600, nur root):

```
/opt/secrets/
├── global/
│   ├── keys.env        # BREVO_API_KEY (shared, Account-weit)
│   └── inwx.env        # INWX-User vector-agent (DNS-01-Challenge)
├── stalwart/
│   └── keys.env        # STALWART_ADMIN_USER, STALWART_ADMIN_PASS (in RocksDB!)
├── maxone/
│   └── keys.env        # SUPABASE_*, ZENTINEL_HEALTH_KEY, projekt-eigener Brevo-SMTP-Key
├── slf/
│   └── keys.env        # eigene Supabase-Instanz, eigener Brevo-SMTP-Key
└── vanfree/
    └── keys.env
```

**Wichtige Mail-Secrets im Detail:**

| Secret | Ort | Verwendet von | Rotations-Risiko |
|---|---|---|---|
| `BREVO_API_KEY` (global) | `/opt/secrets/global/keys.env` | Vector (rotiert SMTP-Keys), `email-client` Edge Function | hoch — alle Outbound-Mails brechen |
| Brevo SMTP-Key (pro Projekt) | `/opt/secrets/<projekt>/keys.env` | GoTrue (Supabase Auth, OTP-Mails), `email-client` | mittel — nur betroffenes Projekt |
| `STALWART_ADMIN_USER` / `_PASS` | `/opt/secrets/stalwart/keys.env` UND **RocksDB** | `stalwart-cli`, Recovery-Skripte | hoch — DB hat Vorrang vor `config.toml` ([[zentinel-rules#regel-7]]) |
| `SUPABASE_SERVICE_ROLE_KEY` | `/opt/secrets/maxone/keys.env` | `email-client`, alles was `email_accounts.jmap_password` lesen will | **kritisch** — ([[zentinel-rules#regel-9]]) |
| `ZENTINEL_HEALTH_KEY` | `/opt/secrets/maxone/keys.env` und `/opt/supabase/docker/.env` | Watchdog-Health-Check, Operator-Probes | niedrig |

**TLS-Zertifikate** (User-Direktive 2026-04-22): Alle neuen Projekte nutzen den ACME-Resolver `letsencrypt` mit **DNS-01-Challenge via INWX**. HTTP-01 ist verboten, auch als Fallback.

- **Warum DNS-01:** HTTP-01 koppelt alle Projekte am Account-Rate-Limit. Ein einzelner kaputter Container (falscher DNS-Eintrag, gekündigte Domain) kann das Kontingent sprengen und blockiert dann alle anderen Projekte für bis zu eine Woche. Genau das passierte 2026-04-22 mit `autoconfig.altrading.eu`. DNS-01 isoliert Projekte voneinander.
- **Wie:** Traefik-Label `traefik.http.routers.<name>.tls.certresolver=letsencrypt`. Der Resolver ist server-weit auf DNS-01 umkonfiguriert.
- **INWX-Credentials:** `/opt/secrets/global/inwx.env` (User `vector-agent`). Traefik liest sie direkt per `env_file`.
- **Wildcards möglich** (z.B. `*.maxone.one`): Label `traefik.http.routers.<name>.tls.domains[0].main=<domain>` + `.sans=*.<domain>`.

Mail-relevant: Wenn ein neuer Mail-Hostname (`mail.<projekt>.de`, `autoconfig.<projekt>.de`) angelegt wird, kommt das Zertifikat über DNS-01.

## Key Rules [coverage: high -- 2 sources]

- **Erst speichern, dann eintragen** — Neue Keys IMMER zuerst in `/opt/secrets/`, dann in der Projekt-`.env` referenzieren. Nie nur in der `.env`, sonst geht die Single-Source-of-Truth verloren.
- **Backup nach jeder Änderung** — Google Drive `Meine Ablage/00. Kunden & Projekte/Claude/Secrets Store/`.
- **Permissions** — 700 auf Ordner, 600 auf Dateien, nur root.
- **Brevo-Account pro Projekt** — keine shared SMTP-Keys ([[zentinel-rules#regel-11]]).
- **Rotations-Protokoll** ([[zentinel-rules#regel-3]]): Neuen Key generieren → Store updaten → ALLE betroffenen `.env` updaten → Container `--force-recreate` → JEDEN Endpunkt testen → Drive-Backup → Vector informieren → erst DANN den alten Key löschen.
- **`SUPABASE_SERVICE_ROLE_KEY`** ist Mail-kritisch — ohne Migration-Playbook NICHT rotieren ([[zentinel-rules#regel-9]]).
- **DNS-01 only** — kein HTTP-01, auch nicht als Fallback.

## Notable Failures [coverage: low -- 1 source]

- **2026-03-24 — Brevo SMTP-Key in CLI exponiert.** Konsequenz: Key-Rotation, Downtime in allen Projekten. Lehre: [[zentinel-rules#regel-2]]. Volle Postmortem: [[failure-modes#2026-03-24]].
- **2026-04-22 — autoconfig.altrading.eu Rate-Limit-Lockout.** Ein Container mit falschem DNS-Eintrag versuchte HTTP-01-Challenges → Let's Encrypt ratelimitete den Account → alle anderen Projekte konnten für mehrere Tage keine Certs holen. Server-weite Migration auf DNS-01.
- Hypothetisch: Stalwart-Hash-Spielerei 2026-03-24 (Passwort in `config.toml` geändert ohne RocksDB-Vorrang zu kennen) → siehe [[zentinel-rules#regel-7]].

## Operational Patterns [coverage: medium -- 1 source]

**Sichere Credential-Übergabe via SSH** (Bibel-Pattern):

```bash
ssh root@128.140.40.235 '. /opt/secrets/stalwart/keys.env && \
  docker exec -e CREDS="$STALWART_ADMIN_USER:$STALWART_ADMIN_PASS" stalwart-mail \
  stalwart-cli -u http://localhost:8080 --credentials="$CREDS" server list-config'
```

Kein Klartext in der lokalen History, kein Klartext in der Remote-History (Single-Quotes verhindern lokale Expansion, Source lädt erst im Remote-Shell).

**Rotation eines Brevo-SMTP-Keys** (Vector-Workflow):

1. Vector erzeugt neuen Key via Brevo-API (mit `BREVO_API_KEY` global).
2. Schreibt neuen Key in `/opt/secrets/<projekt>/keys.env`.
3. Updated alle betroffenen `.env`-Files (Supabase GoTrue `GOTRUE_SMTP_PASS`, `email-client`-ENV).
4. `docker compose --force-recreate <containers>`.
5. Test: OTP-Mail aus dem betroffenen Projekt versenden, Empfang verifizieren.
6. Drive-Backup. Vector loggt das Event.
7. Erst dann alten Brevo-Key revoken.

**TLS-Cert manuell erneuern** (Notfall): Traefik macht das normal selbst. Wenn ein einzelner Router stuck ist:

```bash
docker compose -f /opt/traefik/docker-compose.yml restart
```

Bei Account-Rate-Limit: warten (max 1 Woche), oder Domains zwischenzeitlich auf den staging-Resolver mappen.

## Sources

- `~/.claude/CLAUDE.md` — "Secrets Hierarchie & Hoheit", "Zentraler Secrets Store", "TLS-Zertifikate: IMMER DNS-01"
- [[../../briefings/ZENTINEL-STALWART-BIBEL]] — Regeln 2, 3, 7, 9, 11; Vorfall 2026-03-24
