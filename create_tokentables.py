from hashlib import sha256
import random
import sys


try:
    import psycopg2
except ImportError:
    import pip
    pip.main(['install', '--user', 'psycopg2'])
    import psycopg2


# Adnans local test db:
"""
db_host = "localhost"
db_port = 5432
db_name = "wahl"
db_user = "postgres"
db_password = ""


# Inkens local test db:
db_host = "localhost"
db_port = 5432
db_name = "postgres"
db_user = "newuser"
db_password = "pw"
"""

db_host = sys.argv[1]
db_port = sys.argv[2]
db_name = sys.argv[3]
db_user = sys.argv[4]
db_password = sys.argv[5]


try:
    sql_con = psycopg2.connect(
        host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
    cur = sql_con.cursor()
    print("Success")
except:
    print("Fail")

# create table for tokenrange for wahlkreise
create_tokenrangetable_query = """
DROP TABLE IF EXISTS tokenrange;
CREATE TABLE tokenrange (
	Wahlkreis int primary key,
	TokenRangeMin bigint NOT NULL,
    TokenRangeMax bigint NOT NULL,
	FOREIGN KEY (wahlkreis) REFERENCES wahlkreis ON DELETE CASCADE
);
"""

cur.execute(create_tokenrangetable_query)
sql_con.commit()


# fill tokenrange table
tokenmin = 0
tokenrange = 10_000_000_000
for i in range(1, 300):
    fill_tokenrangetable_query = """
    INSERT INTO tokenrange 
    VALUES ({}, {}, {})
    """.format(i, tokenmin, tokenmin + tokenrange - 1)
    cur.execute(fill_tokenrangetable_query)
    tokenmin += tokenrange


# create table for admintokens, one for each wahlkreis
# TODO: enumeration for tokens in admin_tokens.txt
create_tokenrangetable_query = """
DROP TABLE IF EXISTS adminTokens;
CREATE TABLE adminTokens (
    token char(64) primary key,
	wahlkreis int NOT NULL REFERENCES wahlkreis ON DELETE CASCADE
);
"""

cur.execute(create_tokenrangetable_query)
sql_con.commit()

# fill admintokens table
tokenmin = 1_000_000_000_000_000
tokenmax = 9_999_999_999_999_999
admintoken_list = []
for i in range(1, 300):
    cur_token = random.randint(tokenmin, tokenmax)
    admintoken_list.append(cur_token)
    hashed_token = sha256(cur_token.to_bytes(
        8, 'big', signed=False)).hexdigest()
    fill_tokenrangetable_query = """
    INSERT INTO adminTokens 
    VALUES ('{}', {})
    """.format(hashed_token, i)
    cur.execute(fill_tokenrangetable_query)

file = open('admin_tokens.txt', 'w')
for admin_token in admintoken_list:
    file.write(str(admin_token)+"\n")
file.close()


create_dynamic_tokentable_query = """
DROP TABLE IF EXISTS tokens;
CREATE TABLE tokens (
	token char(64) primary key,
	wahlkreis int NOT NULL REFERENCES wahlkreis ON DELETE CASCADE
);
CREATE INDEX tokens_hash_idx ON tokens USING hash(token);
"""
cur.execute(create_dynamic_tokentable_query)
sql_con.commit()

sql_con.commit()
sql_con.close()
