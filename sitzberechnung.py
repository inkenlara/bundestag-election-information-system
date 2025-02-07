import sys


try:
    import psycopg2
except ImportError:
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
"""
db_host = "localhost"
db_port = 5432
db_name = "postgres"
db_user = "newuser"
db_password = "pw"

db_host = "localhost"
db_port = 5432
db_name = "wahl"
db_user = "postgres"
db_password = ""
"""

with open("db_credentials.txt", "r") as f:
    db_host = f.readline().strip()
    db_port = f.readline().strip()
    db_name = f.readline().strip()
    db_user = f.readline().strip()
    db_password = f.readline().strip()


try:
    sql_con = psycopg2.connect(
        host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
    cur = sql_con.cursor()
    print("Success")
except:
    print("Fail")

wahljahre = [2017, 2021]

for wahljahr in wahljahre:
    if wahljahr == 2017:
        cur.execute(
            "DROP MATERIALIZED VIEW IF EXISTS sitzverteilungparteienprobundesland2017")
        sql_con.commit()
        cur.execute("DROP TABLE IF EXISTS sitzverteilungbundestag2017")
        sql_con.commit()
        cur.execute(
            "DROP MATERIALIZED VIEW IF EXISTS vorlaufigesitzverteilungparteienprobundesland2017")
        sql_con.commit()
        cur.execute("DROP MATERIALIZED VIEW IF EXISTS ParteienInBT2017")
        cur.execute(
            "DROP MATERIALIZED VIEW IF EXISTS VorlaeufigeSitzverteilung")
        sql_con.commit()
    else:
        cur.execute(
            "DROP MATERIALIZED VIEW IF EXISTS sitzverteilungparteienprobundesland")
        sql_con.commit()
        cur.execute("DROP TABLE IF EXISTS sitzverteilungbundestag")
        sql_con.commit()
        cur.execute(
            "DROP MATERIALIZED VIEW IF EXISTS vorlaufigesitzverteilungparteienprobundesland")
        sql_con.commit()
        cur.execute("DROP MATERIALIZED VIEW IF EXISTS ParteienInBT")
        cur.execute(
            "DROP MATERIALIZED VIEW IF EXISTS VorlaeufigeSitzverteilung")
        sql_con.commit()

    ###########################################################################################
    ####################################### Preparation #######################################
    ###########################################################################################

    # compute parties that will enter the Bundestag

    if wahljahr == 2021:
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
        """.format(wahljahr, wahljahr)
        load_bundestags_parteien = "CREATE MATERIALIZED VIEW ParteienInBT AS {};".format(
            bundestags_parteien)
    else:
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
        """.format(wahljahr, wahljahr)
        load_bundestags_parteien = "CREATE MATERIALIZED VIEW ParteienInBT2017 AS {};".format(
            bundestags_parteien)

    cur.execute(load_bundestags_parteien)
    sql_con.commit()

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

    while (True):
        vorlaeufige_sitzverteilung_summe_query = """
        with vorlaeufigSitzverteilung as (
            select bundesland, round((1.00*Bevoelkerung)/{}) as sitze
                from bundeslandaggregation
                where wahljahr = {}
        )
        select sum(sitze) from vorlaeufigSitzverteilung
        """.format(divisor, wahljahr)

        cur.execute(vorlaeufige_sitzverteilung_summe_query)
        summe_sitze = cur.fetchall()[0][0]

        echte_sitze = 598

        if summe_sitze < echte_sitze:
            divisor -= 1
        elif summe_sitze > echte_sitze:
            divisor += 1
        else:
            break

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

    # input: bundeslandID int
    # output: list((bundesland int, partei int, sitze int))

    def sitze_parteien_pro_bundesland(bundeslandID):
        if wahljahr == 2017:
            p = "parteieninbt2017"
        else:
            p = "parteieninbt"

        divisor_query = """
        select sum(b.anzahlzweitstimmen)/(select sitze from VorlaeufigeSitzverteilung where bundesland = {}) as divisor
            from  bundeslandstimmenaggregation b, {} p
            where b.bundesland = {}
            and b.wahljahr = {}
            and p.partei = b.partei
        """.format(bundeslandID, p, bundeslandID, wahljahr)

        cur.execute(divisor_query)
        divisor = round(cur.fetchall()[0][0])

        while (True):
            summe_sitze_query = """
            with sitzeParteienVorlaufig as 
                (select p.partei, round((1.00*b.anzahlzweitstimmen)/{}) as sitze
                from  bundeslandstimmenaggregation b, {} p
                where b.bundesland = {}
                and b.wahljahr = {}
                and p.partei = b.partei
                )
                
            select sum(sitze)
            from sitzeParteienVorlaufig
            """.format(divisor, p, bundeslandID, wahljahr)

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

        divisor_query = """
        select b.bundesland, p.partei, round((1.0000*b.anzahlzweitstimmen)/{}) as Sitzkontingente, b.direktmandate
            from  bundeslandstimmenaggregation b, {} p
            where b.bundesland = {}
            and b.wahljahr = {}
            and p.partei = b.partei
        """.format(divisor, p, bundeslandID, wahljahr)

        return divisor_query

    total_query = ""
    for i in range(1, 17):
        if (i != 16):
            total_query = total_query + \
                sitze_parteien_pro_bundesland(i) + "union"
        else:
            total_query = total_query + sitze_parteien_pro_bundesland(i)

    if wahljahr == 2017:
        vorlaeufige_sitzverteilung_partei_bundesland = "CREATE MATERIALIZED VIEW VorlaufigeSitzverteilungParteienProBundesland2017 AS {};".format(
            total_query)
    else:
        vorlaeufige_sitzverteilung_partei_bundesland = "CREATE MATERIALIZED VIEW VorlaufigeSitzverteilungParteienProBundesland AS {};".format(
            total_query)

    cur.execute(vorlaeufige_sitzverteilung_partei_bundesland)
    sql_con.commit()

    #########################################################################################
    ####################################### Schritt 3 #######################################
    #########################################################################################

    # Verteile 598 Sitze im Bundestag auf die Parteien und vergrößere eventuell den Bundestag

    # 1. Bestimmung Divisor ohne Überhang
    if wahljahr == 2017:
        v = "VorlaufigeSitzverteilungParteienProBundesland2017"
    else:
        v = "VorlaufigeSitzverteilungParteienProBundesland"

    divisor_parteien_ohne = """
        with divisoren as (select v.partei, avg(d.anzahlzweitstimmen)/(sum(v.sitzkontingente)-0.5) as Divisor
            from {} v, deutschlandstimmenaggregation d
            where v.partei = d.partei
            and wahljahr = {}
            group by v.partei)
        
        select min(Divisor)
        from divisoren
        """.format(v, wahljahr)
    cur.execute(divisor_parteien_ohne)
    divisor_ohne = int(cur.fetchall()[0][0])

    # 2. Bestimme Divisor mit Überhang
    divisor_parteien_mit = """
        with mindestsitze as (select partei, sum(direktmandate) as mindestsitze
        from {} v
        group by partei
        having sum(sitzkontingente) < sum(direktmandate) ),
        divisoren_parteien_mit as (
        select m.partei, (1.0000*d.anzahlzweitstimmen)/(m.mindestsitze-0.5) as divisor
        from  mindestsitze m, deutschlandstimmenaggregation d
        where m.partei = d.partei
        and wahljahr = {}
        union
        select m.partei, (1.0000*d.anzahlzweitstimmen)/(m.mindestsitze-1.5) as divisor
        from  mindestsitze m, deutschlandstimmenaggregation d
        where m.partei = d.partei
        and wahljahr = {}
        union
        select m.partei, (1.0000*d.anzahlzweitstimmen)/(m.mindestsitze-2.5) as divisor
        from  mindestsitze m, deutschlandstimmenaggregation d
        where m.partei = d.partei
        and wahljahr = {}
        union
        select m.partei, (1.0000*d.anzahlzweitstimmen)/(m.mindestsitze-3.5) as divisor
        from  mindestsitze m, deutschlandstimmenaggregation d
        where m.partei = d.partei
        and wahljahr = {} 
        order by divisor asc)

        select divisor
        from divisoren_parteien_mit
        LIMIT 1 OFFSET 3
        """.format(v, wahljahr, wahljahr, wahljahr, wahljahr)

    cur.execute(divisor_parteien_mit)
    divisor_mit = int(cur.fetchall()[0][0])

    # 3. Bestimme endgültigen Divisor und berechne damit die Sitzverteilung

    divisor_total = min(divisor_mit, divisor_ohne)
    if wahljahr == 2017:
        p = "parteieninbt2017"
    else:
        p = "parteieninbt"

    sitze_bundestag_query = """
        select p.partei, case when d.direktmandate > round((1.000*d.anzahlzweitstimmen)/{}) then d.direktmandate else round((1.000*d.anzahlzweitstimmen)/{}) end as sitze
        from  deutschlandstimmenaggregation d, {} p
        where d.partei = p.partei
        and wahljahr = {}
        """.format(divisor_total, divisor_total, p, wahljahr)

    if wahljahr == 2017:
        sitze_bundestag = "CREATE TABLE SitzverteilungBundestag2017 AS {};".format(
            sitze_bundestag_query)
    else:
        sitze_bundestag = "CREATE TABLE SitzverteilungBundestag AS {};".format(
            sitze_bundestag_query)

    cur.execute(sitze_bundestag)
    sql_con.commit()

    #########################################################################################
    ####################################### Schritt 4 #######################################
    #########################################################################################

    # Verteile die Sitze auf die Parteien in den Bundesländern

    if wahljahr == 2017:
        s = "SitzverteilungBundestag2017"
    else:
        s = "SitzverteilungBundestag"

    def parteisitze_pro_bundesland(partei):
        divisor_query = """
        select ((1.000*d.anzahlzweitstimmen)/s.sitze) as divisor
        from deutschlandstimmenaggregation d, {} s
        where d.wahljahr = {}
        and d.partei = s.partei
        and d.partei = {}
        """.format(s, wahljahr, partei)

        cur.execute(divisor_query)
        divisor = round(cur.fetchall()[0][0])

        while (True):
            summe_sitze_query = """
            with sitzeBundeslaenderVorlaufig as 
                (select bundesland, case when round((1.000*anzahlzweitstimmen)/{}) > direktmandate then round((1.000*anzahlzweitstimmen)/{}) else direktmandate end as sitze, round((1.000*anzahlzweitstimmen)/{}) as sitze_ohne_dm
                from  bundeslandstimmenaggregation b
                where partei = {}
                and wahljahr = {}
                )
                
            select sum(sitze)
            from sitzeBundeslaenderVorlaufig        
            """.format(divisor, divisor, divisor, partei, wahljahr)

            cur.execute(summe_sitze_query)
            summe_sitze = cur.fetchall()[0][0]

            echte_sitze_query = """
            select sitze
            from {}
            where partei = {}
            """.format(s, partei)

            cur.execute(echte_sitze_query)
            echte_sitze = cur.fetchall()[0][0]

            if summe_sitze < echte_sitze:
                divisor -= 1
            elif summe_sitze > echte_sitze:
                divisor += 1
            else:
                break

        endgueltig_query = """
        select bundesland, partei, case when round((1.000*anzahlzweitstimmen)/{}) > direktmandate then round((1.000*anzahlzweitstimmen)/{}) else direktmandate end as sitze, round((1.000*anzahlzweitstimmen)/{}) as sitze_ohne_dm
        from  bundeslandstimmenaggregation b
        where partei = {}
        and wahljahr = {}
        """.format(divisor, divisor, divisor, partei, wahljahr)

        return endgueltig_query

    parteien_bt_query = """
    select partei
    from {}
    """.format(s)
    cur.execute(parteien_bt_query)
    parteien_bt = cur.fetchall()

    total_query = ""
    for i in range(len(parteien_bt)):
        if (i != len(parteien_bt) - 1):
            total_query = total_query + \
                parteisitze_pro_bundesland(parteien_bt[i][0]) + "union"
        else:
            total_query = total_query + \
                parteisitze_pro_bundesland(parteien_bt[i][0])

    if wahljahr == 2017:
        sitzverteilung_partei_bundesland = "CREATE MATERIALIZED VIEW SitzverteilungParteienProBundesland2017 AS {};".format(
            total_query)
    else:
        sitzverteilung_partei_bundesland = "CREATE MATERIALIZED VIEW SitzverteilungParteienProBundesland AS {};".format(
            total_query)
    cur.execute(sitzverteilung_partei_bundesland)

    cur.execute("DROP MATERIALIZED VIEW IF EXISTS VorlaeufigeSitzverteilung")
    sql_con.commit()

sql_con.commit()
sql_con.close()
