from fastapi import FastAPI #from staapi import the class FAST API
from src.main.storage import *
from pydantic import BaseModel

class Delivery(BaseModel):
    name: str
     #define the schema of the network that you are working on.

app = FastAPI() #retrives fastapi instance
@app.get('/')#decorator which tells it that when this path is provided activate this function
async def root(): # it will run this function when the specific path is described.# async means it can handle multiple requests at once.
    return {'message':'Stock App'}
@app.post('/users') #path params are for search, query params are for filtering. dont use path mostly post since the information is sent alongside the request body.
async def create(deliver:Delivery): 
    create_user(deliver.name,str(date.today()))# it is intialized in a schema instead.
    user_id = get_id(deliver.name)
    return {'name':deliver.name, 'user_id':user_id}#json is a language-independent text format used to display data.
