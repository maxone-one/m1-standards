# Die Abfragen für das Kontoinventar

Fertig vorbereitet am 22.08.2026, damit der Tag nach dem Einrichten aus Ausführen besteht
und nicht aus Nachdenken. Alle Abfragen sind **lesend**, mehr kann der offizielle Server
ohnehin nicht. Sie laufen über das Werkzeug `search` mit der jeweiligen Kundennummer.

**Beträge stehen in Micros.** `cost_micros` geteilt durch 1.000.000 ergibt Euro. Wer das
vergisst, meldet Max eine Million Euro Werbeausgaben.

## 1. Welche Konten hängen unter dem Verwaltungskonto

Zuerst `list_accessible_customers`, das braucht kein GAQL. Danach die Hierarchie:

```sql
SELECT customer_client.id,
       customer_client.descriptive_name,
       customer_client.manager,
       customer_client.status,
       customer_client.currency_code
FROM customer_client
WHERE customer_client.level <= 1
```

Diese eine Abfrage beantwortet, ob alle fünf bekannten Kundennummern wirklich
darunterhängen und ob eine sechste auftaucht, die im Postfach nie erwähnt wurde.

## 2. Wer hat Zugriff, und hängt CleverAds noch dran

Der erste Blick, der wirklich zählt. 2022 wurden „CleverAds APP" und „Plai" als fremde
Verwaltungskonten verknüpft.

```sql
SELECT customer_manager_link.manager_customer,
       customer_manager_link.status
FROM customer_manager_link
```

```sql
SELECT customer_user_access.email_address,
       customer_user_access.access_role,
       customer_user_access.access_creation_date_time
FROM customer_user_access
```

`[?]` Ob `customer_user_access` unter Explorer Access lesbar ist, ist ungeprüft. Diese
Stufe sperrt die Kontoverwaltung, und die Grenze zwischen Lesen und Verwalten ist dort
nicht dokumentiert. Fällt sie aus, geht dieselbe Frage von Hand über Einstellungen,
Zugriff und Sicherheit.

## 3. Was hat jedes Konto gekostet, Monat für Monat

```sql
SELECT segments.month,
       metrics.cost_micros,
       metrics.clicks,
       metrics.conversions
FROM customer
WHERE segments.date BETWEEN '2025-08-01' AND '2026-08-21'
ORDER BY segments.month
```

Das ist die Zahl, um die es geht: Wo ist in zwölf Monaten Geld rausgelaufen, und wofür.

## 4. Welche Kampagnen stehen noch scharf

```sql
SELECT campaign.id,
       campaign.name,
       campaign.status,
       campaign.advertising_channel_type,
       campaign_budget.amount_micros,
       metrics.cost_micros,
       metrics.conversions
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
ORDER BY metrics.cost_micros DESC
```

`campaign.status = ENABLED` bei einem Konto, das nicht mehr ausliefert, heißt: Sobald die
Zahlung wieder geht, läuft es sofort weiter. Das ist der Unterschied zwischen gestoppt und
abgestellt, und er kostet Geld.

## 5. Wofür wurde tatsächlich bezahlt

```sql
SELECT search_term_view.search_term,
       metrics.cost_micros,
       metrics.clicks,
       metrics.conversions
FROM search_term_view
WHERE segments.date DURING LAST_30_DAYS
ORDER BY metrics.cost_micros DESC
LIMIT 200
```

Die Suchbegriffe sind die härteste Quelle für verschwendetes Budget. Was hier oben steht
und keine Conversion trägt, gehört in die Negativliste. Der zugehörige Ablauf steht im
Suchbegriff-Ritual in `~/.claude/marketing-skills/ads/references/google-search-playbook.md`.

## 6. Misst das Konto überhaupt etwas

```sql
SELECT conversion_action.name,
       conversion_action.status,
       conversion_action.type,
       conversion_action.primary_for_goal
FROM conversion_action
```

Ohne aktive Conversion-Aktion ist jede Optimierung im Konto blind gewesen. Das wäre kein
Detail, sondern die Erklärung für alles andere.

## Reihenfolge

Erst 1 und 2, das sind Bestand und Sicherheit. Dann 6, denn ohne Messung sind 3 bis 5 nur
Kosten ohne Gegenwert. Danach 3, 4, 5 für die eigentliche Auswertung.
