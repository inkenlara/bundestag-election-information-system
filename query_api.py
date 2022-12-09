try:
    import sys
except ImportError:
    import pip
    pip.main(['install', '--user', 'sys'])
    import sys
try:
    import psycopg2
except ImportError:
    import pip
    pip.main(['install', '--user', 'psycopg2'])
    import psycopg2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/query9_high")
async def query9_high_call():
    query9_high()
    return FileResponse("public/img/query9_high.png")

@app.get("/query9_low")
async def query9_low_call():
    query9_low()
    return FileResponse("public/img/query9_low.png")

@app.get("/query8_rich")
async def query8_rich_call():
    query8_rich()
    return FileResponse("public/img/query8_rich.png")

@app.get("/query8_poor")
async def query8_poor_call():
    query8_poor()
    return FileResponse("public/img/query8_poor.png")


@app.get("/query4_table")
async def query4_call():
    value = query4_table()
    return HTMLResponse(content=value, status_code=200)

@app.get("/query3_wahlbeteiligung/{kreis_id}")
async def query3_wahlbeteiligung_call(kreis_id: int):
    value = query3_wahlbeteiligung(kreis_id)
    return HTMLResponse(content=value, status_code=200)

@app.get("/query3_direktkandidaten/{kreis_id}")
async def query3_direktkandidaten_call(kreis_id: int):
    value = query3_direktkandidaten(kreis_id)
    return HTMLResponse(content=value, status_code=200)


@app.get("/query3_stimmen_entwicklung/{kreis_id}")
async def query3_stimmen_entwicklung_call(kreis_id: int):
    value = query3_stimmen_entwicklung(kreis_id)
    return HTMLResponse(content=value, status_code=200)


@app.get("/query1_chart")
async def query1_chart_call():
    query1_chart()
    return FileResponse("public/img/query1_chart.png")

@app.get("/query1_table")
async def query1_table_call():
    value = query1_table()
    return HTMLResponse(content=value, status_code=200)

@app.get("/query2_table")
async def query2_table_call():
    value = query2_table()
    return HTMLResponse(content=value, status_code=200)



db_host = "localhost"
db_port = 5432
db_name = "wahl"
db_user = "postgres"
db_password = ""

# Inkens local test db:
"""db_host = "localhost"
db_port = 5432
db_name = "postgres"
db_user = "newuser"
db_password = "pw"
"""


try:
    sql_con = psycopg2.connect(
        host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
    cur = sql_con.cursor()
    print("Success")
except:
    print("Fail")

plt.switch_backend('Agg') 


def query1_chart():
    cur.execute("""SELECT p.KurzBezeichnung, s.sitze FROM sitzverteilungbundestag s, partei p
WHERE s.partei = p.parteiid""")

    party = []
    performance = []
    mobile_records = cur.fetchall()
    for i in mobile_records:
        party.append(i[0])
        performance.append(int(i[1]))
    y_pos = np.arange(len(party))
    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, party)
    plt.ylabel('Sitze')
    plt.title('Sitzverteilung')
    plt.savefig('public/img/query1_chart.png')
    plt.close()



# TODO TEST
def query1_table():

    cur.execute("""SELECT p.KurzBezeichnung, s.sitze FROM sitzverteilungbundestag s, partei p
    WHERE s.partei = p.parteiid""")

    data =  cur.fetchall()
    str_table = '<table>'
    str_table = str_table + '<tr>'
    str_table = str_table + '<th>Partei</th>'
    str_table = str_table + '<th>Sitze</th>'
    str_table = str_table + '</tr>'
    for i in data:
        str_table = str_table + '<tr>'
        str_table = str_table + '<td>' + str(i[0]) + '</td><td>' + str(i[1]) + '</td>'
        str_table = str_table + '</tr>'
    str_table = str_table + ' </table>'
    return str_table



# TODO TEST
def query2_table():

    cur.execute("""with wahlkreis_max as (
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
and p.parteiid = k.partei""")

    data =  cur.fetchall()
    str_table = '<table>'
    str_table = str_table + '<tr>'
    str_table = str_table + '<th>Vorname</th>'
    str_table = str_table + '<th>Nachname</th>'
    str_table = str_table + '<th>Beruf</th>'
    str_table = str_table + '<th>Partei</th>'
    str_table = str_table + '</tr>'
    for i in data:
        str_table = str_table + '<tr>'
        str_table = str_table + '<td>' + str(i[1]) + '</td><td>' + str(i[2]) + '</td><td>' + str(i[3]) + '</td><td>' + str(i[4]) + '</td>'
        str_table = str_table + '</tr>'
    str_table = str_table + ' </table>'
    return str_table


def query4_table():

    cur.execute("""with erststimmensieger as (
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
  select w.wahlkreisname,e.wahljahr,e.erststimmensieger,z.zweitstimmensieger
  from erststimmensieger e, zweitstimmensieger z, wahlkreis w
  where e.wahlkreis = z.wahlkreis AND e.wahlkreis = w.wahlkreisid""")

    data =  cur.fetchall()
    str_table = '<table>'
    str_table = str_table + '<tr>'
    str_table = str_table + '<th>Wahlkreisname</th>'
    str_table = str_table + '<th>Wahljahr</th>'
    str_table = str_table + '<th>Erststimmensieger</th>'
    str_table = str_table + '<th>Zweitstimmensieger</th>'
    str_table = str_table + '</tr>'
    for i in data:
        str_table = str_table + '<tr>'
        str_table = str_table + '<td>' + str(i[0]) + '</td><td>' + str(i[1]) + '</td><td>' + str(i[2]) + '</td><td>' + str(i[3]) +'</td>'
        str_table = str_table + '</tr>'
    str_table = str_table + ' </table>'
    return str_table



def query3_wahlbeteiligung(kreis):
    cur.execute("""select a.wahlkreis, w.wahlkreisname, (1.00*anzahlwahlende)/anzahlwahlberechtigte as wahlbeteiligung, wahljahr
        from wahlkreisaggretation as a, wahlkreis as w
        WHERE wahljahr = 2021 AND a.wahlkreis = w.wahlkreisid""")
    data =  cur.fetchall()
    result = 0.0
    for i in data:
        if(int(i[0]) == int(kreis)):
            result = i[2] * 100
    stringy = '<p> ' + str(float("{:.3f}".format(result))) + " %" + ' </p>' 
    jsony = {"data": stringy}
    return json.dumps(jsony)


def query3_direktkandidaten(kreis):
    cur.execute("""with erststimmensieger as (
  select we.wahlkreis, we.wahljahr, we.parteikurz as erststimmensieger, we.wahljahr
  from wahlkreisprozenterst we
  where we.wahljahr = 2021
  and not exists                        
          (select *                    
          from wahlkreisprozenterst we2            
          where we.wahlkreis = we2.wahlkreis  
          and we2.wahljahr = 2021
          and we2.prozenterststimmen > we.prozenterststimmen    
          )
)
select e.wahlkreis,wk.wahlkreisname, k.firstname, k.lastname, e.erststimmensieger, k.wahljahr
from erststimmensieger e, direktkandidaten dk, kandidaten k, partei p, wahlkreis wk
where e.erststimmensieger = p.KurzBezeichnung
and p.parteiid = k.partei
and wk.wahlkreisid = e.wahlkreis
and k.kandidatid = dk.kandidatid
and dk.wahlkreis = e.wahlkreis
and k.wahljahr = 2021""")
    data = cur.fetchall()
    stringy = ''
    for i in data:
        if(int(i[0]) == int(kreis)):
            stringy = '<p> ' + str(i[2]) + '   ' + str(i[3]) + '   ' + str(i[4]) + '   ' + str(i[5]) + ' </p>'
    jsony = {"data": stringy}
    return json.dumps(jsony)


def query3_stimmen_entwicklung(kreis):
    cur.execute("""with vorjahr as (
    select w.wahlkreis, pz.parteikurz, w.anzahlstimmen, pz.prozentzweitstimmen
    from wahlkreisprozentzweit pz, wahlkreiszweitstimmenaggregation w, partei p
    where pz.wahljahr = 2017
    and w.wahljahr = 2017
    and pz.wahlkreis = w.wahlkreis
    and w.partei = p.parteiid
    and p.KurzBezeichnung = pz.parteikurz
)
select w.wahlkreis, pz.parteikurz, w.anzahlstimmen, pz.prozentzweitstimmen, w.anzahlstimmen-v.anzahlstimmen as stimmendifferenz, pz.prozentzweitstimmen-v.prozentzweitstimmen as prozentdifferenz
from wahlkreisprozentzweit pz, wahlkreiszweitstimmenaggregation w, partei p, vorjahr v
where pz.wahljahr = 2021
and w.wahljahr = 2021
and pz.wahlkreis = w.wahlkreis
and w.partei = p.parteiid
and p.KurzBezeichnung = pz.parteikurz
and w.wahlkreis = v.wahlkreis
and p.KurzBezeichnung = v.parteikurz""")
    data =  cur.fetchall()
    str_table = '<table>'
    str_table = str_table + '<tr>'
    str_table = str_table + '<th>Partei</th>'
    str_table = str_table + '<th>Anzahlstimmen</th>'
    str_table = str_table + '<th>Prozentzweitstimmen</th>'
    str_table = str_table + '<th>Stimmendifferenz</th>'
    str_table = str_table + '<th>Prozentdifferenz</th>'
    str_table = str_table + '</tr>'
    for i in data:
        if(int(i[0]) == int(kreis)):
            str_table = str_table + '<tr>'
            str_table = str_table + '<td>' + str(i[1]) + '</td><td>' + str(i[2]) + '</td><td>' + str(float("{:.2f}".format(i[3]))) + '%' + '</td><td>' + str(i[4]) +'</td><td>' + str(float("{:.2f}".format(i[5]))) + '%' +'</td>'
            str_table = str_table + '</tr>'
    str_table = str_table + ' </table>'
    jsony = {"data": str_table}
    return json.dumps(jsony)



def query8_rich():
    cur.execute("""with ten_richest as (SELECT wahlkreis, wahlkreisname, einkommenprivatehaushalte as ein FROM strukturdaten
    ORDER BY ein DESC
    LIMIT 10),
    ten_poorest as (SELECT wahlkreis, wahlkreisname, einkommenprivatehaushalte as ein FROM strukturdaten
    ORDER BY ein ASC
    LIMIT 10),

    -- CDU/CSU Union average richest
    cdu_csu_average_rich as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
    WHERE WahlKreis IN
    (SELECT wahlkreis FROM ten_richest)
    AND (parteikurz = 'CDU' OR parteikurz = 'CSU') AND wahljahr = 2021
                            GROUP BY parteikurz),
    -- SPD average richest
    spd_average_rich as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
    WHERE WahlKreis IN
    (SELECT wahlkreis FROM ten_richest)
    AND (parteikurz = 'SPD') AND wahljahr = 2021
                        GROUP BY parteikurz),
    -- fdp average richest
    fdp_average_rich as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
    WHERE WahlKreis IN
    (SELECT wahlkreis FROM ten_richest)
    AND (parteikurz = 'FDP') AND wahljahr = 2021
                        GROUP BY parteikurz),
    -- grüne average richest
    grune_average_rich as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
    WHERE WahlKreis IN
    (SELECT wahlkreis FROM ten_richest)
    AND (parteikurz = 'GRÜNE') AND wahljahr = 2021
                        GROUP BY parteikurz),
    -- AfD average richest
    afd_average_rich as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
    WHERE WahlKreis IN
    (SELECT wahlkreis FROM ten_richest)
    AND (parteikurz = 'AfD') AND wahljahr = 2021
                        GROUP BY parteikurz),

    -- CDU/CSU Union average poorest
    cdu_csu_average_poor as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
    WHERE WahlKreis IN
    (SELECT wahlkreis FROM ten_poorest)
    AND (parteikurz = 'CDU' OR parteikurz = 'CSU') AND wahljahr = 2021
                            GROUP BY parteikurz),
    -- SPD average poorest
    spd_average_poor as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
    WHERE WahlKreis IN
    (SELECT wahlkreis FROM ten_poorest)
    AND (parteikurz = 'SPD') AND wahljahr = 2021
                        GROUP BY parteikurz),
    -- fdp average poorest
    fdp_average_poor as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
    WHERE WahlKreis IN
    (SELECT wahlkreis FROM ten_poorest)
    AND (parteikurz = 'FDP') AND wahljahr = 2021
                        GROUP BY parteikurz),
    -- grüne average poorest
    grune_average_poor as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
    WHERE WahlKreis IN
    (SELECT wahlkreis FROM ten_poorest)
    AND (parteikurz = 'GRÜNE') AND wahljahr = 2021
                        GROUP BY parteikurz),
    -- AfD average poorest
    afd_average_poor as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
    WHERE WahlKreis IN
    (SELECT wahlkreis FROM ten_poorest)
    AND (parteikurz = 'AfD') AND wahljahr = 2021
                        GROUP BY parteikurz),
                        
    rich_total as (					  
    SELECT parteikurz, avg, 'rich' as category FROM cdu_csu_average_rich UNION 
    SELECT parteikurz, avg, 'rich' as category FROM spd_average_rich UNION
    SELECT parteikurz, avg, 'rich' as category FROM fdp_average_rich UNION
    SELECT parteikurz, avg, 'rich' as category FROM grune_average_rich UNION
    SELECT parteikurz, avg, 'rich' as category FROM afd_average_rich),

    poor_total as (
    SELECT parteikurz, avg, 'poor' as category FROM cdu_csu_average_poor UNION 
    SELECT parteikurz, avg, 'poor' as category FROM spd_average_poor UNION
    SELECT parteikurz, avg, 'poor' as category FROM fdp_average_poor UNION
    SELECT parteikurz, avg, 'poor' as category FROM grune_average_poor UNION
    SELECT parteikurz, avg, 'poor' as category FROM afd_average_poor)

    SELECT * FROM rich_total""")

    mobile_records = cur.fetchall()
    results = []
    total = 0
    for i in mobile_records:
        if(i[0] == "CSU"): continue
        results.append(i[1])
        total += i[1]
    results.append(100 - total)
    
    
    labels = 'Grüne', 'FDP', 'SPD', 'CDU', 'AfD', 'Others'
    explode = (0.1, 0.1, 0.1, 0.1, 0.1, 0.1) 

    fig1, ax1 = plt.subplots()
    ax1.pie(results, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.savefig('public/img/query8_rich.png')
    plt.close()



def query8_poor():

    cur.execute("""with ten_richest as (SELECT wahlkreis, wahlkreisname, einkommenprivatehaushalte as ein FROM strukturdaten
    ORDER BY ein DESC
    LIMIT 10),
    ten_poorest as (SELECT wahlkreis, wahlkreisname, einkommenprivatehaushalte as ein FROM strukturdaten
    ORDER BY ein ASC
    LIMIT 10),

    -- CDU/CSU Union average richest
    cdu_csu_average_rich as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
    WHERE WahlKreis IN
    (SELECT wahlkreis FROM ten_richest)
    AND (parteikurz = 'CDU' OR parteikurz = 'CSU') AND wahljahr = 2021
                            GROUP BY parteikurz),
    -- SPD average richest
    spd_average_rich as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
    WHERE WahlKreis IN
    (SELECT wahlkreis FROM ten_richest)
    AND (parteikurz = 'SPD') AND wahljahr = 2021
                        GROUP BY parteikurz),
    -- fdp average richest
    fdp_average_rich as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
    WHERE WahlKreis IN
    (SELECT wahlkreis FROM ten_richest)
    AND (parteikurz = 'FDP') AND wahljahr = 2021
                        GROUP BY parteikurz),
    -- grüne average richest
    grune_average_rich as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
    WHERE WahlKreis IN
    (SELECT wahlkreis FROM ten_richest)
    AND (parteikurz = 'GRÜNE') AND wahljahr = 2021
                        GROUP BY parteikurz),
    -- AfD average richest
    afd_average_rich as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
    WHERE WahlKreis IN
    (SELECT wahlkreis FROM ten_richest)
    AND (parteikurz = 'AfD') AND wahljahr = 2021
                        GROUP BY parteikurz),

    -- CDU/CSU Union average poorest
    cdu_csu_average_poor as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
    WHERE WahlKreis IN
    (SELECT wahlkreis FROM ten_poorest)
    AND (parteikurz = 'CDU' OR parteikurz = 'CSU') AND wahljahr = 2021
                            GROUP BY parteikurz),
    -- SPD average poorest
    spd_average_poor as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
    WHERE WahlKreis IN
    (SELECT wahlkreis FROM ten_poorest)
    AND (parteikurz = 'SPD') AND wahljahr = 2021
                        GROUP BY parteikurz),
    -- fdp average poorest
    fdp_average_poor as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
    WHERE WahlKreis IN
    (SELECT wahlkreis FROM ten_poorest)
    AND (parteikurz = 'FDP') AND wahljahr = 2021
                        GROUP BY parteikurz),
    -- grüne average poorest
    grune_average_poor as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
    WHERE WahlKreis IN
    (SELECT wahlkreis FROM ten_poorest)
    AND (parteikurz = 'GRÜNE') AND wahljahr = 2021
                        GROUP BY parteikurz),
    -- AfD average poorest
    afd_average_poor as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
    WHERE WahlKreis IN
    (SELECT wahlkreis FROM ten_poorest)
    AND (parteikurz = 'AfD') AND wahljahr = 2021
                        GROUP BY parteikurz),
                        
    rich_total as (					  
    SELECT parteikurz, avg, 'rich' as category FROM cdu_csu_average_rich UNION 
    SELECT parteikurz, avg, 'rich' as category FROM spd_average_rich UNION
    SELECT parteikurz, avg, 'rich' as category FROM fdp_average_rich UNION
    SELECT parteikurz, avg, 'rich' as category FROM grune_average_rich UNION
    SELECT parteikurz, avg, 'rich' as category FROM afd_average_rich),

    poor_total as (
    SELECT parteikurz, avg, 'poor' as category FROM cdu_csu_average_poor UNION 
    SELECT parteikurz, avg, 'poor' as category FROM spd_average_poor UNION
    SELECT parteikurz, avg, 'poor' as category FROM fdp_average_poor UNION
    SELECT parteikurz, avg, 'poor' as category FROM grune_average_poor UNION
    SELECT parteikurz, avg, 'poor' as category FROM afd_average_poor)

    SELECT * FROM poor_total""")

    mobile_records = cur.fetchall()
    results = []
    total = 0
    for i in mobile_records:
        results.append(i[1])
        total += i[1]
    results.append(100 - total)
    
    
    labels = 'AfD', 'CDU', 'FDP', 'SPD', 'Grüne', 'Others'
    explode = (0.1, 0.1, 0.1, 0.1, 0.1, 0.1) 

    fig1, ax1 = plt.subplots()
    ax1.pie(results, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.savefig('public/img/query8_poor.png')
    plt.close()







def query9_high():
    cur.execute("""with ten_most_educated as (SELECT wahlkreis, wahlkreisname, bildung as ein FROM strukturdaten
ORDER BY ein DESC
LIMIT 10),
ten_least_educated as (SELECT wahlkreis, wahlkreisname, bildung as ein FROM strukturdaten
ORDER BY ein ASC
LIMIT 10),

-- CDU/CSU Union average most_educated
cdu_csu_average_most_educated as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
WHERE WahlKreis IN
(SELECT wahlkreis FROM ten_most_educated)
AND (parteikurz = 'CDU' OR parteikurz = 'CSU') AND wahljahr = 2021
						GROUP BY parteikurz),
-- SPD average most_educated
spd_average_most_educated as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
WHERE WahlKreis IN
(SELECT wahlkreis FROM ten_most_educated)
AND (parteikurz = 'SPD') AND wahljahr = 2021
					GROUP BY parteikurz),
-- fdp average most_educated
fdp_average_most_educated as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
WHERE WahlKreis IN
(SELECT wahlkreis FROM ten_most_educated)
AND (parteikurz = 'FDP') AND wahljahr = 2021
					GROUP BY parteikurz),
-- grüne average most_educated
grune_average_most_educated as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
WHERE WahlKreis IN
(SELECT wahlkreis FROM ten_most_educated)
AND (parteikurz = 'GRÜNE') AND wahljahr = 2021
					  GROUP BY parteikurz),
-- AfD average most_educated
afd_average_most_educated as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
WHERE WahlKreis IN
(SELECT wahlkreis FROM ten_most_educated)
AND (parteikurz = 'AfD') AND wahljahr = 2021
					GROUP BY parteikurz),


-- CDU/CSU Union average least educated
cdu_csu_average_least_educated as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
WHERE WahlKreis IN
(SELECT wahlkreis FROM ten_least_educated)
AND (parteikurz = 'CDU' OR parteikurz = 'CSU') AND wahljahr = 2021
						GROUP BY parteikurz),
-- SPD average least educated
spd_average_least_educated as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
WHERE WahlKreis IN
(SELECT wahlkreis FROM ten_least_educated)
AND (parteikurz = 'SPD') AND wahljahr = 2021
					GROUP BY parteikurz),
-- fdp average least educated
fdp_average_least_educated as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
WHERE WahlKreis IN
(SELECT wahlkreis FROM ten_least_educated)
AND (parteikurz = 'FDP') AND wahljahr = 2021
					GROUP BY parteikurz),
-- grüne average least educated
grune_average_least_educated as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
WHERE WahlKreis IN
(SELECT wahlkreis FROM ten_least_educated)
AND (parteikurz = 'GRÜNE') AND wahljahr = 2021
					  GROUP BY parteikurz),
-- AfD average least educated
afd_average_least_educated as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
WHERE WahlKreis IN
(SELECT wahlkreis FROM ten_least_educated)
AND (parteikurz = 'AfD') AND wahljahr = 2021
					  GROUP BY parteikurz),
					  
most_educated_total as (					  
SELECT parteikurz, avg, 'high' as category FROM cdu_csu_average_most_educated UNION 
SELECT parteikurz, avg, 'high' as category FROM spd_average_most_educated UNION
SELECT parteikurz, avg, 'high' as category FROM fdp_average_most_educated UNION
SELECT parteikurz, avg, 'high' as category FROM grune_average_most_educated UNION
SELECT parteikurz, avg, 'high' as category FROM afd_average_most_educated),

least_educated_total as (
SELECT parteikurz, avg, 'low' as category FROM cdu_csu_average_least_educated UNION 
SELECT parteikurz, avg, 'low' as category FROM spd_average_least_educated UNION
SELECT parteikurz, avg, 'low' as category FROM fdp_average_least_educated UNION
SELECT parteikurz, avg, 'low' as category FROM grune_average_least_educated UNION
SELECT parteikurz, avg, 'low' as category FROM afd_average_least_educated)


SELECT * FROM most_educated_total""")

    mobile_records = cur.fetchall()
    results = []
    total = 0
    for i in mobile_records:
        results.append(i[1])
        total += i[1]
    results.append(100 - total)
    
    
    labels = 'Grüne', 'SPD', 'AfD', 'CDU', 'FDP', 'Others'
    explode = (0.1, 0.1, 0.1, 0.1, 0.1, 0.1) 

    fig1, ax1 = plt.subplots()
    ax1.pie(results, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    # ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.savefig('public/img/query9_high.png')
    plt.close()






def query9_low():
    cur.execute("""with ten_most_educated as (SELECT wahlkreis, wahlkreisname, bildung as ein FROM strukturdaten
ORDER BY ein DESC
LIMIT 10),
ten_least_educated as (SELECT wahlkreis, wahlkreisname, bildung as ein FROM strukturdaten
ORDER BY ein ASC
LIMIT 10),

-- CDU/CSU Union average most_educated
cdu_csu_average_most_educated as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
WHERE WahlKreis IN
(SELECT wahlkreis FROM ten_most_educated)
AND (parteikurz = 'CDU' OR parteikurz = 'CSU') AND wahljahr = 2021
						GROUP BY parteikurz),
-- SPD average most_educated
spd_average_most_educated as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
WHERE WahlKreis IN
(SELECT wahlkreis FROM ten_most_educated)
AND (parteikurz = 'SPD') AND wahljahr = 2021
					GROUP BY parteikurz),
-- fdp average most_educated
fdp_average_most_educated as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
WHERE WahlKreis IN
(SELECT wahlkreis FROM ten_most_educated)
AND (parteikurz = 'FDP') AND wahljahr = 2021
					GROUP BY parteikurz),
-- grüne average most_educated
grune_average_most_educated as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
WHERE WahlKreis IN
(SELECT wahlkreis FROM ten_most_educated)
AND (parteikurz = 'GRÜNE') AND wahljahr = 2021
					  GROUP BY parteikurz),
-- AfD average most_educated
afd_average_most_educated as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
WHERE WahlKreis IN
(SELECT wahlkreis FROM ten_most_educated)
AND (parteikurz = 'AfD') AND wahljahr = 2021
					GROUP BY parteikurz),


-- CDU/CSU Union average least educated
cdu_csu_average_least_educated as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
WHERE WahlKreis IN
(SELECT wahlkreis FROM ten_least_educated)
AND (parteikurz = 'CDU' OR parteikurz = 'CSU') AND wahljahr = 2021
						GROUP BY parteikurz),
-- SPD average least educated
spd_average_least_educated as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
WHERE WahlKreis IN
(SELECT wahlkreis FROM ten_least_educated)
AND (parteikurz = 'SPD') AND wahljahr = 2021
					GROUP BY parteikurz),
-- fdp average least educated
fdp_average_least_educated as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
WHERE WahlKreis IN
(SELECT wahlkreis FROM ten_least_educated)
AND (parteikurz = 'FDP') AND wahljahr = 2021
					GROUP BY parteikurz),
-- grüne average least educated
grune_average_least_educated as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
WHERE WahlKreis IN
(SELECT wahlkreis FROM ten_least_educated)
AND (parteikurz = 'GRÜNE') AND wahljahr = 2021
					  GROUP BY parteikurz),
-- AfD average least educated
afd_average_least_educated as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
WHERE WahlKreis IN
(SELECT wahlkreis FROM ten_least_educated)
AND (parteikurz = 'AfD') AND wahljahr = 2021
					  GROUP BY parteikurz),
					  
most_educated_total as (					  
SELECT parteikurz, avg, 'high' as category FROM cdu_csu_average_most_educated UNION 
SELECT parteikurz, avg, 'high' as category FROM spd_average_most_educated UNION
SELECT parteikurz, avg, 'high' as category FROM fdp_average_most_educated UNION
SELECT parteikurz, avg, 'high' as category FROM grune_average_most_educated UNION
SELECT parteikurz, avg, 'high' as category FROM afd_average_most_educated),

least_educated_total as (
SELECT parteikurz, avg, 'low' as category FROM cdu_csu_average_least_educated UNION 
SELECT parteikurz, avg, 'low' as category FROM spd_average_least_educated UNION
SELECT parteikurz, avg, 'low' as category FROM fdp_average_least_educated UNION
SELECT parteikurz, avg, 'low' as category FROM grune_average_least_educated UNION
SELECT parteikurz, avg, 'low' as category FROM afd_average_least_educated)


SELECT * FROM least_educated_total""")
    mobile_records = cur.fetchall()
    results = []
    total = 0
    for i in mobile_records:
        if(i[0] == "CSU"): continue
        results.append(i[1])
        total += i[1]
    results.append(100 - total)
    
    
    labels = 'FDP', 'Grüne', 'AfD', 'CDU', 'SPD', 'Others'
    explode = (0.1, 0.1, 0.1, 0.1, 0.1, 0.1) 

    fig1, ax1 = plt.subplots()
    ax1.pie(results, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    # ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.savefig('public/img/query9_low.png')
    plt.close()

