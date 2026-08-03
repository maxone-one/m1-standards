# maxone-mail-pilot Knowledge Base

Last compiled: 2026-05-30
Total topics: 5 | Total concepts: 1 | Total sources: ~11

Pilot-Wiki für das Mail/Zentinel/Stalwart-Subsystem. Komprimiert die [ZENTINEL-STALWART-BIBEL](../../../Projects/maxone.one/briefings/ZENTINEL-STALWART-BIBEL.md) (24 Regeln, 6 Vorfälle, Stand 2026-05-22) plus Mail-Blöcke aus `~/.claude/CLAUDE.md` in vier Topic-Artikel und einen Concept-Artikel.

## Topics

| Topic | Also Known As | Sources | Last Updated | Status |
|-------|---------------|---------|--------------|--------|
| [[topics/mail-architecture]] | Brevo, Stalwart, JMAP, email-client, Sent-Folder | 5 | 2026-05-27 | active |
| [[topics/zentinel-rules]] | Bibel-Regeln, 24 Regeln, Disziplin, Stalwart-Rules | 2 | 2026-05-22 | active |
| [[topics/secrets-tls]] | Secrets-Store, BREVO_API_KEY, SUPABASE_SERVICE_ROLE_KEY, DNS-01, INWX | 2 | 2026-05-02 | active |
| [[topics/failure-modes]] | Postmortems, Vorfälle, Outages, Lehren | 3 | 2026-05-22 | active |
| [[topics/sieve-runtime]] | vacation, Sieve trusted-vs-per-account, SieveScript/set, B-VAC-TRUSTED | 4 | 2026-05-30 | active |

## Concepts

| Concept | Topics Connected | Last Updated |
|---------|------------------|--------------|
| [[concepts/silent-failures]] | mail-architecture, zentinel-rules, failure-modes | 2026-05-02 |

## Wann diese Wiki nutzen

| Situation | Start mit |
|---|---|
| "Hat X meine Mail bekommen?" | [[concepts/silent-failures]] → [[topics/mail-architecture#operational-patterns]] |
| Code-Änderung in `email-client` | [[topics/zentinel-rules]] (Code-Patterns: Regel 19, 20, 21) |
| Stalwart-Restart oder Recovery | [[topics/zentinel-rules#operational-patterns]] (Sicherheits-Checkliste) |
| Neue Domain anlegen / Mail-Setup | [[topics/secrets-tls]] + [[topics/zentinel-rules#regel-12]] + [[topics/zentinel-rules#regel-20]] |
| Sent-Folder leer oder Anhang fehlt | [[topics/zentinel-rules#regel-19]] und [[topics/zentinel-rules#regel-21]] |
| Blue/Green-Swap | [[topics/zentinel-rules#regel-22]] |
| Mailbox-Passwort ändern (Stalwart/Atelier) | [[topics/zentinel-rules#regel-23]] + Standard 016-mail |
| OOM / Container-Spikes / `swapoff` / mem_limit-Frage | [[topics/zentinel-rules#regel-24]] + Standard 015-container-safety |
| Ein Vorfall wiederholt sich (Symptom-Match) | [[topics/failure-modes]] zuerst — prüfe ob historischer Match |
| Vacation / Auto-Reply / OOO einrichten | [[topics/sieve-runtime]] — niemals in trusted Scripts, immer per-account JMAP |
| Sieve-Aktion feuert nicht obwohl Script installiert | [[topics/sieve-runtime#stalwart-jmap-quirks]] — Runtime-Trennung trusted vs per-account |
| Architektonische Frage zu Mail-Pipeline | [[topics/mail-architecture]] |

## Recent Changes

- 2026-05-02: Initial pilot compile (manual run) — 3 Topics, 1 Concept.
- 2026-05-02: Refactor — failure-modes als eigenes Topic extrahiert; Concept-Wechsel `brevo-vs-stalwart` → `silent-failures`; Coverage-Tags auf Section-Ebene; INDEX/Schema spec-konform.
- 2026-05-22: +Regel 23 (Mailbox-Passwort-Sync, Standard 016) + Regel 24 (mem_limit Pflicht für Stalwart, kein `swapoff -a`, Standard 015). +Vorfall 2026-05-16 (Passwort-Desync hey@viktoria-from.de) + Vorfall 2026-05-21 (OOM-Storm). zentinel-rules + failure-modes nachgezogen, Bibel ist Source-of-Truth.
- 2026-05-27: mail-architecture +Projekt-Status-Tabelle. venfree ist live mit eigenem Brevo-Account (`mail@venfree.de`, Org `6a10d33f1e4d419de9018610`). Cleanup im Maxone-Account offen.

## Compile-Stand

- Modus: knowledge
- Compiler: manual-pilot-run (kein Plugin installiert; LLM hat das 5-Phasen-Verfahren manuell ausgeführt)
- Source-Hashes: nicht erfasst (kein Auto-Update; Detection nur über `last_compiled`-Vergleich)

Siehe [[log]] für Compile-Details, [[schema]] für Konventionen.
