from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient import discovery
import psycopg2

def insert_to_db(spreadsheet_id,range_):

    ## getting permision to connect to sheets (oauth)
    scope = 'https://www.googleapis.com/auth/spreadsheets.readonly'

    creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)

    ## conecting to the api
    service = discovery.build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    ## getting the values from the sheet
    data = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_).execute()
    values = data['values']

    index = 0
    for item in values:
        ## variable index is used to ignore the title of the columns 
        if index == 0:
            index += 1
            continue
        try:    
            company = item[0].lower()
        except:
            company = None
        try:
            ticker = item[13].lower()
        except:
            ticker = None
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
            print(f'\nticker {ticker} is related to the company {company_in_db}')
            continue
        except:
            pass
        try:
            net_income = int(item[1])
        except:
            net_income = None
        try:
            income_date = item[2]
        except:
            income_date = None
        try:
            current_assets = int(item[3])
        except:
            current_assets = None
        try:    
            tangible_assets = int(item[4])
        except:
            tangible_assets = None
        try:
            total_assets = int(item[5])
        except:
            total_assets = None
        try:
            current_lia = int(item[6])
        except:
            current_lia = None
        try:
            total_lia = int(item[7])
        except:
            total_lia = None
        try:    
            total_equity = int(item[8])
        except:
            total_equity = None
        try:
            sheet_date = item[9]
        except:
            sheet_date = None
        try:
            shares = int(item[10])
        except:
            shares = None
        try:
            value = int(item[11])
        except:
            value = None
        try:
            total_debt = int(item[12])
        except:
            total_debt = None
        try:
            price = float(item[14])
        except:
            price = None
        try:
            exchange = item[15].lower()
        except:
            exchange = None
        try:
            forward_rate = float(item[16])
        except:
            forward_rate = None
        try:
            forward_yield = float(item[17])
        except:
            forward_yield = None
        try:
            trailing_rate = float(item[18])
        except:
            trailing_rate = None
        try:
            trailing_yield = float(item[19])
        except:
            trailing_yield = None
        try:
            average = float(item[20])
        except:
            average = None
        try:
            date = item[21]
        except:
            date = None
        try:
            price_currency = item[22].lower()
        except:
            price_currency = None
        try:
            financials_currency = item[23].lower()
        except:
            financials_currency = None
        try:
            debt_equity = round(total_debt / total_equity, 2) 
        except TypeError:
            debt_equity = None
        try:
            current_ratio = round(current_assets / current_lia, 2)
        except TypeError:
            current_ratio = None
        try:
            eps = round(net_income / shares, 2)
        except TypeError:
            eps = None
        try:
            pe = round(price / eps, 2)
        except TypeError:
            pe = None    
        try:
            book_value = round(total_equity / shares, 2)
        except TypeError:
            book_value = None

        ## insert companies
        if date == '':
            cur.execute ('''
            INSERT INTO companies ("name", "total market value", "shares outstanding", "currency") VALUES (%s, %s, %s, %s);
            ''', (company, value, shares, price_currency,))
        else:
            cur.execute ('''
            INSERT INTO companies ("name", "total market value", "shares outstanding", "last update", "currency") VALUES (%s, %s, %s, %s, %s);
            ''', (company, value, shares, date, price_currency,))

        ## save the data in the database
        conn.commit()
        
        ## register the insertion
        companies_inserted[ticker] = company
        
        ## getting the id of the company
        cur.execute('''
        SELECT id FROM companies WHERE "name" = %s''', (company,))
        companies_id = cur.fetchone()[0]

        ## insert incomes
        if income_date == '':
            cur.execute ('''
            INSERT INTO incomes ("net income", companies_id, "currency") VALUES (%s, %s, %s);
            ''', (net_income, companies_id, financials_currency,))
        else:
            cur.execute ('''
            INSERT INTO incomes ("net income", "date", companies_id, "currency") VALUES (%s, %s, %s, %s);
            ''', (net_income, income_date, companies_id, financials_currency,))

        ## save the data in the database
        conn.commit()    

        ## insert balance_sheets
        if sheet_date == '':
            cur.execute ('''
            INSERT INTO balance_sheets ("current assets", "tangible assets", "total assets", 
            "current liabilities", "total liabilities", "total equity", companies_id, "currency") 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            ''', (current_assets, tangible_assets, total_assets, current_lia, total_lia, total_equity, companies_id, financials_currency,))
        else:
            cur.execute ('''
            INSERT INTO balance_sheets ("current assets", "tangible assets", "total assets", 
            "current liabilities", "total liabilities", "total equity", "date", companies_id, "currency") 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            ''', (current_assets, tangible_assets, total_assets, current_lia, total_lia, total_equity, sheet_date, companies_id, financials_currency,))
        
        ## save the data in the database
        conn.commit()

        ## insert debt
        if sheet_date == '':
            cur.execute ('''
            INSERT INTO debt ("total debt", "debt/equity ratio", "current ratio", companies_id, "currency") VALUES (%s, %s, %s, %s, %s);
            ''', (total_debt, debt_equity, current_ratio, companies_id, financials_currency,))
                    
        else:
            cur.execute ('''
            INSERT INTO debt ("total debt", "debt/equity ratio", "current ratio", "date", companies_id, "currency") VALUES (%s, %s, %s, %s, %s, %s);
            ''', (total_debt, debt_equity, current_ratio, sheet_date, companies_id, financials_currency,))

        ## save the data in the database
        conn.commit()

        ## insert shares
        if date == '':
            cur.execute ('''
            INSERT INTO shares ("ticker", "PE", "EPS", "book value", "exchange", "price", companies_id, "currency") 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            ''', (ticker, pe, eps, book_value, exchange, price, companies_id, price_currency,))
        else:
            cur.execute ('''
            INSERT INTO shares ("ticker", "PE", "EPS", "book value", "exchange", "price", "date", companies_id, "currency") 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            ''', (ticker, pe, eps, book_value, exchange, price, date, companies_id, price_currency,))

        ## save the data in the database
        conn.commit()

        ## insert dividends
        if date == '':
            cur.execute ('''
            INSERT INTO dividends ("trailing rate", "forward rate", "trailing yield", "forward yield", "5 year average yield", companies_id) VALUES (%s, %s, %s, %s, %s, %s);
            ''', (trailing_rate, forward_rate, trailing_yield, forward_yield, average, companies_id,))
                    
        else:
            cur.execute ('''
            INSERT INTO dividends ("trailing rate", "forward rate", "trailing yield", "forward yield", "5 year average yield", "date", companies_id) VALUES (%s, %s, %s, %s, %s, %s, %s);
            ''', (trailing_rate, forward_rate, trailing_yield, forward_yield, average, date, companies_id,))

        ## save the data in the database
        conn.commit()

    print(len(companies_inserted),"companies inserted")

def update_sheet_inside(spreadsheet_id,range_):
    ## adding the new additions to the worksheet 'already inside'
    scope = 'https://www.googleapis.com/auth/spreadsheets'

    creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)

    service = discovery.build('sheets', 'v4', credentials=creds)
    
    values_append = [[v,k] for k,v in companies_inserted.items()]
    value_input_option = 'USER_ENTERED'
    insert_data_option = 'INSERT_ROWS'
    value_range_body = {
    "range": range_,
    "majorDimension": 'ROWS',
    "values": values_append
    }

    sheet = service.spreadsheets()
    request = sheet.values().append(spreadsheetId=spreadsheet_id, range=range_, valueInputOption=value_input_option, insertDataOption=insert_data_option, body=value_range_body)
    response = request.execute()

    print('worksheet already inside updated')

def clear_sheet_upcoming(spreadsheet_id,range_):
    ## clear the worksheet 'upcoming additions'
    scope = 'https://www.googleapis.com/auth/spreadsheets'

    creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)

    service = discovery.build('sheets', 'v4', credentials=creds)

    clear_values_request_body = {}

    sheet = service.spreadsheets()
    request = sheet.values().clear(spreadsheetId=spreadsheet_id, range=range_, body=clear_values_request_body)
    response = request.execute()

    value_input_option = 'USER_ENTERED'
    insert_data_option = 'INSERT_ROWS'
    value_range_body = {
    "range": range_,
    "majorDimension": 'ROWS',
    "values": [
        ['company','net income','income stament date','current assets','tangible assets','total assets',
        'current liabilities','total liabilities','total equity','balance sheet date','shares outstanding',
        'market cap','total debt','ticker','price','exchange','forward rate','forward yield','trailing rate',
        'trailing yield','5 year average','current date','price currency','financials currency']
    ]
    }

    sheet = service.spreadsheets()
    request = sheet.values().append(spreadsheetId=spreadsheet_id, range=range_, valueInputOption=value_input_option, insertDataOption=insert_data_option, body=value_range_body)
    response = request.execute()

if __name__ == '__main__':
    ## this dict is created to append the companies inserted in the database to the worksheet 'already inside'
    companies_inserted = {}
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
    
    ## insert the data
    insert_to_db('13WhjYprLaLRhj1uhxfWGyv3lb0zRx_LmCtSJE-1SsQQ','upcoming additions')

    ## close the connection to the database
    cur.close()
    conn.close()

    update_sheet_inside('13WhjYprLaLRhj1uhxfWGyv3lb0zRx_LmCtSJE-1SsQQ', 'already inside')
    clear_sheet_upcoming('13WhjYprLaLRhj1uhxfWGyv3lb0zRx_LmCtSJE-1SsQQ', 'upcoming additions')
