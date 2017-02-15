import sqlite3
from os import path

if path.exists('reg_time.db'):
    print('db files not found')

try:
    conn = sqlite3.connect('reg_time.db')    
except Exception(e):
    print('ERROR: %s', e) 
else:
    print('Connection Success')           


def create_table():
    c = conn.cursor()
    sql = "CREATE TABLE Users (id text, name text, password text, email, phone)"
    c.execute(sql)
    conn.commit()

    sql = "CREATE TABLE Visits (user_id text, dateFrom text, dateTo text)"
    c.execute(sql)
    conn.commit()

    c.close()
    conn.close()

create_table()    

