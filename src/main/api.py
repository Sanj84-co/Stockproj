from fastapi import FastAPI,requests #from staapi import the class FAST API
from src.main.storage import *
from pydantic import BaseModel
from src.main.Back import pnL,alert_noti
from src.fetch.scrape import currentP
from contextlib import asynccontextmanager
from datetime import date, datetime,time
from apscheduler.schedulers.background import BackgroundScheduler
import logging 
from fastapi.responses import JSONResponse
logger = logging.getLogger(__name__)#intializes the logging instance.
logging.basicConfig(filename='status.log',encoding='utf-8',level=logging.DEBUG)# sets up the basic config. utf-8 is the character that it can have including the type.
logger.debug('First debugging statement')
class Delivery(BaseModel):
    name: str
    email:str
     #define the schema of the network that you are working on.
class added(BaseModel):
    name: str
    Ticker: str
class transaction(BaseModel):
    name:str
    Ticker:str
    shares: int
class alert(BaseModel):
    name:str
    Ticker:str
    threshold:float
@asynccontextmanager
async def lifespan(app:FastAPI):#app as a parameter 
    scheduler = BackgroundScheduler() #create a background scheduler instance
    scheduler.add_job(alert_noti,'interval',seconds = 60)# add a job to call alert noti function every 60 seconds 
    scheduler.start()#start the instance so when the server runs
    logger.info('Server starts')
    yield #when the server is actually taking requests
    scheduler.shutdown()
    logger.info('Server shuts down')

app = FastAPI(lifespan=lifespan) #retrives fastapi instance
@app.get('/')#decorator which tells it that when this path is provided activate this function
async def root(): # it will run this function when the specific path is described.# async means it can handle multiple requests at once.
    return {'message':'Stock App'}
@app.post('/users') #path params are for search, query params are for filtering. dont use path mostly post since the information is sent alongside the request body.
async def create(deliver:Delivery): 
    create_user(deliver.name,deliver.email,str(date.today()))# it is intialized in a schema instead.
    user_id = get_id(deliver.name)
    return {'name':deliver.name, 'user_id':user_id}#json is a language-independent text format used to display data.
@app.get('/users/{name}')
async def getuser_id(name:str):
    a = get_id(name)
    return {'name':name,'user_id':a}
@app.get('/user/{name}')
async def user_profile(name:str):
    a = get_id(name)
    r = retrieve_profile(a)
    return{
        'name':name,
        'email':r[len(r)-1]
    }
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
            'PnL':str(round(profit[0],2)),
            "Status": item[len(item)-1]
        }
        conta.append(p)
    return{
        'transactions':conta
    }
@app.post('/transactions')
async def new_transaction(transaction:transaction):
    id = get_id(transaction.name)
    b = add_transactions(id,transaction.Ticker,transaction.shares)
    return{
        'transaction':{
            'Name':transaction.name,
            'Ticker':transaction.Ticker,
            'Shares':transaction.shares,
            "Status": b[len(b)-1]
        }
    }
@app.delete('/transactions/{name}/{ticker}')
async def give_transaction(name:str,ticker:str):
    user_id = get_id(name)
    t_id = get_transaction_id(user_id,ticker)
    sell_transaction(user_id,t_id)
    return{
        "name":name,
        "ticker":ticker,
    }

@app.get('/alerts/{Name}')
async def get_alerts(Name:str):
    a = get_id(Name)
    lis =  view_alerts(a)
    conda = []
    for item in lis:
        p = {
            'name':Name,
            'Ticker':item[2],
            'Threshold':item[3],
            "Status":item[4]
        }
        conda.append(p)
    return{
        'alerts': conda
    }
@app.post('/alerts')
async def add_al(alert:alert):
    a = get_id(alert.name)
    add_alerts(a,alert.Ticker,alert.threshold)
    return{
        'name':alert.name,
        'Ticker':alert.Ticker,
        'Threshold':alert.threshold
    }
@app.delete('/alerts/{name}/{Ticker}')
async def remove_a(name:str,Ticker:str):
    a = get_id(name)
    remove_alerts(Ticker,a)
    return{
        'name':name,
        'Ticker':Ticker
    }
@app.exception_handler(DuplicateTickerError)
async def duplicate_exception_handler(req,exe):
    return JSONResponse(
        status_code=409,
        content = {
            "message": "Ticker already exists."
        }

    )
@app.exception_handler(TickerNotFoundError)
async def tickernotfound_handler(req,exe):
    return JSONResponse(
        status_code = 404,
        content = {
            "message": "Ticker not Found"
        }
    )
@app.exception_handler(EmptyTickerError)
async def emptyticker_handler(req,exe):
    return JSONResponse(
        status_code=422,
        content = {
            "message":"Entered an empty string for ticker"
        }
    )
@app.exception_handler(TooLongTickerError)
async def toolongticker_handler(req,exe):
    return JSONResponse(
        status_code=422,
        content = {
            "message":'Input is too long!'
        }
    )
@app.exception_handler(InavlidTickerFormatError)
async def invalidticker_handler(req,exe):
   return  JSONResponse(
        status_code=422,
        content = {
            "message":'Invalid ticker'
        }
    )
@app.exception_handler(InvalidPeriodError)
async def invalidperiod_handler(req,exe):
   return  JSONResponse(
        status_code = 400,
        content = {
            "message":'Period is too long'
        }
    )
@app.exception_handler(AlertDoesNotExist)
async def alertdoesnotexist_handler(req,exe):
   return  JSONResponse(
        status_code=404,
        content = {
            "message":"Alert is not found "
        }
    )
@app.exception_handler(DuplicateAlertError)
async def duplicate_exception_handler(req,exe):
    return JSONResponse(
        status_code= 409,
        content = {
            "message": "Alert already exists"
        }
    )
@app.exception_handler(TransactionNotFoundError)
async def transaction_Not_Found_Error(req,exe):
    return JSONResponse(
        status_code=404,
        content = {
            "message": 'This transaction has not been made'
        }
    )