
from src.fetch.scrape import take
import matplotlib.pyplot as MatPlot
import numpy as np
str = input("Please tell which stocks' data you want ")
dat = take(str)
def graphit(data):
    graph = input("What type of data on your ticker do you want for to be plotted:")
    graph2 = input("What type of data on your ticker do you want for to be plotted:")
    print(data)
    new = np.array(data[graph])
    np.diff(new)
    print(new)
    new2 = np.array(data[graph2])
    np.diff(new2)
    Operation = input("what type of operation do you want to perform on the data")
    a = new2
    print(a)
    fig,ax = MatPlot.subplots()
    ax.scatter(a[:-1],a[:-1],c = "#1f77b4",marker=".",linewidths= 1.5, edgecolors = 'face', colorizer='none',plotnonfinite = False)
    ax.grid(True)
    fig.tight_layout()
    MatPlot.show()


graphit(dat)


