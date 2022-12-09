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
import matplotlib.pyplot as plt
import numpy as np
import query_api

db_host = "localhost"
db_port = 5432
db_name = "wahl"
db_user = "postgres"
db_password = ""

# Inkens local test db:
"""db_host = "localhost"
db_port = 5432
db_name = "postgres"
db_user = "newuser"
db_password = "pw"
"""






