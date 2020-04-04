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

    while True:
        index = input("to which index do you want to add the company:\n")
        try:
            cur.execute('''
            SELECT id FROM indices WHERE "name" = %s''', (index,))
            indices_id = cur.fetchone()[0]
            break
        except TypeError:
            print("the index is not in the indices table\n")
            continue

    
    print("are you sure you want to add", company, "into", index)
    answer = input("(y/n)\n")
    
    if answer == 'y':
        cur.execute ('''
        INSERT INTO indices_companies (indices_id, companies_id) 
        VALUES (%s, %s);
        ''', (indices_id, companies_id,))
        break
    else:
        continue

## save the data in the database
conn.commit()

## close the connection
cur.close()
conn.close()

print('done')