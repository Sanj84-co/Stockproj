import numpy as np
import pandas as pd
class stockalgo:
    def __init__(self,df): # close prices so df[close] should probably be one.  we also need the len of df[close] to conduct a check
        self.prices = []
        self.df = df 
        self.rsi = None
    def mVA(self, prices, period):
        prices = prices[:-period]
        sum = 0
        for i in enumerate(prices):
            sum+=i
        return sum/period
    def Rsi(self):
       # percentC = ((self.df-self.df.iloc[0])/self.df.iloc[0])*100 # not the faily percent change 
        percentC = (np.diff(self.df)/self.df[:-1]) * 100
        positiveC = percentC.where(percentC>0,0)
        negativeC = percentC.where(percentC<0,0)
        avgG = positiveC.rolling(14).mean()
        avgL = abs(negativeC.rolling(14).mean())
        RS = avgG/avgL
        RSI = 100-(100/(1+RS))
        new = pd.Series(float('nan'))
        nRSI = pd.concat([new,RSI])
        self.rsi = nRSI
        
 