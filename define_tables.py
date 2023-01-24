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


cur.execute("drop table if exists partei cascade")
cur.execute("drop table if exists bundesland cascade")
cur.execute("drop table if exists wahlkreis cascade")
cur.execute("drop table if exists WahlKreisAggretation cascade")
cur.execute("drop table if exists bundeslandaggregation cascade")
cur.execute("drop table if exists deutschlandaggregation cascade")
cur.execute("drop table if exists WahlKreisZweitStimmenAggregation cascade")
cur.execute("drop table if exists BundeslandStimmenAggregation cascade")
cur.execute("drop table if exists DeutschlandStimmenAggregation cascade")
cur.execute("drop table if exists BundesLandProzentErst cascade")
cur.execute("drop table if exists BundesLandProzentZwei cascade")
cur.execute("drop table if exists WahlKreisProzentErst cascade")
cur.execute("drop table if exists WahlKreisProzentZweit cascade")
cur.execute("drop table if exists kandidaten cascade")
cur.execute("drop table if exists direktkandidaten cascade")
cur.execute("drop table if exists listenkandidaten cascade")
cur.execute("drop table if exists strukturdaten cascade")  
cur.execute("drop table if exists erststimmen cascade")  
cur.execute("drop table if exists zweitstimmen cascade")  

sql_con.commit()

cur.execute("""
CREATE TABLE BundesLand (
	BundesLandID int primary key,
	BundesLandName varchar(30) NOT NULL
);
""")

cur.execute("""
CREATE TABLE Partei (
	ParteiID int primary key,
	Bezeichnung varchar(200) unique not null,
	KurzBezeichnung varchar(30)
);
""")

cur.execute("""
CREATE TABLE WahlKreis (
	WahlKreisID int primary key,
	WahlKreisName varchar(100) NOT NULL,
	Bundesland int NOT NULL references BundesLand
);
""")

cur.execute("""
CREATE TABLE Kandidaten (
	KandidatID int primary key,
	FirstName varchar(60) not null,
	LastName varchar(60) not null,
	Beruf varchar(120),
	Partei int references Partei ON DELETE SET NULL,
	WahlJahr int NOT NULL
);
""")

cur.execute("""
CREATE TABLE Direktkandidaten (
	KandidatID int primary key,
	Wahlkreis int NOT NULL references WahlKreis ON DELETE CASCADE,
	FOREIGN KEY (KandidatID) REFERENCES Kandidaten ON DELETE CASCADE
);
""")

cur.execute("""
CREATE TABLE ListenKandidaten(
	KandidatID int primary key,
	Bundesland int NOT NULL references BundesLand,
	ListenPlatz int not null,
	FOREIGN KEY (KandidatID) REFERENCES Kandidaten ON DELETE CASCADE
);
""")

cur.execute("""
CREATE TABLE ErstStimmen(
	ErstimmID int primary key,
	WahlKreis int NOT NULL references WahlKreis,
	Partei int references Partei ON DELETE SET NULL
);
""")

cur.execute("""
CREATE TABLE ZweitStimmen(
	ZweitstimmID int primary key,
	WahlKreis int NOT NULL references WahlKreis,
	Partei int references Partei ON DELETE SET NULL
);
""")

cur.execute("""
CREATE TABLE WahlKreisAggretation(
	WahlKreis int references WahlKreis ON DELETE CASCADE,
	WahlJahr int NOT NULL,
	PRIMARY KEY (WahlKreis, WahlJahr),
	UngueltigeErst int NOT NULL,
	UngueltigeZweit int NOT NULL,
	AnzahlWahlberechtigte int NOT NULL,
	AnzahlWaehlende int NOT NULL
);
""")

cur.execute("""
CREATE TABLE BundesLandAggregation(
	BundesLand int references BundesLand,
	WahlJahr int NOT NULL,
	PRIMARY KEY (BundesLand, WahlJahr),
	UnGueltigeErst int NOT NULL,
	UnGueltigeZweit int NOT NULL,
	AnzahlWahlBerechtigte int NOT NULL,
	AnzahlWaehlende int NOT NULL,
	Bevoelkerung int NOT NULL
);
""")

cur.execute("""
CREATE TABLE DeutschlandAggregation(
	WahlJahr int primary key,
	UnGueltigeErst int NOT NULL,
	UnGueltigeZweit int NOT NULL,
	AnzahlWahlBerechtigte int NOT NULL,
	AnzahlWaehlende int NOT NULL,
	Bevoelkerung int NOT NULL
);
""")

cur.execute("""
CREATE TABLE WahlKreisZweitStimmenAggregation (
	WahlJahr int NOT NULL,
	Partei int references Partei,
	WahlKreis int references WahlKreis,
	AnzahlStimmen int NOT NULL,
	PRIMARY KEY(Partei, WahlKreis, WahlJahr)
);
""")

cur.execute("""
CREATE TABLE WahlKreisProzentErst(
	WahlJahr int NOT NULL,
	WahlKreis int references WahlKreis,
	ParteiKurz varchar(60),
	ProzentErstStimmen decimal(10, 8) NOT NULL,
	PRIMARY KEY(WahlJahr, WahlKreis, ParteiKurz)
);
""")

cur.execute("""
CREATE TABLE WahlKreisProzentZweit(
	WahlJahr int NOT NULL,
	WahlKreis int references WahlKreis,
	ParteiKurz varchar(60),
	ProzentZweitStimmen decimal(10, 8) NOT NULL,
	PRIMARY KEY(WahlJahr, WahlKreis, ParteiKurz)
);
""")

cur.execute("""
CREATE TABLE BundesLandProzentErst(
	WahlJahr int NOT NULL,
	BundesLand int references BundesLand,
	ParteiKurz varchar(60),
	ProzentErstStimmen decimal(10, 8) NOT NULL,
	PRIMARY KEY(WahlJahr, BundesLand, ParteiKurz)
);
""")

cur.execute("""
CREATE TABLE BundesLandProzentZwei(
	WahlJahr int NOT NULL,
	BundesLand int references BundesLand,
	ParteiKurz varchar(60),
	ProzentZweitStimmen decimal(10, 8) NOT NULL,
	PRIMARY KEY(WahlJahr, BundesLand, ParteiKurz)
);
""")

cur.execute("""
CREATE TABLE BundeslandStimmenAggregation (
    Wahljahr int NOT NULL,
    Bundesland int NOT NULL references BundesLand,
    Partei int NOT NULL references Partei,
	PRIMARY KEY(Partei, Bundesland, WahlJahr),
    AnzahlErstStimmen int NOT NULL,
	AnzahlZweitStimmen int NOT NULL,
	DirektMandate int NOT NULL
);
""")

cur.execute("""
CREATE TABLE DeutschlandStimmenAggregation (
    Wahljahr int NOT NULL,
    Partei int NOT NULL references Partei,
	PRIMARY KEY(Partei, WahlJahr),
    AnzahlErstStimmen int NOT NULL,
	AnzahlZweitStimmen int NOT NULL,
	DirektMandate int NOT NULL
);
""")

cur.execute("""
CREATE TABLE StrukturDaten (
	WahlKreis int references WahlKreis PRIMARY KEY,
	Bildung decimal(3,1) NOT NULL,           -- AG
	EinkommenPrivateHaushalte int NOT NULL   -- AJ
); 
""")

sql_con.commit()
sql_con.close()