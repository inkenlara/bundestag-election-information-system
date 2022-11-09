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
try:
    import csv
except ImportError:
    import pip
    pip.main(['install', '--user', 'csv'])
    import csv


db_host = "localhost"
db_port = 5432
db_name = "wahl"
db_user = "postgres"
db_password = ""

try:
    sql_con = psycopg2.connect(host = db_host, port = db_port, database = db_name, user = db_user, password = db_password)
    cur = sql_con.cursor()
    print("Success")
except:
    print("Fail")




sql_con.close()