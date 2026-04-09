
from src.fetch.scrape import take
from matplotlib import ticker
import mplfinance as mpf
import matplotlib.pyplot as MatPlot
import matplotlib.dates as md
import numpy as np
import pandas as pd 
import seaborn as sns
import datetime 
from datetime import timedelta, date, datetime,time
from src.main.Exceptions import *
from Back import *
import json
from watchlist import *
from indicatorStock import *
from storage import * 
def option():
    str =  input("These are the options that you have\n"         
    " 1. Want to calculate stock data\n" 
    " 2. Want to compare Stock data between two stocks\n" 
    " 3. Choose and analyze any of technical indicators below\n" 
    " Moving Value Average, Ichimoku Cloud , Relative Strength Index, Volume Weighted Average Price")
def comparison(data1,data2): # retreive the close data, find the starting period close for each stock then apply the formula to the entire column, then plot the data on the same graph. 
    Closed1 = data1[2]['Close']
    Closed2 = data2[2]['Close']
    start1,start2= data1[0],data2[0]
    percentClose = ((Closed1-Closed1.iloc[0])/Closed1.iloc[0])* 100 
    percentClose2 = ((Closed2-Closed2.iloc[0])/Closed2.iloc[0])*100
    fig, ax = MatPlot.subplots()
    ax.plot(percentClose,label = data1[3])
    ax.plot(percentClose2,label = data2[3])
    if int(data1[1]) > 20 and int(data2[1])>20:
        a= md.MonthLocator()
        b = md.WeekdayLocator()
        ax.xaxis.set_major_locator(a)
        ax.xaxis.set_minor_locator(b)
        ax.set_ylabel(ylabel = '%')
        ax.tick_params(which='minor', color ='red', bottom = True, length = 10 )
    else:
        MatPlot.xticks(rotation = 20)
    ax.legend()
    print(percentClose)

    print("hello")
if __name__ == "__main__": #all of this will run if imported but it should only be triggered when the user executes the file.
    name = input("What is your name user? ")
    user_id = get_id(name)
    if user_id == None:
         create_user(name,date.today())
         user_id = get_id(name)
    a=(view_transactions(user_id))
    b = alert_noti()
    for item in a:
        print('Ticker: ' + item[2])
        print('Shares: ' + str(item[3]))
        print('Bought Price: ' + str(item[4]))
        print('Bought on: ' + str(item[5])) 
        p = pnL(item)
        print('Current Price: ' + str(p[1]))
        print('PnL: ' + str(round(p[0],2))) #if name is not in database. you create the new user and then retreive the user_id.
    while True:
        print("Hello user!!Welcome to SeeStock")
        print("You can keep track and study your stocks here")
        a = input("What do you want to do,  add/remove/view/nothing: ")
        tick = input("What ticker do you want: ")
        checkTicker(tick)
        try:
            if a == 'add':
                ask = input("Do you want to add a transaction or not")
                if ask == 'yes':
                    add_transactions(user_id,tick,3)
                    print(view_transactions(user_id))
                add(user_id,tick,date.today())
            elif a == 'remove':
                remove(tick,user_id)
            else:
                get_user(user_id)
        except ValueError as e :
            print(e)
        d = input("do you want to see data or do you want to view the watchlist first ? ")
        if d == "view":
            watch = get_user(user_id)
            for i in watch:
                print('Stock: ' + i[2])
                print('Time_Added: ' + i[3])
        else:   
            #fig,ax = MatPlot.subplots()
            #df =df.xs(strs ,level='Ticker',axis=1)
            further = input("Do you want to see OHLC data for one stock or compare two? ") 
            if further == 'one':
                stock = input("What stock? ")
                indicator = input("Do you want to see the indicator for the stock(yes or no)? ")
                if indicator == 'yes':
                  while True:
                    try:
                        tainer = period(stock,indicator)
                        if len(tainer[2]['Close'])>=28:
                            obj = stockalgo(tainer[2]['Close'])
                            obj.Rsi()
                            candlestick(tainer[0],tainer[1],tainer[2],tainer[3],Rsi=obj.rsi)
                            break 
                        continue
                    except e as ValueError:
                        print('The amount of periods or trading days has to be 14+')
                else:
                    tainer = period(stock)
                    candlestick(tainer[0],tainer[1],tainer[2],tainer[3])
            else: # i want to take in input as operation and then perform this operation on two data sets . for example,you can compare microsoft and AAPL based off their data through a scatterplot.
                stock1 = input("What is the first stock?")
                stock2 = input("What is the second stock?")
                adata1 = period(stock1)
                adata2 = period(stock2)
                comparison(adata1,adata2)
# things I want to do:
#  account for non trading days.