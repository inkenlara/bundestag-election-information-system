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


tokenmin = 0
tokenrange = 10_000_000_000
for i in range(1, 300):
    fill_tokenrangetable_query = """
    INSERT INTO tokenrange 
    VALUES ({}, {}, {})
    """.format(i, tokenmin, tokenmin + tokenrange - 1)
    cur.execute(fill_tokenrangetable_query)
    tokenmin += tokenrange


create_dynamic_tokentable_query = """
DROP TABLE IF EXISTS tokens;
CREATE TABLE tokens (
	token bigint primary key,
	wahlkreis int NOT NULL REFERENCES wahlkreis ON DELETE CASCADE
);
CREATE INDEX tokens_hash_idx ON tokens USING hash(token);
"""
cur.execute(create_dynamic_tokentable_query)
sql_con.commit()

sql_con.commit()
sql_con.close()
