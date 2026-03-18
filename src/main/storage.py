import sqlite3
with sqlite3.connect("store.db") as con: # need to create and actually connect to the database. conec
    cur = con.cursor() # to make the queries this is waht you need to do.
    cur.execute("CREATE TABLE IF NOT EXISTS user(user_id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT,time_joined TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS watchlist( ticker_id INTEGER PRIMARY KEY AUTOINCREMENT, " \
    "user_id INTEGER,Ticker TEXT, time_added TEXT, FOREIGN KEY(user_id)REFERENCES user(user_id))")
con.commit()

def get_user():
    with sqlite3.connect('store.db') as con:
        cur = con.cursor()
        cur.execute('SELECT * FROM watchlist WHERE user_id = ?')
    con.commit()
def add():
    with sqlite3.connect('store.db') as con:
        cur = con.cursor()
        cur.execute('INSERT INTO watchlist(user_id,Ticker,time_added ) VALUES(?,?,?')
    con.commit()
def remove(): # permantely save the change
    with sqlite3.connect('store.db') as con:
        cur = con.cursor()
        cur.execute('DELETE FROM watchlist WHERE ticker_id = ? AND ticker = ?')
    con.commit()
def create_user():
    with sqlite3.connect('store.db') as con: # connection automatically closes each time
        sql_query =  'INSERT INTO user(Name,time_joined)VALUES(?,?)'
        cur = con.cursor()
        cur.execute('INSERT INTO user(Name, time_joined)VALUES(?,?)')
    con.commit()
    con.close()
