import datetime 
from datetime import timedelta, date, datetime,time
from src.main.Exceptions import *
import json 
import sqlite3
def checkTicker(name):
    if name == "" or name is None:
        raise EmptyTickerError("Cannot be Empty")
    elif len(name)>5 :
        raise TooLongTickerError("The length is too big")
    elif not name.isupper():
        raise InavlidTickerFormatError("The name has to be Upper Case")