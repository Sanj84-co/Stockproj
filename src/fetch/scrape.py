import yfinance as yf 
def take(str):
    data = yf.download(str)
    return (data)

