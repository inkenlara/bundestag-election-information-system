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
path_kerg2 = "csvs/kerg2.csv"
path_kandidaturen = "csvs/kandidaturen.csv"


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

# Übrige sind mit NULL bezeichnet
def partei():
    with open(path_kerg, encoding='utf-8') as f:
        csv_buffer = csv.reader(f, delimiter=';', quotechar='"')
        # next(csv_buffer)
        partei_data = []
        i = 0
        for row in csv_buffer:
            i = i + 1
            for k in range(19, 208, 4):    # 48 total
                partei_data.append(row[k])
            if (i == 1):
                break
        ids = []
        for k in range(1, 49):
            ids.append(k)
        total_partei = []
        for n in range(0, 48):
            total_partei.append([ids[n], partei_data[n]])
    with open(path_kands_2021, encoding='utf-8') as f:
        csv_buffer2 = csv.reader(f, delimiter=';', quotechar='"')
        next(csv_buffer2)
        kurz = []
        lang = []
        for row in csv_buffer2:
            if(row[22].startswith('EB')):
                continue
            else:
                kurz.append(row[22])
                lang.append(row[23])
        ded_kurz = list(dict.fromkeys(kurz))
        ded_lang = list(dict.fromkeys(lang))
        kurz_lang = []
        for n in range(0, 51):
            kurz_lang.append([ded_kurz[n], ded_lang[n]])
        k_l = dict(zip(ded_lang, ded_kurz))
        total_partei.append([49, "RESIST! FRIEDLICHE ÖKOLINKSLIBERALE DEMOKRATISCHE REVOLUTION. FREIHEITEN, DEMOKRATIE, WOHLSTAND, GESUNDHEIT FÜR ALLE! BULTHEEL WÄHLEN!"])
        total_partei.append([50, "Unabhängig! Für Dich. Für Uns. Für Alle."])
        total_partei.append([51, "Erststimme fürs Klima"])
        total_partei.append([52, "Transparent, Nah am Bürger, Treu den Wählern"])
        for r in total_partei:
            dict_key = r[1]
            if(dict_key == "Übrige"):
                r.append(None)
            else:
                r.append(k_l[dict_key])
        cur.executemany('INSERT INTO Partei VALUES(%s, %s, %s)', total_partei)


def direktKandidaten2021():
    with open(path_kands_2021, encoding='utf-8') as f:
        csv_buffer = csv.reader(f, delimiter=';', quotechar='"')
        next(csv_buffer)
        lis = []
        KandidatID = 0
        for row in csv_buffer:
            KandidatID = KandidatID + 1
            LastName = row[4]
            FirstName = row[5]
            Beruf = row[15]
            Partei = None                      # TODO Have to JOIN with Partei, in order to get Partei IDs
            WahlKreis = row[19]
            WahlJahr = 2021
            AnzahlStimmen = None               # TODO Missing number of votes
            ProzentWahlhKreis = None           # TODO Missing prozent of votes
            lis.append([KandidatID, FirstName, LastName, Beruf, Partei, WahlKreis, WahlJahr, AnzahlStimmen, ProzentWahlhKreis])
    cur.executemany('INSERT INTO DirektKandidaten VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)', lis)


# TODO very tricky to export data for 2017, maybe wait for a better source
def direktKandidaten2017():
    with open(path_kands_2017, encoding='utf-8') as f:
        csv_buffer = csv.reader(f, delimiter=';', quotechar='"')
        next(csv_buffer)
        for row in csv_buffer:
            pass





# CALLING THE FUNCTIONS
# bundesland()
# kreise()
# partei()
# direktKandidaten2021()
direktKandidaten2017()


sql_con.commit()
sql_con.close()