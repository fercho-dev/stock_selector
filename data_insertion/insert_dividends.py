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
    while True:
        company = input("what company do you want to register:\n")
        try:
            cur.execute('''
            SELECT id FROM companies WHERE "name" = %s''', (company,))
            companies_id = cur.fetchone()[0]
            break
        except TypeError:
            print("the company is not in the companies table\n")
            continue

    trailing_rate = float(input("trailing rate:\n"))
    forward_rate = float(input("forward rate:\n"))
    trailing_yield = float(input("trailing yield:\n"))
    forward_yield = float(input("forward yield:\n"))
    average = float(input("5 year average yield:\n"))
    date = input("date (yyyy/mm/dd):\n")
    
    print(
        "are you sure you want to add these values to the database?\n",
        "company:",company,"\n",
        "trailing rate",trailing_rate,"\n",
	    "forward rate",forward_rate,"\n",
	    "trailing yield",trailing_yield,"\n",
        "forward yield",forward_yield,"\n",
        "5 year average yield",average,"\n"
        "date:",date,"\n",
    )
    answer = input("(y/n)\n")
    
    if answer == 'y':
        if date == '':
            cur.execute ('''
            INSERT INTO dividends ("trailing rate", "forward rate", "trailing yield", "forward yield", "5 year average yield", companies_id) VALUES (%s, %s, %s, %s, %s, %s);
            ''', (trailing_rate, forward_rate, trailing_yield, forward_yield, average, companies_id,))
            break
        else:
            cur.execute ('''
            INSERT INTO dividends ("trailing rate", "forward rate", "trailing yield", "forward yield", "5 year average yield" "date", companies_id) VALUES (%s, %s, %s, %s, %s, %s, %s);
            ''', (trailing_rate, forward_rate, trailing_yield, forward_yield, average, date, companies_id,))
            break
    else:
        continue

## save the data in the database
conn.commit()

## close the connection
cur.close()
conn.close()

print('done')