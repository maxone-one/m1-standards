---
title: Der Linux-Stapel auf Max' Arbeitsplatz
description: Wer unter Kubuntu wofuer zustaendig ist, die drei dauernd verwechselten Namen, die vier Nahtstellen mit bekannten Fehlerbildern, Diagnose von unten nach oben
---

# Der Linux-Stapel auf Max' Arbeitsplatz

**Wann diese Datei zu lesen ist:** Bevor an Bluetooth, Ton, Anmeldung, Fenstern oder
Geraeten gesucht wird, und immer dann, wenn ein Dienst gruen meldet und das Geraet
trotzdem nicht tut. Fast jeder Fehler dieser Art sitzt nicht in einer Schicht, sondern an
einer Naht zwischen zweien.

## Der Stapel, von unten nach oben

Stand 28.08.2026, gemessen auf `max-nuc11pahi7`. Versionen veralten, die Rollen nicht.

| Schicht | Laeuft hier als | Zustaendig fuer | Nachsehen mit |
|---|---|---|---|
| Firmware | `intel/ibt-19-0-4.sfi` | Betriebssoftware im Chip selbst, vom Hersteller | `journalctl -b -k \| grep -i firmware` |
| Kernel | Linux 7.0.0-30-generic | Hardware ansprechen, Geraete anlegen, `rfkill` | `uname -r`, `rfkill list` |
| Init | systemd | Was startet und stoppt, in welcher Reihenfolge | `systemctl status <dienst>` |
| Geraetezuordnung | udev | Benennt und richtet ein, was auftaucht | `udevadm monitor` |
| Dienste | BlueZ 5.85, PipeWire, WirePlumber | Bluetooth, Ton | `bluetoothctl show`, `wpctl status` |
| Sprechanlage | D-Bus | Nachrichten zwischen Programmen | `busctl monitor` |
| Rechte | PolicyKit, AppArmor | Wer darf was, wer sitzt im Kaefig | `journalctl \| grep -i "apparmor\|polkit"` |
| Distribution | Kubuntu 26.04.1 LTS, Resolute Raccoon | Auswahl und Versionen, `apt` und `snap` | `lsb_release -ds` |
| Anmeldung | SDDM | Laeuft **vor** jeder Sitzung | `systemctl status display-manager` |
| Anzeige | Wayland | Protokoll zwischen Programm und Bildschirm | `echo $XDG_SESSION_TYPE` |
| Oberflaeche | KDE Plasma 6.6.6 auf Qt 6.10.2 | Was Max sieht und klickt | `plasmashell --version` |
| Plasmas Hintergrunddienst | `kded6` mit Modulen, darunter Bluedevil 6.6.4 | Bindet die Oberflaeche an die Dienste | `qdbus6 org.kde.kded6 /kded loadedModules` |

## Die drei Namen, die dauernd verwechselt werden

**KDE ist der Hersteller, Plasma das Produkt, Qt das Material.** KDE ist die Gemeinschaft
und das Projekt, Plasma die Arbeitsoberflaeche, die sie baut, Qt der Werkzeugkasten, mit
dem Plasma programmiert ist. Wer "KDE ist abgestuerzt" sagt, meint fast immer
`plasmashell`.

**Ubuntu ist die Zusammenstellung, Kubuntu deren KDE-Ausgabe.** Darunter identisch, der
Unterschied ist die Oberflaeche. `lsb_release` meldet auf beiden "Ubuntu", der Beleg fuer
Kubuntu ist das Paket `kubuntu-desktop`.

**Linux ist nur der Kernel.** Alles, was danach kommt, ist Beiwerk der Distribution.

## Die vier Nahtstellen, an denen es bricht

**Erstens: Ein Dienst meldet einen Zustand, die Oberflaeche merkt ihn sich als Wunsch.**
Programme reden ueber D-Bus. Meldet BlueZ "Bluetooth ist jetzt aus", kann Bluedevil nicht
unterscheiden, ob Max geklickt hat oder ob gerade das System zumacht. Es speichert den
Zustand als Nutzerwunsch und stellt ihn beim naechsten Start wieder her. Genau so gingen
am 28.08.2026 Maus und Tastatur verloren, siehe `werkstatt/bugs/F-70`. Bekannter
KDE-Fehler, offen seit 2020: 418865, 445376, 469119.

**Zweitens: systemd stoppt Dienste, waehrend die Sitzung noch laeuft.** Beim
Herunterfahren faellt `bluetooth.target` vor Plasma. Wer beim Herunterfahren etwas
sichern will, kaempft gegen eine Reihenfolge, die systemd bestimmt. Der Ausweg ist immer
derselbe: **beim Start ansetzen, nicht beim Stoppen**, und dort vor `display-manager.service`.
Vor der Anmeldung laeuft garantiert noch kein Plasma, also gibt es kein Wettrennen.

**Drittens: Wayland ist nicht X11.** Programme, die X11 erwarten, brauchen einen
ausdruecklichen Hinweis. Chrome laeuft hier nur mit `--ozone-platform=x11`, sonst bleibt
jedes neu gestartete Fenster weiss. Memory: `chrome-braucht-hier-ozone-platform-x11`.

**Viertens: Snap-Programme sitzen im Kaefig.** Firefox und Spotify laufen als Snap, nicht
ueber `apt`. AppArmor verweigert ihnen Dinge, die anderen Programmen erlaubt sind, und
schreibt das ins Journal. Solche `DENIED`-Zeilen beim Herunterfahren sind Normalbetrieb
und kein Befund.

## Diagnose von unten nach oben

Die Reihenfolge ist die Ersparnis: Jede Antwort schliesst alles darunter aus.

```bash
rfkill list                                   # 1. Funkschalter offen?
journalctl -b -k | grep -i bluetooth          # 2. Kernel und Firmware da?
systemctl status bluetooth                    # 3. Dienst laeuft?
bluetoothctl show                             # 4. Adapter an? (Powered)
bluetoothctl devices Paired                   # 5. Geraet bekannt?
journalctl -b --since "-10min" | grep -i bluetooth   # 6. Wer hat eingegriffen?
```

**Ein gruener Dienst ist kein Beleg fuer ein funktionierendes Geraet.** Am 28.08.2026 war
Schritt 3 gruen und Schritt 4 lieferte `Powered: no`. Wer bei Schritt 3 aufhoert, sucht
anschliessend beim Funkchip.

## Was auf diesem Rechner schon passiert ist

- **F-70, 28.08.2026:** Bluedevil merkte sich den Shutdown als Nutzerwunsch, Maus und
  Tastatur weg. Reparatur: `werkstatt/systemd/bluetooth-zustand-wiederherstellen.service`
  setzt den gemerkten Zustand vor dem Anmeldebildschirm zurueck.
- **Chrome und Wayland:** ohne `--ozone-platform=x11` weisse Fenster.
- **KWallet ist seit dem 24.08.2026 aus**, Chrome legt Passwoerter seitdem unverschluesselt ab.
- **SSH-Zugang, seit 03.09.2026:** Der NUC hat einen gehaerteten `sshd`, erreichbar aus dem
  Heimnetz und ueber Tailscale, nur per Schluessel. Wer ein Geraet dazunehmen will oder eine
  Anmeldung ohne Grund abgewiesen bekommt, liest zuerst
  [ssh-zugang-zum-nuc.md](ssh-zugang-zum-nuc.md) — dort steht auch, warum ein kaputter
  Eintrag in `authorized_keys` nie eine Fehlermeldung erzeugt, sondern nur verweigert.
