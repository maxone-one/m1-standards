# Fish Audio — Bibel der Lehren

**Zweck:** Sammelt jede Erfahrung, jeden Fehler und jede Tücke rund um **Fish Audio**, die
Ersatzstimme für Vera. Toolbezogen und projektübergreifend, das Pendant zu `BUGS.md` und
`IRRTUEMER.md`. Wer die Sprachausgabe anfasst, liest sie **vorher**.

**Last updated:** 2026-08-19 (angelegt)
**Geltungsbereich:** Konto `karastoni@googlemail.com`, Plus-Paket mit 250.000 Credits, bezahlt
bis 02/2027. Bei Vera **nicht verdrahtet**, aber als Ausweichweg vorgesehen. Originaldoku in
[`doku/`](doku/).

---

## I. Die unverhandelbaren Regeln

### FISH-01 — NIEMALS den Pay-as-you-go-Wallet für den Kontostand halten
**Fish Audio hat zwei Töpfe.** Der Wallet zeigte 1,65 Dollar, während das unangetastete
Plus-Paket 250.000 Credits hielt. Wer nur den Wallet liest, hält ein volles Konto für fast
leer und baut darauf eine falsche Entscheidung.
*Lehre:* 18.08.2026, von Max binnen Minuten gefunden, nachdem die Guthabenprüfung genau
dagegen gebaut worden war. Steht in `vera/IRRTUEMER.md`. **Richtiger Endpunkt für das Paket:**
`api.fish.audio/wallet/self/package`.

### FISH-02 — Fish Audio gibt seinen Kontostand heraus, Cartesia nicht
Das ist der entscheidende betriebliche Unterschied und der Grund, warum Fish Audio als
Ausweichweg taugt: Der Stand lässt sich **ohne Verbrauch** abfragen. Bei Cartesia gibt es
sechs geprüfte Endpunkte, die alle mit 404 antworten, und der einzige belastbare Weg ist eine
Zwei-Zeichen-Probe, die echte Credits kostet.
*Lehre:* 18.08.2026, `agent/kontingent.py`.

### FISH-03 — NIEMALS mit dem Google-Knopf anmelden
Der Google-Weg landet im privaten Konto `karastoni@gmail.com`, nicht im Konto, das das
Plus-Paket und den API-Schlüssel trägt. Anmeldung mit `karastoni@googlemail.com` **und
Passwort**. Zur Gegenprobe: Die Nutzerkennung im Konto muss zu der aus dem API-Schlüssel
passen.
*Lehre:* 18.08.2026, TODO 1.

### FISH-04 — Ein Kunstwort wird buchstabiert, und das entscheidet Hörtests
Im Hörtest am 15.08.2026 buchstabierte Fish Audio „maxone", Cartesia sprach es. Max wörtlich:
„Fish Audio hat maxone buchstabiert und sie redet wie eine Therapeutin." **Der tragende Grund
war objektiv, nicht geschmacklich:** Der Firmenname fällt in Veras erstem Satz, also in jedem
einzelnen Gespräch.
*Lehre:* DEC-27. Wer Fish Audio je einschaltet, prüft **zuerst** diesen einen Fall.

### FISH-05 — Eine Adressänderung ist im Profil nicht vorgesehen
Die Profilbearbeitung kennt nur Avatar, Name und soziale Links. Eine Umstellung des Kontos auf
`vera@maxone.work` ist dort **nicht möglich**, und das ist kein Bedienfehler.
*Lehre:* 18.08.2026, TODO 1.

### FISH-06 — Das Paket ist bezahlt, der Ausweichweg ist es nicht
250.000 Credits liegen bis Februar 2027 bereit, aber `agent/entrypoint.py` kennt weiterhin
**genau ein** TTS. Fällt Cartesia aus, bleibt Vera stumm, obwohl ein bezahlter Ersatz
danebenliegt.
*Lehre:* BUG-016, Lücke 1, offen seit 17.08.2026. **Ein bezahlter Ausweichweg, der nicht
verdrahtet ist, ist kein Ausweichweg.**

---

## II. Verbotene Griffe

- **Kein Wechsel der Stimme im laufenden Betrieb ohne Hörprobe.** Die Stimmenwahl ist eine
  Entscheidung von Max' Ohr (DEC-27), keine technische.
- **Kein Schlüssel in einer Kommandozeile**, immer aus dem Secret-Store.
- **Kein Umstieg allein wegen des Minutenpreises.** Fish Audio ist billiger (0,021 gegen
  0,03 Dollar je Sprechminute), verlor den Hörtest aber an der Aussprache. Der Preis war nie
  das Kriterium.

---

## III. Erlaubte Operationen (Cheatsheet)

```bash
# Kontostand des Pakets, ohne Verbrauch
python tools/kontingent_pruefen.py     # 0 = frei, 1 = leer, 2 = unbekannt (und 2 ist NICHT 0)

# Direkt am Anbieter
curl -s -H "Authorization: Bearer $FISHAUDIO_API_KEY" https://api.fish.audio/wallet/self/package
```

---

## IV. Die Vorfälle (kurz)

### 2026-08-15 — Hörtest verloren
Gegen Cartesia, an einem einzigen Wort. Beide Aufnahmen mit angeglichenem Format und Pegel,
sonst wäre der Vergleich wertlos gewesen (`vera/hoerprobe/`).

### 2026-08-18 — Der falsche Topf
Die Guthabenprüfung las den Wallet statt des Pakets und meldete Beinahe-Leere für ein volles
Konto. Behoben am selben Tag.

---

## V. Checkliste, bevor Fish Audio je scharf geschaltet wird

1. Kontostand am **Paket** prüfen, nicht am Wallet (FISH-01).
2. Eine Hörprobe mit „maxone", „maxone.work" und einer Mailadresse erzeugen (FISH-04).
3. Prüfen, ob Fish Audio ein eigenes Dockerfile verlangt — bei der Entscheidung für Cartesia
   war genau das der Unterschied im Deployment.
4. Erst danach in `agent/entrypoint.py` als Ausweichweg verdrahten (FISH-06).

---

## VI. Querverweise

- [Cartesia](../cartesia/INDEX.md) — die eingesetzte Stimme, Marlene, `sonic-3`
- `vera/BUGS.md` (BUG-016), `vera/IRRTUEMER.md`, `vera/agent/kontingent.py`
- `vera/.planning/vorarbeit/stimme-und-ton.md`, `vera/docs/hoertest-ablauf.md`
- Originaldoku: [`doku/`](doku/)

---

## VII. Updates an dieser Bibel

Jede neue Lehre als nummerierte Regel, mit `*Lehre:*`, Datum und Beleg. Widerlegtes bekommt
einen Korrekturvermerk statt gelöscht zu werden.
