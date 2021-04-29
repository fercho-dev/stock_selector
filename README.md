# stock_selector

Get financial data from YahooFinance web page and save into a Google Sheet or a PostgreSQL database.

### How does it work?

I used a combination of BeautifulSoup and Selenium to scrape YahooFinance. To send the data to google sheets I used the google-api-python-client library to connect to Google's API. And Psycopg2 library to connect to PostgreSQL.

### File structure

__Backups folder__

Here you'll find the code to create a csv-backup of the database.

__Data base design folder__

Inside the db_schema_code.txt file there is the sql script to create the database.

The other two files are images of the database diagrams.

__Data insertion folder__

In this folder is the code to scrape YahooFinance, insert data to google sheets, insert data through command line and to the database.
