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
while True:
    name = input("what index do you want to register?\n")

    print("are you sure you want to add this index to the database\n",name)
    answer = input("(y/n)\n")

    if answer == 'y':
        cur.execute ('''
        INSERT INTO indices (name) VALUES (%s);
        ''', (name,))
        break
    else:
        continue

## save the data in the database
conn.commit()

## close the connection
cur.close()
conn.close()

print('done')