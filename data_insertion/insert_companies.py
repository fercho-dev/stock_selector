import psycopg2

## connect to the db
host = "192.168.0.9"
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
    company = input("what company do you want to register:\n")

    cur.execute('''
        SELECT "name" FROM companies WHERE "name" = %s''', (company,))
    try:
        duplicate = cur.fetchone()[0]
        print("this company is already on the database")
        continue
    except TypeError:
        pass

    shares = int(input("shares outstanding:\n"))
    try:
        value = int(input("market cap:\n"))
    except ValueError:
        value = int(input("price:\n")) * shares
    update = input("date (yyyy/mm/dd):\n")
    
    print("are you sure you want to add these values to the database?\n",
    "company:",company,"\n",
    "shares outstanding",shares,"\n",
    "market value:",value,"\n")
    answer = input("(y/n)\n")

    if answer == 'y':
        if update == '':
            cur.execute ('''
            INSERT INTO companies ("name", "total market value", "shares outstanding") VALUES (%s, %s, %s);
            ''', (company, value, shares,))
            break
        else:
            cur.execute ('''
            INSERT INTO companies ("name", "total market value", "shares outstanding", "last_update") VALUES (%s, %s, %s, %s);
            ''', (company, value, shares, update,))
            break
    else:
        continue

## save the data in the database
conn.commit()

## close the connection
cur.close()
conn.close()

print('done')