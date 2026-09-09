# Design-Brief: die neun Dimensionen, die ein Werkzeug abfragt

**Herkunft:** Bis zum 09.09.2026 stand das hier im Standard `007-required-ui.md`, Abschnitt F.
Beim Neuschnitt ist es hierher gewandert, **ohne dass ein Punkt entfallen ist**.

**Die Regel steht in**
[`standards/017-pflichtbausteine-oberflaeche.md`](../../standards/017-pflichtbausteine-oberflaeche.md)
**Abschnitt F** (Max-Direktive 2026-07-01): Jedes neue Projekt und jede neue kundenseitige
Oberfläche wird zuerst über ein visuelles Design-Werkzeug validiert. **Niemals blind bauen.**
Hier steht, was in den Brief gehört, damit das Werkzeug nicht nachfragen muss.

## Die Werkzeuge

- **Claude Design** (claude.ai/design), Sync zum Code über `/design-sync` (bidirektional).
  **Kein Zeichenlimit** im Brief. Stellt vor dem Bau strukturierte Rückfragen, die ein guter
  Brief bereits vollständig vorwegnimmt.
- **Figma Make / Figma-MCP** (design-to-code und code-to-design). **Prompt-Limit 2000
  Zeichen**, also verdichten (echte Umlaute sparen Zeichen).
- **Framer** oder ähnliche visuelle Tools.

## Die Checkliste

1. **Deliverable:** interaktiver Prototyp (Screens klickbar verbunden) / statische
   Hi-Fi-Screens / Varianten zum Vergleich.
2. **Viewport-Priorität:** mobil zuerst (unser Default) / mobil + Desktop / Desktop zuerst.
3. **Interaktivitätsgrad:** voll interaktiv / teilweise / rein visuell.
4. **Von welchen Screens Varianten gewünscht sind.**
5. **Typografie-Richtung:** neutral-präzise / geometrisch-technisch / humanistisch-freundlich
   / charaktervolle Grotesk.
6. **Datenrealismus:** echte Domänen-Namen plus realistische Daten (Default, macht testbar)
   statt generischer Platzhalter. **Echte Firmen- oder Personendaten nie** (DSGVO),
   öffentliche Namen wie Netzbetreiber sind in Ordnung.
7. **Preisdarstellung:** dezent; bei noch unvalidiertem Preis beide Modelle zeigen, nicht
   festnageln.
8. **Domänen- und Regions-Referenz:** Branche, Region, reale Bezugsgrößen für realistische
   Beispiele.
9. **Look- und Flow-Vorbild:** den gewünschten Effekt **NEUTRAL** beschreiben, **niemals eine
   fremde Marke nennen**
   ([019-marke-und-sprache.md](../../standards/019-marke-und-sprache.md)).

## Stack und weiterführende Werkzeuge

shadcn/Radix/Base UI, Motion, React Hook Form plus Zod, die Formular-Prinzipien, die
`gsd-ui-*`-Skills und die Playwright-Verifikation stehen in der Memory
`reference_design_ux_toolchain`.
