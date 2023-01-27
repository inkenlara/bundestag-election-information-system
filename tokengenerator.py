try:
    import psycopg2
except ImportError:
    import pip
    pip.main(['install', '--user', 'psycopg2'])
    import psycopg2
import random
from hashlib import sha256
import sys

wahlkreis = 66

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


def generate_token(wahlkreisid):
    range_query = """
    select tokenrangemin, tokenrangemax
    from tokenrange
    where wahlkreis = {}
    """.format(wahlkreisid)
    cur.execute(range_query)
    range = cur.fetchall()[0]
    mini = range[0]
    maxi = range[1]
    return random.randrange(mini, maxi)


token = generate_token(wahlkreis)

try:
    hashed_token = sha256(token.to_bytes(8, 'big', signed=False)).hexdigest()
    print(hashed_token)
    insert_token_query = """
    INSERT INTO tokens 
        VALUES ('{}', {})
    """.format(hashed_token, wahlkreis)
    cur.execute(insert_token_query)
    print(token)
except psycopg2.errors.UniqueViolation:
    print("Token already exists. Try generating again.")


sql_con.commit()
sql_con.close()
