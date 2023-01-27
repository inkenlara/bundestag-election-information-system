
CREATE TABLE BundesLand (
	BundesLandID int primary key,
	BundesLandName varchar(30) NOT NULL
);

CREATE TABLE Partei (
	ParteiID int primary key,
	Bezeichnung varchar(200) unique not null,
	KurzBezeichnung varchar(30)
);

CREATE TABLE WahlKreis (
	WahlKreisID int primary key,
	WahlKreisName varchar(100) NOT NULL,
	Bundesland int NOT NULL references BundesLand
);

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



CREATE TABLE ErstStimmen(
	ErstimmID int primary key,
	WahlKreis int NOT NULL references WahlKreis,
	Partei int references Partei ON DELETE SET NULL
);


CREATE TABLE ZweitStimmen(
	ZweitstimmID int primary key,
	WahlKreis int NOT NULL references WahlKreis,
	Partei int references Partei ON DELETE SET NULL
);



CREATE TABLE WahlKreisAggretation(
	WahlKreis int references WahlKreis ON DELETE CASCADE,
	WahlJahr int NOT NULL,
	PRIMARY KEY (WahlKreis, WahlJahr),
	UngueltigeErst int NOT NULL,
	UngueltigeZweit int NOT NULL,
	AnzahlWahlberechtigte int NOT NULL,
	AnzahlWaehlende int NOT NULL
);	


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


CREATE TABLE DeutschlandAggregation(
	WahlJahr int primary key,
	UnGueltigeErst int NOT NULL,
	UnGueltigeZweit int NOT NULL,
	AnzahlWahlBerechtigte int NOT NULL,
	AnzahlWaehlende int NOT NULL,
	Bevoelkerung int NOT NULL
);	


CREATE TABLE WahlKreisZweitStimmenAggregation (
	WahlJahr int NOT NULL,
	Partei int references Partei,
	WahlKreis int references WahlKreis,
	AnzahlStimmen int NOT NULL,
	PRIMARY KEY(Partei, WahlKreis, WahlJahr)
);

CREATE TABLE WahlKreisProzentErst(
	WahlJahr int NOT NULL,
	WahlKreis int references WahlKreis,
	ParteiKurz varchar(60),
	ProzentErstStimmen decimal(10, 8) NOT NULL,
	PRIMARY KEY(WahlJahr, WahlKreis, ParteiKurz)
);

CREATE TABLE WahlKreisProzentZweit(
	WahlJahr int NOT NULL,
	WahlKreis int references WahlKreis,
	ParteiKurz varchar(60),
	ProzentZweitStimmen decimal(10, 8) NOT NULL,
	PRIMARY KEY(WahlJahr, WahlKreis, ParteiKurz)
);

CREATE TABLE BundesLandProzentErst(
	WahlJahr int NOT NULL,
	BundesLand int references BundesLand,
	ParteiKurz varchar(60),
	ProzentErstStimmen decimal(10, 8) NOT NULL,
	PRIMARY KEY(WahlJahr, BundesLand, ParteiKurz)
);

CREATE TABLE BundesLandProzentZwei(
	WahlJahr int NOT NULL,
	BundesLand int references BundesLand,
	ParteiKurz varchar(60),
	ProzentZweitStimmen decimal(10, 8) NOT NULL,
	PRIMARY KEY(WahlJahr, BundesLand, ParteiKurz)
);

CREATE TABLE BundeslandStimmenAggregation (
    Wahljahr int NOT NULL,
    Bundesland int NOT NULL references BundesLand,
    Partei int NOT NULL references Partei,
	PRIMARY KEY(Partei, Bundesland, WahlJahr),
    AnzahlErstStimmen int NOT NULL,
	AnzahlZweitStimmen int NOT NULL,
	DirektMandate int NOT NULL
);


CREATE TABLE DeutschlandStimmenAggregation (
    Wahljahr int NOT NULL,
    Partei int NOT NULL references Partei,
	PRIMARY KEY(Partei, WahlJahr),
    AnzahlErstStimmen int NOT NULL,
	AnzahlZweitStimmen int NOT NULL,
	DirektMandate int NOT NULL
);

--TODO: kann wahrscheinlich gelöscht werden
CREATE TABLE WahlKreisErstStimmenAggregation (
WahlJahr int NOT NULL,
Kandidat int references Direktkandidaten,
WahlKreis int references WahlKreis,
AnzahlStimmen int NOT NULL,
ProzentWahlhKreis decimal(3, 2),
PRIMARY KEY(Partei, WahlKreis, WahlJahr) -- TODO: partei is not in this table??
); 


CREATE TABLE StrukturDaten (
	WahlKreis int references WahlKreis PRIMARY KEY,
	Bildung decimal(3,1) NOT NULL,           -- AG
	EinkommenPrivateHaushalte int NOT NULL   -- AJ
); 