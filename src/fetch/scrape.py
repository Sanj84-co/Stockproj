import yfinance as yf 
import pandas as pa 
def take(str):
    dat = yf.download(str)
    clean(dat)
    return (dat)

def clean(dat):
    df1 = pa.DataFrame(dat)
    pa.isnull(df1)
    df1.fillna(0)
    df1 = df1.drop_duplicates() ##duplicates, null values, 
