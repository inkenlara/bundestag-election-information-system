-- in python add something like .format(numbervotes,numbervotes,wahlkreis) after the strings containing the sql queries 

-- BUNDESLANDAGGREGATION
update bundeslandaggregation
set anzahlwahlberechtigte = anzahlwahlberechtigte + {}, anzahlwaehlende = anzahlwaehlende + {}, bevoelkerung = bevoelkerung + {}
where wahljahr = 2021
and bundesland = (select bundesland from wahlkreis where wahlkreisid = {})
-- if (erststimme ungültig)
update bundeslandaggregation
set ungueltigeerst = ungueltigeerst + {}
where wahljahr = 2021
and bundesland = (select bundesland from wahlkreis where wahlkreisid = {})
-- if(zweitstimme ungültig)
update bundeslandaggregation
set ungueltigezweit = ungueltigezweit + {}
where wahljahr = 2021
and bundesland = (select bundesland from wahlkreis where wahlkreisid = {})


-- BUNDESLANDSTIMMENAGGREGATION
-- erststimmen
update bundeslandstimmenaggregation
set anzahlerststimmen = anzahlerststimmen + {}
where wahljahr = 2021
and bundesland = (select bundesland from wahlkreis where wahlkreisid = {})
and partei = {}

-- zweitstimmen
update bundeslandstimmenaggregation
set anzahlzweitstimmen = anzahlzweitstimmen + {}
where wahljahr = 2021
and bundesland = (select bundesland from wahlkreis where wahlkreisid = {})
and partei = {}



-- DEUTSCHLANDAGGREGATION
update DeutschlandAggregation
set anzahlwahlberechtigte = anzahlwahlberechtigte + {}, anzahlwaehlende = anzahlwaehlende + {}, bevoelkerung = bevoelkerung + {}
where wahljahr = 2021
-- if (erststimme ungültig)
update DeutschlandAggregation
set ungueltigeerst = ungueltigeerst + {}
where wahljahr = 2021
-- if(zweitstimme ungültig)
update DeutschlandAggregation
set ungueltigezweit = ungueltigezweit + {}
where wahljahr = 2021


-- DEUTSCHLANDSTIMMENAGGREGATION
-- erststimmen
update deutschlandstimmenaggregation
set anzahlerststimmen = anzahlerststimmen + {}
where wahljahr = 2021
and partei = {}
-- zweitstimmen
update deutschlandstimmenaggregation
set anzahlzweitstimmen = anzahlzweitstimmen + {}
where wahljahr = 2021
and partei = {}

-- WAHLKREISAGGREGATION
update wahlkreisaggregation
set anzahlwahlberechtigte = anzahlwahlberechtigte + {}, anzahlwaehlende = anzahlwaehlende + {}
where wahljahr = 2021
and wahlkreisid = {}
-- if (erststimme ungültig)
update wahlkreisaggregation
set ungueltigeerst = ungueltigeerst + {}
where wahljahr = 2021
and wahlkreisid = {}
-- if(zweitstimme ungültig)
update wahlkreisaggregation
set ungueltigezweit = ungueltigezweit + {}
where wahljahr = 2021
and wahlkreisid = {}

--WAHLKREISSTIMMENAGGREGATION
update wahlkreisstimmenaggregation
set anzahlstimmen = anzahlstimmen + {}
where wahljahr = 2021
and wahlkreisid = {}
and partei = {}


-- BUNDESLANDPROZENTERST + BUNDESLANDPROZENTZWEIT
with neue_prozente as (
    select ba.bundesland, p.KurzBezeichnung, bsa.anzahlerststimmen*100.0000/(ba.anzahlwaehlende-ba.ungueltigeerst) as prozenterst, bsa.anzahlzweitstimmen*100.0000/(ba.anzahlwaehlende-ba.ungueltigezweit)as prozentzweit
    from bundeslandaggregation ba, bundeslandstimmenaggregation bsa, partei p
    where ba.wahljahr = 2021
    and ba.wahljahr = bsa.wahljahr
    and ba.bundesland =  (select bundesland from wahlkreis where wahlkreisid = {})
    and ba.bundesland = bsa.bundesland
    and bsa.partei = p.parteiid
)
-- update erst
update bundeslandprozenterst
set prozenterststimmen = np.prozenterst
from neue_prozente as np
where np.KurzBezeichnung = bundeslandprozenterst.parteikurz
and bundeslandprozenterst.bundesland = np.bundesland
and bundeslandprozenterst.wahljahr = 2021
-- update zweit
update bundeslandprozentzwei
set prozentzweitstimmen = np.prozentzweit
from neue_prozente as np
where np.KurzBezeichnung = bundeslandprozentzwei.parteikurz
and bundeslandprozentzwei.bundesland = np.bundesland
and bundeslandprozentzwei.wahljahr = 2021


-- DEUTSCHLANDSTIMMENAGGREGATION
with neue_prozente as (
    select dsa.partei, dsa.anzahlerststimmen*100.0000/(da.anzahlwaehlende-ba.ungueltigeerst) as prozenterst, dsa.anzahlzweitstimmen*100.0000/(da.anzahlwaehlende-da.ungueltigezweit)as prozentzweit
    from DeutschlandAggregation da, deutschlandstimmenaggregation dsa
    where ba.wahljahr = 2021
    and da.wahljahr = dsa.wahljahr
)
-- update erst und zweit
update deutschlandstimmenaggregation
set prozenterststimmen = np.prozenterst, prozentzweitstimmen = np.prozentzweit
from neue_prozente as np
where np.partei = deutschlandstimmenaggregation.partei
and deutschlandstimmenaggregation.wahljahr = 2021


-- WAHLKREISPROZENTERST + WAHLKREISPROZENTZWEIT
with neue_prozente as (
    select wa.wahlkreis, p.KurzBezeichnung as partei, wsa.anzahlzweitstimmen*100.0000/(wa.anzahlwaehlende-wa.ungueltigezweit)as prozentzweit, wsa.anzahlerststimmen*100.0000/(wa.anzahlwaehlende-wa.ungueltigeerst)as prozenterst
    from wahlkreisaggretation wa, wahlkreisstimmenaggregation wsa, partei p
    where wa.wahljahr = 2021
    and wa.wahljahr = wsa.wahljahr
    and wa.wahlkreis = {}
    and wsa.partei = p.parteiid
)
-- update erst
update wahlkreisprozenterst
set prozenterststimmen = np.prozenterst
from neue_prozente as np
where np.partei = wahlkreisprozenterst.parteikurz
and np.wahlkreis = wahlkreisprozenterst.wahlkreis
and wahljahr = 2021

-- update zweit
update wahlkreisprozentzweit
set prozentzweitstimmen = np.prozentzweit
from neue_prozente as np
where np.partei = wahlkreisprozentzweit.parteikurz
and np.wahlkreis = wahlkreisprozentzweit.wahlkreis
and wahljahr = 2021