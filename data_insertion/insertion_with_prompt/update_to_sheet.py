from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient import discovery
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

while True:
    ## getting the variables
    company = input("what company do you want to register:\n").lower()
    ticker = input("ticker:\n").lower()
    ## checking if company already exists in database 
    try:
        cur.execute('''
        SELECT "name" FROM companies WHERE "name" = %s''', (company,))
        duplicate = cur.fetchone()[0]
        print(company, "is already on the database")
        continue
    except TypeError:
        pass
    try:
        cur.execute('''
        SELECT "ticker", companies_id FROM shares WHERE "ticker" = %s''', (ticker,))
        info = cur.fetchall()[0]
        ticker_duplicate = info[0]
        companies_id = info[1]
        cur.execute('''
        SELECT "name" FROM companies WHERE id = %s''', (companies_id,))
        company_in_db = cur.fetchone()[0]
        print(f'\nticker {ticker} is related to company {company_in_db}')
        continue
    except:
        pass
    try:
        net_income = int(input("net income:\n"))
    except ValueError:
        net_income = None
    income_date = input("date of the income stament you get the net income from (yyyy/mm/dd):\n")
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
    sheet_date = input("date of the balance sheet(yyyy/mm/dd):\n")
    shares = int(input("shares outstanding:\n"))
    try:
        value = int(input("market cap:\n"))
    except ValueError:
        value = int(input("price:\n")) * shares
    try:
        total_debt = int(input("total debt:\n"))
    except ValueError:
        total_debt = None
    price = float(input("price:\n"))
    exchange = input("exchange:\n").lower()
    try:
        trailing_rate = float(input("trailing rate:\n"))
    except:
        trailing_rate = None
    try:
        forward_rate = float(input("forward rate:\n"))
    except:
        forward_rate = None
    try:
        trailing_yield = float(input("trailing yield:\n"))
    except:
        trailing_yield = None
    try:
        forward_yield = float(input("forward yield:\n"))
    except:
        forward_yield = None
    try:
        average = float(input("5 year average yield:\n"))
    except:
        average = None
    current_date = input("date (yyyy/mm/dd):\n")
    price_currency = input("price currency:\n").lower()
    financials_currency = input("financial currency:\n").lower()

    ## conecting and adding values in sheet
    scope = 'https://www.googleapis.com/auth/spreadsheets'

    creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)

    service = discovery.build('sheets', 'v4', credentials=creds)

    spreadsheet_id = '13WhjYprLaLRhj1uhxfWGyv3lb0zRx_LmCtSJE-1SsQQ'

    range_ = 'updates'

    value_input_option = 'USER_ENTERED'
    insert_data_option = 'INSERT_ROWS'
    value_range_body = {
      "range": 'updates',
      "majorDimension": 'ROWS',
      "values": [
        [company, net_income, income_date, current_assets, tangible_assets, total_assets,
        current_lia, total_lia, total_equity, sheet_date, shares,
        value, total_debt, ticker, price, exchange, forward_rate, forward_yield, trailing_rate,
        trailing_yield, average, current_date, price_currency, financials_currency]
      ]
    }

    sheet = service.spreadsheets()
    request = sheet.values().append(spreadsheetId=spreadsheet_id, range=range_, valueInputOption=value_input_option, insertDataOption=insert_data_option, body=value_range_body)
    response = request.execute()

    print(company,"added to updates")
    break

## close the connection to the database
cur.close()
conn.close()