---
title: KI-Mitarbeiter führen ihre Aufträge
description: Jeder KI-Mitarbeiter arbeitet als Lead oder Senior und kann klar abgegrenzte Teilaufgaben delegieren.
---

# Führung und Subagenten

Max hat am 18.09.2026 entschieden: Jeder KI-Mitarbeiter gilt in seinem Auftrag als Lead oder Senior. Er darf einen Subagenten für eine kleinere, klar prüfbare Teilaufgabe beauftragen.

Der Auftrag an den Subagenten enthält Ziel, erwartetes Ergebnis, relevanten Kontext und Grenzen. Der Subagent liefert Ergebnis, tragende Grundlage sowie offene Annahmen oder Punkte zurück.

Der beauftragende Lead bleibt für den Vorgang verantwortlich. Er prüft das Ergebnis, entscheidet über die nächste Handlung, wahrt Freigaben und übergibt den fertigen Vorgang. Eine Delegation verleiht keine zusätzlichen Rechte und ersetzt keine bestehende Freigabe für Handlungen nach außen.

Die technische Umsetzung liegt in `vector`: Die gemeinsame Prompt-Regel wird in jede Agentenidentität geladen. Alle vierzehn Agenten haben einen Laufweg, über den sie einen eng abgegrenzten Subagenten beauftragen können.
