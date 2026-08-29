---
title: Remote Control, und warum alte Sessions in der Liste stehen bleiben
description: "Die Sessionliste auf claude.ai raeumt sich nicht selbst auf. Warum das so ist, wann Claude Code doch von allein archiviert, und die drei Handgriffe zum Aufraeumen"
---

# Remote Control: die Sessionliste raeumt sich nicht selbst auf

**Anlass:** Max am 29.08.2026: „Ich verstehe nicht, warum bereits gelaufene Sessions immer
noch in der Auflistung stehen. Auf die habe ich doch sowieso keinen Zugriff mehr."

**Kurz:** Es gibt keine automatische Aufraeumung, und der Nebensatz stimmt nicht. Genau
darin liegt der Grund.

## Warum sie stehen bleiben

**Eine Remote-Control-Session ist keine Verbindung, sondern eine gespeicherte
Konversation.** Solange Remote Control verbunden ist, liegt das Transkript auf
Anthropic-Servern, damit die Konversation ueber Geraete hinweg synchron bleibt und nach
einem Netzabbruch weiterlaufen kann [B: [Remote Control](https://code.claude.com/docs/en/remote-control),
Abschnitt zur Datenhaltung].

**Und sie ist wieder aufnehmbar**, deshalb waere automatisches Wegraeumen ein Verlust:

- lokal ueber `claude --continue` oder `claude --resume`, was die Konversation
  zurueckholt und die Verbindung wiederherstellt;
- die Doku sagt ausdruecklich, dass `/remote-control` sogar eine **archivierte** Session
  wieder aufmacht.

Wer also glaubt, er habe keinen Zugriff mehr, hat den Zugriff nur nicht gesucht.

## Wann Claude Code doch von allein archiviert

Nur in zwei Faellen, beide sind Sonderfaelle [B: [Remote Control](https://code.claude.com/docs/en/remote-control)]:

1. **Ein Remote-Control-Server, der mit `--no-create-session-in-dir` gestartet wurde**,
   archiviert seine Sessions beim Stoppen. Dann gibt es nichts mehr fortzusetzen.
2. **Beim Wiederverbinden nach einem Verbindungsfehler**, wenn zwischenzeitlich eine
   Verdichtung die Konversation umgeschrieben hat oder mit `/resume` gewechselt wurde.
   Claude Code archiviert dann die alte Server-Session, statt sie in der Liste zu lassen.

**Der Normalfall ist keiner von beiden.** Wer Remote Control benutzt und das Fenster
schliesst, behaelt seine Session in der Liste.

## Die drei Handgriffe, alle in der Oberflaeche

[B: [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web),
Abschnitte „Archive sessions" und „Delete sessions"]

**Archivieren:** in der Seitenleiste auf claude.ai/code ueber die Session fahren und das
Archiv-Symbol waehlen. Archivierte Sessions sind aus der Standardliste ausgeblendet,
ueber einen Filter aber weiter erreichbar.

**Wiederfinden:** in der Seitenleiste auf archivierte Sessions filtern.

**Loeschen, endgueltig und nicht rueckgaengig zu machen:** entweder auf archivierte
filtern und dann das Loeschsymbol waehlen, oder in der geoeffneten Session ueber das
Aufklappmenue neben dem Titel.

## Was es NICHT gibt, gemessen

**Keinen Weg ueber die Kommandozeile.** `claude --help` kennt weder einen Archiv- noch
einen Aufraeumbefehl [B: geprueft 29.08.2026 an CLI 2.1.250]. Wer die Liste kuerzen will,
tut das in der Weboberflaeche oder in der App.

**Keine Verfallszeit.** In der Doku steht an keiner Stelle, dass Sessions nach einer Frist
verschwinden. Was verfaellt, ist etwas anderes: **die VM einer Cloud-Session** wird nach
Untaetigkeit eingezogen, und die Session wird in der Liste als abgelaufen markiert. Sie
verschwindet dabei nicht, sondern bekommt beim Wiederoeffnen eine frische VM samt
Gespraechsverlauf. Das ist ein anderer Vorgang und betrifft `--cloud`, nicht Remote
Control.

## Die Verwechslung, die dabei leicht passiert

**`--cloud` und `--remote-control` sind zwei verschiedene Dinge**, und die Doku sagt es
selbst: `--cloud` erzeugt eine Sitzung, die auf Anthropics Rechnern laeuft.
`--remote-control` legt eine **lokale** Sitzung fuer die Fernbedienung offen; Code und
Dateizugriff bleiben dabei auf dem eigenen Rechner. Beide erscheinen in derselben Liste
auf claude.ai/code, weshalb man sie dort leicht durcheinanderbringt. Remote-Control-
Sessions sind an einem Computer-Symbol mit gruenem Punkt zu erkennen, wenn sie online sind.

## Bei Max

`remoteControlAtStartup` steht in `~/.claude/settings.json` auf `true`, Remote Control ist
also in jeder Session an. Das erklaert, warum die Liste bei ihm schneller waechst als bei
jemandem, der es einzeln einschaltet: **jede Sitzung legt einen Eintrag an**, auch die
kurzen.
