import datetime 
from datetime import timedelta, date, datetime,time
from src.main.Exceptions import *
import json 
try:
    with open('watch.json','r') as f:
        watchlist = json.load(f)
except FileNotFoundError and json.JSONDecodeError:
    watchlist = {}

print(watchlist)
def checkTicker(name):
    if name == "" or name is None:
        raise EmptyTickerError("Cannot be Empty")
    elif len(name)>5 :
        raise TooLongTickerError("The length is too big")
    elif not name.isupper():
        raise InavlidTickerFormatError("The name has to be Upper Case")
def addTicker(name):
    checkTicker(name)
    if name in watchlist:
        raise DuplicateTickerError("Already Exists") # raise stops the execution and makes the person handle it. 
    watchlist[name] = {'Ticker':name,  'date-added': str(date.today())}
    with open("watch.json","w") as f:
        json.dump(watchlist,f)
def removeTicker(name):
    checkTicker(name)
    if name not in watchlist:
        raise TickerNotFoundError("Does not Exist")
    watchlist.pop(name)
    with open("watch.json","w") as f:
        json.dump(watchlist,f)
def viewWatchist(): #easier to loop through 
    return list(watchlist.values())