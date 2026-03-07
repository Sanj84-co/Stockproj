
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
def period(df,strs):
    while True:
        period4 = input("to what specific amount of days do you want your data to be reflected on:")
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
    print(sub)
    df = df[df.index>=sub]
    print(df.index[0].date())
    df =df.xs(strs ,level='Ticker',axis=1)
    candlestick(sub,period4,df,strs)
def candlestick(start, enduration,df,strs):
    print((list(range(len(df)))))
    def formatter(x,pos):
        return df.index[x].date()
    ab = datetime.combine(start, time())
    ba =  ab.timestamp()
    fig, axlist = mpf.plot(df, type='candle', volume = True, title= strs +" " +enduration, ylabel = 'OHLC candles', xlabel ='Date',returnfig = True )
    xticks = ticker.FuncFormatter(formatter)
    axlist[1].set_xticks(list(range(len(df)))) # controls wehere the ticks are which is in the middle of the candle
    axlist[1].xaxis.set_major_formatter(xticks) # controls what the actual name which i set through the formatter function.
    mpf.show() # it holds to this one instead of making a new plot each time
    return "hello"
# things I want to do:
#  account for non trading days.
