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
company = input("what company do you want to register:\n")
ticker = input("ticker:\n")
pe = float(input("PE ratio:\n"))
eps = float(input("EPS ratio:\n"))
book_value = float(input("book value:\n"))
exchange = input("exchange:\n")
price = float(input("price:\n"))
date = input("date (yyyy/mm/dd):\n")
cur.execute('''
SELECT id FROM companies WHERE name = %s''', (company,))
companies_id = cur.fetchone()[0]

if date == '':
    cur.execute ('''
    INSERT INTO shares (ticker, PE, EPS, "book value", exchange, price, companies_id) VALUES (%s, %s, %s, %s, %s, %s, %s);
    ''', (ticker, pe, eps, book_value, exchange, price, companies_id,))
else:
    cur.execute ('''
    INSERT INTO shares (ticker, PE, EPS, "book value", exchange, price, "date", companies_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    ''', (ticker, pe, eps, book_value, exchange, price, date, companies_id,))

## save the data in the database
conn.commit()

## close the connection
cur.close()
conn.close()

print('done')