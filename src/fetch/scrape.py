import yfinance as yf 
import pandas as pa 
import seaborn as s
def take(str):
    dat = yf.download(str)
    clean(dat)
    return (dat)

def clean(dat):
    df1 = pa.DataFrame(dat)
    pa.isnull(df1)
    df1.fillna(0)
    print(df1.duplicated())
    df1 = df1.drop_duplicates() ##duplicates, null values, 
