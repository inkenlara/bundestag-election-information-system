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
    
    
hostname = 'localhost'
database = 'postgres'
username = 'postgres'
pwd = ''
port_id = 5432

conn = None
cur = None

try:
    conn = psycopg2.connect(host = hostname, port = port_id, database = database, user = username, password = pwd)
    cur = conn.cursor()
    print("Success")
except:
    print("Fail")
    

path_kands_2017 = "csvs/kandidaten2017.csv"
path_kands_2021 = "csvs/btw21_kandidaturen_utf8.csv"
path_kerg = "csvs/kerg.csv"
path_kerg2 = "csvs/kerg2.csv"
path_kandidaturen = "csvs/kandidaturen.csv"


#loads kandidaten, direkt- und listenkandidaten for year 2021
def Kandidaten():
    with open(path_kerg, encoding='utf-8') as f: 
        csv_buffer = csv.reader(f, delimiter=';', quotechar='"')
        next(csv_buffer)
        next(csv_buffer)
        csv_list = list(csv_buffer)
        
        partei_namen = []
        for k in range(19, len(csv_list[0]) - 3, 4):    # 48 total
            partei_namen.append(csv_list[0][k])
            
        
    with open(path_kands_2021, encoding='utf-8') as f:
        csv_buffer = csv.reader(f, delimiter=';', quotechar='"')

        
        for i in range(9):
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
                kandidaten.append((id, vorname, nachname, beruf, partei, wahljahr))
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
                    kandidaten.append((id, vorname, nachname, beruf, partei, wahljahr))
                    listen[(partei, bundesland, platz)] = id
                    
    cur.executemany('INSERT INTO Kandidaten VALUES(%s, %s, %s, %s, %s, %s)', kandidaten)
    cur.executemany('INSERT INTO Direktkandidaten VALUES(%s, %s)', direkt)
    
    for kandidat in listen:
        bundesland =  kandidat[1]
        platz = kandidat[2]
        id = listen[kandidat]
        cur.execute('INSERT INTO Listenkandidaten VALUES(%s, %s, %s)', (id, bundesland, platz))
        
                
    
#Kandidaten()
            
conn.commit()              
cur.close()
conn.close()          
                    
                    
            
                
            
            
            