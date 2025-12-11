import psycopg2

conn = psycopg2.connect(
    dbname="pudge_learning",
    user="postgres",
    password="Ramil2007",
    host="localhost",
    port="5432"
)

conn.autocommit = True

def get_cursor():
    return conn.cursor()
