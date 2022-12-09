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
try:
    import numpy as np
except ImportError:
    import pip
    pip.main(['install', '--user', 'numpy'])
    import numpy as np
try:
    import pandas as pd
except ImportError:
    import pip
    pip.main(['install', '--user', 'pandas'])
    import pandas as pd
try:
    import timeit
except ImportError:
    import pip
    pip.main(['install', '--user', 'timeit'])
    import timeit


# path_kands_2017 = "csvs/kandidaten2017.csv"
path_kands_2021 = "csvs/btw21_kandidaturen_utf8.csv"
path_kerg = "csvs/kerg.csv"

# no unvalid stimmen, man wählt mit erst und zweitstimme eine partei, kandidat kann später über join herausgefunden werden


def WahlkreisStimmenGenerator(WahlkreisID, firstIDErst, firstIDZweit):
    # get number of votes for each party
    with open(path_kerg) as f:
        csv_buffer = csv.reader(f, delimiter=';', quotechar='"')

        csv_list = list(csv_buffer)
        # get column index of every party
        columnIndexParty = {}
        for i in range(19, len(csv_list[0])-3, 4):
            columnIndexParty[i] = csv_list[0][i]

        # get number first votes and second votes for each party
        for row in csv_list:
            if (row[0].isdecimal() and int(row[0]) == WahlkreisID and row[2].isdecimal() and int(row[2]) != 99):
                vergebeneStimmen = int(row[7])
                ungueltig_erst = int(row[11])
                ungueltig_zweit = int(row[13])

                vergebeneStimmenErst = vergebeneStimmen - ungueltig_erst
                vergebeneStimmenZweit = vergebeneStimmen - ungueltig_zweit
                partyErstZweitStimmen = {}

                j = 0
                for i in columnIndexParty:
                    j += 1
                    erststimmen = int(
                        row[i]) if row[i] and row[i].isdecimal() else 0
                    zweitstimmen = int(
                        row[i+2]) if row[i+2] and row[i+2].isdecimal() else 0
                    partyErstZweitStimmen[j] = [erststimmen, zweitstimmen]

                # erstimmen: [id, wahlkreis, erststimme (partei)]
                # zweitstimmen: [id, wahlkreis, zweistimme (partei)]

                erststimmen = np.ndarray(
                    shape=(vergebeneStimmenErst, 3), dtype=int)

                zweitstimmen = np.ndarray(
                    shape=(vergebeneStimmenZweit, 3), dtype=int)
                # fill in stimmzettel ID
                erststimmen[:, 0] = range(
                    firstIDErst, firstIDErst + vergebeneStimmenErst)
                zweitstimmen[:, 0] = range(
                    firstIDZweit, firstIDZweit + vergebeneStimmenZweit)

                # fill in wahlkreis
                erststimmen[:, 1] = np.full(
                    shape=vergebeneStimmenErst, fill_value=WahlkreisID)
                zweitstimmen[:, 1] = np.full(
                    shape=vergebeneStimmenZweit, fill_value=WahlkreisID)

                # fill in all the erst und zweitstimmen
                erststimmenFill = np.array([])
                zweitstimmenFill = np.array([])
                for i in partyErstZweitStimmen:
                    arr1 = np.full(
                        shape=partyErstZweitStimmen[i][0],
                        fill_value=i)
                    erststimmenFill = np.concatenate(
                        (erststimmenFill, arr1), axis=0)
                    arr2 = np.full(
                        shape=partyErstZweitStimmen[i][1],
                        fill_value=i)
                    zweitstimmenFill = np.concatenate(
                        (zweitstimmenFill, arr2), axis=0)

                # erststimmenFill = np.concatenate(
                #    (erststimmenFill, np.full(shape=ungueltig_erst, fill_value=0)), axis=0)
                # zweitstimmenFill = np.concatenate(
                #    (zweitstimmenFill, np.full(shape=ungueltig_zweit, fill_value=0)), axis=0)

                erststimmen[:, 2] = erststimmenFill
                zweitstimmen[:, 2] = zweitstimmenFill

    return erststimmen, zweitstimmen

    """
    # get number of votes for each candidate
    with open(path_kands_2021) as f2:
        csv_buffer = csv.reader(f2, delimiter=';', quotechar='"')

        for i in range(8):
            next(csv_buffer)

        candidate_stimmen = {}
        for row in csv_buffer:
            kreis = int(row[19]) if row[19] and row[19].isdecimal() else None
            if kreis == WahlkreisID:
                candidate_name = row[5]
                candidate_surname = row[4]
                partei = row[23]

                # TODO: gilt nur, wenn es nur eine EB in dem Wahlkreis gibt:
                if (partei[:3] == "EB:"):
                    stimmen = partyErstZweitStimmen["Übrige"][0]
                else:
                    stimmen = partyErstZweitStimmen[partei][0]

                candidate_stimmen[partei] = [
                    candidate_name, candidate_surname, stimmen]

        print(partyErstZweitStimmen)
    """

# WahlkreisStimmenGenerator(1)


allErststimmen = np.array([], dtype=np.int64).reshape(0, 3)
allZweitstimmen = np.array([], dtype=np.int64).reshape(0, 3)

startTime = timeit.default_timer()
startFillingArrysStartTime = timeit.default_timer()

for i in range(1, 300):
    firstIDErst = len(allErststimmen) + 1
    firstIDZweit = len(allZweitstimmen) + 1
    erststimmen, zweitstimmen = WahlkreisStimmenGenerator(
        i, firstIDErst, firstIDZweit)
    allErststimmen = np.vstack(
        [allErststimmen, erststimmen])
    allZweitstimmen = np.vstack(
        [allZweitstimmen, zweitstimmen])


print("Filling arrays took:", timeit.default_timer() - startFillingArrysStartTime)

#erstimmen_test = WahlkreisStimmenGenerator(1)[0]
#zweitstimmen_test = WahlkreisStimmenGenerator(1)[1]

#DF = pd.DataFrame(zweitstimmen_test)
#DF.to_csv("zweitstimmen_test.csv", header=None, index=None)

DF1 = pd.DataFrame(allErststimmen)
DF2 = pd.DataFrame(allZweitstimmen)

DF1.to_csv("erststimmen.csv", header=None, index=None)
DF2.to_csv("zweitstimmen.csv", header=None, index=None)

"""
db_host = "localhost"
db_port = 5432
db_name = "postgres"
db_user = "newuser"
db_password = "pw"
"""
db_host = "localhost"
db_port = 5432
db_name = "wahl"
db_user = "postgres"
db_password = ""

try:
    conn = psycopg2.connect(
        host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
    cur = conn.cursor()
    print("Success")

    cur.execute("truncate table erststimmen cascade")
    cur.execute("truncate table zweitstimmen cascade")
    conn.commit()

    #f = open('/Users/inkengruner/Documents/Studium/Master/1. Semester/Datenbanken/wahl/erstimmen_test.csv', 'r')
    #cur.copy_from(f, 'erststimmen', sep=',')
    # f.close()

    #f = open('/Users/inkengruner/Documents/Studium/Master/1. Semester/Datenbanken/wahl/zweitstimmen_test.csv', 'r')
    #cur.copy_from(f, 'zweitstimmen', sep=',')
    # f.close()

    copyDataStartTime = timeit.default_timer()

    # Inken
    """f = open('/Users/inkengruner/Documents/Studium/Master/1. Semester/Datenbanken/wahl/erststimmen.csv', 'r')
    cur.copy_from(f, 'erststimmen', sep=',')
    f.close()

    f = open('/Users/inkengruner/Documents/Studium/Master/1. Semester/Datenbanken/wahl/zweitstimmen.csv', 'r')
    cur.copy_from(f, 'zweitstimmen', sep=',')
    f.close()"""

    # Adnan
    f = open('erststimmen.csv', 'r')
    cur.copy_from(f, 'erststimmen', sep=',')
    f.close()

    f = open('zweitstimmen.csv', 'r')
    cur.copy_from(f, 'zweitstimmen', sep=',')
    f.close()


    print("Filling tables took:", timeit.default_timer() - copyDataStartTime)

    print("Whole process took:", timeit.default_timer() - startTime)

    conn.commit()
except Exception as error:
    print(error)
finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()
