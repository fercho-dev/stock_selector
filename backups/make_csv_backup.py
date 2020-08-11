import pandas as pd 
import psycopg2
import datetime

def main():
    sql_queries = {'companies':'SELECT * FROM companies', 'shares':'SELECT * FROM shares', 
                   'incomes':'SELECT * FROM incomes', 'debt':'SELECT * FROM debt',
                   'balance_sheets':'SELECT * FROM balance_sheets', 'dividends':'SELECT * FROM dividends'}

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
    
    for table_name, query in sql_queries.items():
        ## get data
        df = get_data_from_db(query, conn)
        ## make csv files
        create_csv_file(df, table_name)


def get_data_from_db(query, conn):
    df = pd.read_sql(query, conn)
    return df


def create_csv_file(df, table_name):
    print(f'MAKING CSV FILE FOR {table_name}')
    now = datetime.datetime.now().strftime('%Y_%B')
    file_path = f'./csv_files/{table_name}_{now}.csv'
    df.to_csv(file_path, index=False, encoding='utf-8')


if __name__ == '__main__':
    main()