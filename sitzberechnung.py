try:
    import psycopg2
except ImportError:
    import pip
    pip.main(['install', '--user', 'psycopg2'])
    import psycopg2
try:
    import numpy as np
except ImportError:
    import pip
    pip.main(['install', '--user', 'numpy'])
    import numpy as np
try:
    import math
except ImportError:
    import pip
    pip.main(['install', '--user', 'math'])
    import math

from psycopg2 import sql

# TODO: close connection to database


def create_db_connection(host, user, pw, db, port):
    connection = None
    try:
        conn = psycopg2.connect(
            host=host,
            dbname=db,
            user=user,
            password=pw,
            port=port)
        cur = conn.cursor()
        print("Database connection successful")
    except Exception as err:
        print(f"Error: '{err}'")
    return conn


def execute_query(connection, query):
    cur = connection.cursor()
    try:
        cur.execute(query)
        connection.commit()
        print("Query successful")
    except Exception as err:
        print(f"Error: '{err}'")


def read_query(connection, query):
    cur = connection.cursor()
    result = None
    try:
        cur.execute(query)
        result = cur.fetchall()
        return result
    except Exception as err:
        print(f"Error: '{err}'")


wahljahr = 2021
conn = create_db_connection()  # TODO: db argumente eintragen

# Parteien, die in den Bundestag kommen
bundestags_parteien = f"""
select d.Partei
from DeutschlandStimmenAggregation d
where d.ProzentZweitStimmen >= 0.05
and d.wahljahr = {wahljahr}
union
select d.Partei
from DeutschlandStimmenAggregation d
where d.DirektMandate >= 3
and wahljahr = {wahljahr}
"""
bundestags_parteien = read_query(conn, bundestags_parteien)[0]

print(bundestags_parteien)

divisor = read_query(conn, bundestags_parteien)[0][0]

#######################################################################################
####################################### Schritt 1#######################################
#######################################################################################

# Verteile Sitzkontingente (598) nach Bevölkerungsanteil auf die Bundesländer
sitze = 0
divisor = f"""
select (1.0000 * d.Bevoelkerung)/598 as divisor
    from DeutschlandAggregation d
    where d.wahljahr = {wahljahr}
"""
divisor = read_query(conn, divisor)[0][0]
t = True
# finde richtigen Divisor
while (t):
    sitze = f"""
    with Sitze as (
        select b.BundesLandID, round(b.Bevoelkerung/{divisor}) as sitze
        from BundesLand b
        where b.wahljahr = {wahljahr}
        )

    select sum(s.sitze) as Gesamtsitze
    from Sitze s
    """
    sitze = read_query(conn, sitze)[0][0]
    if sitze == 598:
        # TODO: eventuelle Fehlerquelle und eventuell Grund falls richtiges Ergebnis sich leicht unterscheidet
        divisor = round(divisor)
        t = False
    else:
        divisor = f"""
        -- berechne die anzahl an sitzen, die jedes bundesland mit dem jetzigen divisor bekaeme
        with Sitze as (
            select b.BundesLandID, round(b.Bevoelkerung/{divisor}) as sitze
            from BundesLand b
            where b.wahljahr = {wahljahr}
        ),
        -- addiere oder subtrahiere 0.5 je nachdem, ob der divisor verkleinert oder vergrößert werden muss
        Zwischenschritt as (
            select s.BundesLandID, case when {sitze} < 598 then s.sitze + 0.5 
                                        else s.sitze - 0.5 
                                    end as sitze
            from Sitze s
        ),
        -- berechne für jedes bundesland den divisorkandidaten
        Divisorkandidaten as (
            select z.BundesLandID, round(b.Bevoelkerung/z.sitze) as Divisorkandidat
            from BundesLand b, Zwischenschritt z
            where b.wahljahr = {wahljahr}
            and b.BundesLandID = z.BundesLandID
        )
        --wähle den mittelwert zwischen den zwei groeßten (verkleinerung) oder zwei kleinsten (vergroeßerung) kandidaten als neuen divisor
        select case when {sitze} > 598 then 
                    (min(d.Divisorkandidat) + (select min(d1.Divisorkandidat)
                                                from Divisorkandidaten d1 
                                                where d1.Divisorkandidat > (select min(d2.Divisorkandidat)
                                                                            from Divisorkandidaten d2)))/2
                else  
                    (max(d.Divisorkandidat) + (select max(d1.Divisorkandidat)
                                                from Divisorkandidaten d1 
                                                where d1.Divisorkandidat < (select max(d2.Divisorkandidat)
                                                                            from Divisorkandidaten d2)))/2
                end
        from Divisorkandidaten d
        """
        divisor = read_query(conn, divisor)[0][0]

sitze_pro_bundesland = f"""
    select b.BundesLandID, round(b.Bevoelkerung/{divisor}) as sitze
    from BundesLand b
    where b.wahljahr = {wahljahr}
"""
sitze_pro_bundesland = read_query(conn, sitze_pro_bundesland)


#######################################################################################
####################################### Schritt 2#######################################
#######################################################################################
# Mindestsitzzahlen pro Partei pro Bundesland

def mindestsitzzahl(bundesland, sitze_pro_bundesland, wahljahr, bundestags_parteien):
    anzahl_sitze = 0
    for i in sitze_pro_bundesland:
        if i[0] == bundesland:
            anzahl_sitze = i[1]

    zweitstimmen_gesamt = f"""
       select sum(b.AnzahlZweitStimmen) as zweitstimmen_gesamt
        from BundeslandStimmenAggregation b
        where b.Bundesland = {bundesland}
        and b.wahljahr = {wahljahr}
        and b.Partei in {bundestags_parteien}
    """
    zweitstimmen_gesamt = read_query(conn, zweitstimmen_gesamt)[0][0]
    divisor = zweitstimmen_gesamt/anzahl_sitze

    t = True
    # finde richtigen Divisor
    while (t):
        sitze_parteien = f"""
        with sitze_parteien as (
            select b.Partei, round(b.AnzahlZweitStimmen/{divisor}) as sitze
            from BundeslandStimmenAggregation b
            where b.Bundesland = {bundesland}
            and b.wahljahr = {wahljahr}
            and b.Partei in {bundestags_parteien}
            )

        select sum(s.sitze) as Gesamtsitze
        from sitze_parteien s
        """
        sitze_parteien = read_query(conn, sitze_parteien)[0][0]

        if sitze_parteien == anzahl_sitze:
            # TODO: eventuelle Fehlerquelle und eventuell Grund falls richtiges Ergebnis sich leicht unterscheidet
            divisor = round(divisor)
            t = False
        else:
            divisor = f"""
            -- berechne die anzahl an sitzen, die jede partei mit dem jetzigen divisor bekaeme
            with sitze_parteien as (
                select b.Partei, round(b.AnzahlZweitStimmen/{divisor}) as sitze
                from BundeslandStimmenAggregation b
                where b.Bundesland = {bundesland}
                and b.wahljahr = {wahljahr}
                and b.Partei in {bundestags_parteien}
                ),
            -- addiere oder subtrahiere 0.5 je nachdem, ob der divisor verkleinert oder vergrößert werden muss
            Zwischenschritt as (
                select s.Partei, case when {sitze_parteien} < {anzahl_sitze} then s.sitze + 0.5 
                                            else s.sitze - 0.5 
                                        end as sitze
                from sitze_parteien s
            ),
            -- berechne für jede partei den divisorkandidaten
            Divisorkandidaten as (
                select z.Partei, round(b.AnzahlZweitStimmen/z.sitze) as Divisorkandidat
                from BundeslandStimmenAggregation b, Zwischenschritt z
                where b.Bundesland = {bundesland}
                and b.wahljahr = {wahljahr}
                and b.Partei = z.Partei
            )
            -- berechne neuen Divisor
            select case when {sitze_parteien} < {anzahl_sitze} then 
                        (max(d.Divisorkandidat) + (select max(d1.Divisorkandidat)
                                                    from Divisorkandidaten d1 
                                                    where d1.Divisorkandidat < (select max(d1.Divisorkandidat)
                                                                                from Divisorkandidaten d1)))/2
                    else  
                        (min(d.Divisorkandidat) + (select min(d1.Divisorkandidat)
                                                    from Divisorkandidaten d1 
                                                    where d1.Divisorkandidat > (select min(d1.Divisorkandidat)
                                                                                from Divisorkandidaten d1)))/2
                    end
            from Divisorkandidaten d
            """
            divisor = read_query(conn, divisor)[0][0]

    sitze_pro_partei = f"""
    select b.Partei, case when round(b.AnzahlZweitStimmen/{divisor}) <= b.DirektMandate then b.DirektMandate 
                          else round((b.AnzahlZweitStimmen/{divisor}) + b.DirektMandate))/2) as sitze --falsch, einfach maximum nehmen
    from BundeslandStimmenAggregation b
    where b.Bundesland = {bundesland}
    and b.wahljahr = {wahljahr}
    and b.Partei = z.Partei
    """
    sitze_pro_partei = read_query(conn, sitze_pro_partei)

    return sitze_pro_partei


#######################################################################################
####################################### Schritt 3#######################################
#######################################################################################
# ermittle Anzahl Sitze für jede Partei im Bundestag

def Sitze(parteien, mindestsitze_ohne, mindestsitze_mit, ueberhang):

    zweitstimmenanteil = []  # mit sql befüllen
    divisoren_ohne = []
    for i in range(len(parteien)):
        divisoren_ohne.append(zweitstimmenanteil[i]/(mindestsitze_ohne-0.5))

    minimum = min(divisoren_ohne)

    divisoren_mit = []
    for i in range(len(parteien)):
        if (ueberhang[i] == 0):
            pass
        else:
            divisoren_mit.append(
                zweitstimmenanteil[i]/(mindestsitze_mit[i]-0.5))
            divisoren_mit.append(
                zweitstimmenanteil[i]/(mindestsitze_mit[i]-1.5))
            divisoren_mit.append(
                zweitstimmenanteil[i]/(mindestsitze_mit[i]-2.5))
            divisoren_mit.append(
                zweitstimmenanteil[i]/(mindestsitze_mit[i]-3.5))

    for i in range(3):
        divisoren_mit = divisoren_mit.remove(min(divisoren_mit))

    viertkleinstes = min(mindestsitze_mit)

    divisor = math.floor(min(minimum, viertkleinstes))

    sitze_echt = []

    for i in range(len(parteien)):
        sitze_echt.append(round(zweitstimmenanteil/divisor))

    return sitze_echt


#######################################################################################
####################################### Schritt 4#######################################
#######################################################################################
# verteile Sitze an Parteien in Ländern

# berechnet sitzverteilung auf länder für eine partei
def sitzverteilung__auf_laender(partei, sitze_bundestag):
    zweitstimmenanteile = []  # mit sql befüllen

    zweitstimmen_deutschland = None  # mit sql befüllen

    divisor = zweitstimmen_deutschland/sitze_bundestag

    stimmen_bundeslaender = []# mit sql befüllen

    summe = 0
    while (summe != sitze_bundestag):
        sitze_bundeslander = []

        for i in range(len(stimmen_bundeslaender)):
            sitze_bundeslander.append(round(zweitstimmenanteile[i]/divisor))

        summe = sum(sitze_bundeslander)

        if (summe < sitze_bundestag):
            divisor -= 1
        elif (summe < sitze_bundestag):
            divisor += 1
    
    return sitze_bundeslander
