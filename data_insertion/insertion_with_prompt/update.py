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

## updating the company
while True:
    company = input("what company do you want to update?\n")
    try:
        ## getting the id of the company
        cur.execute('''
        SELECT id FROM companies WHERE "name" = %s''', (company,))
        companies_id = cur.fetchone()[0]
    except TypeError:
        print("that company is not in the database\n")
        continue
    
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
            UPDATE companies SET "total market value" = %s, "shares outstanding" = %s WHERE id = %s;
            ''', (value, shares, companies_id,))
            break
        else:
            cur.execute ('''
            UPDATE companies SET "total market value" = %s, "shares outstanding" = %s, "last update" = %s WHERE id = %s;
            ''', (value, shares, update, companies_id,))
            break
    else:
        continue

## save the data in the database
conn.commit()
print("company updated\n")

## insert incomes
answer = input("do you want to register an income?\n(y/n)\n")
if answer == 'y':
    while True:
        net_income = int(input("net income:\n"))
        date = input("date of the income stament you get the net income from (yyyy/mm/dd):\n")
    
        print(
            "are you sure you want to add these values to the database?\n",
            "company:",company,"\n",
            "net income:",net_income,"\n",
            "date:",date,"\n"
        )
        answer = input("(y/n)\n")
    
        if answer == 'y':
            if date == '':
                cur.execute ('''
                INSERT INTO incomes ("net income", companies_id) VALUES (%s, %s);
                ''', (net_income, companies_id,))
                break
            else:
                cur.execute ('''
                INSERT INTO incomes ("net income", "date", companies_id) VALUES (%s, %s, %s);
                ''', (net_income, date, companies_id,))
                break
        else:
            continue

    ## save the data in the database
    conn.commit()
    print("income inserted\n")
else:
    print("income not inserted\n")

## insert balance_sheets
answer = input("do you want to register a balance sheet?\n(y/n)\n")
if answer == 'y':
    while True:        
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
            total_equity = int(input("total equity:\n"))
        except ValueError:
            try:
                total_equity = total_assets - total_lia
            except TypeError:
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
    print("balance sheet inserted\n")
else:
    print("balance sheet not inserted\n")

## insert debt
answer = input("do you want to register debt?\n(y/n)\n")
if answer == 'y':
    while True:          
        try:
            total_debt = int(input("total debt:\n"))
        except ValueError:
            total_debt = None 
        if total_debt != None:      
            try:
                debt_equity = round(total_debt / total_equity, 2) 
            except TypeError:
                try:
                    debt_equity = float(input("debt/equity ratio:\n"))
                except ValueError:
                    debt_equity = None
        try:
            current_ratio = round(current_assets / current_lia, 2)
        except TypeError:
            try:
                current_ratio = float(input("current ratio:\n"))
            except ValueError:
                current_ratio = None
    
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
    print("debt inserted\n")
else:
    print("debt not inserted\n")

## insert shares
answer = input("do you want to register a share?\n(y/n)\n")
if answer == 'y':
    while True:
        ticker = input("ticker:\n")
        price = float(input("price:\n"))
        try:
            eps = round(net_income / shares, 2)
        except TypeError: 
            try:    
                eps = float(input("EPS ratio:\n"))
            except ValueError:
                eps = None
        try:
            pe = round(price / eps, 2)
        except TypeError:
            try:
                pe = float(input("PE ratio:\n"))
            except ValueError:
                pe = None    
        try:
            book_value = round(total_equity / shares, 2)
        except TypeError:
            try:    
                book_value = float(input("book value:\n"))
            except ValueError:
                book_value = None
        exchange = input("exchange:\n")
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
                INSERT INTO shares ("ticker", "PE", "EPS", "book value", "exchange", "price", companies_id) 
                VALUES (%s, %s, %s, %s, %s, %s, %s);
                ''', (ticker, pe, eps, book_value, exchange, price, companies_id,))
                break
            else:
                cur.execute ('''
                INSERT INTO shares ("ticker", "PE", "EPS", "book value", "exchange", "price", "date", companies_id) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                ''', (ticker, pe, eps, book_value, exchange, price, date, companies_id,))
                break
        else:
            continue

    ## save the data in the database
    conn.commit()
    print("share inserted\n")
else:
    print("share not inserted\n")

## insert dividends
answer = input("do you want to register dividends?\n(y/n)\n")
if answer == 'y':
    while True:
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
    print("dividends inserted\n")
else:
    print("dividends not inserted\n")

## close the connection
cur.close()
conn.close()

print('done')