--Q1: Sitzverteilung 2021

SELECT p.KurzBezeichnung, s.sitze FROM sitzverteilungbundestag s, partei p
WHERE s.partei = p.parteiid


--Q2: Mitglieder Bundestag 2021

--Teil fuer Direktmandate
with wahlkreis_max as (
    select wahlkreis, max(prozenterststimmen) as maxi
    from wahlkreisprozenterst
    where wahljahr = 2021
    group by wahlkreis
),
direktmandate_wahlkreis as (
    select w.wahlkreis, w.parteikurz
    from wahlkreis_max b, wahlkreisprozenterst w
    where b.wahlkreis = w.wahlkreis 
    and b.maxi = w.prozenterststimmen
),
direktmandate as(
    select k.kandidatid, k.firstname, k.lastname, k.beruf, dw.parteikurz as partei
    from direktmandate_wahlkreis dw, direktkandidaten dk, kandidaten k, partei p
    where dw.wahlkreis = dk.wahlkreis
    and dk.kandidatid = k.kandidatid
    and p.KurzBezeichnung = dw.parteikurz
    and p.parteiid = k.partei
    and k.wahljahr = 2021
),
-- Teil für Listenmandate
-- anzahl sitze pro partei pro bundesland minus die direktmandate, die schon verbraucht wurden
sitze_fuer_liste as(
    select b.partei, b.bundesland, (s.sitze-b.direktmandate) as listensitze
    from sitzverteilungparteienprobundesland s, bundeslandstimmenaggregation b 
    where b.wahljahr = 2021
    and s.partei = b.partei
    and s.bundesland = b.bundesland
),
-- rausloeschen derer aus listenkandidaten, die schon per direktmandat in den BT kommen
liste_ohne_direktmandate as(
    select *
    from listenkandidaten lk
    where lk.kandidatid not in (select kandidatid from direktmandate)
),
-- kandidaten sortieren, um spaeter nur die top X herauszufiltern
reihennummern as(
  select ld.kandidatid, sl.partei, ld.bundesland, ROW_NUMBER() OVER(PARTITION BY sl.partei, sl.bundesland ORDER BY ld.listenplatz ASC) AS row_number
  from liste_ohne_direktmandate ld, sitze_fuer_liste sl, kandidaten k
  where ld.kandidatid = k.kandidatid
  and sl.bundesland = ld.bundesland
  and sl.partei = k.partei
),
-- kandidaten, die einen sitz bekommen herausfiltern
listenkandidaten as(
    select r.kandidatid, sl.partei, sl.bundesland
    from sitze_fuer_liste sl, reihennummern r
    where sl.partei = r.partei
    and sl.bundesland = r.bundesland
    and r.row_number <= sl.listensitze
)
-- direktkandidaten und listenkandidaten vereinigen
select * from direktmandate
union
select k.kandidatid, k.firstname, k.lastname, k.beruf, p.KurzBezeichnung as partei
from listenkandidaten l, kandidaten k, partei p
where l.kandidatid = k.kandidatid
and k.wahljahr = 2021
and p.parteiid = k.partei


--Q3: Wahlkreisuebersicht

--Q4: Wahlkreissieger 2021

with erststimmensieger as (
  select we.wahlkreis, we.wahljahr, we.parteikurz as erststimmensieger
  from wahlkreisprozenterst we
  where we.wahljahr = 2021
  and not exists                        
          (select *                    
          from wahlkreisprozenterst we2            
          where we.wahlkreis = we2.wahlkreis  
          and we2.wahljahr = 2021
          and we2.prozenterststimmen > we.prozenterststimmen    
          )
  ),
  zweitstimmensieger as(
    select we.wahlkreis, we.wahljahr, we.parteikurz as zweitstimmensieger
    from wahlkreisprozentzweit we
    where we.wahljahr = 2021
    and not exists                        
          (select *                    
          from wahlkreisprozentzweit we2            
          where we.wahlkreis = we2.wahlkreis  
          and we2.wahljahr = 2021
          and we2.prozentzweitstimmen > we.prozentzweitstimmen    
          )
  )
  select e.wahlkreis,e.wahljahr,e.erststimmensieger,z.zweitstimmensieger
  from erststimmensieger e, zweitstimmensieger z
  where e.wahlkreis = z.wahlkreis



--Q5: Ueberhangsmandate

--Q6: Knappste Sieger

--Q7: Wahlkreisuebersicht (Einzelstimmen)