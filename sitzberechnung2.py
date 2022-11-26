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

###########################################################################################
####################################### Preparation #######################################
###########################################################################################

# compute parties that will enter the Bundestag


bundestags_parteien = """
select d.Partei
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

# TODO: Direktmandate sind noch nicht in Deutschlandaggregation, deswegen fehlt noch die Linke


######################################################################################
####################################### Step 1 #######################################
######################################################################################

# Distribute the 598 seats in the bundestag to the Länder according to their population


# TODO: add bevoelkerung to deutschlandaggregation
bevoelkerung = 72463198
divisor_query = """
select (1.0000 * {})/598 as divisor
    from DeutschlandAggregation d
    where d.wahljahr = {}
""".format(bevoelkerung, wahljahr)

cur.execute(divisor_query)
divisor = round(cur.fetchall()[0][0])

# TODO: add bevoelkerung to bundesland
vorlaeufigeSitzverteilung = """
select BundesLandID, round(b.Bevoelkerung/{}) as sitze
        from BundesLand
""".format(divisor, wahljahr)

load_bundestags_parteien = "CREATE MATERIALIZED VIEW VorlaeufigeSitzverteilung AS {};".format(
    bundestags_parteien)

sql_con.commit()
sql_con.close()
