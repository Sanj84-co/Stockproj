import datetime 
from datetime import timedelta, date, datetime,time
from src.main.Exceptions import *
watchlist = {}
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
    watchlist[name] = {'Ticker':name,  'date-added': date.today()}
def removeTicker(name):
    checkTicker(name)
    if name not in watchlist:
        raise TickerNotFoundError("Does not Exist")
    return watchlist.pop(name)
def viewWatchist(): #easier to loop through 
    return list(watchlist.values())
addTicker('AAPL')
print(watchlist)