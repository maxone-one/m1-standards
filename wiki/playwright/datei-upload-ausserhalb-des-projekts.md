# Datei-Upload von außerhalb des Projektordners

Stand 14.09.2026, werkstatt-Session, Anlass ELSTER-Login mit Zertifikatsdatei im tagesplaner.

## Das Fehlerbild

```
Error: File access denied: <pfad> is outside allowed roots.
Allowed roots: <projekt>/.playwright-mcp, <projekt>
```

`browser_file_upload` nimmt nur Dateien aus zwei Wurzeln: dem Ausgabeordner
`<projekt>/.playwright-mcp` und dem Arbeitsverzeichnis, in dem der Server startet. Beim Server
`playwright` ist das der Projektordner, weil `~/.claude/bin/playwright-mcp-projekt.py` ihn dort
startet.

`[B:]` Gelesen am ausgelieferten `@playwright/mcp` 0.0.80, `checkFile()` und `isPathInside()` in
`playwright-core/lib/coreBundle.js`.

## Was es dagegen gibt

| Weg | Wirkung | Wann |
|---|---|---|
| Datei in den Projektordner kopieren | wirkt, aber der Inhalt liegt dann doppelt, womöglich im Repo | nie bei Schlüsseln und Zugangsdateien |
| `allowUnrestrictedFileAccess` (Config) oder `PLAYWRIGHT_MCP_ALLOW_UNRESTRICTED_FILE_ACCESS` | gibt **jede** Datei des Nutzers für Uploads frei | nur mit ausdrücklicher Freigabe von Max |
| Symlink im Ausgabeordner auf den einen Ordner | gibt genau diesen Ordner frei, nur für den Server dieses Projekts | der enge Weg |

**Warum der Symlink trägt:** `isPathInside()` vergleicht nur `path.resolve`-Pfade und löst
Symlinks nicht auf. Ein Pfad `<projekt>/.playwright-mcp/<link>/<datei>` gilt als innerhalb.
Ein `..`-Ausbruch bleibt gesperrt, weil `resolve` ihn vor dem Vergleich auflöst. `[SIM]`
nachgerechnet am 14.09.2026.

**Grenze:** Stellt eine spätere Version auf `realpath` um, kommt die Abweisung zurück, laut und
nicht still.

## Der Bestand

| Projekt | Symlink | Ziel | Freigabe |
|---|---|---|---|
| tagesplaner | `.playwright-mcp/elster` | `/home/max/.elster` (ELSTER-Zertifikat) | Max, 14.09.2026, 12:04, klickbar im tagesplaner |

**Vor jedem neuen Symlink dieser Art:** Max fragen, den Ausgabeordner auf Git-Ignore prüfen und
nachsehen, dass kein Werkzeug Inhalte aus `.playwright-mcp` kopiert. Ein kopierendes Werkzeug,
das Symlinks folgt, nähme den Schlüssel mit. Am 14.09.2026 gab es keins.

Fall im Volltext: `werkstatt/bugs/F-95`, Nachtrag vom 14.09.2026.
