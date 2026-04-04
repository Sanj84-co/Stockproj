from fastapi import FastAPI #from staapi import the class FAST API
from src.main.storage import *
from pydantic import BaseModel
from src.main.Back import *
class Delivery(BaseModel):
    name: str
    
     #define the schema of the network that you are working on.
class added(BaseModel):
    name: str
    Ticker: str
class transaction(BaseModel):
    name:str
    Ticker:str
    shares: int
app = FastAPI() #retrives fastapi instance
@app.get('/')#decorator which tells it that when this path is provided activate this function
async def root(): # it will run this function when the specific path is described.# async means it can handle multiple requests at once.
    return {'message':'Stock App'}
@app.post('/users') #path params are for search, query params are for filtering. dont use path mostly post since the information is sent alongside the request body.
async def create(deliver:Delivery): 
    create_user(deliver.name,str(date.today()))# it is intialized in a schema instead.
    user_id = get_id(deliver.name)
    return {'name':deliver.name, 'user_id':user_id}#json is a language-independent text format used to display data.
@app.get('/users/{name}')
async def getuser_id(name:str):
    a = get_id(name)
    return {'name':name,'user_id':a}
@app.get('/watchlist/{name}')
async def getwatchlist(name:str):
    a = get_id(name)
    watchlist = get_user(a)
    conta = []
    for item in watchlist:
        prompt = {'Info':{
            'Stock': item[2],
            'Time-added':item[3]
        }
        }
        conta.append(prompt)
    return{
        'watchlist':conta
    }
@app.post('/watchlist')
async def add_stock(adder:added):
    a = get_id(adder.name)
    add(a,adder.Ticker,str(date.today()))
    return{
        'Ticker': adder.Ticker,
        'Date-added':str(date.today())
    }
@app.delete('/watchlist/{name}/{Ticker}')
async def delete_stock(name:str, Ticker:str):
    id = get_id(name)
    remove(Ticker,id)
    return {
        'Ticker':Ticker,
        'Date-Removed': str(date.today())
    }
@app.get('/transactions/{name}')
async def user_transactions(name:str):
    id = get_id(name)
    a = view_transactions(id)
    conta = []
    for item in a:
        profit = pnL(item)
        p = {
            'Ticker': item[2],
            'shares': str(item[3]),
            'Bought Price': str(item[4]),
            'Bought on': str(item[5]),
            'Current Price': str(profit[1]),
            'PnL':str(round(profit[0],2))
        }
        conta.append(p)
    return{
        'transactions':conta
    }
@app.post('/transactions')
async def new_transaction(transaction:transaction):
    id = get_id(transaction.name)
    add_transactions(id,transaction.Ticker,transaction.shares)
    return{
        'transaction':{
            'Name':transaction.name,
            'Ticker':transaction.Ticker,
            'Shares':transaction.shares
        }
    }