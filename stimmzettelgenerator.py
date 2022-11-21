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
    import re
except ImportError:
    import pip
    pip.main(['install', '--user', 're'])
    import re
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
    
    
    

#path_kands_2017 = "csvs/kandidaten2017.csv"
path_kands_2021 = "csvs/btw21_kandidaturen_utf8.csv"
path_kerg = "csvs/kerg.csv"

#if stimme ungültig -> 0, man wählt mit erst und zweitstimme eine partei, kandidat kann später über join herausgefunden werden
def WahlkreisStimmenGenerator(WahlkreisID):
    # get number of votes for each party
    with open(path_kerg) as f:
        csv_buffer = csv.reader(f, delimiter=';', quotechar='"')
        next(csv_buffer)
        next(csv_buffer)

        csv_list = list(csv_buffer)
        # get column index of every party
        columnIndexParty = {}
        for i in range(19, len(csv_list[0])-3, 4):
            columnIndexParty[i] = csv_list[0][i]

        # get number first votes and second votes for each party
        for row in csv_list:
            try:
                if (int(row[0]) == WahlkreisID and int(row[2]) != 99):
                    vergebeneStimmen = int(row[7])
                    ungueltig_erst = int(row[11])
                    ungueltig_zweit = int(row[13])
                    partyErstZweitStimmen = {}
                    j = 0
                    for i in columnIndexParty:
                            j +=1
                            erststimmen = int(row[i]) if row[i] and row[i].isdecimal() else 0
                            zweitstimmen = int(row[i+2]) if row[i+2] and row[i+2].isdecimal() else 0
                            partyErstZweitStimmen[j] = [erststimmen, zweitstimmen]   
                    # one stimmzettel consists of [id, erststimme (partei), zweitstimme (partei), wahlkreis]
                    stimmzettel = np.ndarray(shape=(vergebeneStimmen, 4), dtype=int)
                    #fill in stimmzettel ID
                    stimmzettel[:, 0] = range(1, vergebeneStimmen + 1)
                    #fill in wahlkreis     
                    stimmzettel[:, 3] = np.full(shape=vergebeneStimmen, fill_value=WahlkreisID)          
                    #fill in all the erst und zweitstimmen
                    erststimmen = np.array([])
                    zweitstimmen = np.array([])
                    for i in partyErstZweitStimmen:
                        arr1 = np.full(
                            shape=partyErstZweitStimmen[i][0],
                            fill_value=i)
                        erststimmen = np.concatenate((erststimmen, arr1), axis=0)
                        arr2 = np.full(
                            shape=partyErstZweitStimmen[i][1],
                            fill_value=i)
                        zweitstimmen = np.concatenate((zweitstimmen, arr2), axis=0)
                    erststimmen = np.concatenate((erststimmen, np.full(shape = ungueltig_erst, fill_value = 0)), axis=0)
                    zweitstimmen = np.concatenate((zweitstimmen, np.full(shape = ungueltig_zweit, fill_value = 0)), axis=0)
                    stimmzettel[:, 1] = erststimmen
                    stimmzettel[:, 2] = zweitstimmen     
                    break                                          
            except Exception as error:
                print(error)
                pass      
    return stimmzettel     
            

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

#WahlkreisStimmenGenerator(1)

"""
hostname = 'localhost'
database = 'postgres'
username = 'postgres'
pwd = ''
port_id = 5432

conn = None
cur = None

try:
    conn = psycopg2.connect(
        host=hostname,
        dbname=database,
        user=username,
        password=pwd,
        port=port_id)
    cur = conn.cursor()
    
        
    allStimmzettel = np.empty([])
    for i in range(1,300):
        arr = np.append(allStimmzettel, WahlkreisStimmenGenerator(i))

    DF = pd.DataFrame(WahlkreisStimmenGenerator(i))        
    DF.to_csv("stimmzettel.csv")
    
    cur.execute("COPY Stimmzettel FROM %s WITH (FORMAT csv)", "stimmzettel.csv")


    # cur.execute - execute SQL queries

    conn.commit()
except Exception as error:
    print(error)
finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()
"""
