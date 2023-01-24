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
import re

# Adnans local test db:
"""
db_host = "localhost"
db_port = 5432
db_name = "wahl"
db_user = "postgres"
db_password = ""
"""


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

path_kands_2017 = "csvs/kandidaten2017.csv"
path_kands_2021 = "csvs/btw21_kandidaturen_utf8.csv"
path_kerg = "csvs/kerg.csv"
path_kerg2 = "csvs/kerg2.csv"
path_kandidaturen = "csvs/kandidaturen.csv"
path_strukturdaten = "csvs/btw21_strukturdaten.csv"


# loads kandidaten, direkt- und listenkandidaten for year 2021

"""
CREATE TABLE Kandidaten (
	KandidatID int primary key,
	FirstName varchar(60) not null,
	LastName varchar(60) not null,
	Beruf varchar(120),
	Partei int references Partei ON DELETE SET NULL,
	WahlJahr int NOT NULL
);

CREATE TABLE Direktkandidaten (
	KandidatID int primary key,
	Wahlkreis int NOT NULL references WahlKreis ON DELETE CASCADE,
	FOREIGN KEY (KandidatID) REFERENCES Kandidaten ON DELETE CASCADE
);

CREATE TABLE ListenKandidaten(
	KandidatID int primary key,
	Bundesland int NOT NULL references BundesLand,
	ListenPlatz int not null,
	FOREIGN KEY (KandidatID) REFERENCES Kandidaten ON DELETE CASCADE
);
"""


def kandidaten():
    # kandidaten 2021:
    with open(path_kerg, encoding='utf-8') as f:
        csv_buffer = csv.reader(f, delimiter=';', quotechar='"')
        csv_list = list(csv_buffer)

        partei_namen = []
        for k in range(19, len(csv_list[0]) - 3, 4):    # 48 total
            partei_namen.append(csv_list[0][k])

    with open(path_kands_2021, encoding='utf-8') as f:
        csv_buffer = csv.reader(f, delimiter=';', quotechar='"')

        next(csv_buffer)

        id = 0

        nachname_idx = 4
        vorname_idx = 5
        beruf_idx = 15
        bundesland_idx = 19
        gebietsart_idx = 18
        wahlkreis_idx = 19
        partei_idx = 23
        platz_idx = 24
        verkn_liste_idx = 25
        platz_dk_idx = 31
        bundesland_dk_idx = 27
        wahljahr = 2021

        kandidaten = []
        direkt = []
        listen = {}

        for row in csv_buffer:
            nachname = row[nachname_idx]
            vorname = row[vorname_idx]
            if row[partei_idx] in partei_namen:
                partei = partei_namen.index(row[partei_idx]) + 1
            else:
                partei = None
            beruf = row[beruf_idx]
            if row[gebietsart_idx] == "Wahlkreis":
                id += 1
                wahlkreis = row[wahlkreis_idx]
                kandidaten.append(
                    (id, vorname, nachname, beruf, partei, wahljahr))
                direkt.append((id, wahlkreis))
                if row[verkn_liste_idx] != '':
                    bundesland = row[bundesland_dk_idx]
                    platz = row[platz_dk_idx]
                    listen[(partei, bundesland, platz)] = id
            elif row[gebietsart_idx] == "Land":
                bundesland = row[bundesland_idx]
                platz = row[platz_idx]
                if ((partei, bundesland, platz) not in listen):
                    id += 1
                    kandidaten.append(
                        (id, vorname, nachname, beruf, partei, wahljahr))
                    listen[(partei, bundesland, platz)] = id

    cur.executemany(
        'INSERT INTO Kandidaten VALUES(%s, %s, %s, %s, %s, %s)', kandidaten)
    cur.executemany('INSERT INTO Direktkandidaten VALUES(%s, %s)', direkt)

    for kandidat in listen:
        bundesland = kandidat[1]
        platz = kandidat[2]
        id = listen[kandidat]
        cur.execute('INSERT INTO Listenkandidaten VALUES(%s, %s, %s)',
                    (id, bundesland, platz))

    # kandidaten 2017:
    kand_id = len(kandidaten) + 1
    with open(path_kands_2017, encoding='utf-8') as f:
        csv_buffer = csv.reader(f, delimiter=';', quotechar='"')
        next(csv_buffer)

        kandidaten17 = []
        direkt17 = []
        listen17 = []
        for row in csv_buffer:
            name = row[0]
            komma_idx = name.find(',')
            # candidate is direktkandidat and listenkandidat
            if komma_idx == -1:
                kand_id -= 1
                kand_in = row[3]
                land_start_idx = kand_in.find(' ')
                land_end_idx = kand_in.find('(') - 1
                land = kand_in[land_start_idx + 1:land_end_idx]
                platz = re.search("[0-9]+", kand_in).group()
                bundeslandid_query = """
                select bundeslandid
                from bundesland 
                where bundeslandname = '{}'
                """.format(land)
                cur.execute(bundeslandid_query)
                land_id = cur.fetchall()[0][0]
                listen17.append((kand_id, land_id, platz))
            else:
                vorname = name[komma_idx + 2:]
                nachname = name[:komma_idx]
                beruf = None
                partei_kurz = row[2]
                if re.match("EB", partei_kurz):
                    parteiid = None
                else:
                    partei_id_query = """
                    select parteiid
                    from partei 
                    where kurzbezeichnung = '{}'
                    """.format(partei_kurz)
                    cur.execute(partei_id_query)
                    # TODO/HACK: try except kann entfernt werden, wenn wir auch alle parteien von 2017 haben
                    try:
                        parteiid = cur.fetchall()[0][0]
                    except IndexError:
                        parteiid = None
                kandidaten17.append(
                    (kand_id, vorname, nachname, beruf, parteiid, 2017))
                kand_in = row[3]
                if re.match("Land", kand_in):
                    land_start_idx = kand_in.find(' ')
                    land_end_idx = kand_in.find('(') - 1
                    land = kand_in[land_start_idx + 1:land_end_idx]
                    platz = re.search("[0-9]+", kand_in).group()
                    bundeslandid_query = """
                    select bundeslandid
                    from bundesland 
                    where bundeslandname = '{}'
                    """.format(land)
                    cur.execute(bundeslandid_query)
                    land_id = cur.fetchall()[0][0]
                    listen17.append((kand_id, land_id, platz))
                else:
                    wahlkreisid = re.search("[0-9]+", kand_in).group()
                    direkt17.append((kand_id, wahlkreisid))

            kand_id += 1
    cur.executemany(
        'INSERT INTO kandidaten VALUES(%s, %s, %s, %s, %s, %s)', kandidaten17)
    cur.executemany(
        'INSERT INTO direktkandidaten VALUES(%s, %s)', direkt17)
    cur.executemany(
        'INSERT INTO listenkandidaten VALUES(%s, %s, %s)', listen17)


# bundesländer


def bundesland():
    with open(path_kerg) as f:
        csv_buffer = csv.reader(f, delimiter=';', quotechar='"')
        next(csv_buffer)
        bundesland_data = []
        for rows in csv_buffer:
            if (rows[2] == "99"):
                bundesland_data.append([int(rows[0]), rows[1]])
        cur.executemany(
            'INSERT INTO BundesLand VALUES(%s, %s)', bundesland_data)

#   WahlKreisID int primary key,
# 	WahlKreisName varchar(100) NOT NULL,
#   Bundesland int NOT NULL references BundesLand

# kreise


def kreise():
    with open(path_kerg) as f:
        csv_buffer = csv.reader(f, delimiter=';', quotechar='"')
        next(csv_buffer)
        next(csv_buffer)
        next(csv_buffer)
        kreis_data = []
        for rows in csv_buffer:
            if (rows[2] == "99" or rows[1] == "Bundesgebiet"):
                continue
            else:
                # print([int(rows[0]), int(rows[1]), rows[2]])
                kreis_data.append([int(rows[0]), rows[1], int(rows[2])])
        cur.executemany('INSERT INTO WahlKreis VALUES(%s, %s, %s)', kreis_data)

# Übrige sind mit NULL bezeichnet
# Ungültige haben parteiID -1

def partei():
    total_partei = []
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
        for n in range(0, 48):
            total_partei.append([ids[n], partei_data[n]])
    with open(path_kands_2021, encoding='utf-8') as f:
        csv_buffer2 = csv.reader(f, delimiter=';', quotechar='"')
        next(csv_buffer2)
        kurz = []
        lang = []
        for row in csv_buffer2:
            if (row[22].startswith('EB')):
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
        total_partei.append(
            [49, "RESIST! FRIEDLICHE ÖKOLINKSLIBERALE DEMOKRATISCHE REVOLUTION. FREIHEITEN, DEMOKRATIE, WOHLSTAND, GESUNDHEIT FÜR ALLE! BULTHEEL WÄHLEN!"])
        total_partei.append([50, "Unabhängig! Für Dich. Für Uns. Für Alle."])
        total_partei.append([51, "Erststimme fürs Klima"])
        total_partei.append(
            [52, "Transparent, Nah am Bürger, Treu den Wählern"])
        for r in total_partei:
            dict_key = r[1]
            if (dict_key == "Übrige"):
                r.append(None)
            else:
                r.append(k_l[dict_key])
        total_partei.append([-1, "Ungültig", "Ungültig"])
        cur.executemany('INSERT INTO Partei VALUES(%s, %s, %s)', total_partei)



"""WahlKreis int references WahlKreis ON DELETE CASCADE,
	WahlJahr int NOT NULL,
	PRIMARY KEY (WahlKreis, WahlJahr),
	UnGultigeErst int NOT NULL,
	UnGultigeZweit int NOT NULL,
	AnzahlWahlBerechtigte int NOT NULL,
	AnzahlWahlende int NOT NULL"""


def WahlKreisAggretation():
    final = []
    with open(path_kerg, encoding='utf-8') as f:  # 2021
        csv_buffer = csv.reader(f, delimiter=';', quotechar='"')
        next(csv_buffer)
        next(csv_buffer)
        next(csv_buffer)
        for row in csv_buffer:
            if (row[2] == "99" or row[1] == "Bundesgebiet"):
                continue
            else:
                WahlKreis = row[0]
                WahlJahr = 2021
                UnGultigeErst = row[11]
                UnGultigeZweit = row[13]
                AnzahlWahlBerechtigte = row[3]
                AnzahlWahlende = row[7]
                final.append([WahlKreis, WahlJahr, UnGultigeErst,
                             UnGultigeZweit, AnzahlWahlBerechtigte, AnzahlWahlende])
    with open(path_kerg, encoding='utf-8') as f:  # 2017
        csv_buffer = csv.reader(f, delimiter=';', quotechar='"')
        next(csv_buffer)
        next(csv_buffer)
        next(csv_buffer)
        for row in csv_buffer:
            if (row[2] == "99" or row[1] == "Bundesgebiet"):
                continue
            else:
                WahlKreis = row[0]
                WahlJahr = 2017
                UnGultigeErst = row[12]
                UnGultigeZweit = row[14]
                AnzahlWahlBerechtigte = row[4]
                AnzahlWahlende = row[8]
                final.append([WahlKreis, WahlJahr, UnGultigeErst,
                             UnGultigeZweit, AnzahlWahlBerechtigte, AnzahlWahlende])
        cur.executemany(
            'INSERT INTO WahlKreisAggretation VALUES(%s, %s, %s, %s, %s, %s)', final)

    """BundesLand int references BundesLand,
	WahlJahr int NOT NULL,
	PRIMARY KEY (BundesLand, WahlJahr),
	UnGultigeErst int NOT NULL,
	UnGultigeZweit int NOT NULL,
	AnzahlWahlBerechtigte int NOT NULL,
	AnzahlWahlende int NOT NULL"""


def BundesLandAggregation():
    final = []
    with open(path_kerg, encoding='utf-8') as f:  # 2021
        bevoelkerung = {"Schleswig-Holstein": 2659792, "Mecklenburg-Vorpommern": 1532412, "Hamburg": 1537766, "Niedersachsen": 7207587, "Bremen": 548941, "Brandenburg": 2397701, "Sachsen-Anhalt": 2056177,
                        "Berlin": 2942960, "Nordrhein-Westfalen": 15415642, "Sachsen": 3826905, "Hessen": 5222158, "Thüringen": 1996822, "Rheinland-Pfalz": 3610865, "Bayern": 11328866, "Baden-Württemberg": 9313413, "Saarland": 865191}
        csv_buffer = csv.reader(f, delimiter=';', quotechar='"')
        next(csv_buffer)
        next(csv_buffer)
        next(csv_buffer)
        for row in csv_buffer:
            if (not row[2] == "99"):
                continue
            else:
                BundesLand = row[0]
                BundesLandName = row[1]
                WahlJahr = 2021
                UnGultigeErst = row[11]
                UnGultigeZweit = row[13]
                AnzahlWahlBerechtigte = row[3]
                AnzahlWahlende = row[7]
                final.append([BundesLand, WahlJahr, UnGultigeErst,
                             UnGultigeZweit, AnzahlWahlBerechtigte, AnzahlWahlende, bevoelkerung[BundesLandName]])
    with open(path_kerg, encoding='utf-8') as f:  # 2017
        bevoelkerung = {"Schleswig-Holstein": 2673803, "Mecklenburg-Vorpommern": 1548400, "Hamburg": 1525090, "Niedersachsen": 7278789, "Bremen": 568510, "Brandenburg": 2391746, "Sachsen-Anhalt": 2145671,
                        "Berlin": 2975745, "Nordrhein-Westfalen": 15707569, "Sachsen": 3914671, "Hessen": 5281198, "Thüringen": 2077901, "Rheinland-Pfalz": 3661245, "Bayern": 11362245, "Baden-Württemberg": 9365001, "Saarland": 899748}
        csv_buffer = csv.reader(f, delimiter=';', quotechar='"')
        next(csv_buffer)
        next(csv_buffer)
        next(csv_buffer)
        for row in csv_buffer:
            if (not row[2] == "99"):
                continue
            else:
                BundesLand = row[0]
                BundesLandName = row[1]
                WahlJahr = 2017
                UnGultigeErst = row[12]
                UnGultigeZweit = row[14]
                AnzahlWahlBerechtigte = row[4]
                AnzahlWahlende = row[8]
                final.append([BundesLand, WahlJahr, UnGultigeErst,
                             UnGultigeZweit, AnzahlWahlBerechtigte, AnzahlWahlende, bevoelkerung[BundesLandName]])
    cur.executemany(
        'INSERT INTO BundesLandAggregation VALUES(%s, %s, %s, %s, %s, %s, %s)', final)


"""WahlJahr int primary key,
	UnGultigeErst int NOT NULL,
	UnGultigeZweit int NOT NULL,
	AnzahlWahlBerechtigte int NOT NULL,
	AnzahlWahlende int NOT NULL"""


def deutschland():
    final = []
    with open(path_kerg, encoding='utf-8') as f:
        csv_buffer = csv.reader(f, delimiter=';', quotechar='"')
        next(csv_buffer)
        next(csv_buffer)
        next(csv_buffer)
        for row in csv_buffer:
            if (not row[0] == "99" and not row[1] == "Bundesgebiet"):
                continue
            else:
                WahlJahr = 2021
                UnGultigeErst = row[11]
                UnGultigeZweit = row[13]
                AnzahlWahlBerechtigte = row[3]
                AnzahlWahlende = row[7]
                final.append([WahlJahr, UnGultigeErst, UnGultigeZweit,
                             AnzahlWahlBerechtigte, AnzahlWahlende, 72463198])
    with open(path_kerg, encoding='utf-8') as f:
        csv_buffer = csv.reader(f, delimiter=';', quotechar='"')
        next(csv_buffer)
        next(csv_buffer)
        next(csv_buffer)
        for row in csv_buffer:
            if (not row[0] == "99" and not row[1] == "Bundesgebiet"):
                continue
            else:
                WahlJahr = 2017
                UnGultigeErst = row[12]
                UnGultigeZweit = row[14]
                AnzahlWahlBerechtigte = row[4]
                AnzahlWahlende = row[8]
                final.append([WahlJahr, UnGultigeErst, UnGultigeZweit,
                             AnzahlWahlBerechtigte, AnzahlWahlende, 73377332])
    cur.executemany(
        'INSERT INTO DeutschlandAggregation VALUES(%s, %s, %s, %s, %s, %s)', final)


"""WahlJahr int NOT NULL,
	Partei int references Partei,
	WahlKreis int references WahlKreis,
	AnzahlStimmen int NOT NULL,
	ProzentWahlhKreis decimal(3, 2),
    ParteiName varchar(200)"""


def WahlKreisZweitStimmenAggregation():
    final = []
    with open(path_kerg, encoding='utf-8') as f:
        csv_buffer = csv.reader(f, delimiter=';', quotechar='"')
        partei_namen = []
        head = next(csv_buffer)
        for k in range(19, 208, 4):    # 48 total
            partei_namen.append(head[k])
        next(csv_buffer)
        next(csv_buffer)
        WahlJahr = 2021
        for row in csv_buffer:
            if (row[2] == "99" or row[1] == "Bundesgebiet"):
                continue
            else:
                ProzentWahlhKreis = 0
                WahlKreis = row[0]
                i = 21
                for partei in partei_namen:
                    Partei = partei_namen.index(partei) + 1
                    if (not row[i]):
                        AnzahlStimmen = 0
                    else:
                        AnzahlStimmen = row[i]
                    final.append([WahlJahr, Partei, WahlKreis,
                                 AnzahlStimmen])
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
            if (row[2] == "99" or row[1] == "Bundesgebiet"):
                continue
            else:
                ProzentWahlhKreis = 0
                WahlKreis = int(row[0])
                i = 21
                for partei in partei_namen:
                    Partei = partei_namen.index(partei) + 1
                    if (not row[i + 1]):
                        AnzahlStimmen = 0
                    else:
                        AnzahlStimmen = row[i + 1]
                    final.append([WahlJahr, Partei, WahlKreis,
                                 AnzahlStimmen])
                    i = i + 4
    cur.executemany(
        'INSERT INTO WahlKreisZweitStimmenAggregation VALUES(%s, %s, %s, %s)', final)


"""   Wahljahr int NOT NULL,
    Bundesland int NOT NULL references BundesLand,
    Partei int NOT NULL references Partei,
	PRIMARY KEY(Partei, Bundesland, WahlJahr),
    AnzahlErstStimmen int NOT NULL,
	ProzentErstStimmen decimal(3, 2) NOT NULL,
	AnzahlZweitStimmen int NOT NULL,
	ProzentZweitStimmen decimal(3, 2) NOT NULL,
	DirektMandate int NOT NULL,
	ListenMandate int NOT NULL,
	UberhangsMandate int NOT NULL"""


def BundeslandStimmenAggregation():
    final = []
    with open(path_kerg, encoding='utf-8') as f:
        csv_buffer = csv.reader(f, delimiter=';', quotechar='"')
        partei_namen = []
        head = next(csv_buffer)
        for k in range(19, 208, 4):    # 48 total
            partei_namen.append(head[k])
        next(csv_buffer)
        next(csv_buffer)
        WahlJahr = 2021
        for row in csv_buffer:
            if (not row[2] == "99"):
                continue
            else:
                Bundesland = row[0]
                i = 19
                for partei in partei_namen:
                    Partei = partei_namen.index(partei) + 1
                    if (not row[i]):
                        AnzahlErstStimmen = 0
                    else:
                        AnzahlErstStimmen = row[i]
                    if (not row[i + 2]):
                        AnzahlZweitStimmen = 0
                    else:
                        AnzahlZweitStimmen = row[i + 2]
                    DirektMandate = 0               
                    final.append([WahlJahr, Bundesland, Partei, AnzahlErstStimmen,
                                 AnzahlZweitStimmen, DirektMandate])
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
            if (not row[2] == "99"):
                continue
            else:
                Bundesland = row[0]
                i = 19
                for partei in partei_namen:
                    Partei = partei_namen.index(partei) + 1
                    if (not row[i + 1]):
                        AnzahlErstStimmen = 0
                    else:
                        AnzahlErstStimmen = row[i + 1]
                    if (not row[i + 2 + 1]):
                        AnzahlZweitStimmen = 0
                    else:
                        AnzahlZweitStimmen = row[i + 2 + 1]
                    DirektMandate = 0               # computed in different function
                    final.append([WahlJahr, Bundesland, Partei, AnzahlErstStimmen,
                                 AnzahlZweitStimmen, DirektMandate])
                    i = i + 4
    cur.executemany(
        'INSERT INTO BundeslandStimmenAggregation VALUES(%s, %s, %s, %s, %s, %s)', final)


"""
computes direktmandate per bundesland per partei for 2021
IMPORTANT: has to be called after BundeslandStimmenAggregation committed!
"""


def DirektmandateBundeslandStimmenAggregation():
    wahljahre = [2017, 2021]
    for wahljahr in wahljahre:
        direktmandate_query = """
        with wahlkreis_max as 
        (select wahlkreis, max(prozenterststimmen) as maxi
        from wahlkreisprozenterst
        where wahljahr = {}
        group by wahlkreis),
        direktmandate_wahlkreis as (
        select w.wahlkreis, w.parteikurz
        from wahlkreis_max b, wahlkreisprozenterst w
        where b.wahlkreis = w.wahlkreis 
        and b.maxi = w.prozenterststimmen),
        aggregated_direktmandate as(
        select w.bundesland, d.parteikurz, count(*) as direktmandate, p.parteiid
        from wahlkreis w, direktmandate_wahlkreis d, partei p
        where w.wahlkreisid = d.wahlkreis
        and p.kurzbezeichnung = d.parteikurz
        group by w.bundesland, d.parteikurz, p.parteiid)
        update BundeslandStimmenAggregation b 
        set direktmandate = case 
        when (select direktmandate from aggregated_direktmandate d where b.bundesland = d.bundesland and b.partei = d.parteiid) is not null 
        then (select direktmandate from aggregated_direktmandate d where b.bundesland = d.bundesland and b.partei = d.parteiid)
        else 0
        end
        """.format(wahljahr)

        cur.execute(direktmandate_query)


def DirektmandateDeutschlandStimmenAggregation():
    wahljahre = [2017, 2021]
    for wahljahr in wahljahre:
        direktmandate_query = """
        with aggregation as(
        select partei, sum(direktmandate) as direktmandate
        from BundeslandStimmenAggregation
        where wahljahr = {}
        group by partei)
        update deutschlandstimmenaggregation d
        set direktmandate = (select direktmandate from aggregation a where a.partei = d.partei)
        """.format(wahljahr)

    cur.execute(direktmandate_query)


"""Wahljahr int NOT NULL,
    Partei int NOT NULL references Partei,
	PRIMARY KEY(Partei, WahlJahr),
    AnzahlErstStimmen int NOT NULL,
	ProzentErstStimmen decimal(3, 2) NOT NULL,
	AnzahlZweitStimmen int NOT NULL,
	ProzentZweitStimmen decimal(3, 2) NOT NULL,
	DirektMandate int NOT NULL,
	ListenMandate int NOT NULL,
	UberhangsMandate int NOT NULL"""


def DeutschlandStimmenAggregation():
    final2021 = []
    final2017 = []
    with open(path_kerg, encoding='utf-8') as f:
        csv_buffer = csv.reader(f, delimiter=';', quotechar='"')
        partei_namen = []
        head = next(csv_buffer)
        for k in range(19, 208, 4):    # 48 total
            partei_namen.append(head[k])
        next(csv_buffer)
        next(csv_buffer)
        WahlJahr = 2021
        for row in csv_buffer:
            if (not row[0] == "99" and not row[1] == "Bundesgebiet"):
                continue
            else:
                i = 19
                for partei in partei_namen:
                    Partei = partei_namen.index(partei) + 1
                    if (not row[i]):
                        AnzahlErstStimmen = 0
                    else:
                        AnzahlErstStimmen = row[i]
                        AnzahlZweitStimmen = row[i + 2] if row[i + 2] else 0
                    ProzentErstStimmen = 0
                    ProzentZweitStimmen = 0
                    DirektMandate = 0              
                    final2021.append([WahlJahr, Partei, AnzahlErstStimmen, ProzentErstStimmen, AnzahlZweitStimmen,
                                     ProzentZweitStimmen, DirektMandate])
                    i = i + 4
    with open(path_kerg2, encoding='utf-8') as f:  # 2021
        csv_buffer = csv.reader(f, delimiter=';', quotechar='"')
        for i in range(0, 16):
            next(csv_buffer)
        list_erst = []
        list_zwei = []
        for row in csv_buffer:
            if (row[3] == "99" and row[4] == "Bundesgebiet" and not row[7] == "Einzelbewerber/Wählergruppe"):
                if (row[10] == "1"):  # Erststimme
                    ProzentErstStimmen = row[12] if row[12] else 0
                    list_erst.append(ProzentErstStimmen)
                    for i in range(0, len(list_erst)):
                        final2021[i][3] = round(
                            float(str(list_erst[i]).replace(",", ".")), 4)
                if (row[10] == "2"):  # Zweitstimmen
                    ProzentZweitStimmen = row[12] if row[12] else 0
                    list_zwei.append(ProzentZweitStimmen)
                    for i in range(0, len(list_zwei)):
                        final2021[i][5] = round(
                            float(str(list_zwei[i]).replace(",", ".")), 4)
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
            if (not row[0] == "99" and not row[1] == "Bundesgebiet"):
                continue
            else:
                i = 19
                for partei in partei_namen:
                    Partei = partei_namen.index(partei) + 1
                    if (not row[i + 1]):
                        AnzahlErstStimmen = 0
                    else:
                        AnzahlErstStimmen = row[i + 1]
                        AnzahlZweitStimmen = row[i +
                                                 2 + 1] if row[i + 2 + 1] else 0
                    ProzentErstStimmen = 0
                    ProzentZweitStimmen = 0
                    DirektMandate = 0               
                    final2017.append([WahlJahr, Partei, AnzahlErstStimmen, ProzentErstStimmen, AnzahlZweitStimmen,
                                     ProzentZweitStimmen, DirektMandate])
                    i = i + 4
    with open(path_kerg2, encoding='utf-8') as f:  # 2017
        csv_buffer = csv.reader(f, delimiter=';', quotechar='"')
        for i in range(0, 16):
            next(csv_buffer)
        list_erst = []
        list_zwei = []
        for row in csv_buffer:
            if (row[3] == "99" and row[4] == "Bundesgebiet" and not row[7] == "Einzelbewerber/Wählergruppe"):
                if (row[10] == "1"):  # Erststimme
                    ProzentErstStimmen = row[14] if row[14] else 0
                    list_erst.append(ProzentErstStimmen)
                    for i in range(0, len(list_erst)):
                        final2017[i][3] = round(
                            float(str(list_erst[i]).replace(',', ".")), 4)
                if (row[10] == "2"):  # Zweitstimmen
                    ProzentZweitStimmen = row[14] if row[14] else 0
                    list_zwei.append(ProzentZweitStimmen)
                    for i in range(0, len(list_zwei)):
                        final2017[i][5] = round(
                            float(str(list_zwei[i]).replace(',', '.')), 4)
    final = final2021 + final2017
    cur.executemany(
        'INSERT INTO DeutschlandStimmenAggregation VALUES(%s, %s, %s, %s, %s, %s, %s)', final)


"""WahlJahr int NOT NULL,
	BundesLand int references BundesLand,
	ParteiKurz varchar(60),
	ProzentErstStimmen decimal(10, 8) NOT NULL,"""


def BundesLandProzentErst():
    final = []
    with open(path_kerg2, encoding='utf-8') as f:  # 2021
        csv_buffer = csv.reader(f, delimiter=';', quotechar='"')
        for i in range(0, 16):
            next(csv_buffer)
        Wahljahr = 2021
        parteikurz_idx = 8
        prozent = 12
        b_idx = 3
        for row in csv_buffer:
            if (row[2] == "Land" and row[10] == "1" and row[5] == "BUND" and (row[7] == "Partei" or row[7] == "System-Gruppe") and row[8] != "Wahlberechtigte" and row[8] != "Wählende" and row[8] != "Ungültige" and row[8] != "Gültige"):
                Prozent = round(
                    float(str(row[prozent] if row[prozent] else 0).replace(',', ".")), 4)
                final.append(
                    [Wahljahr, row[b_idx], row[parteikurz_idx], Prozent])
    with open(path_kerg2, encoding='utf-8') as f:  # 2017
        csv_buffer = csv.reader(f, delimiter=';', quotechar='"')
        for i in range(0, 16):
            next(csv_buffer)
        Wahljahr = 2017
        parteikurz_idx = 8
        prozent = 12 + 2
        for row in csv_buffer:
            if (row[2] == "Land" and row[10] == "1" and row[5] == "BUND" and (row[7] == "Partei" or row[7] == "System-Gruppe") and row[8] != "Wahlberechtigte" and row[8] != "Wählende" and row[8] != "Ungültige" and row[8] != "Gültige"):
                Prozent = round(
                    float(str(row[prozent] if row[prozent] else 0).replace(',', ".")), 4)
                final.append(
                    [Wahljahr, row[b_idx], row[parteikurz_idx], Prozent])
    cur.executemany(
        'INSERT INTO BundesLandProzentErst VALUES(%s, %s, %s, %s)', final)


"""WahlJahr int NOT NULL,
	BundesLand int references BundesLand,
	ParteiKurz varchar(60),
	ProzentZweitStimmen decimal(10, 8) NOT NULL"""


def BundesLandProzentZwei():
    final = []
    with open(path_kerg2, encoding='utf-8') as f:  # 2021
        csv_buffer = csv.reader(f, delimiter=';', quotechar='"')
        for i in range(0, 16):
            next(csv_buffer)
        Wahljahr = 2021
        parteikurz_idx = 8
        prozent = 12
        b_idx = 3
        for row in csv_buffer:
            if (row[2] == "Land" and row[10] == "2" and row[5] == "BUND" and (row[7] == "Partei" or row[7] == "System-Gruppe") and row[8] != "Wahlberechtigte" and row[8] != "Wählende" and row[8] != "Ungültige" and row[8] != "Gültige"):
                Prozent = round(
                    float(str(row[prozent] if row[prozent] else 0).replace(',', ".")), 4)
                final.append(
                    [Wahljahr, row[b_idx], row[parteikurz_idx], Prozent])
    with open(path_kerg2, encoding='utf-8') as f:  # 2017
        csv_buffer = csv.reader(f, delimiter=';', quotechar='"')
        for i in range(0, 16):
            next(csv_buffer)
        Wahljahr = 2017
        parteikurz_idx = 8
        prozent = 12 + 2
        for row in csv_buffer:
            if (row[2] == "Land" and row[10] == "2" and row[5] == "BUND" and (row[7] == "Partei" or row[7] == "System-Gruppe") and row[8] != "Wahlberechtigte" and row[8] != "Wählende" and row[8] != "Ungültige" and row[8] != "Gültige"):
                Prozent = round(
                    float(str(row[prozent] if row[prozent] else 0).replace(',', ".")), 4)
                final.append(
                    [Wahljahr, row[b_idx], row[parteikurz_idx], Prozent])
    cur.executemany(
        'INSERT INTO BundesLandProzentZwei VALUES(%s, %s, %s, %s)', final)


"""WahlJahr int NOT NULL,
	WahlKreis int references WahlKreis,
	ParteiKurz varchar(60),
	ProzentErstStimmen decimal(10, 8) NOT NULL,"""


def WahlKreisProzentErst():
    final = []
    with open(path_kerg2, encoding='utf-8') as f:  # 2021
        csv_buffer = csv.reader(f, delimiter=';', quotechar='"')
        for i in range(0, 16):
            next(csv_buffer)
        Wahljahr = 2021
        parteikurz_idx = 8
        prozent = 12
        b_idx = 3
        for row in csv_buffer:
            if (row[2] == "Wahlkreis" and row[10] == "1" and row[5] == "LAND" and (row[7] == "Partei" or row[7] == "System-Gruppe") and row[8] != "Wahlberechtigte" and row[8] != "Wählende" and row[8] != "Ungültige" and row[8] != "Gültige"):
                Prozent = round(
                    float(str(row[prozent] if row[prozent] else 0).replace(',', ".")), 4)
                final.append(
                    [Wahljahr, row[b_idx], row[parteikurz_idx], Prozent])
    with open(path_kerg2, encoding='utf-8') as f:  # 2017
        csv_buffer = csv.reader(f, delimiter=';', quotechar='"')
        for i in range(0, 16):
            next(csv_buffer)
        Wahljahr = 2017
        parteikurz_idx = 8
        prozent = 12 + 2
        for row in csv_buffer:
            if (row[2] == "Wahlkreis" and row[10] == "1" and row[5] == "LAND" and (row[7] == "Partei" or row[7] == "System-Gruppe") and row[8] != "Wahlberechtigte" and row[8] != "Wählende" and row[8] != "Ungültige" and row[8] != "Gültige"):
                Prozent = round(
                    float(str(row[prozent] if row[prozent] else 0).replace(',', ".")), 4)
                final.append(
                    [Wahljahr, row[b_idx], row[parteikurz_idx], Prozent])
    cur.executemany(
        'INSERT INTO WahlKreisProzentErst VALUES(%s, %s, %s, %s)', final)


"""WahlJahr int NOT NULL,
	WahlKreis int references WahlKreis,
	ParteiKurz varchar(60),
	ProzentZweitStimmen decimal(10, 8) NOT NULL,"""


def WahlKreisProzentZweit():
    final = []
    with open(path_kerg2, encoding='utf-8') as f:  # 2021
        csv_buffer = csv.reader(f, delimiter=';', quotechar='"')
        for i in range(0, 16):
            next(csv_buffer)
        Wahljahr = 2021
        parteikurz_idx = 8
        prozent = 12
        b_idx = 3
        for row in csv_buffer:
            if (row[2] == "Wahlkreis" and row[10] == "2" and row[5] == "LAND" and (row[7] == "Partei" or row[7] == "System-Gruppe") and row[8] != "Wahlberechtigte" and row[8] != "Wählende" and row[8] != "Ungültige" and row[8] != "Gültige"):
                Prozent = round(
                    float(str(row[prozent] if row[prozent] else 0).replace(',', ".")), 4)
                final.append(
                    [Wahljahr, row[b_idx], row[parteikurz_idx], Prozent])
    with open(path_kerg2, encoding='utf-8') as f:  # 2017
        csv_buffer = csv.reader(f, delimiter=';', quotechar='"')
        for i in range(0, 16):
            next(csv_buffer)
        Wahljahr = 2017
        parteikurz_idx = 8
        prozent = 12 + 2
        for row in csv_buffer:
            if (row[2] == "Wahlkreis" and row[10] == "2" and row[5] == "LAND" and (row[7] == "Partei" or row[7] == "System-Gruppe") and row[8] != "Wahlberechtigte" and row[8] != "Wählende" and row[8] != "Ungültige" and row[8] != "Gültige"):
                Prozent = round(
                    float(str(row[prozent] if row[prozent] else 0).replace(',', ".")), 4)
                final.append(
                    [Wahljahr, row[b_idx], row[parteikurz_idx], Prozent])
    cur.executemany(
        'INSERT INTO WahlKreisProzentZweit VALUES(%s, %s, %s, %s)', final)


def load_strukturdaten():
    with open(path_strukturdaten, encoding='utf-8') as f:  # 2021
        csv_buffer = csv.reader(f, delimiter=';', quotechar='"')
        next(csv_buffer)
        next(csv_buffer)
        next(csv_buffer)
        next(csv_buffer)
        next(csv_buffer)
        next(csv_buffer)
        next(csv_buffer)
        next(csv_buffer)
        next(csv_buffer)
        lis = []
        for row in csv_buffer:
            if (int(row[1]) > 300):
                continue
            bildung = round(
                float(str(row[32]).replace(',', ".")), 1)
            lis.append([int(row[1]), bildung, int(row[35])])
        cur.executemany(
            'INSERT INTO strukturdaten VALUES(%s, %s, %s)', lis)


# TRUNCATE THE TABLES
cur.execute("truncate table partei cascade")
cur.execute("truncate table bundesland cascade")
cur.execute("truncate table wahlkreis cascade")
cur.execute("truncate table WahlKreisAggretation cascade")
cur.execute("truncate table bundeslandaggregation cascade")
cur.execute("truncate table deutschlandaggregation cascade")
cur.execute("truncate table WahlKreisZweitStimmenAggregation cascade")
cur.execute("truncate table BundeslandStimmenAggregation cascade")
cur.execute("truncate table DeutschlandStimmenAggregation cascade")
cur.execute("truncate table BundesLandProzentErst cascade")
cur.execute("truncate table BundesLandProzentZwei cascade")
cur.execute("truncate table WahlKreisProzentErst cascade")
cur.execute("truncate table WahlKreisProzentZweit cascade")
cur.execute("truncate table kandidaten cascade")
cur.execute("truncate table direktkandidaten cascade")
cur.execute("truncate table listenkandidaten cascade")
cur.execute("truncate table strukturdaten cascade")
sql_con.commit()

# CALLING THE FUNCTIONS AND FILL THE TABLES
bundesland() 
kreise()
partei()
WahlKreisAggretation()
BundesLandAggregation()
deutschland()
WahlKreisZweitStimmenAggregation()
BundeslandStimmenAggregation()
DeutschlandStimmenAggregation()
BundesLandProzentErst()
BundesLandProzentZwei()
WahlKreisProzentErst()
WahlKreisProzentZweit()
kandidaten()
load_strukturdaten()
DirektmandateBundeslandStimmenAggregation()
DirektmandateDeutschlandStimmenAggregation()


sql_con.commit()
sql_con.close()
