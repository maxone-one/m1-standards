---
title: Der SSH-Zugang zum NUC
description: Seit 03.09.2026 laeuft sshd auf max-nuc, gehaertet auf Schluessel; wer reinkommt, wie ein Geraet dazukommt, und der stille Defekt, den ein kaputter Eintrag in authorized_keys erzeugt
---

# Der SSH-Zugang zum NUC

**Wann diese Datei zu lesen ist:** Bevor jemand einen Fernzugang zu Max' Arbeitsrechner
einrichtet, aendert oder debuggt, und immer dann, wenn eine Schluesselanmeldung ohne
erkennbaren Grund abgewiesen wird.

## Der Stand seit dem 03.09.2026

Bis zu diesem Tag war auf dem NUC **kein SSH-Server installiert**: `openssh-client` ja,
`openssh-server` nein, kein `sshd`, nichts auf Port 22. Von hier kam man raus, herein kam
niemand. Auf Max' Freigabe laeuft der Dienst jetzt.

| | |
|---|---|
| Hostname im Tailnet | `max-nuc` |
| Tailscale-Adresse | `100.92.222.127` |
| Heimnetz | `192.168.178.20` (Kabel), `192.168.178.30` (WLAN), beide per DHCP |
| Portfreigabe im Router | **keine**, aus dem offenen Internet ist der Rechner nicht erreichbar |
| Konfiguration | `/etc/ssh/sshd_config.d/99-maxone-haertung.conf` |

Die Haertung, wirksam gemessen mit `sshd -T`:

```
permitrootlogin no
passwordauthentication no
kbdinteractiveauthentication no
authenticationmethods publickey
allowusers max
maxauthtries 3
```

**Die Gegenprobe gehoert zur Einrichtung**, nicht die Behauptung: Ein Verbindungsversuch mit
`-o PreferredAuthentications=password -o PubkeyAuthentication=no` muss mit
`Permission denied (publickey)` enden. Tut er es, ist der Passwortweg wirklich zu.

## Warum dort keine ListenAddress steht

**Beide Heimnetz-Adressen kommen per DHCP.** Eine feste `ListenAddress` in der Konfiguration
waere ein Messwert von heute: Wechselt die Adresse, bindet `sshd` auf eine IP, die es nicht
gibt, und startet gar nicht mehr. Dazu kommt, dass dieses Ubuntu ueber `ssh.socket` lauscht,
das eine `ListenAddress` in `sshd_config` ohnehin ignoriert. Die Reichweite ergibt sich
stattdessen aus der Lage: Heimnetz und Tailnet, sonst nichts, weil im Router nichts
freigegeben ist.

## Wer reinkommt, und wie ein Geraet dazukommt

Zutritt hat, wer einen privaten Schluessel zu einem Eintrag in `~/.ssh/authorized_keys` des
Benutzers `max` besitzt. Stand 03.09.2026 sind das **zwei**:

| Fingerabdruck | Kommentar | Einschraenkung |
|---|---|---|
| `SHA256:ESDlTCWT…` | `vector@maxone-prod` | keine, von Max selbst gesetzt |
| `SHA256:NY3dUGgv…` | `root@maxone-prod` | `from="128.140.40.235,100.94.149.44"` |

**Der `from=`-Praefix ist die billigste Verengung, die es gibt**: Der Schluessel gilt dann nur
noch, wenn die Verbindung von genau diesen Adressen kommt, hier die oeffentliche IP von
maxone-prod und dessen Tailscale-Adresse. Wer einen Serverschluessel eintraegt, sollte ihn
immer so binden; ein Server im Rechenzentrum ist ein groesseres Ziel als ein Rechner im
Wohnzimmer.

Gegengeprueft am 03.09.2026 mit einer echten Verbindung von maxone-prod aus, Antwort
`max@max-nuc11pahi7`.

**`ssh-copy-id` funktioniert hier nicht**, und das ist Absicht: Es meldet sich zuerst per
Passwort an, und dieser Weg ist zu. Ein neues Geraet kommt so dazu:

1. Auf dem Geraet den oeffentlichen Schluessel auslesen (`cat ~/.ssh/id_ed25519.pub`), bei
   einer Telefon-App aus deren Schluesselverwaltung heraus.
2. Die Zeile auf dem NUC an `~/.ssh/authorized_keys` **anhaengen**, nie die Datei ersetzen.
3. Vorher sichern, danach mit `ssh-keygen -lf ~/.ssh/authorized_keys` gegenpruefen.

**Schritt 3 ist der eigentliche Punkt dieser Datei**, siehe unten.

## Der stille Defekt: ein kaputter Eintrag verweigert, er meldet nichts

Am 03.09.2026 sollte Max' iPhone Zutritt bekommen. Der Schluessel dafuer lag schon auf
`maxone-prod` in `/root/.ssh/authorized_keys`, Kommentar `iphone-max`, und sah dort
vollkommen normal aus. **Er ist ungueltig:** Sein Base64-Teil hat **69 Zeichen**, ein
ed25519-Public-Key hat immer **68**. Ein Zeichen zu viel, das typische Ergebnis eines
Kopiervorgangs aus einer Telefon-App.

**Die Folge ist unsichtbar:** In der Datei steht ein Zugang, der keiner ist. Niemand bekommt
eine Fehlermeldung, das Geraet wird nur abgewiesen, und die Ursache sieht wie ein
Berechtigungsproblem aus. Wie lange Max' iPhone schon nicht mehr auf maxone-prod kam, ist
ungemessen.

**Die zwei Pruefungen, die das in Sekunden zeigen:**

```
ssh-keygen -lf ~/.ssh/authorized_keys
```

```
awk '{print length($2), $NF}' ~/.ssh/authorized_keys
```

Die erste gibt **je gueltiger Zeile** einen Fingerabdruck aus; fehlt einer, ist die Zeile
kaputt. Die zweite zeigt die Base64-Laenge je Eintrag: 68 bei ed25519, 372 oder mehr bei
RSA. **Ein Schluessel laesst sich nicht reparieren, indem man das ueberzaehlige Zeichen
sucht**, welches es ist, laesst sich nicht erraten. Der Eintrag wird entfernt und der echte
Schluessel neu geholt.

## Tailscale SSH ist nicht eingeschaltet

`RunSSH` steht auf `false`. Eingeschaltet wuerde es Anmeldungen ohne jeden Schluessel
erlauben, geregelt ueber die Tailnet-ACL, und damit **jedes Geraet im Tailnet** zum
moeglichen Zutritt machen, `maxone-prod` und `maxone-prod-1` eingeschlossen. Das ist eine
Entscheidung fuer Max, keine Einrichtungsfrage; Claude Codes Sicherheitsschranke blockiert
`tailscale set --ssh` aus gutem Grund.

Verwandt: [INDEX.md](INDEX.md), `inventories/` fuer die Serverliste.
