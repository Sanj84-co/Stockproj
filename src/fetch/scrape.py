import yfinance as yf 
import pandas as pa 
def take(str):
    data = yf.download(str)
    clean(data)
    return (data)

def clean(data):
    df1 = pa.DataFrame(data)
    print(pa.isna(df1))

