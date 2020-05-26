import logging
logging.basicConfig(level=logging.INFO)
import subprocess
import argparse

logger = logging.getLogger(__name__)

def main(ticker):
    run_scraper(ticker)
    answer = input('\ndo you want to continue and insert the data into the database (y/n)\n')
    if answer == 'y':
        insert_to_db()
    else:
        print('\ndata was not inserted into the database\n')

def run_scraper(ticker):
    logger.info('starting scraping process')
    subprocess.run(['python3.7', 'add_to_sheet.py', ticker], cwd='./scraping_yfinance')

def insert_to_db():
    logger.info('starting insertion process')
    subprocess.run(['python3.7', 'add_to_db.py'], cwd='./insertion_with_sheets')
    subprocess.run(['python3.7', 'update_not_listed.py'], cwd='./insertion_with_sheets')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('ticker',
                        help='the ticker you are looking for',
                        type=str)
    args = parser.parse_args()

    main(args.ticker)