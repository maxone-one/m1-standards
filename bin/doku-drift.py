"""Prueft, ob sich die abgelegte Anbieterdoku beim Anbieter geaendert hat.

**Warum es das gibt.** Die Bibeln im Wiki stehen auf Doku, die an einem bestimmten Tag
gezogen wurde. Aendert ein Anbieter seine API oder seine Syntax, bleibt unsere Regel
felsenfest falsch, und zwar lautlos. Weil die Doku seit dem 19.08.2026 **persistent**
liegt, ist die Gegenprobe billig: neu ziehen, Pruefsumme vergleichen, die betroffenen
Regeln melden.

**Was es NICHT tut:** Es urteilt nicht. Eine geaenderte Seite kann eine neue Ueberschrift
sein oder eine gekippte Regel; das entscheidet ein Mensch oder Claude, nicht dieses Skript.

Aufruf:
    python bin/doku-drift.py --erfassen   Quellen und Pruefsummen neu aufnehmen
    python bin/doku-drift.py              alle Quellen pruefen, Abweichungen melden
    python bin/doku-drift.py --holen      geaenderte Seiten gleich ersetzen
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import urllib.request
from datetime import date
from pathlib import Path

WIKI = Path(__file__).resolve().parent.parent / "wiki"
VERZEICHNIS = "quellen.json"

# Welche Regeln an welcher Seite haengen. Wird von Hand gepflegt: Ein Skript kann
# nicht wissen, welche Lehre auf welchem Absatz steht, aber genau diese Zuordnung
# macht aus einer Aenderungsmeldung eine Handlungsanweisung.
# Seiten, die sich bei jedem Abruf so stark aendern, dass jeder Vergleich Alarm
# schlaegt (wechselnde Werbeblocks, Sprachumschaltung, Sitzungsmerkmale). Sie tragen
# "vergleich": "aus" und werden als nicht pruefbar gezaehlt, statt jeden Lauf zu
# vergiften. Ihre Regeln muessen von Hand nachgesehen werden.
REGELN_JE_SEITE = {
    "deepgram/doku/keyterm.md": ["DG-02", "DG-07", "DG-08"],
    "deepgram/doku/interim-results.md": ["DG-01", "DG-09"],
    "deepgram/doku/endpointing.md": ["DG-04", "DG-09"],
    "deepgram/doku/flux-flux-nova-3-comparison.md": ["DG-10"],
    "google-calendar/doku/events-insert.txt": ["GCAL-04", "GCAL-05", "GCAL-06", "GCAL-07"],
    "zadarma/doku/sip-trunk-asterisk.txt": ["ZAD-06"],
}


# Zeilen, die sich bei JEDEM Abruf aendern und deshalb vor dem Vergleich fallen.
# Ohne sie meldet der Prueflauf jede Seite als geaendert, und ein Waechter, der immer
# Alarm gibt, wird nach dem zweiten Mal ignoriert.
FLUECHTIG = re.compile(r"^.*(rendered at|Gezogen am|Last-Modified|generated on).*$", re.M | re.I)


def stabil(roh: bytes) -> bytes:
    text = roh.decode("utf-8", "ignore")
    text = FLUECHTIG.sub("", text)
    return re.sub(r"\s+", " ", text).strip().encode()


# **Warum HTML-Abzuege anders verglichen werden als Markdown.** Eine gerenderte Webseite
# aendert sich bei jedem Abruf ein wenig: Build-Kennungen, Sitzungsmerkmale, wechselnde
# Hinweisboxen. Ein Pruefsummenvergleich meldet dann jedes Mal Drift, und ein Waechter, der
# immer Alarm gibt, wird ignoriert. Verglichen wird deshalb der WORTSCHATZ: alle Woerter ab
# vier Zeichen, kleingeschrieben, ohne Dubletten, sortiert. Umsortierte Bausteine faellt
# damit durch, ein geaenderter Satz nicht.
def wortschatz(roh: bytes) -> str:
    text = roh.decode("utf-8", "ignore")
    # Erst Skript und Stil heraus, dann die Tags. Sonst zaehlt der Wortschatz
    # JavaScript-Bezeichner mit, und die aendern sich bei jedem Build.
    text = re.sub(r"<(script|style)[^>]*>.*?</>", " ", text, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    woerter = {w.lower() for w in re.findall(r"[A-Za-zÄÖÜäöüß]{4,}", text)}
    return hashlib.sha256(" ".join(sorted(woerter)).encode()).hexdigest()[:16]


def hashwert(pfad: Path) -> str:
    return hashlib.sha256(stabil(pfad.read_bytes())).hexdigest()[:16]


def url_aus_datei(pfad: Path) -> str | None:
    """Findet die Quell-URL im Dateikopf oder -fuss.

    Deepgram und LiveKit schreiben sie selbst ans Ende ("For the latest version of this
    document, see ..."), unsere Text-Abzuege tragen sie in der ersten Zeile.
    """
    text = pfad.read_text(encoding="utf-8", errors="ignore")
    kopf = re.search(r"Gezogen am [\d.]+ von (https?://\S+)", text[:300])
    if kopf:
        return kopf.group(1)
    fuss = re.search(r"see \[(https?://[^\]]+)\]", text[-800:])
    if fuss:
        return fuss.group(1)
    # Deepgram schreibt keine Quellzeile in die Seite. Der Pfad laesst sich aber
    # aus dem Dateinamen zurueckbauen, weil wir ihn beim Ziehen aus der URL gebildet
    # haben (Schraegstriche zu Bindestrichen).
    if "deepgram" in str(pfad):
        if pfad.name == "llms.txt":
            return "https://developers.deepgram.com/llms.txt"
        rest = pfad.stem.replace("flux-flux-", "flux/flux-")
        return f"https://developers.deepgram.com/docs/{rest}.md"
    return None


def erfassen() -> int:
    for ordner in sorted(WIKI.glob("*/doku")):
        eintraege = {}
        for datei in sorted(ordner.glob("*")):
            if datei.name == VERZEICHNIS or not datei.is_file():
                continue
            url = url_aus_datei(datei)
            roh = datei.read_bytes()
            # **HTML-Abzuege sind grundsaetzlich nicht automatisch pruefbar.** Zwei
            # Laeufe unmittelbar hintereinander melden dieselbe Seite als geaendert,
            # weil gerenderte Doku-Seiten bei jedem Abruf anders aussehen. Nur echte
            # Markdown-Quellen (Deepgram, LiveKit) lassen sich vergleichen. Das ist
            # zugleich das beste Argument dafuer, Anbieter mit .md-Doku zu bevorzugen.
            if datei.suffix == ".txt":
                eintraege[datei.name] = {
                    "url": url,
                    "vergleich": "aus",
                    "grund": "HTML-Abzug, rendert bei jedem Abruf anders. Von Hand nachsehen.",
                    "gezogen_am": date.today().isoformat(),
                }
                continue
            eintraege[datei.name] = {
                "url": url,
                "sha256": hashwert(datei),
                "vergleich": "pruefsumme",
                "gezogen_am": date.today().isoformat(),
            }
        (ordner / VERZEICHNIS).write_text(
            json.dumps(eintraege, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        ohne = [n for n, e in eintraege.items() if not e["url"]]
        print(f"{ordner.parent.name:16s} {len(eintraege)} Seiten erfasst"
              + (f", ohne Quell-URL: {', '.join(ohne)}" if ohne else ""))
    return 0


def pruefen(holen: bool) -> int:
    geaendert: list[tuple[str, list[str]]] = []
    unpruefbar = 0
    for verzeichnis in sorted(WIKI.glob("*/doku/" + VERZEICHNIS)):
        eintraege = json.loads(verzeichnis.read_text(encoding="utf-8"))
        for name, eintrag in eintraege.items():
            rel = f"{verzeichnis.parent.parent.name}/doku/{name}"
            if not eintrag.get("url") or eintrag.get("vergleich") == "aus":
                unpruefbar += 1
                continue
            try:
                anfrage = urllib.request.Request(
                    eintrag["url"], headers={"User-Agent": "Mozilla/5.0"}
                )
                with urllib.request.urlopen(anfrage, timeout=30) as antwort:
                    frisch = antwort.read()
            except Exception as fehler:  # Netz, 404, Umzug: alles derselbe Befund
                print(f"  NICHT ERREICHBAR  {rel}  ({fehler})")
                continue
            neu = wortschatz(frisch) if name.endswith(".txt") else hashlib.sha256(stabil(frisch)).hexdigest()[:16]
            alt = eintrag["sha256"]
            if alt and neu != alt:
                betroffen = REGELN_JE_SEITE.get(rel, [])
                geaendert.append((rel, betroffen))
                if holen:
                    (verzeichnis.parent / name).write_bytes(frisch)
    if not geaendert:
        print(f"Keine Abweichung. ({unpruefbar} Seiten ohne Quell-URL, nicht pruefbar)")
        return 0
    print(f"{len(geaendert)} Seite(n) haben sich geaendert:")
    for rel, regeln in geaendert:
        hinweis = f"  ->  pruefe {', '.join(regeln)}" if regeln else "  ->  keine Regel zugeordnet"
        print(f"  {rel}{hinweis}")
    print("\nDie genannten Regeln in der jeweiligen Bibel gegen die neue Doku halten.")
    return 1


if __name__ == "__main__":
    if "--erfassen" in sys.argv:
        raise SystemExit(erfassen())
    raise SystemExit(pruefen("--holen" in sys.argv))
