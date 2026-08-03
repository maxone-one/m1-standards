---
title: GitHub Self-Hosted Runner
aka: [Runner-Pool, runs-on Labels, Org-Runner, maxone-prod-Runner]
sources:
  - C:\Users\max\.claude\CLAUDE.md (archived 2026-05-22, Zeilen 286-309)
last_updated: 2026-05-22
status: active
---

# GitHub Self-Hosted Runner (Org-Pool)

**Globale Regel:** GitHub wird ausschliesslich kostenlos genutzt. GitHub-Hosted Runner (`ubuntu-latest` etc.) sind verboten. **Immer Self-Hosted.** Siehe CLAUDE.md → "GitHub: NIEMALS kostenpflichtig".

## Runner-Inventar

**Org `maxone-one` hat drei Org-Level-Runner.** GitHub verteilt Jobs round-robin auf alle Runner, deren Labels matchen — `runs-on: self-hosted` allein nimmt alle gemischt.

| Runner-Name       | Server           | IP              | Pfad                  | Custom-Labels                  | Zweck                                                          |
|-------------------|------------------|-----------------|-----------------------|--------------------------------|----------------------------------------------------------------|
| `voltfair-server` | `maxone-prod`    | 128.140.40.235  | `/opt/github-runner/` | `maxone-prod`, `maxone-deploy` | Alle maxone-prod-Projekte (SLF, vanfree, snapflow, vector, ...) |
| `voltfair-cli`    | `voltfair-cli`   | 46.225.107.118  | `/opt/github-runner/` | (keine)                        | voltfair.de-Deploys                                            |
| `maxone-staging`  | `maxone-staging` | 178.105.124.92  | `/opt/github-runner/` | `maxone-staging`               | Staging-Deploys (fsn1, cpx32)                                  |

## Pflicht-Regel (User-Direktive 2026-05-11)

Workflows, die maxone-prod-Pfade brauchen (`/opt/<projekt>/.env.local`, `/usr/local/bin/traefik-probe-fix.sh`, etc.) MUESSEN `runs-on:` auf das Custom-Label pinnen:

```yaml
runs-on: [self-hosted, maxone-prod]
```

**Why:** Am 2026-05-11 schlugen 3 SLF-Deploys hintereinander fehl, weil GitHub den Job an `voltfair-cli` verteilte — dort existiert `/opt/stadtlahnflow/.env.local` nicht. Der `[ -f ] && source`-Short-Circuit failte still, der Build lief weiter und stolperte erst beim Supabase-ENV-Check.

## How to apply

- Neue Workflows auf maxone-prod-Projekten: immer `[self-hosted, maxone-prod]`
- Bestand auditieren bei `Drift`-Sweeps: `grep -rn 'runs-on: self-hosted' .github/` auf allen maxone-prod-Repos
- voltfair-cli kann perspektivisch ein eigenes `voltfair-cli`-Label bekommen, sobald voltfair selbst auf Label-Pin migriert

## Service-Namen

`actions.runner.maxone-studio-org.<runner-name>.service` (Service-Namen bleiben bis zur Re-Registrierung — kein operatives Risiko).

## Bekannte Drift

Auf `maxone-prod` ist die systemd-Unit zeitweise weg, der Runner-Prozess lebt aber weiter. Ueberlebt keinen Reboot. Details: `~/.claude/projects/c--Users-max-Projects-vector/memory/reference_runner_systemd_drift.md`.

## Verwandt

- Server-Aufstellung pro Runner-Host → [[servers]]
- Custom-Label-Theorie (warum self-hosted allein nicht reicht) → `~/.claude/projects/c--Users-max-Projects-vector/memory/reference_org_runner_labels.md`
