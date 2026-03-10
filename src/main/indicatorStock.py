class stockalgo:
    def __init__(self,prices,df): # close prices so df[close] should probably be one.  we also need the len of df[close] to conduct a check
        self.prices = []
    def mVA(self, prices, period):
        prices = prices[:-period]
        sum = 0
        for i in enumerate(prices):
            sum+=i
        return sum/period
    def Rsi(self,)
