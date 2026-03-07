
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
from watchlist import *


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
if __name__ == "__main__": #all of this will run if imported but it should only be triggered when the user executes the file.
    while True:
        input("Hello user!!Welcome to SeeStock")
        input("You can keep track and study your stocks here")
        checkTicker()
        try:
            a = input("What do you want to do,  add/remove/view/nothing: ")
            tick = input("What ticker do you want: ")
            if a == 'add':
                addTicker()
            elif a == 'remove':
                removeTicker()
            else:
                viewWatchist()
        except:
            input("Fix the error")
        d = input("What stock do you want to see data for or do you want to view the watchlist first ? ")
        if d == "view":
            viewWatchist()
    


        
    dat = take(strs)
    df = pd.DataFrame(dat)
    period(df,strs)
    fig,ax = MatPlot.subplots()
    #df =df.xs(strs ,level='Ticker',axis=1)
    new = graphit(dat,strs,fig,ax)
    op = input("Do you want to perform an operation on two datasets(T/F): ") # i want to take in input as operation and then perform this operation on two data sets . for example,you can compare microsoft and AAPL based off their data through a scatterplot.
    if op == "T":
        operation = input("what type: ")
        stoc = input("what stock")
        data2 = take(stoc)
        calculate(data2,dat,op)
        period()
# things I want to do:
#  account for non trading days.