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
company = input("what company do you want to check if it's in the database?\n").lower()
ticker = input("what's the ticker of the company?\n").lower()

try:
    cur.execute('''
    SELECT "name" FROM companies WHERE "name" = %s ''', (company,))
    name = cur.fetchone()[0]
    print(f'\nthe company {name} is in the database')
except TypeError:
    print("\nthat company name is not in the database")
    try:
        cur.execute('''
        SELECT s."ticker", c."name" FROM shares AS s JOIN companies AS c ON s.companies_id = c.id WHERE "ticker" = %s''', (ticker,))
        info = cur.fetchall()[0]
        ticker = info[0]
        company_in_db = info[1]
        print(f'\nticker {ticker} is related to the company {company_in_db}')
    except:
        print("\nthat ticker is not related to any company in the database")


## close the connection
cur.close()
conn.close()