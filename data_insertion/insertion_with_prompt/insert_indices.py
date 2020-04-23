import psycopg2

## connect to the db
host = "localhost"
db = "stock_selector_db"
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
    index = input("what index do you want to register?\n")

    cur.execute('''
    SELECT "name" FROM indices WHERE "name" = %s''', (index,))
    try:
        duplicate = cur.fetchone()[0]
        print("this index is already on the database")
        continue
    except TypeError:
        pass

    print("are you sure you want to add this index to the database\n",index)
    answer = input("(y/n)\n")

    if answer == 'y':
        cur.execute ('''
        INSERT INTO indices ("name") VALUES (%s);
        ''', (index,))
        break
    else:
        continue

## save the data in the database
conn.commit()

## close the connection
cur.close()
conn.close()

print('done')