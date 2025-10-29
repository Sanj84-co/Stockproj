
from src.fetch.scrape import take
import matplotlib.pyplot as MatPlot
import numpy as np
import pandas as pd 
import seaborn as sns
str = input("Please tell which stocks' data you want ")
dat = take(str)
def graphit(dat,str):
    graph = input("What type of data on your ticker do you want for to be plotted:")
    graph2 = input("What type of data on your ticker do you want for to be plotted:")
    new = np.array(dat[graph])
    np.diff(new)
    new2 = np.array(dat[graph2])
    np.diff(new2)
    Operation = input("what type of operation do you want to perform on the data: ") # want to convert the opeartions string into a value
    df = pd.DataFrame(dat)
    df = df.xs(str ,level='Ticker',axis=1) #So df has one row which dalled date and two columns which have levels in each, price which is level 0 and contaisn [close, open, ...etc...] whereas level1 contains ticker and 'appl' so basically, you remove levl one and make the level 0 a column 
    sns.catplot(data=df,x='Close')
    MatPlot.show()
    fig,ax = MatPlot.subplots()
    df2 = np.array(df[graph])
    np.diff(df2)
    ax.scatter(df2[:-1],df2[:-1],c = "#1f77b4",marker=".",linewidths= 1.5, edgecolors = 'face', colorizer='none',plotnonfinite = False)
    ax.grid(True)
    fig.tight_layout()
    MatPlot.show()
graphit(dat,str)

def calculate(data2, dat, str ):
    graph = input("What type of data of each stock do you want to compare")
    st1 = np.array(dat[graph])
    st2 = np.array(data2[graph])
    fig,ax = MatPlot.subplots()
    if ddad
op = input("Do you want to perform an operation on two datasets(T/F): ") # i want to take in input as operation and then perform this operation on two data sets . for example,you can compare microsoft and AAPL based off their data through a scatterplot.
if op == "True":
    operation = input("what type: ")
    stoc = input("what stock")
    data2 = take(stoc)
    if operation == "add":



