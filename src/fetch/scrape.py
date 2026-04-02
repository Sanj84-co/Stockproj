import yfinance as yf 
import pandas as pa 
def take(strs,start):
    print(str(start))
    dat = yf.download(strs,start = str(start))
    ds = clean(dat)
    return (ds)

def clean(dat):
    df1 = pa.DataFrame(dat)
    pa.isnull(df1)
    df1 = df1.fillna(0)
    df1 = df1.drop_duplicates() 
    return df1 ##duplicates, null values, 
def currentP(ticker):
    ticker = yf.Ticker(ticker)
    cprice = ticker.info.get('currentPrice')
    return cprice
