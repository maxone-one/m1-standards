# Zadarma — Bibel der Lehren

**Zweck:** Sammelt jede Erfahrung, jeden Fehler und jede Tücke rund um **Zadarma**, den
Telefonie-Anbieter hinter Veras Rufnummer. Toolbezogen und projektübergreifend, das Pendant
zu `BUGS.md` und `IRRTUEMER.md`. Wer eine Rufnummer anbindet, liest sie **vorher**.

**Last updated:** 2026-08-19 (angelegt aus dem Abend, an dem die Nummer erstmals klingelte)
**Geltungsbereich:** Konto `max@maxone.one`, Rufnummer **+49 32 212 243 841**, SIP `#521528`
(Cloud-PBX, Max' Anlage) und `#507247` („VeraLiveKit"), Zugangsdaten in
`/opt/secrets/karastelev/zadarma.env`. Originaldoku in [`doku/`](doku/).

---

## I. Die unverhandelbaren Regeln

### ZAD-01 — NIEMALS an der Oberfläche raten, immer zuerst die Doku ziehen
Zadarma dokumentiert unseren Fall in den eigenen Anleitungen für **Vapi** und **Retell AI**,
und ein LiveKit-Community-Bericht nennt sogar den typischen Fehler. Eine halbe Stunde Klicken
hat nichts gelöst, zehn Minuten Doku alles.
*Lehre:* 18.08.2026. Daraus wurde die globale Regel „Doku vor dem ersten Griff".

### ZAD-02 — NIEMALS die WebRTC-Subdomain als SIP-Ziel eintragen
Die SIP-Adresse leitet sich aus der **Projekt-ID** ab (`p_2vkbqov8xmr` → 
`2vkbqov8xmr.sip.livekit.cloud`), nicht aus der WebSocket-Subdomain. Fehlerbild:
`404 No trunk found`.
*Lehre:* 18.08.2026, häufigster Fehler laut Community.

### ZAD-03 — NIEMALS DNS als Beleg für eine SIP-Adresse nehmen
Unter `.sip.livekit.cloud` löst **jede erfundene Subdomain** auf dieselben zwei IPs auf. Eine
Namensauflösung hätte also auch die falsche Adresse bestätigt.
*Lehre:* 18.08.2026.

### ZAD-04 — NIEMALS einen eingehenden Trunk ohne Adressliste betreiben
Ohne `allowed_addresses` nimmt der Trunk Anrufe von jedem an, der SIP-Adresse und Rufnummer
kennt, und jedes Gespräch geht auf unsere Rechnung. Gesetzt ist `185.45.152.0/24`, belegt
über drei unabhängige Quellen und danach mit einem echten Anruf geprüft.
*Lehre:* 18.08.2026, 22:44. Wurzel: `vera/docs/missbrauch-und-kostenschutz.md`.

### ZAD-05 — NIEMALS „gültig bis" für eine Freigabe halten
Die Zeile auf der Startseite ist die **bezahlte Laufzeit**. Eine Nummer kann bezahlt und
gleichzeitig in Prüfung sein. Der einzige verlässliche Ort ist
`my.zadarma.com/dirnum/active/` unter „Ihre Rufnummern", mit SIP-Nummer und Status
„Angeschlossen".
*Lehre:* 15.08.2026, in `vera/IRRTUEMER.md` festgehalten. **Ein Dokument über eine Sache ist
nicht die Sache.**

### ZAD-06 — Die IP-Bestätigung per Anruf an 8888 gilt nur für AUSGEHENDE Anrufe
Für die Zustellung an einen externen Server braucht es sie nicht. Unsere zwei eingetragenen
LiveKit-IPs stehen bis heute auf „Nicht bestätigt" und stören nicht. Der Prüfanruf scheitert
ohnehin (`sip server required auth`), weil LiveKit sich bei einem Provider **nicht
registrieren kann**.
*Lehre:* 18.08.2026, eine halbe Stunde.

### ZAD-07 — Eine Rufnummer an der Cloud-PBX kennt keinen externen Server
Der Reiter erscheint erst, wenn die Nummer von der PBX gelöst und einem eigenen SIP-Konto
zugeordnet ist. Solange sie dort hängt, gibt es kein Feld für eine SIP-Adresse und kein
freies Konto für einen Trunk.
*Lehre:* 18.08.2026.

---

## II. Drei Wege, die geprüft und versperrt sind

Damit sie niemand ein zweites Mal geht:

1. **Die Cloud-PBX kann nicht an eine externe SIP-Adresse zustellen.** „Externe Leitungen"
   holen fremde Nummern *herein*; Szenarien und Menüs kennen als Ziel nur interne
   Nebenstellen; die Weiterleitung je Nebenstelle geht auf eine **Telefonnummer** und wäre
   ein zweiter, kostenpflichtiger ausgehender Anruf je Anrufer.
2. **Die Weiterleitung eines SIP-Kontos geht nur „von SIP auf Telefon"**, wörtlich so im
   Formular. Keine SIP-Adresse.
3. **Ohne freies SIP-Konto gibt es keinen Trunk.** Das Auswahlfeld bleibt leer, solange nur
   das PBX-gebundene Konto existiert.

---

## III. Der Weg, der trägt (Cheatsheet)

1. Nummer von der Cloud-PBX lösen (Max' Anlage behält `#521528`).
2. Eigenes SIP-Konto anlegen, CallerID = die Rufnummer.
3. Bei der Rufnummer unter `dirnum/active/` das Zahnrad, Reiter **„Externer Server"**,
   Schalter *Externer Server (SIP URI)*, Feld `user@server[:port]`:
   `+4932212243841@2vkbqov8xmr.sip.livekit.cloud`
4. Bei LiveKit eingehenden Trunk mit derselben Nummer plus Dispatch-Regel anlegen, danach
   `allowed_addresses` setzen (ZAD-04).

**Kontrollanzeige:** „SIP 5xxxxx: Sie haben keine aktiven Endgeräte" ist ohne Trunk
erwartbar; verschwindet sie, ist die Zustellung verdrahtet.

---

## IV. Die Vorfälle (kurz)

### 2026-08-15 bis 18 — Dokumentenprüfung, vier Tage
Abgelehnte Ausweisfotos verschwinden aus der Dokumentengruppe, **ohne dass der Status es
sagt**. Der Vorgang lag drei Tage bei uns, nicht bei Zadarma. Klickpfad und drei tote Wege:
`vera/docs/zadarma-status-pruefen.md`.

### 2026-08-18 — Der Abend, an dem die Nummer klingelte
Erster echter Anruf um 22:07, nach einer halben Stunde Raten und zehn Minuten Doku. Wurzel
mit allen Einzelheiten: `vera/TODO.md`, Punkt 25.

### 2026-08-18 — Prüfanrufe an 8888 erzeugen echte Gesprächsprotokolle
Veras Worker läuft ohne festen Agentennamen und wird deshalb in **jeden** neuen Raum geholt.
Bei Testaufbauten im Blick behalten.

---

## V. Kosten, Rufnummernart, offene Punkte

**(0)32 ist eine nationale Teilnehmerrufnummer ohne Ortsbezug.** Für den Anrufer regelmäßig
teurer als eine geografische Nummer, und das trifft den Interessenten, der von unterwegs
zurückruft. **Eine Ortsnetznummer scheidet aus:** Der Ortsnetzbezug (Verfügung 25/2006 der
Bundesnetzagentur) verlangt Wohn- oder Betriebssitz im selben Ortsnetzbereich. Kein
Anbieterwechsel ändert daran etwas.

**Offen:** 0800 gegen Rückrufangebot rechnen (`vera/TODO.md`, Punkt 28). **Ungeprüft:**
Zadarmas mitgeliefertes CRM (Punkt 11) — bis dahin nichts dort anschließen.

**Fragil:** Zadarma betreibt mehrere Rechenzentren (`sipfr3`, `pbxfr1`, Frankreich). Ein
Standortwechsel für unsere Nummer läuft in die Adressliste aus ZAD-04 und sperrt uns aus.
**Bei „klingelt, aber niemand erreicht Vera" zuerst dort nachsehen.**

---

## VI. Querverweise

- [LiveKit-Bibel](../livekit/INDEX.md) — Trunk, Dispatch-Regel, SIP-Attribute
- `vera/TODO.md` Punkt 25 (der vollständige Weg), Punkt 11 und 28
- `vera/docs/zadarma-status-pruefen.md`, `vera/docs/missbrauch-und-kostenschutz.md`
- Originaldoku: [`doku/`](doku/)

---

## VII. Updates an dieser Bibel

Jede neue Lehre als nummerierte Regel, mit `*Lehre:*`, Datum und Beleg. Widerlegtes bekommt
einen Korrekturvermerk, es wird nicht gelöscht.
