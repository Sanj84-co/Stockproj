
from src.fetch.scrape import take
import matplotlib.pyplot as MatPlot
import matplotlib.dates as md
import numpy as np
import pandas as pd 
import seaborn as sns
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


def option():
    str =  input("These are the options that you have\n"         
    " 1. Want to calculate stock data\n" 
    " 2. Want to compare Stock data between two stocks\n" 
    " 3. Choose and analyze any of technical indicators below\n" 
    " Moving Value Average, Ichimoku Cloud , Relative Strength Index, Volume Weighted Average Price")
def graphit(dat,strs,fig,ax):
    graph = input("What type of data on your ticker do you want for to be plotted:")
    graph2 = input("What type of data on your ticker do you want for to be plotted:")
    new = np.diff(dat[graph])
    new2 = np.diff(np.array(dat[graph2])) # just a litle more efficient than typing new two different times.
    df = pd.DataFrame(dat)
    df =df.xs(strs ,level='Ticker',axis=1)

    print(df.columns) #So df has one row which dalled date and two columns which have levels in each, price which is level 0 and contaisn [close, open, ...etc...] whereas level1 contains ticker and 'appl' so basically, you remove levl one and make the level 0 a column 
    sns.catplot(data=df,x='Close')
    #MatPlot.show()
    #fig,ax = MatPlot.subplots()
    df2 =  abs(df['Open']-df['Close']) #try to convert the dates into time. first retreive the dates by themselves
    MatPlot.bar(df['Close'],height=df2,width=0.8,align='center')
    #MatPlot.show()
    ax.scatter(new,new2,c = "#1f77b4",marker=".",linewidths= 1.5, edgecolors = 'face', colorizer='none',plotnonfinite = False)
    ax.grid(True)
    ax.set_xlabel(graph)
    ax.legend()
    ax.set_ylabel(graph2)
    fig.tight_layout()
    #MatPlot.show()
    return new
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
def period():
    period4 = input("to what specific amount of days do you want your data to be reflected on:")
    duration = timedelta(days=int(period4))
    today = date.today()
    sub = today-duration + timedelta(days = 1)
    final = str(sub)
    print(final)
    candlestick(sub,period4)
def candlestick(start, enduration):
    ab = datetime.combine(start, time())
    ba =  ab.timestamp()
    print(enduration)
    dates = start
    add = []
    fig,ax = MatPlot.subplots() # it holds to this one instead of making a new plot each time
    while str(dates) != str(start+timedelta(days= int(enduration))):
        print(str(dates))
        MatPlot.bar(str(dates),0.5,0.2,'center')
        dates = (dates+ timedelta(days=1))
    ax.plot(0,2,'d',)
    MatPlot.tick_params
    MatPlot.bar_label(ba,label_type='center')#
    MatPlot.show()

    return "hello"
if __name__ == "__main__": #all of this will run if imported but it should only be triggered when the user executes the file.
    strs = input("Please tell which stocks' data you want ")
    dat = take(strs)
    fig,ax = MatPlot.subplots()
    new = graphit(dat,strs,fig,ax)
    op = input("Do you want to perform an operation on two datasets(T/F): ") # i want to take in input as operation and then perform this operation on two data sets . for example,you can compare microsoft and AAPL based off their data through a scatterplot.
    if op == "T":
        operation = input("what type: ")
        stoc = input("what stock")
        data2 = take(stoc)
        calculate(data2,dat,op)
        period()

