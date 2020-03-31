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
    name = input("what company you want to register:\n")
    shares = int(input("shares outstanding:\n"))
    value = int(input("total assets:\n"))
    update = input("date of the balance sheet you get the total assets from (yyyy/mm/dd):\n")
    
    print("are you sure you want to add these values to the database?\n",
    "company:",name,"\n",
    "shares outstanding",shares,"\n",
    "market value:",value,"\n")
    answer = input("(y/n)\n")

    if answer == 'y':
        if update == '':
            cur.execute ('''
            INSERT INTO companies (name, "total market value", "shares outstanding") VALUES (%s, %s, %s);
            ''', (name, value, shares,))
            break
        else:
            cur.execute ('''
            INSERT INTO companies (name, "total market value", "shares outstanding", last_update) VALUES (%s, %s, %s, %s);
            ''', (name, value, shares, update,))
            break
    else:
        continue

## save the data in the database
conn.commit()

## close the connection
cur.close()
conn.close()

print('done')