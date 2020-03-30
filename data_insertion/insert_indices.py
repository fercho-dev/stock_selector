import psycopg2

## connect to the db
host = "localhost"
db = "conection_test"
user = "postgres"
pw = "123"

conn = psycopg2.connect(
    host = host,
    database = db,
    user = user,
    password = pw)

cur = conn.cursor()

## insert data
name = input("what is the index you want to register:\n")

cur.execute ('''
INSERT INTO indices (name) VALUES (%s);
''', (name,))

## save the data in the database
conn.commit()

## close the connection
cur.close()
conn.close()

print('done')