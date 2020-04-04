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
        current_assets = int(input("current assets:\n"))
    except ValueError:
        current_assets = None
    try:
        tangible_assets = int(input("tangible assets:\n"))
    except ValueError:
        tangible_assets = None
    try:
        total_assets = int(input("total assets:\n"))
    except ValueError:
        total_assets = None
    try:
        current_lia = int(input("current liabilities:\n"))
    except ValueError:
        current_lia = None
    try:
        total_lia = int(input("total liabilities:\n"))
    except ValueError:
        total_lia = None
    try:   
        total_equity = total_assets - total_lia
    except TypeError:
        try:
            total_equity = int(input("total equity:\n"))
        except ValueError:
            total_equity = None

    date = input("date of the balance sheet(yyyy/mm/dd):\n")
    
    print(
        "are you sure you want to add these values to the database?\n",
        "company:",company,"\n",
        "current assets",current_assets,"\n",
	    "tangible assets",tangible_assets,"\n",
	    "total assets",total_assets,"\n",
	    "current liabilities",current_lia,"\n",
	    "total liabilities",total_lia,"\n",
	    "total equity",total_equity,"\n",
        "date:",date,"\n",
    )
    answer = input("(y/n)\n")
    
    if answer == 'y':
        if date == '':
            cur.execute ('''
            INSERT INTO balance_sheets ("current assets", "tangible assets", "total assets", 
            "current liabilities", "total liabilities", "total equity", companies_id) 
            VALUES (%s, %s, %s, %s, %s, %s, %s);
            ''', (current_assets, tangible_assets, total_assets, current_lia, total_lia, total_equity, companies_id,))
            break
        else:
            cur.execute ('''
            INSERT INTO balance_sheets ("current assets", "tangible assets", "total assets", 
            "current liabilities", "total liabilities", "total equity", "date", companies_id) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            ''', (current_assets, tangible_assets, total_assets, current_lia, total_lia, total_equity, date, companies_id,))
            break
    else:
        continue

## save the data in the database
conn.commit()

## close the connection
cur.close()
conn.close()

print('done')