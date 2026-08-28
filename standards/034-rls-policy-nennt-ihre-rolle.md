# 034: Jede RLS-Policy nennt ihre Rolle mit `TO`

**Status:** active
**Seit:** 2026-08-29
**Gilt für:** jedes Projekt mit einer Postgres- oder Supabase-Datenbank

**Eine Policy ohne `TO` gilt in Postgres für `PUBLIC`**, also auch für `anon` und
`authenticated`, deren Schlüssel im Browser jedes Besuchers stehen. `TO` ist deshalb
Pflicht in jeder `CREATE POLICY`, ohne Ausnahme, auch wenn der Name der Policy die
Beschränkung schon zu sagen scheint.

```sql
-- FALSCH: heißt "service role", gilt aber für jeden
CREATE POLICY "Service role full access to kunden"
  ON public.kunden FOR ALL USING (true) WITH CHECK (true);

-- RICHTIG
CREATE POLICY "kunden_service_all"
  ON public.kunden FOR ALL TO service_role USING (true) WITH CHECK (true);
```

## Der Name ist kein Beleg, und genau daran scheitert die Sichtprüfung

**Ein Bezeichner, der eine Beschränkung behauptet, und ein Kommentar, der sie
wiederholt, sehen zusammen so plausibel aus, dass niemand die fehlende Zeile
vermisst.** Deshalb ist der Policy-Name in einem Review wertlos: Er beschreibt die
Absicht, nicht die Wirkung.

**Die einzige Quelle ist `pg_policies`, Spalte `roles`.** Die Prüffrage nach jeder neuen
Policy und in jedem Review lautet: Steht dort etwas anderes als `{public}`?

```sql
SELECT tablename, policyname, cmd, roles::text
  FROM pg_policies
 WHERE schemaname = 'public' AND roles::text = '{public}'
   AND (qual IS NOT DISTINCT FROM 'true' OR with_check IS NOT DISTINCT FROM 'true');
```

## Wer eine solche Stelle findet, sucht die ganze Datenbank ab

**Nie nur die gemeldete Stelle reparieren.** Am 29.08.2026 in venfree: Der Code-Review
nannte drei Objekte. Die Abfrage oben fand elf Treffer, davon zwei weitere echte, und
**einer davon lag in einer Tabelle, die mit dem gemeldeten Bereich nichts zu tun hatte**
(`bom_waitlist`, mit Mailadresse, IP-Adresse und der kompletten Stückliste). Wäre nur
das Gemeldete repariert worden, stünde dieser Fall heute noch offen.

## Belegt wird mit dem öffentlichen Schlüssel, nicht mit der Migration

**Eine Migration zeigt die Absicht, nicht den Zustand.** Ob eine Lücke offen steht,
beantwortet genau eine Anfrage gegen die laufende API, mit dem `anon`-Schlüssel aus dem
ausgelieferten HTML:

```
curl "$SUPABASE_URL/rest/v1/<tabelle>?select=*&limit=1" \
     -H "apikey: $ANON_KEY" -H "Authorization: Bearer $ANON_KEY"
```

`HTTP 200` mit Inhalt heißt offen. `HTTP 401` heißt zu. `HTTP 200` mit `[]` heißt, das
Tabellenrecht besteht, aber RLS greift; das ist bei reinen Formular-Tabellen mit
`INSERT`-Recht der Normalfall und kein Mangel. **Diese Prüfung ist rein lesend und
gehört zu jeder Abnahme einer Datenbankänderung.**

## Das Tabellenrecht wird zusätzlich entzogen

**RLS allein genügt für die Wirkung, aber nicht für die Haltbarkeit.** Ein Recht ohne
Nutzen ist die nächste Lücke, sobald jemand eine Policy hinzufügt und das `TO` wieder
vergisst. Wo keine Codestelle mit dem Anon- oder Nutzerschlüssel liest, gehört das Recht
weg:

```sql
REVOKE ALL ON public.<tabelle> FROM anon, authenticated;
```

**Vorher wird geprüft, wer die Tabelle im Browser liest.** Findet sich eine Stelle, bekommt
sie eine Server-Route, die genau das herausgibt, was die Anzeige braucht, und nicht die
Tabelle. In venfree war das eine Pool-Anzeige, die eine ganze Punktetabelle samt Adressen
las, um eine Summe zu bilden.

## Die Reihenfolge beim Ausrollen

**Ein einschränkendes Schema geht NACH dem Code, ein additives davor.** Wer Rechte entzieht,
bevor der neue Code live ist, bricht die Seite; wer eine Spalte hinzufügt, nachdem der Code
live ist, ebenso. Der Fehler ist dabei oft still: Eine Zählung, die kein Recht mehr hat,
liefert null und keinen Fehler.

*Anlass: venfree am 29.08.2026. Die Kontaktdaten von 33 Personen waren mit dem öffentlichen
Schlüssel abrufbar, dieselbe Rolle hatte `DELETE` und `TRUNCATE`, und eine Punktetabelle war
von außen beschreibbar. Ursache war fünfmal dieselbe fehlende Zeile. Der technische Hergang
steht in `venfree/BUGS.md`, die Fixes in den Migrationen 109 und 110.*
