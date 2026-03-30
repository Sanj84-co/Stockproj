import sqlite3
from Exceptions import *
from watchlist import checkTicker
with sqlite3.connect("store.db") as con: # need to create and actually connect to the database. conec
    cur = con.cursor() # to make the queries this is waht you need to do.
    cur.execute("CREATE TABLE IF NOT EXISTS user(user_id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT,time_joined TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS watchlist( ticker_id INTEGER PRIMARY KEY AUTOINCREMENT, " \
    "user_id INTEGER,Ticker TEXT, time_added TEXT, FOREIGN KEY(user_id)REFERENCES user(user_id))")
    con.commit()
def get_id(name):
    with sqlite3.connect('store.db') as con:
        cur = con.cursor()
        cur.execute('SELECT user_id FROM user WHERE Name = ?',(name,)) # single element tuples need a trailing comma.
        a = cur.fetchone()
        con.commit()
        print(a[0])
        return int(a[0])
def get_user(user_id):
    with sqlite3.connect('store.db') as con:
        cur = con.cursor()
        cur.execute('SELECT * FROM watchlist WHERE user_id = ?',(user_id,))
        a = cur.fetchall()
        con.commit()
        return a
def add(user_id,Ticker, time_add):
      checkTicker(Ticker)
      with sqlite3.connect('store.db') as con:
        checkTicker(Ticker)
        #checkticker function from watchlist
        cur = con.cursor()
        cur.execute('SELECT * FROM watchlist WHERE user_id = ? AND Ticker = ?',(user_id,Ticker))
        test = cur.fetchone()
        if test:
            raise DuplicateTickerError("Ticker already exists!")
        else:
            cur.execute('INSERT INTO watchlist(user_id,Ticker,time_added ) VALUES(?,?,?)',(user_id,Ticker,str(time_add)))
        con.commit()
def remove(ticker,user_id): # permantely save the change # needs user_id or will delte every instance of a ticker
    checkTicker(ticker) # should check prior to actually starting the connection so you dont have a redundant connection
    with sqlite3.connect('store.db') as con:
        cur = con.cursor()
        cur.execute('SELECT * FROM watchlist WHERE user_id = ? AND Ticker = ?',(user_id,ticker))
        ti = cur.fetchone()
        if not ti:
            raise TickerNotFoundError('Ticker was not found')
        else:
            cur.execute('DELETE FROM watchlist WHERE ticker = ? AND user_id = ?',(ticker,user_id))
        con.commit()
def create_user(Name,time_joined):
    with sqlite3.connect('store.db') as con: # connection automatically closes each time
        cur = con.cursor()
        cur.execute('INSERT INTO user(Name, time_joined)VALUES(?,?)',(Name,str(time_joined)))
        con.commit()
        
        
with sqlite3.connect('Store.db') as con:
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS transactions(INTEGER transaction_id PRIMARY KEY AUTOINCREMENT,  user_id INTEGER, ticker TEXT, Shares Number, purchase_price REAL created_date TIMESTAMP,FOREIGN KEY(user_id)REFERENCES users(user_id))')

#using f strings in injecting data into sql which is dangerous. people can inject malicious code into the input fields
# and use that to view sensitive data. use parameterized quieres instead 
# 1 or 1=1 always true so it returns every row. ? treats it as data not sql code