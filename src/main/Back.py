
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
from src.fetch.scrape import * 
#option()
#dap = take('MSFT')
#nip = np.array(dap['Close'])
#ax.scatter(new,nip,c = 'red',marker=".",linewidths= 1.5, edgecolors = 'face', colorizer='none',plotnonfinite = False)
#MatPlot.show()
def calculate(data2, dat, strs ):
    graph = input("What type of data of each stock do you want to compare")
    st1 = np.array(dat[graph])
    st2 = np.array(data2[graph])
    fig,ax = MatPlot.subplots()
# ax.scatter(st1[:-1],st2[:-1],c = "#1f77b4",marker=".",linewidths= 1.5, edgecolors = 'face', colorizer='none',plotnonfinite = False)
    ax.grid(True)
    fig.tight_layout()
    MatPlot.show()
def period(strs,indicator = "no"):
    while True:
        period4 = input("to what specific amount of calendar  days do you want your data to span over? ")
        try:
            num = int(period4)
            if num <=0 or num> 5200:
                print("Please enter a positive nonzero integer within range: ")
                continue
            break
        except ValueError : 
            print("Please enter an integer")   # tells the program to ingnore what caused the error and to just raise this.
    #None is just the NoneType object and it is nothing. this is what Null is in Python
    today = date.today()
    sub = pd.Timestamp(today)+pd.offsets.BusinessDay(n=int(-1 * (int(period4)-1))) 
    dat = take(strs,sub.date())
    df = pd.DataFrame(dat)
    print(df.index)
    df = df[df.index>=sub]
    print(df.index[0].date())
    df =df.xs(strs ,level='Ticker',axis=1)
    print(df['Close'])
    contain = [sub,period4,df,strs]
    return contain
    candlestick(sub,period4,df,strs)

def candlestick(start, enduration,df,strs,Rsi = None):
    def formatter(x,pos):
        return df.index[x].date()
    ab = datetime.combine(start, time())
    fig, axlist = mpf.plot(df, type='candle', volume = True, title= strs +" " +enduration, ylabel = 'OHLC candles', xlabel ='Date',returnfig = True )
    xticks = ticker.FuncFormatter(formatter)
    axlist[1].set_xticks(list(range(len(df)))) # controls wehere the ticks are which is in the middle of the candle
    axlist[1].xaxis.set_major_formatter(xticks) # controls what the actual name which i set through the formatter function.
    mpf.show() 
    if Rsi is not None: # rsi is a whole series of values so != is the ambigious values. 
        print(len(df))
        print(len(Rsi))
        apd = mpf.make_addplot(Rsi,type = 'line', panel = 1)    
        fig,axlist = mpf.plot(df,addplot = apd,type = 'candle',returnfig = True)
        axlist[2].axhline(70)
        axlist[2].axhline(30)
        mpf.show()
        print(mpf.available_styles())      # it holds to this one instead of making a new plot each time
    return "hello"
def pnL(item):
    ticker = item[2]
    shares = item[3]
    bought_price = item[4]
    total_purchase = shares * bought_price
    current_price = currentP(ticker)
    total_sale = shares * current_price
    total_pnl = total_sale-total_purchase
    return [total_pnl,current_price]

#it does not pay attention to the watchlist at all.
# things I want to do:
#  account for non trading days.
