-- in python add something like .format(numbervotes,numbervotes,wahlkreis) after the strings containing the sql queries 

-- BUNDESLANDAGGREGATION
update bundeslandaggregation
set anzahlwahlberechtigte = anzahlwahlberechtigte + {}, anzahlwaehlende = anzahlwaehlende + {}
where wahljahr = 2021
and bundesland = (select bundesland from wahlkreis where wahlkreisid = {})
-- if (erststimme ungültig)
update bundeslandaggregation
set ungueltigeerst = ungueltigeerst +{}
where wahljahr = 2021
and bundesland = (select bundesland from wahlkreis where wahlkreisid = {})
-- if(zweitstimme ungültig)
update bundeslandaggregation
set ungueltigezweit = ungueltigezweit +{}
where wahljahr = 2021
and bundesland = (select bundesland from wahlkreis where wahlkreisid = {})


-- BUNDESLANDSTIMMENAGGREGATION
update bundeslandstimmenaggregation
set anzahlerststimmen = anzahlerststimmen + {}, anzahlzweitstimmen = anzahlzweitstimmen + {}
where wahljahr = 2021
and bundesland = (select bundesland from wahlkreis where wahlkreisid = {})


-- DEUTSCHLANDAGGREGATION
update DeutschlandAggregation
set anzahlwahlberechtigte = anzahlwahlberechtigte + {}, anzahlwaehlende = anzahlwaehlende + {}
where wahljahr = 2021
and bundesland = (select bundesland from wahlkreis where wahlkreisid = {})
-- if (erststimme ungültig)
update DeutschlandAggregation
set ungueltigeerst = ungueltigeerst +{}
where wahljahr = 2021
and bundesland = (select bundesland from wahlkreis where wahlkreisid = {})
-- if(zweitstimme ungültig)
update DeutschlandAggregation
set ungueltigezweit = ungueltigezweit +{}
where wahljahr = 2021
and bundesland = (select bundesland from wahlkreis where wahlkreisid = {})


-- DEUTSCHLANDSTIMMENAGGREGATION
update deutschlandstimmenaggregation
set anzahlerststimmen = anzahlerststimmen + {}, anzahlzweitstimmen = anzahlzweitstimmen + {}
where wahljahr = 2021
and bundesland = (select bundesland from wahlkreis where wahlkreisid = {})

--TODO: update prozenterststimmen, prozent zweitstimmen

-- WAHLKREISAGGREGATION
update wahlkreisaggregation
set anzahlwahlberechtigte = anzahlwahlberechtigte + {}, anzahlwaehlende = anzahlwaehlende + {}
where wahljahr = 2021
and wahlkreisid = {}
-- if (erststimme ungültig)
update wahlkreisaggregation
set ungueltigeerst = ungueltigeerst +{}
where wahljahr = 2021
and wahlkreisid = {}
-- if(zweitstimme ungültig)
update wahlkreisaggregation
set ungueltigezweit = ungueltigezweit +{}
where wahljahr = 2021
and wahlkreisid = {}


-- BUNDESLANDPROZENTERST + BUNDESLANDPROZENTZWEIT
with neue_prozente as (
    select p.KurzBezeichnung, bsa.anzahlerststimmen*100.0000/(ba.anzahlwaehlende-ba.ungueltigeerst) as prozenterst, bsa.anzahlzweitstimmen*100.0000/(ba.anzahlwaehlende-ba.ungueltigezweit)as prozentzweit
    from bundeslandaggregation ba, bundeslandstimmenaggregation bsa, partei p
    where ba.wahljahr = 2021
    and ba.wahljahr = bsa.wahljahr
    and ba.bundesland =  (select bundesland from wahlkreis where wahlkreisid = {})
    and ba.bundesland = bsa.bundesland
    and bsa.partei = p.parteiid
)


update bundeslandprozenterst
set prozenterststimmen = (select from neue_prozente)
where part
