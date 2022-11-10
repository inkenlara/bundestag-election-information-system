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

path_kands_2017 = "csvs/kandidaten2017.csv"
path_kands_2021 = "csvs/btw21_kandidaturen_utf8.csv"
path_kerg = "csvs/kerg.csv"


# bundesländer
def bundesland():
    with open(path_kerg) as f:
        csv_buffer = csv.reader(f, delimiter=';', quotechar='"')
        next(csv_buffer)
        bundesland_data = []
        for rows in csv_buffer:
            if(rows[2] == "99"):
                bundesland_data.append([int(rows[0]), rows[1]])
        cur.executemany('INSERT INTO BundesLand VALUES(%s, %s)', bundesland_data)

#   WahlKreisID int primary key,
#   Bundesland int NOT NULL references BundesLand
# 	WahlKreisName varchar(100) NOT NULL,

#kreise
def kreise():
    with open(path_kerg) as f:
        csv_buffer = csv.reader(f, delimiter=';', quotechar='"')
        next(csv_buffer)
        next(csv_buffer)
        next(csv_buffer)
        kreis_data = []
        for rows in csv_buffer:
            if(rows[2] == "99" or rows[1] == "Bundesgebiet"):
                continue
            else:
                # print([int(rows[0]), int(rows[2]), rows[1]])
                kreis_data.append([int(rows[0]), int(rows[2]), rows[1]])
        cur.executemany('INSERT INTO WahlKreis VALUES(%s, %s, %s)', kreis_data)







# CALLING THE FUNCTIONS
# bundesland()
# kreise()

sql_con.commit()
sql_con.close()