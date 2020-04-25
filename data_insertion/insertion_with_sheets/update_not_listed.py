from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient import discovery
import re

## this function reads a sheet we get companies from and erase the ones that are already in database
def update(spreadsheet_id,range_):
    ## here we make sure we get authorize
    scope = 'https://www.googleapis.com/auth/spreadsheets'

    creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)

    service = discovery.build('sheets', 'v4', credentials=creds)
    
    ## here we read the sheet an extract the tickers and remember the row of each ticker
    sheet = service.spreadsheets()
    data = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_).execute()
    values = data['values']
    ticker_row = {}
    row = 1
    for item in values:
        if item == [] or row < 6:
            row += 1
            continue
        else:
            ticker = re.findall('\((.*)\)', item[0])
            ticker = ticker[0].lower().strip()
            ticker_row[ticker] = row
            row += 1
    
    ## here we read the database sheet an look for duplications
    sheet = service.spreadsheets()
    data = sheet.values().get(spreadsheetId='13WhjYprLaLRhj1uhxfWGyv3lb0zRx_LmCtSJE-1SsQQ', range='already inside!B2:B').execute()
    values = data['values']
    duplicates = []
    for item in values:
        if item[0] in ticker_row.keys():
            duplicates.append(item[0])
    
    ## here we clear from the sheet the duplicate companies
    if len(duplicates) > 0:
        clear_values_request_body = {}
        sheet = service.spreadsheets()
        for item in duplicates:
            row  = ticker_row[item]
            rango = create_range(range_, row)
            request = sheet.values().clear(spreadsheetId=spreadsheet_id, range=rango, body=clear_values_request_body)
            response = request.execute()

## this function creates the range in A1 notation that we want to clear
def create_range(ws,row):
    rango = ws + '!' + str(row) + ':' + str(row)
    return rango


if __name__ == '__main__':
    update('1-HrOewpbw18vLR1FQP6gIiiz93xGEIQp8S0zz_s8PqE','hoja 1')
    update('19bPfrz5HjDYpfVwbMtNi1I47qSgVaGkkZ4UcZLKbCpE','hoja 1')
    update('1bgAaxpni_rFz9sZgojDXODe7pNFlUzAhdtLWTLmhgrk','hoja 1')
    update('1R0h3A6cmfqbCV7788cLK3DdyRirREs8KbHxppulbf98','hoja 1')
    
