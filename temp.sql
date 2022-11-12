
CREATE TABLE BundesLand(
	BundesLandID int primary key,
	BundesLandName varchar(30) NOT NULL
);

CREATE TABLE WahlKreis (
	WahlKreisID int primary key,
	WahlKreisName varchar(100) NOT NULL,
	Bundesland int NOT NULL references BundesLand
	-- AnzahlWahlBezirke int NOT NULL,    --Brauchen wir nicht wirklich
);

CREATE TABLE Partei (
	ParteiID int primary key,
	Bezeichnung varchar(200) unique not null,
	KurzBezeichnung varchar(30),      --Brauchen wir nicht wirklich
	-- AnzahlMitglieder int,
	-- PolitischeAusrichtung varchar(200),
	-- ParteiVorsitzende varchar(60)
);

CREATE TABLE Direktkandidaten (
	KandidatID int primary key,
	FirstName varchar(60) not null,
	LastName varchar(60) not null,
	Beruf varchar(120),
	Partei int references Partei ON DELETE SET NULL,
	Wahlkreis int NOT NULL references WahlKreis ON DELETE CASCADE,
	WahlJahr int NOT NULL,
	AnzahlStimmen int,
	ProzentWahlhKreis decimal(3, 2)
);


-- CREATE TABLE WahlBezirk(
-- 	WahlBezirkID int primary key,
-- 	AnzahlWahlBerechtigte int NOT NULL,
-- 	WahlKreis int NOT NULL references WahlKreis ON DELETE CASCADE
-- );


-- CREATE TABLE WahlLokal (
--	WahlLokalID int primary key,
--	Adresse varchar(100) NOT NULL,
--	WahlBezirk int NOT NULL references WahlBezirk ON DELETE CASCADE
--);


-- CREATE TABLE WahlBerechtigte (
--	PersonID int primary key,
--	FirstName varchar(30) not null,
--	LastName varchar(30) not null,
--	Gewahlt Bool NOT NULL,
--	WahlKreis int NOT NULL references WahlKreis ON DELETE SET NULL,
--	WahlJahr int NOT NULL
--);


CREATE TABLE ErstStimmen(
	ErstimmID int primary key,
	Kandidat int references Direktkandidaten,   -- NULL am anfang
	WahlJahr int NOT NULL,
	WahlKreis int NOT NULL references WahlKreis,
	KVorName varchar(200),
	KNachName varchar(200)
);

CREATE TABLE LandesListe(
	ListID int primary key,
	BundesLand int NOT NULL references BundesLand,
	Partei int references Partei ON DELETE CASCADE,
	WahlJahr int NOT NULL
);

CREATE TABLE ZweitStimmen(
	ZweitstimmID int primary key,
	WahlKreis int NOT NULL references WahlKreis,
	Partei int references Partei ON DELETE SET NULL,
	LandesListe int NOT NULL references LandesListe,
	WahlJahr int NOT NULL
);



CREATE TABLE ListenKandidaten(
	KandidatenID int not null,
	FirstName varchar(30) not null,
	LastName varchar(30) not null,
	LandesListe int NOT NULL references LandesListe,
	ListenPlatz int not null
);


CREATE TABLE WahlKreisAggretation(
	WahlKreis int references WahlKreis ON DELETE CASCADE,
	WahlJahr int NOT NULL,
	PRIMARY KEY (WahlKreis, WahlJahr),
	UnGultigeErst int NOT NULL,
	UnGultigeZweit int NOT NULL,
	AnzahlWahlBerechtigte int NOT NULL,
	AnzahlWahlende int NOT NULL
);	


CREATE TABLE BundesLandAggregation(
	BundesLand int references BundesLand,
	WahlJahr int NOT NULL,
	PRIMARY KEY (BundesLand, WahlJahr),
	UnGultigeErst int NOT NULL,
	UnGultigeZweit int NOT NULL,
	AnzahlWahlBerechtigte int NOT NULL,
	AnzahlWahlende int NOT NULL
);	


CREATE TABLE DeutschlandAggregation(
	WahlJahr int primary key,
	UnGultigeErst int NOT NULL,
	UnGultigeZweit int NOT NULL,
	AnzahlWahlBerechtigte int NOT NULL,
	AnzahlWahlende int NOT NULL
);	


CREATE TABLE WahlKreisZweitStimmenAggregation (
	WahlJahr int NOT NULL,
	Partei int references Partei,
	WahlKreis int references WahlKreis,
	AnzahlStimmen int NOT NULL,
	ProzentWahlhKreis decimal(3, 2) NOT NULL,
	PRIMARY KEY(Partei, WahlKreis, WahlJahr)
);



CREATE TABLE BundeslandStimmenAggregation (
    Wahljahr int NOT NULL,
    Bundesland int NOT NULL references BundesLand,
    Partei int NOT NULL references Partei,
	PRIMARY KEY(Partei, Bundesland, WahlJahr),
    AnzahlErstStimmen int NOT NULL,
	ProzentErstStimmen decimal(3, 2) NOT NULL,
	AnzahlZweitStimmen int NOT NULL,
	ProzentZweitStimmen decimal(3, 2) NOT NULL,
	DirektMandate int NOT NULL,
	ListenMandate int NOT NULL,
	UberhangsMandate int NOT NULL
);


CREATE TABLE DeutschlandStimmenAggregation (
    Wahljahr int NOT NULL,
    Partei int NOT NULL references Partei,
	PRIMARY KEY(Partei, WahlJahr),
    AnzahlErstStimmen int NOT NULL,
	ProzentErstStimmen decimal(3, 2) NOT NULL,
	AnzahlZweitStimmen int NOT NULL,
	ProzentZweitStimmen decimal(3, 2) NOT NULL,
	DirektMandate int NOT NULL,
	ListenMandate int NOT NULL,
	UberhangsMandate int NOT NULL
);

-- CREATE TABLE StimmZettel (
--	StimmZettelToken int primary key,
--	DirektKandidaten int references Direktkandidaten,
--	LandListe int references LandesListe,
--	Verwendet bool NOT NULL,
--	WahlKreis int NOT NULL references WahlKreis
--);