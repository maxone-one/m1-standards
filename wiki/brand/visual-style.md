---
name: visual-style
description: maxone Brand-Bildsprache — Sony A7 IV + 24-70mm f/2.8 GM II als visueller Standard für KI-Bilder und reale Fotos über alle Properties (maxone.one, voltfair.de, vanfree.de, SLF, snapflow, vector etc.)
metadata:
  scope: brand
---

# maxone Visual Style

Einheitliche Bildsprache über alle maxone-Properties. Festgelegt 2026-05-20, laufend erweitert.

> **Diese Datei ist die SSoT (Single Source of Truth) für alle Bildprompts.** Alles, was generierte oder reale Bilder betrifft, steht hier. Die CLAUDE.md führt nur einen kurzen Pointer hierher, keine eigenen Bildregeln.

## Grundprinzip: Das Bild erzählt den Text (OBERSTE PRIORITAET, 2026-06-25)

Jedes Bild muss **die Kernaussage seines Textes visuell wiedergeben und für sich selbst sprechen**. Vor jedem Prompt zuerst fragen: Was sagt die Headline/der Text dieser Stelle, und wie zeigt das Bild genau das? Das Motiv illustriert die Aussage, nicht nur „Max irgendwo".

- Passt das Motiv nicht zur Aussage, ist es falsch (Vorfall 2026-06-25: Baustelle/Kabel sagte „Handwerk", die Headline war aber „KI-Revolution").
- Zwei Texte mit verschiedener Aussage brauchen zwei sichtbar verschiedene Bilder, nicht dasselbe Motiv in anderem Shirt (siehe „Bild-Set: keine Klone").
- Erst Aussage → dann Bildidee → dann Prompt. Nie ein generisches Porträt über eine spezifische Aussage legen.

## Pflicht-Checkliste (vor jedem Bildprompt durchgehen)

0. **Aussage zuerst:** Das Bild gibt die Kernaussage seines Textes wieder und spricht für sich. → "Grundprinzip: Das Bild erzählt den Text".
1. **Kamera/Look (Sony):** Immer den vollständigen Basis-Prompt verwenden, Sony A7 IV + FE 24-70mm f/2.8 GM II, editorial, natürliches Licht, flache Schärfentiefe, kein HDR/Smartphone-Look. → "Foto-Setup" + "Standard-Prompt".
2. **Brennweite aktiv wählen** nach Motiv (24-28 Architektur, 35 Lifestyle, 50 Portrait/Produkt, 70 Headshot). → "Brennweiten-Guide".
3. **Branding nur maxone.one:** Alle sichtbaren Screens, Devices, Mockups, Schilder, Kleidung zeigen ausschließlich maxone.one-Branding, keine Fremdmarken, keine Hersteller-Logos. → "Brand-Regel".
4. **Monitor & Peripherie:** Nie Dual-/Multi-Monitor, ein einziger ultrawide Curved (Samsung Odyssey G9 49" Form); Tastatur + Maus flach schwarz kabellos (Cherry DW 9500 Slim Form). → "Monitor- & Peripherie-Regel".
5. **Max' Umgebung (story-driven):** breiter Fundus echter Elektrohandwerk-Szenen (am Zählerschrank, an der Steckdose, an der Leuchte, an der Unterverteilung, am Schaltschrank, KNX-Installation, Baustelle, draußen am Gebäude) ODER modernes Büro. Eine kohärente, realistische Szene pro Bild, nie mischen, echte Oberflächen (kein PC auf Werkbank). Nie Kfz-/Schrauber- oder Schweißer-Werkstatt. Serverraum nur bei Infrastruktur-/Datensouveränitäts-Thema. → "Max' Arbeitsumgebung".
6. **Max im Bild:** Identitätsblock steht ZUERST im Prompt, vor Kamera und Szene (→ "Identität zuerst, Szene danach"). Genau EIN hochwertiges Frontal-Referenzfoto hochladen, nie mehrere mischen. Prompt in Ich-Form, niemals sein Aussehen beschreiben (Kategorien ja, Werte nein), kein Foto an Claude.
6b. **Personen = geschlossenes Ensemble (OBERSTE PRIORITÄT, 2026-06-27):** In jedem Personen-Prompt steht ausnahmslos ein echter Name, nie "a woman"/"a founder". Jede Frau ist **Viktoria** (Max' Freundin, auch Fotografin), weitere Personen kommen aus dem **KI-Team**, Max ist er selbst. Bei mehreren Personen sind ALLE aus dem Ensemble; reicht es nicht, gezielt erweitern. Referenzfoto je Figur, Aussehen nie beschreiben. → "Geschlossenes Personen-Ensemble".
7. **Personengruppen:** Diversität organisch, nie erzwungen, konkret benennen. → "Diversity".
8. **Format:** Blog-Cover und Heroes Querformat 16:9.
9. **Volles Foto, kein Blindraum:** Default sind frame-füllende Fotos ohne bewusst leeren schwarzen Negativraum. → "Komposition & Hero-Text".
9b. **Set-Varianz, keine Klone:** in einem Bild-Set nie zweimal dieselbe Einstellung (gleicher Arbeitsplatz/Sitzpose/Winkel, nur andere Kleidung). Setting, Haltung, Winkel, Ausschnitt, Tätigkeit variieren. → "Bild-Set: keine Klone".
10. **Technik immer State of the Art:** gezeigte Technik nie veraltet, besonders **PV-Module nur modern** (full-black monokristallin, keine alten blauen Polypanels). → "Technik State of the Art".
11. **Motiv-spezifische DON'Ts** frisch ableiten, nie aus einer Liste kopieren.
12. **Generatoren:** ChatGPT Image 2, Midjourney, Flux.
13. **Nach dem Generieren:** EXIF mit Sony-A7-IV-Metadaten setzen (exiftool). → "EXIF-Daten".

## Foto-Setup (real + simuliert)

- **Kamera:** Sony A7 IV (Vollformat, 33 MP)
- **Objektiv:** Sony FE 24-70mm f/2.8 GM II
- **Look:** Editorial, natürliches Licht, flache Schärfentiefe, neutrale Farben, kein HDR, kein Smartphone-Look

Bewusst Zoom statt Festbrennweite — mehr Schärfe, flexibler, kein „zitroniges" Festbrennweiten-Bokeh.

## Standard-Prompt für Bild-KI (ChatGPT Image 2, Midjourney, Flux)

**Vollständiger Basis-Prompt — IMMER komplett verwenden:**

```
Use the uploaded reference image as the exact identity reference.
Preserve the exact face, facial proportions, beard, nose, eyes, hairline,
age and expression from that reference. Do not reinterpret, average,
beautify or approximate the identity. The person in the output must be
recognisably the same individual as in the reference photo.

Shot on Sony A7 IV, full-frame mirrorless, Sony FE 24-70mm f/2.8 GM II, [FOCAL]mm.
Aperture f/2.8, ISO 200, 1/250s, natural daylight,
shallow depth of field, creamy bokeh, editorial photography,
true-to-life colors, neutral white balance, sharp focus on subject,
no oversaturation, no HDR look, no smartphone aesthetic,
clean uncluttered composition, professional commercial quality,
8k resolution, RAW workflow look.

DON'T: [motif-specific — freshly derived per prompt]

Brand rule: Unless a specific brand is explicitly requested,
all visible screens, devices, websites, profiles, apps, clothing logos
and signage show maxone.one branding only — no Apple, no Google,
no competitor brands, no generic placeholder UI.

Motif: [description]
```

**[FOCAL]** und **DON'Ts** werden pro Prompt neu entschieden — nie aus einer Liste kopiert.
Claude wählt die Brennweite aktiv anhand des Motivs und schreibt sie direkt rein.

### Identität zuerst, Szene danach (2026-07-25)

**Der Identitätsblock steht ab jetzt ganz oben, vor Kamera, DON'Ts und Markenregel.**
Vorher stand die einzige Identitätsverankerung („I am the person in the reference
photo") am Ende im Motif-Block, also nach rund achtzig Prozent des Prompts und nach
mehr als zwanzig anderen Bedingungen. Anlass: die zuletzt erzeugten Bilder zeigten
nicht mehr Max, sondern einen ähnlichen fremden Mann.

**Was daran belegt ist und was nicht.** Belegt ist nur die Reihenfolge in diesem
Dokument, die oben stand. Die verbreitete Erklärung, OpenAI habe die Gewichtung des
Referenzbildes gesenkt, ist eine plausible Annahme und keine Tatsache: Es gibt dazu
keine öffentliche Angabe, und ohne kontrollierten Gegentest mit identischem Prompt und
identischer Referenz lässt sie sich nicht prüfen. Die Umstellung lohnt sich trotzdem,
weil sie unabhängig davon wirkt: Ist die Annahme falsch, kostet sie nichts. Ist sie
richtig, war unsere alte Reihenfolge genau die anfälligste.

**Kein Widerspruch zur Regel „Aussehen nie beschreiben".** Der Block nennt nur die
Kategorien, die aus der Referenz übernommen werden sollen (Gesicht, Proportionen, Bart,
Nase, Augen, Haaransatz, Alter, Ausdruck), und keine Werte. Er sagt nicht, wie Max
aussieht, sondern dass genau das aus dem hochgeladenen Foto kommen soll. Werte zu
beschreiben bleibt verboten.

**Genau eine Referenz, frontal und hochwertig.** Nie mehrere Referenzfotos mischen, das
mittelt die Identität weg. Bei mehreren Personen im Bild je Figur eine eigene, klar
zugeordnete Referenz.

**Wenn das Ergebnis trotzdem nicht Max ist:** nicht den Prompt aufblähen, sondern
zuerst die Szene abspecken. Je weniger konkurrierende Randbedingungen im Prompt stehen,
desto mehr Gewicht bleibt der Identität. Eine Ferrari-, Werkstatt- oder Büroszene mit
wenigen Vorgaben hat früher zuverlässig funktioniert, ein Rechenzentrum mit Licht,
Kabelführung, Branding und zwanzig Negativanweisungen ist der schwierigste Fall.

## Komposition & Hero-Text: volle Fotos, kein Blindraum (OBERSTE PRIORITAET, 2026-06-25)

Default: **volle, frame-füllende Fotos**. Das Motiv/die Szene füllt den ganzen Rahmen, der Look ist dunkel und low-key, sodass heller Text per Overlay überall lesbar bleibt. **Niemals einen bewusst leeren schwarzen Negativraum prompten** (Formulierungen wie "CENTER/RIGHT dark and empty, reserved for headline text"). Bei zentriertem Hero-Text wirkt so ein reservierter Raum wie ein totes schwarzes Loch (Vorfall 2026-06-25: Elektriker-Werkstatt-Foto mit Max links, rechtes Drittel leerer Block).

Reservierter Negativraum ist NUR erlaubt, wenn der konkrete Hero bewusst so gebaut wird, dass der Text genau auf diese Fläche gelegt wird (seitlich ausgerichteter Hero). Dann Foto-Komposition und Hero-Layout zusammen planen: Text-Seite frei, Subjekt auf der Gegenseite.

Faustregel: **erst Hero-Layout festlegen (zentriert vs. seitlich), dann das Foto dazu komponieren.** Nie ein Foto mit Blindraum bauen, zu dem es kein passendes Layout gibt. Im Prompt für volle Fotos explizit: "the scene fills the entire frame, no empty black areas; overall dark, low-key mood so overlaid headline text stays readable."

## Bild-Set: keine Klone, Varianz erzwingen (OBERSTE PRIORITAET, 2026-06-25)

Mehrere Bilder von Max in einem Set (z.B. die fünf pro-Heroes) dürfen NIEMALS fast identisch sein. Wenn sich nur die Kleidung ändert, Arbeitsplatz, Sitzposition und Kamerawinkel aber gleich bleiben, wirkt das ganze Set wie ein einziger Shooting-Tag (Vorfall 2026-06-25: Startseite + KI-Revolution beide derselbe Ultrawide-Schreibtisch, gleiche Sitzpose, nur anderes Shirt).

**Über ein Set hinweg bewusst variieren** in mindestens je: Setting/Ort, Körperhaltung (sitzend / stehend / in Bewegung / kniend an Technik), Kamerawinkel (frontal / seitlich / über die Schulter / leicht von oben oder unten), Brennweite und Bildausschnitt (enger Headshot vs. mittel vs. weit/environmental), Tätigkeit (tippen / messen / prüfen / gehen / Gespräch). Nicht zweimal dieselbe „Mann sitzt frontal am Ultrawide"-Einstellung.

Höchstens EIN „sitzend frontal am Schreibtisch"-Motiv pro Set. Jedes weitere Büro-Bild braucht eine andere Achse (anderer Winkel, stehend, am Besprechungstisch, mit Unterlagen, weiter Raum), sonst Setting wechseln.

## Brand-Regel (Pflicht, 2026-05-29)

Wenn keine Marke explizit genannt wird, gilt ausnahmslos:
- **Alle Bildschirme/Devices:** zeigen maxone.one
- **Alle Website-Mockups:** maxone.one UI/Brand
- **Alle App-Profile, Social Feeds:** maxone.one
- **Firmenschilder, Beschilderung:** maxone.one oder generisch neutral

**Wichtige Unterscheidung bei Arbeitskleidung:**
- **Stil/Schnitt/Farbe** eines Herstellers (z.B. orange-schwarz wie Engelbert Strauss): darf beschrieben werden
- **Hersteller-Logos, Initialen (ES, etc.)** auf Ärmeln, Brust, Kragen: IMMER explizit ausschließen — "NO manufacturer logos, NO [XY] initials anywhere on clothing"
- **Einzige sichtbare Marke auf der Kleidung:** maxone.one, auf dem Rücken und optional Brust-Stickerei

Grund: Bild-KI setzt automatisch Hersteller-Initialen (ES, etc.) auf die Kleidung sobald der Markenname fällt, kann das echte Logo aber nicht authentisch reproduzieren. Lösung: kein Herstellerlogo, stattdessen maxone.one-Branding überall — Rücken als Wordmark "maxone.one", Ärmel/Brust als kleines lowercase "m" (niemals "M", "MO" oder "mo"). Im Prompt immer: "The only branding visible on clothing is maxone.one — wordmark on back, small lowercase 'm' logo patch on sleeve and chest."

## KI-Kennzeichnung: Hinweis genügt, kein Wasserzeichen (OBERSTE PRIORITÄT, 2026-07-21)

Jedes mit KI erzeugte Bild, das nach außen geht, wird als solches offengelegt. Rechtsgrundlage ist Artikel 50 der KI-Verordnung (EU) 2024/1689, anwendbar ab **2. August 2026** (Art. 113). Quelle: https://artificialintelligenceact.eu/article/50/

**Form:** Absatz 4 verlangt vom Betreiber nur, „dass der Inhalt künstlich erzeugt oder manipuliert wurde" offenzulegen, und schreibt dafür **keine bestimmte Form** vor. Ein sichtbares Wasserzeichen im Bild ist ausdrücklich nicht gefordert und wird bei maxone bewusst nicht gemacht (Entscheidung Max, 21.07.2026), weil es die Bildwirkung zerstört. Absatz 5 legt nur fest, dass die Information „spätestens zum Zeitpunkt der ersten Interaktion oder Exposition" und „in klarer und deutlich erkennbarer Weise" erfolgt, barrierefrei zugänglich.

**Also konkret:** ein Textbaustein dort, wo das Bild zuerst gesehen wird. Auf Plattformen ein Satz im Anzeigentext („Hinweis: Das Anzeigenbild wurde mit KI erzeugt."), auf eigenen Seiten eine Bildunterschrift oder ein klar auffindbarer Vermerk auf derselben Seite. Nicht ausreichend wäre ein Hinweis, den man erst nach Klick auf eine Unterseite findet.

**Die maschinenlesbare Markierung nach Absatz 2 trifft den Anbieter des KI-Systems**, also den Bildgenerator, nicht uns. Wir müssen sie nicht selbst setzen.

**EXIF bleibt wie gehabt (Entscheidung Max, 21.07.2026).** Der AI Act enthält keine Vorgabe zu Metadaten für Betreiber: die maschinenlesbare Markierung aus Absatz 2 adressiert den Anbieter des KI-Systems. Der simulierte Sony-A7-IV-Block unten wird deshalb unverändert weitergeschrieben. Wer die Offenlegung sucht, findet sie im sichtbaren Hinweis, das genügt der Verordnung.

**Text aus KI:** Absatz 4 verlangt eine Textkennzeichnung nur für Inhalte, die die Öffentlichkeit über Angelegenheiten von öffentlichem Interesse informieren, und nimmt redaktionell geprüfte Texte aus. Für Werbetexte besteht damit keine Pflicht. maxone legt es trotzdem offen, aus Haltung, und trennt dabei sauber zwischen Bild und Text (Wortlaut von Max, 21.07.2026):

```
Hinweis: Das Anzeigenbild wurde mit KI erzeugt.
Die Ideen für den Textinhalt entstammen meinem geistigen Eigentum und wurden mit KI augmentiert.
```

Die Trennung ist bewusst: das Bild ist vollständig maschinell erzeugt, der Text nicht. Idee, Angebot und Haltung stammen von Max, die Ausformulierung kam per KI dazu.

**Dieser Wortlaut ist die Single Source of Truth für JEDE KI-Offenlegung (Max, 25.07.2026).** Er gilt kanalübergreifend: eigene Seiten, Blog, Plattform-Anzeigen, Social, Angebote, Portale. Nicht umformulieren, nicht je Kanal neu erfinden, keine Varianten nach Einsatzgrad. Erlaubt ist einzig, das Substantiv im Bild-Satz konkret zu machen („Anzeigenbild", „Beitragsbild"), weil die Aussage dadurch unverändert bleibt. Der Bild-Satz wird nur gesetzt, wenn tatsächlich ein KI-Bild zu sehen ist, der Text-Satz bei jedem Text, an dem KI beteiligt war.

Im Code liegt derselbe Wortlaut als Konstante in `maxone.one/packages/ui/src/content/ai-disclosure.ts` und wird von dort in die Blog-Komponente `packages/ui/src/blog/AIDisclosure.svelte` gezogen. Wer den Satz ändert, ändert beides, diese Wiki-Stelle und die Konstante. **Anlass:** Der Blog trug bis 25.07.2026 drei selbst formulierte Varianten („KI-unterstützt", „KI-Entwurf, Mensch freigegeben", „KI-generiert"), also eine zweite Wahrheit neben diesem Text. Sie sind ersatzlos entfernt, das Frontmatter-Feld `aiUsage` schaltet die Offenlegung seitdem nur noch an oder aus.

Offen (Stand 2026-07-21): die bereits veröffentlichten Bilder auf allen maxone-Properties tragen noch keinen Hinweis. Vor dem 2. August nachziehen.

## EXIF-Daten für generierte Bilder

Nach dem Generieren mit `exiftool` schreiben. Brennweite aus dem KI-Output abfragen oder schätzen.

```bash
FOCAL=35  # je nach Motiv 24, 28, 35, 50, 70

exiftool \
  -Make="Sony" \
  -Model="ILCE-7M4" \
  -LensModel="FE 24-70mm F2.8 GM II" \
  -LensMake="Sony" \
  -FocalLength=$FOCAL \
  -FocalLengthIn35mmFormat=$FOCAL \
  -FNumber=2.8 \
  -ApertureValue=2.8 \
  -ISO=200 \
  -ExposureTime="1/250" \
  -ShutterSpeedValue="1/250" \
  -ExposureProgram="Aperture-priority AE" \
  -MeteringMode="Multi-segment" \
  -WhiteBalance="Auto" \
  -ColorSpace="sRGB" \
  -Software="Adobe Lightroom Classic" \
  -Artist="Max Karastelev" \
  -Copyright="© maxone.one" \
  -Orientation="Horizontal (normal)" \
  -overwrite_original \
  bild.jpg
```

## Brennweiten-Guide (Motiv → mm)

| Motiv | Brennweite |
|---|---|
| Architektur, Innenraum, Gruppe, Weitwinkel-Szene | 24-28mm |
| Office, Lifestyle mit Kontext, halbe Person, Candid | 35mm |
| Portrait klassisch, Produkt mit Umgebung | 50mm |
| Headshot, Detail, Produkt isoliert, Food-Closeup | 70mm |

## Monitor- & Peripherie-Regel (OBERSTE PRIORITAET, 2026-05-29, erweitert 2026-06-25)

**Niemals** zwei oder drei separate Monitore nebeneinander im Bild — das sieht nach generischem Setup aus.

**Max' echter Monitor: Samsung Odyssey G9 49"** — ein einziger ultrabreiter Curved-Monitor (49 Zoll, 32:9, weißes/silbernes Gehäuse mit charakteristischem Curved-Design).

| Arbeitsgerät | Monitor im Prompt |
|---|---|
| Desktop/normaler Arbeitsplatz | Samsung Odyssey G9 49", ultrawide curved, single monitor |
| MacBook | Das MacBook-Display selbst, kein externer Monitor |
| iPad | iPad-Display, kein externer Monitor |

Im Prompt formulieren als: "single ultrawide curved monitor, Samsung Odyssey G9 style, 49-inch panoramic display" — kein Hersteller-Logo im Bild nötig, nur die Form.

**Max' echte Tastatur + Maus: Cherry DW 9500 Slim, schwarz** — ein flaches, schwarzes kabelloses Set (Slim-/Low-Profile-Tastatur + passende flache schwarze Maus). In Büro-/Schreibtisch-Szenen so statt generischer Peripherie zeigen. Im Prompt: "a slim black low-profile wireless keyboard and a matching slim black wireless mouse (Cherry DW 9500 Slim style)" — kein Hersteller-Logo nötig, nur die Form.

**Gilt für alle Arbeitsplatz-/Developer-Szenen**, in denen Monitor oder Peripherie zu sehen sind. DON'T-Block-Pflicht: "NO dual monitors, NO multi-monitor setup, NO generic office monitors side by side."

## Max' Arbeitsumgebung im Bild: Elektrohandwerk-Szenen + Büro, story-driven (OBERSTE PRIORITAET, aktualisiert 2026-06-25)

Max' gelernter Beruf ist **Elektroniker für Energie- und Gebäudetechnik** (Elektrohandwerk, Gebäudeautomation, KNX/Smart-Home). Das ist ein **reicher Fundus authentischer Szenen, nicht nur die Achse "Werkstatt oder Büro"**. Dynamisch und flexibel bleiben, **Geschichten erzählen** statt sich auf zwei Settings festzulegen.

**Szenen-Palette (Beispiele, nicht abschließend):** am Zählerschrank, an einer Steckdose (die verdrahtet wird), an einer Leuchte/Lampe, an der Unterverteilung, am offenen Schaltschrank, bei einer KNX-/Smart-Home-Installation, auf der Baustelle, draußen am Gebäude/an der Fassade, an Energietechnik/PV; dazu das moderne, aufgeräumte **Büro/Developer-Setup**; dazu themengebunden der **Serverraum** (nur wenn das Bild-Thema Infrastruktur/Datensouveränität ist, siehe unten).

**Pro Bild EINE kohärente, realistische Situation (OBERSTE PRIORITAET):** Nichts Unpassendes mischen. Kein teures PC-/Monitor-Setup an einen Einsatzort oder auf eine Werkbank stellen (unrealistisch, Vorfall 2026-06-25). Büro = echter, glatter Schreibtisch (Holz/Laminat/dunkle moderne Tischplatte), keine Werkbank-Oberfläche; dort gehört das Rechner-Setup hin. Einsatz-/Handwerks-Szene = Fokus aufs Elektrohandwerk, kein Office-PC mitten in der Szene.

**Verboten (harte DON'Ts):**
- **Keine Kfz-/Schrauber-/Mechaniker-Werkstatt.**
- **Keine Schweißer-Werkstatt.**
- **Kein Serverraum als generischer Hintergrund** für ein Persona-Porträt.

**Ausnahme Serverraum (themengebunden):** Wenn das Bild-Thema selbst Infrastruktur, Hosting, Self-Hosted oder Datensouveränität ist (z.B. maxone.pro/made-in-germany), ist ein Serverraum/Rack genau das richtige Motiv und ausdrücklich erlaubt. Dann den Serverraum-DON'T weglassen. Die Server-room-Sperre gilt nur als Backdrop für Themen, die nichts mit Infrastruktur zu tun haben.

Generische "tools / workbench"-Formulierungen kippen bei der Bild-KI zuverlässig in eine Auto- oder Schweißer-Werkstatt (Vorfall 2026-06-25), deshalb immer elektrisch konkretisieren.

**Im Prompt konkret nennen** (statt generisch "tools"), je nach Szene z.B.: a meter cabinet (Zählerschrank), a wall socket being wired, a ceiling/wall luminaire, a sub-distribution board, an open electrical control cabinet with circuit breakers on DIN rails, coiled wiring and conduit, terminal blocks, multimeter, wire strippers, KNX / smart-home modules, a construction site or building facade. Büro-Variante: aufgeräumter, ruhiger Arbeitsplatz mit echtem Schreibtisch im Brand-Look.

**DON'T-Block-Pflicht bei Werkstatt-/Arbeitsplatz-Szenen mit Max:** "NO automotive or mechanic's garage elements (no wrenches, sockets, ratchets, engine parts, tires, oil, bench vise), NO welding workshop (no welding torch, sparks, welding mask) — this is an electrician's / building-automation scene or an office." Den Serverraum-DON'T ("NO server room or data center, no server racks") nur ergänzen, wenn das Thema NICHT Infrastruktur/Datensouveränität ist.

## Technik immer State of the Art, besonders PV-Module (OBERSTE PRIORITAET, 2026-06-25)

Gezeigte Technik im Bild ist **immer der aktuelle State of the Art, nie veraltet**.

**PV-Module ausnahmslos modern:** full-black monokristalline Glas-Glas-Module mit homogener schwarzer Fläche, schlanker rahmenarmer/randloser Look. **Niemals veraltet:** keine blauen polykristallinen Panels, keine groben silbernen Sammelschienen/Gitterlinien, keine klobigen dicken Alurahmen im 2010er-Look.

Im Prompt: "modern state-of-the-art all-black monocrystalline glass-glass PV modules, sleek frameless look. NO old blue polycrystalline panels, no dated thick aluminium frames, no visible retro cell grid."

Gilt sinngemäß für alle gezeigte Technik (Geräte, Schaltschränke, Wechselrichter, Werkzeuge, Devices): aktuell statt antiquiert.

## Geschlossenes Personen-Ensemble: nur echte, benannte Wiederkehrer (OBERSTE PRIORITÄT, 2026-06-27)

maxone-Bilder haben ein **geschlossenes, benanntes Ensemble** echter, wiederkehrender Personen, niemals zufällige KI-Gesichter. Bewusst experimentell (Max: "ich weiß nicht ob es funktioniert"), Ziel ist ein unverwechselbares, konsistentes Marken-Ensemble statt austauschbarer Stockgesichter.

> **Cast-SSoT (wer, Rolle, Referenzbild, Status): [`packages/ui/src/content/ensemble.json`](../../../Projects/maxone.one/packages/ui/src/content/ensemble.json) im maxone.one-Repo.** Vor jedem Personen-Prompt dort casten. Diese Datei führt die Personen-Daten, visual-style.md führt die Regeln.

1. **Echter Name in JEDEM Personen-Prompt, ausnahmslos.** Nie "a woman", "a founder", "a customer". Jede Person ist ein benanntes Ensemble-Mitglied per Referenzfoto, Aussehen wird nie in Worten beschrieben. Reine Hände-/Detailaufnahmen ohne Gesicht brauchen kein Referenzfoto, aber der Name (wessen Hände) steht trotzdem im Prompt.
2. **Das Ensemble:** **Max** (er selbst, "I am the person in the reference photo"), **Viktoria** (Max' Freundin, zugleich Fotografin) und die Mitglieder des **KI-Teams** (Wired-Familie).
3. **Bei mehreren Personen sind ALLE aus dem Ensemble**, nicht nur eine. Reichen die bekannten Figuren nicht (das Foto braucht mehr Personen als etabliert sind), wird das Ensemble um genau die fehlenden erweitert: jede neue Figur bekommt einen echten Namen plus Referenz und wird ab dann ebenfalls immer wiederverwendet. Niemals willkürlich Fremde, niemals eine neue Person, außer für eine echte neue Rolle/Zielgruppe (z.B. Elektro-Handwerk).
4. **Diversität kommt aus dem Ensemble**, nicht aus erfundenen Gesichtern: das Ensemble (vor allem das KI-Team) ist divers besetzt, eine diverse Gruppe entsteht durch diverse Ensemble-Mitglieder. Überschreibt die frühere Diversity-Regel insofern: organisch ja, aber nur mit benannten Figuren.
5. **Voraussetzung fotoreal:** Jede Figur braucht eine feste Referenz-Identität (Referenzfoto). Etabliert: Max, Viktoria. Für das KI-Team muss je eine kanonische Referenz festgelegt werden, BEVOR ein Mitglied in einem Foto auftaucht (einmal ein kanonisches Portrait pro Mitglied festlegen, danach wie Max/Viktoria wiederverwenden). Bis dahin sind fotoreale Personen-Bilder auf Max und Viktoria beschränkt.

**Coverage-Stand (2026-06-27):** Das KI-Team hat **13 Mitglieder**. **11 haben** ein fotorealistisches Portrait in `apps/*/static/team/*.webp` (einheitlicher Studio-Look, AI-Ohrhörer, divers): Vector, Vigil, Vault, Vantage, Valor, Vera, Viper, Vista, Vortex, Vox, Vybora; dazu Viktoria. **2 fehlen noch (Lücke):** **Vega** (Video Production) und **Visor** (QA Engineer) haben kein Portrait, müssen erst je eines im Team-Stil bekommen, bevor sie in Bildern auftauchen können. **Vector ist abgedeckt:** kanonischer Ensemble-Look = das fotorealistische `team/vector.webp` (der NEUE, menschliche Vector). Die stilisierte Variante mit orangen Augen (`vector-ki-assistent-closeup-orange-augen.webp`) ist der bisherige Vector und wird nach Abschluss der Transformation zu **Vector Junior** (Archiv/Referenz, nicht der aktive Vector, nicht für Personen-Szenen). Offener Praxistest für alle: hält das Gesicht beim Generieren in echte Szenen (nicht nur Headshot)?

## Diversity in Personenbildern (2026-05-29)

Wo die Situation es natürlich erlaubt, Personengruppen divers besetzen:
- Eine Frau
- Ein Mann arabischer Abstammung
- Ein Mann mit leicht dunklerem Teint

**Niemals auf Zwang.** Wenn das Setting es nicht erlaubt (z.B. historisch, regional, Einzelportrait ohne Kontext), dann nicht erzwingen. Wenn eine Gruppe von 3-4+ Personen dargestellt wird, ist Diversität der Standard — aber sie muss sich organisch anfühlen, nicht wie ein Diversity-Katalog.

Im Prompt: Personen natürlich und konkret beschreiben, keine generischen "diverse people" Formulierungen — lieber: "one woman in her 30s, one man of Middle Eastern descent, ..."

## Wo gilt das?

- Alle KI-generierten Bilder für maxone-Properties
- Reale Fotos von Max (sobald Setup gekauft)
- Hero-Bilder, OG-Images, Blog-Header, Produkt-Mockups
- Nicht für: User-Uploads (Provider-Logos, Bewerbungsfotos etc.)

## Wann diese Wiki nutzen?

- Bei jedem neuen KI-Bild-Auftrag für maxone-Brand-Material
- Bei Brand-Konsistenz-Prüfungen über Properties hinweg
- Bei Foto-Setup-Fragen (Hardware, Workflow, EXIF)

## Sources

- Entscheidung 2026-05-20 (Max + Claude-Session)
- Erweiterung 2026-05-29: DON'T-Liste + Brand-Regel (alle sichtbaren Marken = maxone.one)
- Eintrag in [[MAX.md]] → Brand-Foto-Setup
