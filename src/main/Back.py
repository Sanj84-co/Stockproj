
from src.fetch.scrape import take
import matplotlib.pyplot as MatPlot
import numpy as np
str = input("Please tell which stocks' data you want ")
dat = take(str)
def graphit(data):
    graph = input("What type of data on your ticker do you want for to be plotted:")
    print(data)
    new = np.array(data[graph])
    np.diff(new)
    print(new)
    #new2 = np.diff(data['Open'])
    #a = new-new2
    #print(a)
    fig,ax = MatPlot.subplots()
    ax.scatter(new[:-1],new[:-1],c = "#1f77b4",marker=".",linewidths= 1.5, edgecolors = 'face', colorizer='none',plotnonfinite = False)
    ax.grid(True)
    fig.tight_layout()
    MatPlot.show()


graphit(dat)


