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

## checking existence
company = input("what company do you want to check if it's in the database?\n")
ticker = input("what's the ticker of the company?\n")
try:
    cur.execute('''
    SELECT "name" FROM companies WHERE "name" = %s''', (company,))
    name = cur.fetchone()[0]
    print(f'\nthe company {name} is in the database')
except TypeError:
    print("\nthat company name is not in the database")
    try:
        cur.execute('''
        SELECT "ticker", companies_id FROM shares WHERE "ticker" = %s''', (ticker,))
        info = cur.fetchall()[0]
        ticker = info[0]
        companies_id = info[1]
        cur.execute('''
        SELECT "name" FROM companies WHERE id = %s''', (companies_id,))
        company = cur.fetchone()[0]
        print(f'\nticker {ticker} is related to the company {company}')
    except:
        print("\nthat ticker is not related to any company in the database")


## save the data in the database


## close the connection
cur.close()
conn.close()