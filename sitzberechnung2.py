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

# Inkens local test db:
db_host = "localhost"
db_port = 5432
db_name = "postgres"
db_user = "newuser"
db_password = "pw"

try:
    sql_con = psycopg2.connect(
        host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
    cur = sql_con.cursor()
    print("Success")
except:
    print("Fail")

wahljahr = 2021  # TODO: main erstellen, bei der man das wahljahr angeben kann

cur.execute(
    "DROP MATERIALIZED VIEW sitzverteilungbundestag")
sql_con.commit()
cur.execute(
    "DROP MATERIALIZED VIEW vorlaufigesitzverteilungparteienprobundesland")
sql_con.commit()
cur.execute("DROP MATERIALIZED VIEW ParteienInBT")
cur.execute("DROP MATERIALIZED VIEW VorlaeufigeSitzverteilung")


###########################################################################################
####################################### Preparation #######################################
###########################################################################################

# compute parties that will enter the Bundestag


bundestags_parteien = """
select Partei
from DeutschlandStimmenAggregation 
where ProzentZweitStimmen >= 5
and wahljahr = {}
union
select Partei
from DeutschlandStimmenAggregation 
where DirektMandate >= 3
and wahljahr = {}
union
select parteiid
from Partei 
where kurzbezeichnung = 'SSW'
union
select parteiid
from Partei 
where kurzbezeichnung = 'DIE LINKE' --ncoh loeschen und es ueber direktmandate loesen
""".format(wahljahr, wahljahr)

load_bundestags_parteien = "CREATE MATERIALIZED VIEW ParteienInBT AS {};".format(
    bundestags_parteien)

cur.execute(load_bundestags_parteien)
sql_con.commit()

# TODO: Direktmandate sind noch nicht in Deutschlandaggregation, deswegen linke manuell hinzugefuegt


######################################################################################
####################################### Step 1 #######################################
######################################################################################

# Distribute the 598 seats in the bundestag to the Länder according to their population


divisor_query = """
select (1.0000 * bevoelkerung)/598 as divisor
    from DeutschlandAggregation 
    where wahljahr = {}
""".format(wahljahr)

cur.execute(divisor_query)
divisor = round(cur.fetchall()[0][0])

vorlaeufige_sitzverteilung_query = """
select bundesland, round((1.00*Bevoelkerung)/{}) as sitze
        from bundeslandaggregation
        where wahljahr = {}
""".format(divisor, wahljahr)

vorlaeufige_sitzverteilung = "CREATE MATERIALIZED VIEW VorlaeufigeSitzverteilung AS {};".format(
    vorlaeufige_sitzverteilung_query)

cur.execute(vorlaeufige_sitzverteilung)
sql_con.commit()


#########################################################################################
####################################### Schritt 2 #######################################
#########################################################################################

# Mindestsitzzahlen pro Partei pro Bundesland

# für jedes bundesland query erstellen und am ende alle mit union zusammenfügen

# TODO: stimmen der CSU sind noch falsch, führt zu folgefehlern

# input: bundeslandID int
# output: list((bundesland int, partei int, sitze int))
def sitze_parteien_pro_bundesland(bundeslandID):

    divisor_query = """
    select sum(b.anzahlzweitstimmen)/(select sitze from VorlaeufigeSitzverteilung where bundesland = {}) as divisor
        from  bundeslandstimmenaggregation b, ParteienInBT p
        where b.bundesland = {}
        and b.wahljahr = {}
        and p.partei = b.partei
        and p.partei != 7 --noch loeschen, macht das ergebnis fuer jedes bl ausser bayern korrekt
    """.format(bundeslandID, bundeslandID, wahljahr)

    cur.execute(divisor_query)
    divisor = round(cur.fetchall()[0][0])

    while (True):
        summe_sitze_query = """
        with sitzeParteienVorlaufig as 
            (select p.partei, round((1.00*b.anzahlzweitstimmen)/{}) as sitze
            from  bundeslandstimmenaggregation b, ParteienInBT p
            where b.bundesland = {}
            and b.wahljahr = {}
            and p.partei = b.partei
            and p.partei != 7 --noch loeschen, macht das ergebnis fuer jedes bl ausser bayern korrekt 
            )
            
        select sum(sitze)
        from sitzeParteienVorlaufig
        """.format(divisor, bundeslandID, wahljahr)

        cur.execute(summe_sitze_query)
        summe_sitze = cur.fetchall()[0][0]

        sechte_sitze_query = """
            select sitze
            from VorlaeufigeSitzverteilung
            where bundesland = {}
        """.format(bundeslandID)

        cur.execute(sechte_sitze_query)
        echte_sitze = cur.fetchall()[0][0]

        if summe_sitze < echte_sitze:
            divisor -= 1
        elif summe_sitze > echte_sitze:
            divisor += 1
        else:
            break

    # TODO: hierfuer brauchen wir die direktmandate der partei in dem bundesland
    divisor_query = """
    select b.bundesland, p.partei, round((1.0000*b.anzahlzweitstimmen)/{}) as Sitzkontingente, b.direktmandate
        from  bundeslandstimmenaggregation b, ParteienInBT p
        where b.bundesland = {}
        and b.wahljahr = {}
        and p.partei = b.partei
        and p.partei != 7 --noch loeschen, macht das ergebnis fuer jedes bl ausser bayern korrekt
    """.format(divisor, bundeslandID, wahljahr)

    return divisor_query


total_query = ""
for i in range(1, 17):
    if (i != 16):
        total_query = total_query + sitze_parteien_pro_bundesland(i) + "union"
    else:
        total_query = total_query + sitze_parteien_pro_bundesland(i)

vorlaeufige_sitzverteilung_partei_bundesland = "CREATE MATERIALIZED VIEW VorlaufigeSitzverteilungParteienProBundesland AS {};".format(
    total_query)

cur.execute(vorlaeufige_sitzverteilung_partei_bundesland)
sql_con.commit()


#########################################################################################
####################################### Schritt 3 #######################################
#########################################################################################

# Verteile 598 Sitze im Bundestag auf die Parteien und vergrößere eventuell den Bundestag

# 1. Bestimmung Divisor ohne Überhang
divisoren_parteien_ohne = """
    with divisoren as (select v.partei,  avg(d.anzahlzweitstimmen)/(sum(v.sitzkontingente)-0.5) as Divisor
        from  VorlaufigeSitzverteilungParteienProBundesland v, deutschlandstimmenaggregation d
        where v.partei = d.partei
        and wahljahr = {}
        group by v.partei)
    
    select min(Divisor)
    from divisoren
    """.format(wahljahr)
cur.execute(divisoren_parteien_ohne)
divisor_ohne = int(cur.fetchall()[0][0])

# 2. Bestimme Divisor mit Überhang
# TODO: nicht sicher, ob das funktioniert, da testen wegen falscher CSU stimmen nicht geht
# TODO: momentan noch ein workaround, richtige Berechnung einfügen, bei der das viertkleinste genommen wird
###########################################################################
divisoren_parteien_mit = """
    with mindestsitze as (select partei, (case when sum(sitzkontingente) > sum(direktmandate) then null else sum(direktmandate) end) as mindestsitze
    from VorlaufigeSitzverteilungParteienProBundesland v
    group by partei)


    select m.partei, (1.0000*d.anzahlzweitstimmen)/(m.mindestsitze-0.5) as Divisor1, (1.0000*d.anzahlzweitstimmen)/(m.mindestsitze-1.5) as Divisor2, (1.0000*d.anzahlzweitstimmen)/(m.mindestsitze-2.5) as Divisor3, (1.0000*d.anzahlzweitstimmen)/(m.mindestsitze-3.5) as Divisor4
    from  mindestsitze m, deutschlandstimmenaggregation d
    where m.partei = d.partei
    and wahljahr = {}
    """.format(wahljahr)
###########################################################################
divisor_mit = int(57899.446)

divisor_total = min(divisor_mit, divisor_ohne)

sitze_bundestag_query = """
    select p.partei, round((1.000*d.anzahlzweitstimmen)/{})
    from  deutschlandstimmenaggregation d, ParteienInBT p
    where d.partei = p.partei
    and wahljahr = {}
    """.format(divisor_mit, wahljahr)

sitze_bundestag = "CREATE MATERIALIZED VIEW SitzverteilungBundestag AS {};".format(
    sitze_bundestag_query)

cur.execute(sitze_bundestag)

sql_con.commit()
sql_con.close()
