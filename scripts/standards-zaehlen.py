#!/usr/bin/env python3
"""Misst den Standard-Bestand und prueft ihn gegen die Angaben im README.

ANLASS: Bis zum 09.09.2026 stand in standards/README.md die Zeile
"Aktuell: 33 Standards (0 freie Slots)", waehrend 34 Dateien dalagen. Die Zeile
war zuletzt am 27.08. angefasst worden, die 34. Nummer entstand am 29.08., und
niemand hat nachgezaehlt. Eine getippte Zahl neben einem Ordner ist eine
Behauptung; diese Zahl wird ab jetzt gemessen.

Prueft vier Dinge:
  1. Wie viele Nummern belegt sind und welche frei
  2. Ob jede Nummer in ihrem Themenblock liegt
  3. Ob die Bestandszeile im README zur Messung passt
  4. Ob eine Datei die Groessengrenze reisst (netto, ohne HTML-Kommentare)

Exit 1 bei jeder Abweichung, taugt damit fuer einen Drift-Lauf.
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
STD = REPO / "standards"
README = STD / "README.md"

CAP = 33
GRENZE = 11 * 1024
ZIEL = 10 * 1024

# Die Blockordnung aus README.md, hier als Messgroesse
BLOECKE = [
    ("A · Betrieb und Auslieferung", 1, 5),
    ("B · Netz und Domains", 6, 8),
    ("C · Sicherheit", 9, 13),
    ("D · Daten und Zugang", 14, 16),
    ("E · Oberflaeche, Marke und Community", 17, 21),
    ("F · Ablauf und Qualitaet", 22, 26),
    ("G · Die Projektakte", 27, 30),
    ("H · Dienste, Kosten, Recht", 31, 33),
]


def main() -> int:
    fehler = []
    dateien = sorted(STD.glob("[0-9][0-9][0-9]-*.md"))
    belegt = {}
    for p in dateien:
        nr = int(p.name[:3])
        if nr in belegt:
            fehler.append(f"Nummer {nr:03d} doppelt: {belegt[nr].name} und {p.name}")
        belegt[nr] = p

    frei = [n for n in range(1, CAP + 1) if n not in belegt]
    print(f"Belegt: {len(belegt)}   Frei: {len(frei)}   Cap: {CAP}")

    ausserhalb = [n for n in belegt if n > CAP]
    if ausserhalb:
        fehler.append(f"Nummern ueber der Cap: {sorted(ausserhalb)}")

    print("\nBloecke:")
    for name, von, bis in BLOECKE:
        drin = sorted(n for n in belegt if von <= n <= bis)
        offen = [n for n in range(von, bis + 1) if n not in belegt]
        offen_txt = f"   frei: {', '.join(f'{n:03d}' for n in offen)}" if offen else ""
        print(f"  {name:<40} {von:03d}-{bis:03d}  belegt {len(drin)}{offen_txt}")

    abgedeckt = {n for _, von, bis in BLOECKE for n in range(von, bis + 1)}
    heimatlos = sorted(n for n in belegt if n not in abgedeckt)
    if heimatlos:
        fehler.append(f"Nummern ausserhalb jedes Blocks: {heimatlos}")

    # Bestandszeile im README
    text = README.read_text(encoding="utf-8")
    m = re.search(r"Aktuell \*\*(\d+) belegt, (\d+) frei\*\*", text)
    if not m:
        fehler.append("README nennt keine Bestandszeile in der Form "
                      "'Aktuell **N belegt, M frei**'")
    else:
        r_belegt, r_frei = int(m.group(1)), int(m.group(2))
        if (r_belegt, r_frei) != (len(belegt), len(frei)):
            fehler.append(f"README sagt {r_belegt} belegt / {r_frei} frei, "
                          f"gemessen sind {len(belegt)} / {len(frei)}")

    # Groessen, netto ohne HTML-Kommentare (die werden vor dem Laden entfernt)
    print("\nGroessen ueber dem 10-KB-Ziel:")
    keine = True
    for p in dateien:
        netto = len(re.sub(r"<!--.*?-->", "", p.read_text(encoding="utf-8"),
                           flags=re.S).encode())
        if netto > ZIEL:
            keine = False
            marke = "GRENZE GERISSEN" if netto > GRENZE else "ok, unter der Grenze"
            print(f"  {p.name:<44} {netto:>6}  {marke}")
            if netto > GRENZE:
                fehler.append(f"{p.name} ist {netto} Bytes, Grenze sind {GRENZE}")
    if keine:
        print("  keine")

    if fehler:
        print("\nBEFUNDE:")
        for f in fehler:
            print(f"  - {f}")
        return 1
    print("\nBestand, Blockordnung, README und Groessen stimmen ueberein.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
