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
name = input("what is the company you want to register:\n")
shares = input("shares outstanding:\n")
value = input("total assets\n")
update = input("date of the balance sheet you get the total assets from (yyyy/mm/dd):\n")

cur.execute ('''
INSERT INTO companies (name, "total market value", "shares outstanding", last_update) VALUES (%s, %s, %s, %s);
''', (name, int(value), int(shares), update,))


## save the data in the database
conn.commit()

## close the connection
cur.close()
conn.close()

print('done')