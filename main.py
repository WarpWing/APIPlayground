from typing import Optional
from fastapi import Depends, FastAPI, Request, Form, HTTPException, status
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse
import redis 
import time
import markdown
import jinja2
import aiofiles

# Use this command to start the application: uvicorn main:app --host 0.0.0.0 --port 5050
# Misc array of Variables and Class Instances
app = FastAPI()
cache = redis.Redis(host='0.0.0.0', port=6300)
templates = Jinja2Templates(directory='static/')

def get_hit_count(): # Hit Counter for Visit. Stored in Redis. Should Revamp Hit-Counter as Retries should be exponential.
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.get('/')
def main(request: Request): # This code makes no sense don't worry. This is some experimental stuff for importing markdown into FastAPI
    with open("README.md", "r", encoding="utf-8") as input_file:
        text = input_file.read()
    html = markdown.markdown(text)
    return templates.TemplateResponse("main.html", {"request": request})

@app.get('/hits') # Main Function
def hello():
    count = get_hit_count()
    hits = '{"hitCounter":"%d"}' % (count)
    return hits # I need to find a way to insert JSON somehow into this.... will work on

@app.get('/kfc') # I need to figure out how to get JSON into Redis. I don't understand the Redis Docs but we learn somehome :)
def kfc():
    kfc = {"Salt" : "2/3 Tablespoon","Thyme" : "1/2 Tablespoon","Basil" :  "1/2 Tablespoon","Oregano" : "1/3 Tablespoon","Celery Salt" : "1/3 Tablespoon","Black Pepper": "1 Tablespoon","Dry Mustard" : "1 Tablespoon","Paprika" : "3 Tablespoon","Garlic Salt" : "2 Tablespoon","Ground Ginger" : "1 Tablespoon","White Pepper" : "3 Tablespoon","MSG" : "1 Teaspoon"}
    return kfc




