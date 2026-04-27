from fastapi import FastAPI,requests,Depends,Header,HTTPException #from staapi import the class FAST API. depends lets us pass in the authroization key before each request.
from src.main.storage import *
from pydantic import BaseModel
from src.main.Back import pnL,alert_noti,retrieve_recommendation
from src.fetch.scrape import currentP
from contextlib import asynccontextmanager
from datetime import date, datetime,time,timezone
from apscheduler.schedulers.background import BackgroundScheduler
import logging 
from jose import jwt ,JWTError
from datetime import timedelta
from fastapi.responses import JSONResponse
import os 
from dotenv import load_dotenv
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
logger = logging.getLogger(__name__)#intializes the logging instance.
logging.basicConfig(filename='status.log',encoding='utf-8',level=logging.DEBUG)# sets up the basic config. utf-8 is the character that it can have including the type.
logger.debug('First debugging statement')
class Delivery(BaseModel):
    name: str
    email:str
    password :str
     #define the schema of the network that you are working on.
class added(BaseModel):
    name: str
    Ticker: str
class transaction(BaseModel):
    Ticker:str
    shares: int
class alert(BaseModel):
    Ticker:str
    threshold:float
class login(BaseModel):
    email:str
    password: str 
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
@app.post('/login')
async def login_credentials(log:login):
    email = log.email
    password =log.password
    user = get_user_by_email(email)#retreieve by email and if it the same as the hash then create a jwt token.
    hashed_password = user[len(user)-1]
    user_id = user[0]
    check = pwd_context.verify(password,hashed_password)#verifies the login.
    if check:#only takes in utc the standard clock time i has it in the local.
        encoded_jwt = jwt.encode({"sub":str(user_id),"exp":datetime.now(timezone.utc)+timedelta(minutes=30)},SECRET_KEY,algorithm='HS256')#expirations is 30 minutes in the future.
        return{"key":encoded_jwt}#algo creates the signature, sub identifies the specific user. the secrete key is used to sign the token so it is validated.
    else:
        return JSONResponse(status_code=401,content={
            "message": "Invalid credentials" #but we need to authorizw the jwt each time after. 
        })
# this is not a valid because authroization cannot be in the header than it would be bad. it needs to be in the authroization header.
def get_current_user(authorization:str = Header(...)):
    #make sure you have now quyotes ibnn postman and authroization is in key already.
    try:
        token = authorization.split(" ")[1]#authorization actuall is bearar key so you need to remove the bearer so you take away the key.
        payload = jwt.decode(token,SECRET_KEY,algorithms=["HS256"] )#might want to allow multiple valid arguments. pass in the encoded_jwt
        return payload['sub']
    except JWTError as e:#fast api only knows http so this is the only way but jwt returns a jwt error.
       print(f"JWT ERROR: {e}")
       raise HTTPException(status_code=401)
@app.post('/users') #path params are for search, query params are for filtering. dont use path mostly post since the information is sent alongside the request body.
async def create(deliver:Delivery): 
    create_user(deliver.name,deliver.email,deliver.password,str(date.today()))# it is intialized in a schema instead.
    user_id = get_id(deliver.name)
    return {'name':deliver.name, 'user_id':user_id}#json is a language-independent text format used to display data.
@app.get('/users/{name}')
async def getuser_id(name:str):
    a = get_id(name)
    return {'name':name,'user_id':a}
@app.get('/user/{name}')
async def user_profile(name:str,user_id:str=Depends(get_current_user)):
    r = retrieve_profile(int(user_id))
    return{
        'name':name,
        'email':r[len(r)-2]
    }
@app.get('/watchlist')
async def getwatchlist(user_id : str= Depends(get_current_user)):
    watchlist = get_user(int(user_id))
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
async def add_stock(adder:added,user_id:str=Depends(get_current_user)):
    add(int(user_id),adder.Ticker,str(date.today()))
    return{
        'Ticker': adder.Ticker,
        'Date-added':str(date.today())
    }
@app.delete('/watchlist/{Ticker}')
async def delete_stock( Ticker:str,user_id:str=Depends(get_current_user)):
    remove(Ticker,int(user_id))
    return {
        'Ticker':Ticker,
        'Date-Removed': str(date.today())
    }
@app.get('/transactions')
async def user_transactions(user_id:str=Depends(get_current_user)):
    a = view_transactions(int(user_id))
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
async def new_transaction(transaction:transaction,user_id:str=Depends(get_current_user)):
    b = add_transactions(int(user_id),transaction.Ticker,transaction.shares)
    return{
        'transaction':{
            'Ticker':transaction.Ticker,
            'Shares':transaction.shares,
            "Status": "Bought"
        }
    }
@app.delete('/transactions/{ticker}')
async def give_transaction(ticker:str,user_id:str=Depends(get_current_user)):
    t_id = get_transaction_id(int(user_id),ticker)
    sell_transaction(int(user_id),t_id)
    return{
        "ticker":ticker,
    }

@app.get('/alerts')
async def get_alerts(user_id:str=Depends(get_current_user)):
    lis =  view_alerts(int(user_id))
    conda = []
    for item in lis:
        p = {
            'Ticker':item[2],
            'Threshold':item[3],
            "Status":item[4]
        }
        conda.append(p)
    return{
        'alerts': conda
    }
@app.post('/alerts')
async def add_al(alert:alert,user_id:str=Depends(get_current_user)):
    add_alerts(int(user_id),alert.Ticker,alert.threshold)
    return{
        'Ticker':alert.Ticker,
        'Threshold':alert.threshold
    }
@app.delete('/alerts/{Ticker}')
async def remove_a(Ticker:str,user_id:str=Depends(get_current_user)):
    remove_alerts(Ticker,int(user_id))
    return{
        'Ticker':Ticker
    }
@app.get('/Review/{Ticker}')
async def get_recommendation(Ticker:str,user_id:str=Depends(get_current_user)):
    watchlist = get_user(int(user_id))
    transactions = view_transactions(int(user_id))
    check_watchlist = any(row[2] == Ticker for row in watchlist) # any makes basically a one liner loop. 
    check_transactions = any(row[2] == Ticker for row in transactions)
    if  check_watchlist or check_transactions:
        statement = retrieve_recommendation(Ticker)
        return statement
    else:
        raise TickerNotFoundError('Ticker is not in watchlist or your transactions. RSI analysis cannot be made')
        

    
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