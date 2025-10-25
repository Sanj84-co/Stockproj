
from src.fetch.scrape import take
import matplotlib.pyplot as MatPlot
import numpy as np
import pandas as pd 
import seaborn as sns
str = input("Please tell which stocks' data you want ")
dat = take(str)
opCount = dict{
    '+': +,
    '-': -
}
def graphit(dat):
    graph = input("What type of data on your ticker do you want for to be plotted:")
    graph2 = input("What type of data on your ticker do you want for to be plotted:")
    new = np.array(dat[graph])
    np.diff(new)
    new2 = np.array(dat[graph2])
    np.diff(new2)
    Operation = input("what type of operation do you want to perform on the data") # want to convert the opeartions string into a value
    df = pd.DataFrame(dat)
    #df2 = df.set_index(['Close'])
    df = df.xs( ,level='Ticker',axis=1) #So df has one row which dalled date and two columns which have levels in each, price which is level 0 and contaisn [close, open, ...etc...] whereas level1 contains ticker and 'appl' so basically, you remove levl one and make the level 0 a column 
    sns.catplot(data=df,x='Close')
    MatPlot.show()
    fig,ax = MatPlot.subplots()
    df2 = np.array(df[graph])
    np.diff(df2)
    ax.scatter(df2[:-1],df2[:-1],c = "#1f77b4",marker=".",linewidths= 1.5, edgecolors = 'face', colorizer='none',plotnonfinite = False)
    ax.grid(True)
    fig.tight_layout()
    MatPlot.show()


graphit(dat)


