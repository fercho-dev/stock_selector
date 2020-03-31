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
    while True:
        company = input("what company do you want to register:\n")
        try:
            cur.execute('''
            SELECT id FROM companies WHERE name = %s''', (company,))
            companies_id = cur.fetchone()[0]
            break
        except TypeError:
            print("the company is not in the companies table\n")
            continue

    ticker = input("ticker:\n")
    pe = float(input("PE ratio:\n"))
    eps = float(input("EPS ratio:\n"))
    book_value = float(input("book value:\n"))
    exchange = input("exchange:\n")
    price = float(input("price:\n"))
    date = input("date (yyyy/mm/dd):\n")
    
    print(
        "are you sure you want to add these values to the database?\n",
        "company:",company,"\n",
        "ticker:",ticker,"\n",
        "PE:",pe,"\n",
        "EPS:",eps,"\n",
        "book value:",book_value,"\n",
        "exchange:",exchange,"\n",
        "price:",price,"\n",
        "date:",date,"\n",
    )
    answer = input("(y/n)\n")
    
    if answer == 'y':
        if date == '':
            cur.execute ('''
            INSERT INTO shares (ticker, PE, EPS, "book value", exchange, price, companies_id) VALUES (%s, %s, %s, %s, %s, %s, %s);
            ''', (ticker, pe, eps, book_value, exchange, price, companies_id,))
            break
        else:
            cur.execute ('''
            INSERT INTO shares (ticker, PE, EPS, "book value", exchange, price, "date", companies_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            ''', (ticker, pe, eps, book_value, exchange, price, date, companies_id,))
            break
    else:
        continue

## save the data in the database
conn.commit()

## close the connection
cur.close()
conn.close()

print('done')