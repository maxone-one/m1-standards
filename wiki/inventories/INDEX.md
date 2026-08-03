# inventories Knowledge Base

Last compiled: 2026-05-22
Total topics: 6 | Total concepts: 0

Wiki-Scope für **Inventur-Wissen** — alle Lookups der Form "Welche ID gehört
zu wem?", "Welcher Bot redet mit welchem Konsumenten?", "Wo liegt Secret X?".
Statt Memory-Streu landet hier alles, was sonst in `grep -rln` über mehrere
`.env`-Files endet.

## Topics

| Topic | Also Known As | Sources | Last Updated | Status |
|-------|---------------|---------|--------------|--------|
| [[topics/telegram]] | Bot-Token, Chat-IDs, User-IDs, Schaltzentrale, Privatchat | 3 | 2026-05-04 | active |
| [[topics/paperclip]] | Vision-Familie-Orchestrator, Agent-UUIDs, Company-UUID | 6 | 2026-05-11 | active |
| [[topics/servers]] | Hetzner-Cloud-Inventar, SSH-Zugaenge, maxone-prod, Stalwart-Hosts | 1 | 2026-05-22 | active |
| [[topics/runners]] | GitHub Self-Hosted Runner, Org-Pool, runs-on Labels | 1 | 2026-05-22 | active |
| [[topics/brevo-accounts]] | Brevo-Owner-Accounts pro Projekt, API-Keys, Plan-Stufe | 1 | 2026-05-22 | stub |
| [[topics/mail-aliases]] | 12 funktionsbasierte Aliase pro Domain, Routing-Tabelle | 1 | 2026-05-22 | stub |

## Wann diese Wiki nutzen

| Situation | Start mit |
|---|---|
| "Welche Telegram-Chat-ID hat X?" | [[topics/telegram#chat-und-user-ids]] |
| "Welcher Bot wird von wem benutzt?" | [[topics/telegram#bot-konsumenten]] |
| Bot-Token-Rotation | [[topics/telegram#rotation]] |
| Neuer Telegram-Konsument anlegen | [[topics/telegram#bot-konsumenten]] (Tabelle erweitern) |
| "Was ist die UUID von Agent X in Paperclip?" | [[topics/paperclip#agent-uuids-alle-14]] |
| Neuen Vision-Familie-Agent anlegen | [[topics/paperclip#neuer-agent]] |
| Paperclip Service-Operationen | [[topics/paperclip#service-infra]] |
| "Wie komm ich per SSH auf maxone-prod / voltfair-cli?" | [[topics/servers#ssh-zugang]] |
| "Welche Container laufen auf maxone-prod?" | [[topics/servers#deployte-projekte-auf-maxone-prod-stand-2026-04-02]] |
| Stalwart-Host fuer Projekt X? | [[topics/servers#stalwart-mail-server]] |
| Welchen Runner muss ein Workflow pinnen? | [[topics/runners#pflicht-regel-user-direktive-2026-05-11]] |
| GitHub-Workflow auf maxone-prod audit | [[topics/runners#how-to-apply]] |
| Brevo-Account fuer Projekt X anlegen? | [[topics/brevo-accounts#accounts]] (Status-Tabelle) |
| Welche Aliase pro Domain? | [[topics/mail-aliases#alias-liste-12-gilt-pro-domain]] |
| Wo liegt der Brevo-API-Key fuer Projekt X? | [[topics/brevo-accounts#source-of-truth]] |

## Geplante Topics (kandidaten — anlegen wenn nötig)

- `mailboxen` — Stalwart-Accounts, Domain-Aliase, JMAP-IDs
- `domains` — Welche Domain → Welcher Server / Zweck / Provider
- `secret-store-map` — Was liegt wo in `/opt/secrets/`
- `agents` — Vector/Vault/Vybora/Vigil/Viper Identitäten + Endpunkte

Solange ein Inventar nur in einer Datei lebt, gehört es nicht hierher —
erst wenn der Lookup über mehrere Quellen geht ("wo finde ich X?"),
ist Wiki-Konsolidierung gerechtfertigt.

## Recent Changes

- 2026-05-22: Topics `servers` + `runners` aus CLAUDE.md ausgelagert
  (Server-Tabellen, SSH-Zugaenge, Stalwart-Hosts, Self-Hosted-Runner-Pool
  mit Custom-Labels). CLAUDE.md zeigt jetzt nur noch per Pointer hierher.
- 2026-05-11: Topic `paperclip` mit Company-UUID + 14 Agent-UUIDs der
  Vision-Familie, Service-Pfaden, Operational-Patterns für neue Agenten
  + Prompt-Updates.
- 2026-05-04: Initial scope-Anlage. Topic `telegram` mit Max-User-ID,
  Schaltzentrale, vigil/slf-bridge/vector/karastelev-Bot-Konsumenten.

## Compile-Stand

- Modus: knowledge
- Compiler: manual (kein Plugin)
- Source-Hashes: nicht erfasst

Siehe [[log]] für Compile-Details, [[schema]] für Konventionen.
