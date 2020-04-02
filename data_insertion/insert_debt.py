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

    total_debt = int(input("total debt:\n"))
    debt_equity = float(input("debt/equity ratio:\n"))
    try:
        current_ratio = float(input("current ratio:\n"))
    except ValueError:
        current_ratio = None
    date = input("date (yyyy/mm/dd):\n")
    
    print(
        "are you sure you want to add these values to the database?\n",
        "company:",company,"\n",
        "total debt",total_debt,"\n",
        "debt/equity ratio",debt_equity,"\n",
        "current ratio",current_ratio,"\n",
        "date:",date,"\n",
    )
    answer = input("(y/n)\n")
    
    if answer == 'y':
        if date == '':
            cur.execute ('''
            INSERT INTO debt ("total debt", "debt/equity ratio", "current ratio", companies_id) VALUES (%s, %s, %s, %s);
            ''', (total_debt, debt_equity, current_ratio, companies_id,))
            break
        else:
            cur.execute ('''
            INSERT INTO debt ("total debt", "debt/equity ratio", "current ratio", "date", companies_id) VALUES (%s, %s, %s, %s, %s);
            ''', (total_debt, debt_equity, current_ratio, date, companies_id,))
            break
    else:
        continue

## save the data in the database
conn.commit()

## close the connection
cur.close()
conn.close()

print('done')