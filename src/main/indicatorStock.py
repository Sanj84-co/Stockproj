class stockalgo:
    def __init__(self,prices):
        self.prices = []
    def mVA(self, prices, period):
        prices = prices[:-period]
        sum = 0
        for i in enumerate(prices):
            sum+=i
        return sum/period
    def ichiMoku(self,prices,period):