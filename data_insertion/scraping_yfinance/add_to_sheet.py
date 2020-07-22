from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient import discovery
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import requests
from bs4 import BeautifulSoup
import time
import datetime
import re
from scraper import Scraper
import argparse

def main(ticker):
    scraper = init_scraper(ticker)
    head = get_header(scraper)
    stats = get_stats(scraper)
    financials = get_financials(scraper)
    close(scraper)
    send_to_sheet(head, stats, financials)

def init_scraper(ticker):
    print('generating scraper')
    scraper = Scraper(ticker)
    return scraper

def get_header(scraper):
    print('obtaining header data')
    head = scraper.get_header_data()
    return head

def get_stats(scraper):
    print('obtaining statistics')
    stats = scraper.get_statistics_data()
    return stats
    
def get_financials(scraper):
    print('obtaining financials')    
    financials = scraper.get_financials_data()
    return financials

def close(scraper):
    print('closing scraper')
    scraper.close()

def send_to_sheet(head, stats, financials):
    print('generating variables to send to the google sheet')
    ## creating the variables
    try:
        company = head['company']
        net_income = financials['income']
        income_date = financials['income_date']
        current_assets = financials['current_assets']
        tangible_assets = financials['tangible_assets']
        total_assets = financials['total_assets']
        current_lia = financials['current_lia']
        total_lia = financials['total_lia']
        total_equity = financials['total_equity']
        sheet_date = financials['sheet_date']
        shares = stats['shares']
        try:
            value = str(int(float(head['price']) * int(stats['shares'])))
        except:
            value = ''
        total_debt = stats['debt']
        ticker = head['ticker']
        price = head['price']
        exchange = head['exchange']
        forward_rate = stats['forward_rate']
        forward_yield = stats['forward_yield']
        trailing_rate = stats['trailing_rate']
        trailing_yield = stats['trailing_yield']
        average = stats['average']
        current_date = datetime.datetime.now().strftime('%Y/%m/%d')
        price_currency = head['price_currency']
        if financials['financials_currency'] == '':
            financials_currency = head['price_currency']
        else:
            financials_currency = financials['financials_currency']
        info = True

    except:
        info = False

    ## conecting and adding values in sheet
    print('sending data to google sheet')
    if info == True:
        scope = 'https://www.googleapis.com/auth/spreadsheets'

        creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)

        service = discovery.build('sheets', 'v4', credentials=creds)

        spreadsheet_id = '13WhjYprLaLRhj1uhxfWGyv3lb0zRx_LmCtSJE-1SsQQ'

        range_ = 'upcoming additions'

        value_input_option = 'USER_ENTERED'
        insert_data_option = 'INSERT_ROWS'
        value_range_body = {
        "range": 'upcoming additions',
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

        print(company, 'added to upcoming additions')

    else:
        print(company, 'was not added')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('ticker',
                        help='the ticker you are looking for',
                        type=str)
    args = parser.parse_args()

    main(args.ticker)
    