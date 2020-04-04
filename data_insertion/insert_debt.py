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
    try:
        total_debt = int(input("total debt:\n"))
    except ValueError:
        total_debt = None 
    if total_debt != None:      
        try:
            equity = float(input("total equity:\n"))
            debt_equity = round(total_debt / equity, 2) 
        except ValueError:
            try:
                debt_equity = float(input("debt/equity ratio:\n"))
            except ValueError:
                debt_equity = None
    try:
        current_assets = float(input("current assets:\n"))
        current_lia = float(input("current liabilities:\n"))
        current_ratio = round(current_assets / current_lia, 2)
    except ValueError:
        try:
            current_ratio = float(input("current ratio:\n"))
        except ValueError:
            current_ratio = None    
    date = input("date of the balance sheet you get the assets, liabilities and equity from (yyyy/mm/dd):\n")
    
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