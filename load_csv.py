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


# TODO figure out what to change in this table
# def wahlBerechtigte():
#    pass


"""
	ErstimmID int primary key,
	Kandidat int references Direktkandidaten,   -- NULl
	WahlJahr int NOT NULL,
    WahlKreis int NOT NULL references WahlKreis,
    KVorName varchar(200),
	KNachName varchar(200)
"""
def erstStimmen():
    with open(path_kandidaturen, encoding='utf-8') as f:
        csv_buffer = csv.reader(f, delimiter=';', quotechar='"')
        next(csv_buffer)
        next(csv_buffer)
        next(csv_buffer)
        final = []
        ErstimmID = 0
        WahlJahr = 2021
        Kandidat = None      # TODO join using names to get candidate keys
        WahlKreis = 0
        KVorName = ""
        KNachName = ""
        for row in csv_buffer:
            if(not row[14]):    # if None -> the kandidat ist Direkt kandidat
                ErstimmID = ErstimmID + 1 
                # if(ErstimmID > 20): break
                WahlKreis = row[20]
                KVorName = row[5]
                KNachName = row[4]
                final.append([ErstimmID, None, WahlJahr, WahlKreis, KVorName, KNachName])
        cur.executemany('INSERT INTO erststimmen VALUES(%s, %s, %s, %s, %s, %s)', final)



"""WahlKreis int references WahlKreis ON DELETE CASCADE,
	WahlJahr int NOT NULL,
	PRIMARY KEY (WahlKreis, WahlJahr),
	UnGultigeErst int NOT NULL,
	UnGultigeZweit int NOT NULL,
	AnzahlWahlBerechtigte int NOT NULL,
	AnzahlWahlende int NOT NULL"""
def WahlKreisAggretation():
    with open(path_kerg, encoding='utf-8') as f:  # 2021
        csv_buffer = csv.reader(f, delimiter=';', quotechar='"')
        next(csv_buffer)
        next(csv_buffer)
        next(csv_buffer)
        final = []
        for row in csv_buffer:
            if(row[2] == "99" or row[1] == "Bundesgebiet"):
                continue
            else:
                WahlKreis = row[0]
                WahlJahr = 2021
                UnGultigeErst = row[11]
                UnGultigeZweit = row[13]
                AnzahlWahlBerechtigte = row[3]
                AnzahlWahlende = row[7]
                final.append([WahlKreis, WahlJahr, UnGultigeErst, UnGultigeZweit, AnzahlWahlBerechtigte, AnzahlWahlende])
    with open(path_kerg, encoding='utf-8') as f:  # 2017
        csv_buffer = csv.reader(f, delimiter=';', quotechar='"')
        next(csv_buffer)
        next(csv_buffer)
        next(csv_buffer)
        for row in csv_buffer:
            if(row[2] == "99" or row[1] == "Bundesgebiet"):
                continue
            else:
                WahlKreis = row[0]
                WahlJahr = 2017
                UnGultigeErst = row[12]
                UnGultigeZweit = row[14]
                AnzahlWahlBerechtigte = row[4]
                AnzahlWahlende = row[8]
                final.append([WahlKreis, WahlJahr, UnGultigeErst, UnGultigeZweit, AnzahlWahlBerechtigte, AnzahlWahlende])
        cur.executemany('INSERT INTO WahlKreisAggretation VALUES(%s, %s, %s, %s, %s, %s)', final)


    """BundesLand int references BundesLand,
	WahlJahr int NOT NULL,
	PRIMARY KEY (BundesLand, WahlJahr),
	UnGultigeErst int NOT NULL,
	UnGultigeZweit int NOT NULL,
	AnzahlWahlBerechtigte int NOT NULL,
	AnzahlWahlende int NOT NULL"""
def BundesLandAggregation():
    with open(path_kerg, encoding='utf-8') as f:  # 2021
        csv_buffer = csv.reader(f, delimiter=';', quotechar='"')
        next(csv_buffer)
        next(csv_buffer)
        next(csv_buffer)
        final = []
        for row in csv_buffer:
            if(not row[2] == "99"):
                continue
            else:
                BundesLand = row[0]
                WahlJahr = 2021
                UnGultigeErst = row[11]
                UnGultigeZweit = row[13]
                AnzahlWahlBerechtigte = row[3]
                AnzahlWahlende = row[7]
                final.append([BundesLand, WahlJahr, UnGultigeErst, UnGultigeZweit, AnzahlWahlBerechtigte, AnzahlWahlende])
    with open(path_kerg, encoding='utf-8') as f:  # 2017
        csv_buffer = csv.reader(f, delimiter=';', quotechar='"')
        next(csv_buffer)
        next(csv_buffer)
        next(csv_buffer)
        for row in csv_buffer:
            if(not row[2] == "99"):
                continue
            else:
                BundesLand = row[0]
                WahlJahr = 2017
                UnGultigeErst = row[12]
                UnGultigeZweit = row[14]
                AnzahlWahlBerechtigte = row[4]
                AnzahlWahlende = row[8]
                final.append([BundesLand, WahlJahr, UnGultigeErst, UnGultigeZweit, AnzahlWahlBerechtigte, AnzahlWahlende])
    cur.executemany('INSERT INTO BundesLandAggregation VALUES(%s, %s, %s, %s, %s, %s)', final)


"""WahlJahr int primary key,
	UnGultigeErst int NOT NULL,
	UnGultigeZweit int NOT NULL,
	AnzahlWahlBerechtigte int NOT NULL,
	AnzahlWahlende int NOT NULL"""
def deutschland():
    with open(path_kerg, encoding='utf-8') as f: 
        csv_buffer = csv.reader(f, delimiter=';', quotechar='"')
        next(csv_buffer)
        next(csv_buffer)
        next(csv_buffer)
        final = []
        for row in csv_buffer:
            if(not row[0] == "99" and not row[1] == "Bundesgebiet"):
                continue
            else:
                WahlJahr = 2021
                UnGultigeErst = row[11]
                UnGultigeZweit = row[13]
                AnzahlWahlBerechtigte = row[3]
                AnzahlWahlende = row[7]
                final.append([WahlJahr, UnGultigeErst, UnGultigeZweit, AnzahlWahlBerechtigte, AnzahlWahlende])
    with open(path_kerg, encoding='utf-8') as f: 
        csv_buffer = csv.reader(f, delimiter=';', quotechar='"')
        next(csv_buffer)
        next(csv_buffer)
        next(csv_buffer)
        for row in csv_buffer:
            if(not row[0] == "99" and not row[1] == "Bundesgebiet"):
                continue
            else:
                WahlJahr = 2017
                UnGultigeErst = row[12]
                UnGultigeZweit = row[14]
                AnzahlWahlBerechtigte = row[4]
                AnzahlWahlende = row[8]
                final.append([WahlJahr, UnGultigeErst, UnGultigeZweit, AnzahlWahlBerechtigte, AnzahlWahlende])
    cur.executemany('INSERT INTO DeutschlandAggregation VALUES(%s, %s, %s, %s, %s)', final)




"""WahlJahr int NOT NULL,
	Partei int references Partei,
	WahlKreis int references WahlKreis,
	AnzahlStimmen int NOT NULL,
	ProzentWahlhKreis decimal(3, 2),
    ParteiName varchar(200)"""
def WahlKreisZweitStimmenAggregation():
    with open(path_kerg, encoding='utf-8') as f: 
        csv_buffer = csv.reader(f, delimiter=';', quotechar='"')
        partei_namen = []
        head = next(csv_buffer)
        for k in range(19, 208, 4):    # 48 total
            partei_namen.append(head[k])
        next(csv_buffer)
        next(csv_buffer)
        final = []
        WahlJahr = 2021
        for row in csv_buffer:
            if(row[2] == "99" or row[1] == "Bundesgebiet"):
                continue
            else:
                ProzentWahlhKreis = 0         # TODO Calc prozent
                WahlKreis = row[0]
                i = 21
                for partei in partei_namen:
                    Partei = partei_namen.index(partei) + 1
                    if(not row[i]): AnzahlStimmen = 0
                    else:
                        AnzahlStimmen = row[i]
                    final.append([WahlJahr, Partei, WahlKreis, AnzahlStimmen, ProzentWahlhKreis, partei])
                    i = i + 4
    with open(path_kerg, encoding='utf-8') as f: 
        csv_buffer = csv.reader(f, delimiter=';', quotechar='"')
        partei_namen = []
        head = next(csv_buffer)
        for k in range(19, 208, 4):    # 48 total
            partei_namen.append(head[k])
        next(csv_buffer)
        next(csv_buffer)
        WahlJahr = 2017
        for row in csv_buffer:
            if(row[2] == "99" or row[1] == "Bundesgebiet"):
                continue
            else:
                ProzentWahlhKreis = 0
                WahlKreis = int(row[0])
                i = 21
                for partei in partei_namen:
                    Partei = partei_namen.index(partei) + 1
                    if(not row[i + 1]): AnzahlStimmen = 0
                    else:
                        AnzahlStimmen = row[i + 1]
                    final.append([WahlJahr, Partei, WahlKreis, AnzahlStimmen, ProzentWahlhKreis, partei])
                    i = i + 4
    cur.executemany('INSERT INTO WahlKreisZweitStimmenAggregation VALUES(%s, %s, %s, %s, %s, %s)', final)






# CALLING THE FUNCTIONS
# bundesland()
# kreise()
# partei()
# direktKandidaten2021()
# direktKandidaten2017()
# wahlBerechtigte()
# erstStimmen()
# WahlKreisAggretation()
# BundesLandAggregation()
# deutschland()
WahlKreisZweitStimmenAggregation()


sql_con.commit()
sql_con.close()