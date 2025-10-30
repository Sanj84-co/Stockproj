
from src.fetch.scrape import take
import matplotlib.pyplot as MatPlot
import numpy as np
import pandas as pd 
import seaborn as sns

str = input("Please tell which stocks' data you want ")
dat = take(str)
fig,ax = MatPlot.subplots()
def option():
    str =  input("These are the options that you have\n"         
    " 1. Want to calculate stock data\n" 
    " 2. Want to compare Stock data between two stocks\n" 
    " 3. Choose and analyze any of technical indicators below\n" 
    " Moving Value Average, Ichimoku Cloud , Relative Strength Index, Volume Weighted Average Price")


def graphit(dat,str,fig,ax):
    graph = input("What type of data on your ticker do you want for to be plotted:")
    graph2 = input("What type of data on your ticker do you want for to be plotted:")
    new = np.array(dat[graph])
    np.diff(new)
    new2 = np.array(dat[graph2])
    np.diff(new2)
    df = pd.DataFrame(dat)
    df = df.xs(str ,level='Ticker',axis=1) #So df has one row which dalled date and two columns which have levels in each, price which is level 0 and contaisn [close, open, ...etc...] whereas level1 contains ticker and 'appl' so basically, you remove levl one and make the level 0 a column 
    sns.catplot(data=df,x='Close')
    #MatPlot.show()
    #fig,ax = MatPlot.subplots()
    ax.scatter(new,new,c = "#1f77b4",marker=".",linewidths= 1.5, edgecolors = 'face', colorizer='none',plotnonfinite = False)
    ax.grid(True)
    ax.set_xlabel(graph)
    ax.legend()
    ax.set_ylabel(graph2)
    fig.tight_layout()
    #MatPlot.show()
    return new
option()
new = graphit(dat,str,fig,ax)
dap = take('MSFT')
nip = np.array(dap['Close'])
ax.scatter(new,nip,c = 'red',marker=".",linewidths= 1.5, edgecolors = 'face', colorizer='none',plotnonfinite = False)
MatPlot.show()
def calculate(data2, dat, str ):
    graph = input("What type of data of each stock do you want to compare")
    st1 = np.array(dat[graph])
    st2 = np.array(data2[graph])
    fig,ax = MatPlot.subplots()
    ax.scatter(st1[:-1],st2[:-1],c = "#1f77b4",marker=".",linewidths= 1.5, edgecolors = 'face', colorizer='none',plotnonfinite = False)
    ax.grid(True)
    fig.tight_layout()
    MatPlot.show()
op = input("Do you want to perform an operation on two datasets(T/F): ") # i want to take in input as operation and then perform this operation on two data sets . for example,you can compare microsoft and AAPL based off their data through a scatterplot.
if op == "T":
    operation = input("what type: ")
    stoc = input("what stock")
    data2 = take(stoc)
    calculate(data2,dat,op)



