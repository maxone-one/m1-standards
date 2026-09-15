---
title: skillspector
description: Handbuch für NVIDIA SkillSpector. Agent-Skills und MCP-Server vor der Installation prüfen, Aufrufe, Urteilsstufen, die Falle AE1, der Preis der LLM-Stufe
---

# skillspector

Stand 15.09.2026, angelegt von der werkstatt-Session auf Übergabe von tagesplaner, der das
Werkzeug am selben Abend auf Max' Anweisung installiert hat. Herkunft jeder Aussage:
`[B:]` selbst geprüft, `[A:]` daraus abgeleitet, `[tagesplaner 15.09.]` nur übernommen,
`[?]` offen.

## Wofür und wann

**SkillSpector durchsucht einen Agent-Skill (Ordner mit `SKILL.md`, dazu Skripte) oder einen
MCP-Server (Zusatzprogramm, das einer KI Werkzeuge gibt) nach Sicherheitsrisiken, bevor er
installiert wird.** Von NVIDIA, Lizenz Apache-2.0. `[B: Doku und --help, 15.09.]`

**Benutzen vor jeder Installation** eines fremden Skills oder MCP-Servers, und wenn jemand
fragt, ob ein installierter Skill vertrauenswürdig ist. Den Weg bis zum Urteil geht der Skill
`skill-inspector`.

**Die Zahl ist kein Urteil.** Der Scanner sucht Muster und versteht keine Absicht. Jeder
HIGH-Befund wird im Quelltext nachgelesen, bevor er zählt.

## Was installiert ist

| | |
|---|---|
| Programm | `/home/max/.local/bin/skillspector`, Verweis in `~/.local/share/uv/tools/skillspector/` `[B: 15.09.]` |
| Version | v2.11.2, der Tag zeigt auf Commit `69dcdfb`, auch auf GitHub `[B: --version, git ls-remote, 15.09.]` |
| Python | installiert 3.12.14, das Paket verlangt `>=3.12,<3.15` `[B: pyproject.toml, 15.09.]` |
| Weg | `uv tool install` aus einem lokalen Klon, als Kopie, nicht bearbeitbar verlinkt. Das Programm läuft ohne den Klon weiter `[B: uv-receipt.toml, direct_url.json, 15.09.]` |
| Skill | `~/.claude/skills/skill-inspector/SKILL.md`, byte-gleich mit dem Repo, in `~/.claude` als `e83e75a` eingecheckt `[B: cmp, git log, 15.09.]` |
| Nicht eingerichtet | das Extra `skillspector[mcp]`. Im Tool-Umfeld liegt kein Paket `mcp`, obwohl `skillspector mcp` in der Hilfe steht `[B: 15.09.]` |

**Der Klon liegt im Scratchpad einer tagesplaner-Session unter `/tmp`**
(`/tmp/claude-1000/-home-max-Projekte-tagesplaner/9411c1ad-241e-478d-9795-ec2b216047b5/scratchpad/skillspector-src`).
`/tmp` ist auf dem NUC ein tmpfs, liegt also im Arbeitsspeicher: **Beim nächsten Neustart ist
der Klon weg.** `[B: findmnt, 15.09.]` Das Programm bleibt, aber das Stapelskript unter
`contrib/` und eine Neuinstallation aus dem Klon gehen dann nicht mehr. tagesplaner hatte den
Ort nicht genannt.

### Neu installieren, gepinnt

`[?]` Unerprobt: direkt vom Commit des Tags, ohne Klon. Die Schreibweise `name @ git+URL@ref`
ist die übliche für Git-Quellen in uv, ob `--force` die bestehende Installation sauber
ersetzt, ist nicht gemessen.

```bash
uv tool install --force "skillspector @ git+https://github.com/NVIDIA/SkillSpector@69dcdfb74487d361ba4c811d088cfdea2ff3a9dc"
```

Danach prüfen, erwartet ist `SkillSpector v2.11.2`:

```bash
skillspector --version
```

## Aufrufe

Einen Skill-Ordner nur statisch prüfen, also ohne KI-Modell und ohne Kosten, Bericht als
Markdown `[B: am 15.09. so gelaufen, Rückgabewert 0]`:

```bash
skillspector scan /home/max/.claude/skills/skill-inspector --no-llm --format markdown --output /tmp/skillspector-bericht.md
```

Als Ziel gehen ein Ordner, eine einzelne `SKILL.md`, eine Git-URL oder eine zip-Datei
`[B: Doku, 15.09.]`. Formate: `terminal` (Standard), `json`, `markdown`, `sarif`, das
Austauschformat für Code-Scanning-Werkzeuge `[B: scan --help]`. Eine Git-URL wird laut Doku
selbst geholt, der Skill `skill-inspector` klont sie trotzdem erst in einen Wegwerfordner.

Viele Skills auf einmal: `--recursive` prüft jeden direkten Unterordner mit eigener
`SKILL.md` als eigenen Skill, ohne Klon `[B: scan --help, nicht ausgeführt]`:

```bash
skillspector scan /home/max/.claude/skills --recursive --no-llm --format markdown --output /tmp/skillspector-alle.md
```

Nur die Risikozahl aus einem JSON-Bericht `[B: an tagesplaners scan-skill-inspector.json]`:

```bash
jq '.risk_assessment' /tmp/skillspector-bericht.json
```

Der Stapel über `contrib/batch_scan` `[tagesplaner 15.09.]` läuft nur im Klon, belegt ist
dort die Form `python -m contrib.batch_scan.batch_scan ./tests/fixtures/ -f terminal
--workers 8` `[B: contrib/batch_scan/CONTRIBUTING.md]`. Mit welchem Python er außerhalb
einer eigenen venv läuft, ist offen `[?]`. `[A:]` Für den Normalfall reicht `--recursive`.

## Urteilsstufen

**Die CLI** leitet aus dem Score (0 bis 100) Schwere und Empfehlung ab
`[B: src/skillspector/nodes/report.py]`:

| Score | Schwere | Empfehlung |
|---|---|---|
| 0 bis 20 | LOW | `SAFE` |
| 21 bis 50 | MEDIUM | `CAUTION` |
| 51 bis 80 | HIGH | `DO_NOT_INSTALL` |
| 81 bis 100 | CRITICAL | `DO_NOT_INSTALL` |

**Rückgabewert:** 1, sobald der Score über 50 liegt (`RISK_THRESHOLD = 50`), ebenso mit
`--fail-on-incomplete` bei unvollständiger Prüfung. 2 bei Abbruch oder Eingabefehler, sonst 0
`[B: cli.py, constants.py]`.

**Der Skill `skill-inspector`** spricht ein eigenes Urteil: `APPROVE`, `CAUTION` oder
`REJECT` `[tagesplaner 15.09., B: SKILL.md]`. Er nimmt den Score nur als Grundhaltung und
verlangt `REJECT` bei jedem unerklärten HIGH oder CRITICAL. **Die Wörter unterscheiden sich:**
Die CLI sagt `SAFE` und `DO_NOT_INSTALL`, der Skill `APPROVE` und `REJECT`. Nur `CAUTION`
heißt in beiden gleich.

## Fallen

### AE1 meldet einen Skill, der sich selbst beim Namen nennt

`[B: Probelauf 15.09.2026, 20:50]` am eigenen Skill, ohne LLM-Stufe: **Score 37, MEDIUM,
CAUTION, allein durch zwei Befunde `AE1`** (Kategorie analysis-evasion, also „Analyse
umgangen“), HIGH, Konfidenz 100 %, an `SKILL.md:60` und `SKILL.md:164`. Das deckt sich mit
tagesplaners Lauf von 20:43. Die Datei ist trotzdem ganz gelesen: Abdeckung 100 %, „Fully
inspected 1“. **Der Befund ist Abdeckung, kein Verhalten.**

**Der Mechanismus weicht von tagesplaners Beschreibung ab.** tagesplaner: Der im Text genannte
Dateiname `SKILL.md` werde als nicht auflösbarer Verweis gemeldet. Gemessen:

- Die Zeilen 60 und 164 nennen `SKILL.md`, und dieser Verweis ist **aufgelöst**.
- **Unauflösbar** sind zwei Wörter mit Schrägstrich, die wie Pfade aussehen: `user/context`
  in Zeile 67 und `network/env/files/shell/MCP/git/etc.` in Zeile 143. Sie stehen im
  Prüfprotokoll des Berichts (Abschnitt „Ledger Exceptions“) als `reference_unresolved`.
- Jeder unauflösbare Verweis setzt die Datei, in der er steht, auf „partial“
  (`nodes/build_context.py`). AE1 entsteht nur für aufgelöste Verweise auf ein Ziel mit
  „partial“ (`nodes/finalize_inspection_ledger.py`). `[B: am Quelltext]`
- `[A:]` Zwei Schrägstrich-Wörter machen `SKILL.md` „teilweise geprüft“, und jede Stelle, die
  `SKILL.md` beim Namen nennt, wird zu einem HIGH. `[?]` Ob der Befund ohne diese Wörter
  verschwindet, ist nicht nachgemessen.

**Umgang:** Bei AE1 immer die „Ledger Exceptions“ gegenlesen. Stehen dort nur
`reference_unresolved` auf Wörtern im Fließtext, ist es dieser Fehlalarm. **Fehlt wirklich
eine Datei oder ein Skript, auf das der Skill verweist, ist AE1 ernst**, denn dann wurde Code
nicht geprüft.

### Drei Warnungen bei jedem Start

`Skipping analyzer semantic_developer_intent: required API key is missing`, dazu dieselbe
Zeile für `semantic_quality_policy` und `semantic_security_discovery`. Sie kommen auch bei
`--version` und `--help` `[B: 15.09.]`. **Betroffen sind nur die drei semantischen Analyzer
der LLM-Stufe**, kein Fehler `[tagesplaner 15.09., bestätigt]`.

## LLM-Stufe und ihr Preis

Ohne `--no-llm` prüft zusätzlich ein Sprachmodell, gewählt über `SKILLSPECTOR_PROVIDER`:
`openai`, `anthropic`, `anthropic_proxy`, `bedrock`, `nv_build`, `nv_inference`, `ollama`,
`azure_openai`, `openai_compatible`, `claude_cli`, `codex_cli`, `gemini_cli`. **Ohne Angabe
nimmt SkillSpector den NVIDIA-Weg** (`nv_inference`, sonst `nv_build`), nicht anthropic oder
openai, wie tagesplaner schrieb `[B: scan --help]`. Mit `SKILLSPECTOR_MODEL` lässt sich das
Modell für alle Analyzer festlegen.

**`claude_cli` ruft das lokale `claude` mit dessen Anmeldung auf, ohne API-Schlüssel, und
pinnt kein Modell** `[B: providers/claude_cli/]`. Preis: Abo-Kontingent `[tagesplaner 15.09.]`.

Gemessen, nur lesend, an tagesplaners Lauf über 92 Ziele mit `claude_cli` ab 15.09., 20:49:

- Je Analyse ein Aufruf `claude -p --output-format text` mit leerer Werkzeugliste,
  `--permission-mode dontAsk`, `--strict-mcp-config`, ohne Einstellungsquellen
  `[B: claude-aufrufe.log]`.
- **Jeder Aufruf hinterlässt einen eigenen Projektordner
  `~/.claude/projects/-tmp-skillspector-cli-*` mit Transkript** von 170 bis 200 KB. Um 20:52
  lagen dort 88 Ordner mit zusammen 15,5 MB `[B: find, du]`.
- Modell: `claude-opus-5` in 113 von 115 Antworten, `claude-opus-4-8` in 2. Bis dahin 29.482
  Token ausgegeben, 2,67 Mio. aus dem Cache gelesen, 1,26 Mio. in den Cache geschrieben
  `[B: Transkripte]`.
- Dazu je Analyzer die Warnung `Model '' ... not found in model_registry.yaml`, gerechnet wird
  dann mit 128.000 Token Kontext `[B: probe/lauf.log]`.

`[A:]` Für einen einzelnen fremden Skill ist die LLM-Stufe vertretbar, für den ganzen Bestand
teuer, und sie füllt `~/.claude/projects`. `[?]` Ob `SKILLSPECTOR_MODEL` bei `claude_cli`
wirkt, ist nicht gemessen.

## Quellen

- Repo: <https://github.com/NVIDIA/SkillSpector>, Stand des Pins:
  <https://github.com/NVIDIA/SkillSpector/tree/v2.11.2>
- Doku: <https://docs.nvidia.com/skills/scanning-agent-skills>, abgerufen 15.09.2026. Sie
  beschreibt Installation per `git clone` und `make install` in eigener venv, die vier
  Zielarten, `--format`, `--output`, `--no-llm` und `SKILLSPECTOR_PROVIDER=openai`.
  Score-Stufen, Rückgabewerte, `--recursive`, `claude_cli` und den MCP-Modus nennt sie nicht.
- Score-Stufen:
  <https://github.com/NVIDIA/SkillSpector/blob/v2.11.2/src/skillspector/nodes/report.py>
- AE1: <https://github.com/NVIDIA/SkillSpector/blob/v2.11.2/src/skillspector/nodes/finalize_inspection_ledger.py>
- Übergabe tagesplaner an werkstatt, 15.09.2026 abends
