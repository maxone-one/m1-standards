# Zustellgarantien in Ketten zwischen Diensten

**Pflicht-Spec: Standard 033**, Abschnitt „Eine Kette ist erst gebaut, wenn sie zustellt".
Hier steht, warum die sieben Punkte so und nicht anders geschnitten sind.

## Herkunft

Am 27.08.2026 lag ein diktierter Text eines fremden KI-Fachmanns vor, der Agenturen
vorwirft, n8n-Workflows ohne Infrastruktur zu bauen. Seine Liste: Dead-Letter-Queue,
Circuit-Breaker, Rate-Limit-Handling, Fehler-Logging, strukturiertes Logging,
Webhook-Signaturpruefung, Audit-Logs, Schema-Validierung.

**Die Liste ist richtig und unvollstaendig an genau der teuersten Stelle.** Idempotenz
fehlt darin, und das ist der Fehler, der einem in Woche zwei passiert, nicht in Jahr
zwei. Umgekehrt steht der Circuit-Breaker darin, ein Muster fuer Dienste mit hohem
Durchsatz, das bei einer Kette mit ein paar hundert Vorgaengen am Tag nichts loest. Wer
so priorisiert, hat die Muster gelesen und nicht betrieben.

Daraus die Lehre, die den Abschnitt traegt: **Die Reihenfolge einer Prueflisten ist
selbst eine Aussage.** Was zuerst steht, wird zuerst gebaut. Idempotenz steht deshalb
auf Platz eins und der Circuit-Breaker gar nicht drauf.

## Warum Alarm und Log getrennt gefuehrt werden

Sein eigenes Bild war: Um drei Uhr nachts faellt der Webhook aus und niemand weiss,
warum die Leads nicht mehr ankommen. Gegen genau dieses Bild hilft ein Log nicht, denn
ein Log liest man erst, wenn man schon weiss, dass etwas kaputt ist. Die Trennung im
Standard (Punkt 4 gegen Punkt 7) haelt das auseinander: Punkt 7 dient der Diagnose,
nachdem man Bescheid weiss, Punkt 4 sorgt dafuer, dass man Bescheid weiss.

## Warum die Signatur ein Zeitfenster braucht

Eine reine HMAC-Pruefung sagt nur, dass die Nachricht echt ist, nicht dass sie neu ist.
Wer eine gueltige Nachricht einmal mitschneidet, kann sie ohne Zeitstempel im
Signaturumfang beliebig oft nachspielen. Idempotenz (Punkt 1) faengt das ab, sofern der
Absender einen stabilen Schluessel mitschickt; das Zeitfenster ist die zweite Tuer fuer
den Fall, dass er es nicht tut.

## Was der Text sonst noch hergab, ausserhalb der Technik

**„Infrastructure as a Service" ist der falsche Begriff** fuer das, was er beschreibt.
IaaS ist besetzt und meint gemietete Rechenleistung (EC2, Hetzner). Was er meint, ist
ein Betriebsversprechen: nicht einmal Aufbau gegen Festpreis, sondern eine Zahl im Monat
mit einer Zusage dahinter. Der Gegensatz ist Projekt gegen Betrieb, nicht SaaS gegen IaaS.

**Fuer den Verkauf wird jeder Punkt uebersetzt.** Kein Unternehmer kauft eine
Fehlerschlange. Er kauft „du erfaehrst von einem verlorenen Lead in vier Minuten statt in
vier Wochen, und der Lead ist danach trotzdem im CRM".

*Angelegt 27.08.2026 im Zug der Aufnahme in Standard 033.*
