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

class Scraper():
    def __init__(self, ticker):
        self.__ticker = ticker
        self.__driver = webdriver.Chrome(executable_path='./chromedriver')
        self.__url = self.__search_ticker(self.__ticker)
        self.__html = self.__make_soup(self.__url)
        


    def __search_ticker(self, ticker):
        
        self.__driver.get('https://finance.yahoo.com/')

        try:
            ## making sure the page loaded
            #time.sleep(10)
            delay = 5
            page_loaded = WebDriverWait(self.__driver, delay).until(EC.presence_of_element_located((By.XPATH, '//form[@id="header-search-form"]/input[@id="yfin-usr-qry"]')))
        
            ## searching ticker
            search_box = self.__driver.find_element_by_xpath('//form[@id="header-search-form"]/input       [@id="yfin-usr-qry"]')
            search_box.send_keys(self.__ticker)
            time.sleep(2)
            search_button = self.__driver.find_element_by_xpath('//form[@id="header-search-form"]//button[@id="header-desktop-search-button"]')
            search_button.click()

            ## making sure the page loaded
            #time.sleep(10)
            page_loaded = WebDriverWait(self.__driver, delay).until(EC.presence_of_element_located((By.XPATH, '//div[@id="quote-header-info"]')))

            ## getting url
            url = self.__driver.current_url

            return url
       
        except:
            print('error in search ticker function\n the page took too long to load for ticker', self.__ticker)
            return None

    def __make_soup(self, url):
        if url == None:
            print('error in make soup function unvalid url\n not html for ticker', self.__ticker)
            html = None
            return html
        else:
            ticker_page = requests.get(url)
            html = BeautifulSoup(ticker_page.text, 'html.parser')
            return html
    
    ## header data includes: company, ticker, exchange, price, price_currency 
    def get_header_data(self):
        data = {}
        try:
            header = self.__html.find('div', attrs={'id':'quote-header-info'})
            ## getting company and ticker
            company_ticker = header.find('h1', attrs={'data-reactid':'7'}).get_text().lower()
            #ticker = self.__ticker
            try:
                company = company_ticker.replace(ticker, '').replace('()', '').strip().strip('-').strip()
            except:
                try:
                    company = company_ticker.replace(ticker, '').replace('()', '').strip()
                except:
                    try:
                        company = company_ticker.replace(ticker, '').strip().strip('-').strip()
                    except:
                        company = company_ticker
            
            ## getting exchange and currency
            exchange_pcurrency = header.find('span', attrs={'data-reactid':'9'}).get_text()
            exchange_pcurrency_list = re.split('-', exchange_pcurrency)
            exchange = exchange_pcurrency_list[0].strip().lower()
            price_list = re.split('in', exchange_pcurrency_list[1])
            price_currency = price_list[1].strip().lower()
            
            ## getting price
            price_box_opt = header.find_all('div')
            spans = price_box_opt[8].find_all('span')
            price = spans[0].get_text()
            price = price.replace(',','')
            
            ## adding info to dict data
            try:
                data['company'] = company
            except NameError:
                data['company'] = ''
            data['ticker'] = self.__ticker
            try:
                data['exchange'] = exchange
            except NameError:
                data['exchange'] = ''
            try:
                data['price_currency'] = price_currency
            except NameError:
                data['price_currency'] = ''
            try:
                data['price'] = price
            except NameError:
                data['price'] = ''

            return data
        
        except:
            print('error in get header data function for ticker', self.__ticker)
            return None

    ## statistics data includes: shares, total debt, dividends 
    def get_statistics_data(self):
        data = {}
        try:
            statistics_button = self.__driver.find_element_by_xpath('//li[@data-test="STATISTICS"]/a')
            #[@data-reactid="25"]'
            statistics_button.click()

            ## making sure the page loaded
            time.sleep(5)
            #delay = 10
            #page_loaded = WebDriverWait(self.__driver, delay).until(EC.presence_of_element_located((By.XPATH, '//table[@class="W(100%) Bdcl(c)"]')))

            ## getting url, making the request and soup
            self.__url = self.__driver.current_url
            self.__html = self.__make_soup(self.__url)

            ## get shares
            try:
                stats_tables = self.__html.find_all('table', attrs={'class':'W(100%) Bdcl(c)'})
                share_stats = stats_tables[2].find_all('tr')
                shares_ = share_stats[2].find_all('td')
                shares = shares_[1].get_text()
                shares = self.__convert(shares)
            except:
                print('error getting shares for ticker', self.__ticker)

            ## get market cap
            #values_row = stats_tables[0].find_all('tr')
            #values = values_row[0].find_all('td')
            #value = values[1].get_text()
            #value = self.__convert(value)

            ## get total debt
            try:
                debt_stats = stats_tables[8].find_all('tr')
                debt_ = debt_stats[2].find_all('td')
                debt = debt_[1].get_text()
                debt = self.__convert(debt)
            except:
                print('error getting total debt for ticker', self.__ticker)

            ## get dividends
            try:
                dividends_stats = stats_tables[3].find_all('tr')
                forward_rate_row = dividends_stats[0].find_all('td')
                forward_rate = forward_rate_row[1].get_text()
                forward_rate = self.__convert(forward_rate)
                forward_yield_row = dividends_stats[1].find_all('td')
                forward_yield = forward_yield_row[1].get_text()
                forward_yield = self.__convert(forward_yield)
                trailing_rate_row = dividends_stats[2].find_all('td')
                trailing_rate = trailing_rate_row[1].get_text()
                trailing_rate = self.__convert(trailing_rate)
                trailing_yield_row = dividends_stats[3].find_all('td')
                trailing_yield = trailing_yield_row[1].get_text()
                trailing_yield = self.__convert(trailing_yield)
                average_row = dividends_stats[4].find_all('td')
                average = average_row[1].get_text()
                average = self.__convert(average)
            except:
                print('error getting dividends for ticker', self.__ticker)


            ## adding info to dict data
            ##data['value'] = value
            try:
                data['shares'] = shares
            except NameError:
                data['shares'] = ''
            try:
                data['debt'] = debt
            except NameError:
                data['debt'] = ''
            try:
                data['forward_rate'] = forward_rate
            except NameError:
                data['forward_rate'] = ''
            try:
                data['forward_yield'] = forward_yield
            except NameError:
                data['forward_yield'] = ''
            try:
                data['trailing_rate'] = trailing_rate
            except NameError:
                data['trailing_rate'] = ''
            try:
                data['trailing_yield'] = trailing_yield
            except NameError:
                data['trailing_yield'] = ''
            try:
                data['average'] = average
            except NameError:
                data['average'] = ''
                
            return data
            

        except:
            print('error in get statistics data for ticker', self.__ticker)
            return None

    def close(self):
        self.__driver.close()
    
    ## esta funcion convierte a millones, billones, trillones y elimina el signo % de los dividendos
    def __convert(self, number):
        if number[-1] == 'M':
            number = number.replace('M', '')
            list_ = re.split('\.', number)
            tmp = list_[1]
            while len(tmp) < 6:
              tmp = tmp + '0'
            number_in_m = list_[0] + tmp
            return number_in_m

        elif number[-1] == 'B':
            number = number.replace('B', '')
            list_ = re.split('\.', number)
            tmp = list_[1]
            while len(tmp) < 9:
              tmp = tmp + '0'  
            number_in_b = list_[0] + tmp
            return number_in_b

        elif number[-1] == 'T':
            number = number.replace('T', '')
            list_ = re.split('\.', number)
            tmp = list_[1]
            while len(tmp) < 12:
              tmp = tmp + '0'  
            number_in_t = list_[0] + tmp
            return number_in_t
        
        elif number[-1] == '%':
            new_number = number.replace('%', '')
            return new_number

        else:
            #print('convert function returned the same value for input', number, 'in ticker', self.__ticker)
            return number

    ## financials data includes: assets, liabilities, equity, income
    def get_financials_data(self):
        data = {}
        try:
            financials_button = self.__driver.find_element_by_xpath('//li[@data-test="FINANCIALS"]/a')
            financials_button.click()

            ## making sure the page loaded
            time.sleep(5)
            #delay = 10
            #page_loaded = WebDriverWait(self.__driver, delay).until(EC.presence_of_element_located((By.XPATH, '//section[@data-test="qsp-financial"]//span[text()="Quarterly"]')))

            ## going to quaterly data
            quarterly_button = self.__driver.find_element_by_xpath('//section[@data-test="qsp-financial"]//span[text()="Quarterly"]')
            quarterly_button.click()

            ## making sure the page loaded
            time.sleep(3)
            #delay = 10
            #page_loaded = WebDriverWait(self.__driver, delay).until(EC.presence_of_element_located((By.XPATH, '//div[@title="Net Income Common Stockholders"]/button')))

            expand_table_button = self.__driver.find_element_by_xpath('//div[@title="Net Income Common Stockholders"]/button')
            expand_table_button.click()

            ## making sure the page loaded
            time.sleep(2)
            #page_loaded = WebDriverWait(self.__driver, delay).until(EC.presence_of_element_located((By.XPATH, '//div[@title="Net Income"]')))         

            ## get financials currency
            try:
                financials_currency = self.__driver.find_element_by_xpath('//section[@data-test="qsp-financial"]/div[@class="Mb(10px)"]/span/span').text
                if financials_currency.startswith('Currency') == True:
                    currency_numbers = re.split('\.', financials_currency)
                    currency_list = re.split('in', currency_numbers[0])
                    f_currency = currency_list[1].lower()
                    print('balance sheet', currency_numbers[1], 'for ticker', self.__ticker)
                else:
                    print('balance sheet', financials_currency, 'for ticker', self.__ticker,)
                    f_currency = ''
            except:
                print('error getting financials currency for ticker', self.__ticker)                   

            ## get income
            try:
                net_income = self.__driver.find_element_by_xpath('//div[@title="Net Income"]')
                parent = net_income.find_element_by_xpath('..')
                sibling_1 = parent.find_element_by_xpath('following-sibling::div')
                sibling_2 = sibling_1.find_element_by_xpath('following-sibling::div')
                income_ = sibling_2.find_element_by_xpath('./span').text
                income = income_.replace(',','')
                income = self.__in_thousands(income)
            except:
                print('error getting net income for ticker', self.__ticker)

            ## get income statment date
            try:
                breakdown = self.__driver.find_element_by_xpath('//section[@data-test="qsp-financial"]//span[text()="Breakdown"]')
                parent = breakdown.find_element_by_xpath('..')
                sibling_1 = parent.find_element_by_xpath('following-sibling::div')
                sibling_2 = sibling_1.find_element_by_xpath('following-sibling::div')
                income_date_ = sibling_2.find_element_by_xpath('./span').text
                income_date = self.__format_date(income_date_)
            except:
                print('error getting income statement date for ticker', self.__ticker)            
            
            ## going to balance sheet
            balance_sheet_button = self.__driver.find_element_by_xpath('//section[@data-test="qsp-financial"]//span[text()="Balance Sheet"]')
            balance_sheet_button.click()

            ## making sure the page loaded
            time.sleep(5)
            #delay = 10
            #page_loaded = WebDriverWait(self.__driver, delay).until(EC.presence_of_element_located((By.XPATH, '//section[@data-test="qsp-financial"]//span[text()="Quarterly"]')))

            ## going to quarterly
            quarterly_button = self.__driver.find_element_by_xpath('//section[@data-test="qsp-financial"]//span[text()="Quarterly"]')
            quarterly_button.click()

            ## making sure the page loaded
            time.sleep(3)
            #delay = 10
            #page_loaded = WebDriverWait(self.__driver, delay).until(EC.presence_of_element_located((By.XPATH, '//div[@title="Total Assets"]/button')))

            ## expand table
            try:
                assets_button = self.__driver.find_element_by_xpath('//div[@title="Total Assets"]/button')
                assets_button.click()
                time.sleep(2)
            except:
                pass

            try:
                lia_button = self.__driver.find_element_by_xpath('//div[@title="Total Liabilities Net Minority Interest"]/button')
                lia_button.click()
                time.sleep(2)
            except:
                pass

            try:
                equity_button = self.__driver.find_element_by_xpath('//div[@title="Total Equity Gross Minority Interest"]/button')
                equity_button.click()
                time.sleep(2)
            except:
                pass
        
            ## get balance sheet date
            try:
                sheet_breakdown = self.__driver.find_element_by_xpath('//section[@data-test="qsp-financial"]//span[text()="Breakdown"]')
                parent = sheet_breakdown.find_element_by_xpath('..')
                sibling_1 = parent.find_element_by_xpath('following-sibling::div')
                sheet_date_ = sibling_1.find_element_by_xpath('./span').text
                sheet_date = self.__format_date(sheet_date_)
            except:
                print('error getting balance sheet date for ticker', self.__ticker)

            ## get current assets
            try:
                current_assets_div = self.__driver.find_element_by_xpath('//div[@title="Current Assets"]')
                parent = current_assets_div.find_element_by_xpath('..')
                sibling_1 = parent.find_element_by_xpath('following-sibling::div')
                current_assets_ = sibling_1.find_element_by_xpath('./span').text
                current_assets = current_assets_.replace(',','')
                current_assets = self.__in_thousands(current_assets)
            except:
                print('error getting current assets for ticker', self.__ticker)

            ## get tangible assets
            try:
                tangible_assets_div = self.__driver.find_element_by_xpath('//div[@title="Net Tangible Assets"]')
                parent = tangible_assets_div.find_element_by_xpath('..')
                sibling_1 = parent.find_element_by_xpath('following-sibling::div')
                tangible_assets_ = sibling_1.find_element_by_xpath('./span').text
                tangible_assets = tangible_assets_.replace(',','')
                tangible_assets = self.__in_thousands(tangible_assets)
            except:
                print('error getting tangible assets for ticker', self.__ticker)
            
            ## get total assets
            try:
                total_assets_div = self.__driver.find_element_by_xpath('//div[@title="Total Assets"]')
                parent = total_assets_div.find_element_by_xpath('..')
                sibling_1 = parent.find_element_by_xpath('following-sibling::div')
                total_assets_ = sibling_1.find_element_by_xpath('./span').text
                total_assets = total_assets_.replace(',','')
                total_assets = self.__in_thousands(total_assets)
            except:
                print('error getting total assets for ticker', self.__ticker)

            ## get current liabilities
            try:
                current_lia_div = self.__driver.find_element_by_xpath('//div[@title="Current Liabilities"]')
                parent = current_lia_div.find_element_by_xpath('..')
                sibling_1 = parent.find_element_by_xpath('following-sibling::div')
                current_lia_ = sibling_1.find_element_by_xpath('./span').text
                current_lia = current_lia_.replace(',','')
                current_lia = self.__in_thousands(current_lia)
            except:
                print('error getting current liabilities for ticker', self.__ticker)

            ## get total liabilities
            try:
                total_lia_div = self.__driver.find_element_by_xpath('//div[@title="Total Liabilities Net Minority Interest"]')
                parent = total_lia_div.find_element_by_xpath('..')
                sibling_1 = parent.find_element_by_xpath('following-sibling::div')
                total_lia_ = sibling_1.find_element_by_xpath('./span').text
                total_lia = total_lia_.replace(',','')
                total_lia = self.__in_thousands(total_lia)
            except:
                print('error getting total liabilities for ticker', self.__ticker)

            ## get total equity
            try:
                equity_gross = self.__driver.find_element_by_xpath('//div[@title="Total Equity Gross Minority Interest"]')
                equity_gross_parent = equity_gross.find_element_by_xpath('..')
                equity_gross_parent2 = equity_gross_parent.find_element_by_xpath('..')
                stockholders = equity_gross_parent2.find_element_by_xpath('following-sibling::div/div/div/div')
                sibling_1 = stockholders.find_element_by_xpath('following-sibling::div')
                total_equity_ = sibling_1.find_element_by_xpath('./span').text
                total_equity = total_equity_.replace(',','')
                total_equity = self.__in_thousands(total_equity)
            except:
                print('error getting total equity for ticker', self.__ticker)
            
            ## adding values to data dict
            try:
                data['income'] = income
            except NameError:
                data['income'] = ''
            try:
                data['income_date'] = income_date
            except NameError:
                data['income_date'] = ''
            try:
                data['sheet_date'] = sheet_date
            except NameError:
                data['sheet_date'] = ''
            try:
                data['current_assets'] = current_assets
            except NameError:
                data['current_assets'] = ''
            try:
                data['tangible_assets'] = tangible_assets
            except NameError:
                data['tangible_assets'] = ''
            try:
                data['total_assets'] = total_assets
            except NameError:
                data['total_assets'] = ''
            try:
                data['current_lia'] = current_lia
            except NameError:
                data['current_lia'] = ''
            try:
                data['total_lia'] = total_lia
            except NameError:
                data['total_lia'] = ''
            try:
                data['total_equity'] = total_equity
            except NameError:
                data['total_equity'] = ''
            try:
                data['financials_currency'] = f_currency
            except NameError:
                data['financials_currency'] = ''

            return data


        except:
            print('error in get financials data function for ticker', self.__ticker)
            return None
    
    ## add three zeros to numbers that should be in thousands
    def __in_thousands(self, number):
        tmp = number
        for _ in range(3):
            tmp = tmp + '0'
        
        new_number = tmp
        return new_number

    ## receives a date and format it the way we need it
    def __format_date(self, date):
        list_ = re.split('/', date)
        new_date = list_[2] + '/' + list_[0] + '/' +list_[1]
        return new_date