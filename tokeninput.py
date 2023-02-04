import sys


try:
    import psycopg2
except ImportError:
    import psycopg2


# Adnans local test db:
"""
db_host = "localhost"
db_port = 5432
db_name = "wahl"
db_user = "postgres"
db_password = ""


# Inkens local test db:
db_host = "localhost"
db_port = 5432
db_name = "postgres"
db_user = "newuser"
db_password = "pw"
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


# Output: list of tuples inlcuding strings (firstname, lastname, job, parteikurz, parteilang)
# if candidate does not have a party parteikurz and parteilang are None
def erststimmen_data(wahlkreisid):
    dirketkandidaten_query = """
    select k.firstname, k.lastname, k.beruf, p.kurzbezeichnung, p.bezeichnung
    from direktkandidaten dk, kandidaten k 
    left outer join partei p on k.partei = p.parteiid
    where k.wahljahr = 2021
    and dk.wahlkreis = {}
    and dk.kandidatid = k.kandidatid
    """.format(wahlkreisid)
    cur.execute(dirketkandidaten_query)
    direktkandidaten = cur.fetchall()
    return direktkandidaten


# Output:list of lists containing parteiid, parteikurz, parteilang, list of tuples containg names of first five list candidates
def zweitstimmen_data(wahlkreisid):
    angetretene_parteien_query = """
    select distinct p.parteiid, p.kurzbezeichnung, p.bezeichnung
    from listenkandidaten lk, kandidaten k, partei p, wahlkreis w
    where k.wahljahr = 2021
    and w.wahlkreisid = {}
    and w.bundesland = lk.bundesland
    and lk.kandidatid = k.kandidatid
    and k.partei = p.parteiid
    order by p.parteiid asc
    """.format(wahlkreisid)
    cur.execute(angetretene_parteien_query)
    angetretene_parteien = cur.fetchall()

    parteienliste = []
    for partei in angetretene_parteien:
        p = list(partei)
        parteiid = p[0]
        listenkandidaten_query = """
        select concat_ws(' ', k.firstname, k.lastname) as kandidaten
        from listenkandidaten lk, kandidaten k, wahlkreis w
        where k.wahljahr = 2021
        and w.wahlkreisid = {}
        and w.bundesland = lk.bundesland
        and lk.kandidatid = k.kandidatid
        and k.partei = {}
        order by lk.listenplatz asc
        limit 5
        """.format(wahlkreisid, parteiid)
        cur.execute(listenkandidaten_query)
        listenkandidaten = cur.fetchall()
        p.append(listenkandidaten)
        parteienliste.append(p)

    return parteienliste


def token_to_wahlzettel(token):
    check_token_query = """
    select COUNT(*) from tokens where token = {}
    """.format(token)
    cur.execute(check_token_query)
    record_exists = cur.fetchall()[0][0]
    if not record_exists:
        print("Token not valid.")
        return None, None
    else:
        wahlkreis_query = """
        select wahlkreis
        from tokenrange
        where tokenrangemin < {}
        and tokenrangemax > {}
        """.format(token, token)
        cur.execute(wahlkreis_query)
        wahlkreis = cur.fetchall()[0][0]
        zweitstimmenzettel = zweitstimmen_data(wahlkreis)
        erstimmenzettel = erststimmen_data(wahlkreis)
        delete_token_query = """
        DELETE FROM tokens
        WHERE token = {}
        """.format(token)
        cur.execute(delete_token_query)
        return erstimmenzettel, zweitstimmenzettel


erstimmenzettel, zweitstimmenzettel = token_to_wahlzettel(651679875022)

print(erstimmenzettel)
print(zweitstimmenzettel)

sql_con.commit()
sql_con.close()
