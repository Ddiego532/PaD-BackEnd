from fastapi import FastAPI
import uvicorn
import os
import json 
from fastapi.middleware.cors import CORSMiddleware

FILE_PATH = os.path.dirname(os.path.realpath(__file__))
FILENAME = "all_news.json"
SCRAPPED_NEWS_PATH = os.path.join(os.path.dirname(FILE_PATH), "scraper", "output_data", FILENAME)

app = FastAPI()

# Configura CORS para permitir solicitudes desde todos los orígenes
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def welcome():
    return {"message": "Hello World"}

@app.get("/all_news/")
async def all_news():
    try:
        with open(SCRAPPED_NEWS_PATH, "+r", encoding="utf-8") as json_file:
            return json.load(json_file)
    except IOError:
        return {"error": "all_news.json file not found!"}