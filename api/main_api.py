from fastapi import FastAPI, HTTPException
import uvicorn
import os
import json 
from fastapi.middleware.cors import CORSMiddleware
import socket

import ast
import sys
sys.path.insert(0, 'ranking')
from news_dict import get_news_dict


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

def client_program(query: str):
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    client_socket.send(query.encode())  # send message
    data = client_socket.recv(16384).decode()

    client_socket.close()  # close the connection
    return data

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


@app.get("/dict/")
def get_json():
    news_dict = get_news_dict()
    return news_dict


@app.get("/search/{query}")
def execute_query(query):
    data_str = client_program(query)
    data = ast.literal_eval(data_str)
    news_dict = get_news_dict()

    response_data = []

    for tuple_item in data:
        key = str(tuple_item[0])

        try:
            key = int(key)
        except ValueError:
            print(f"Error converting key to integer: {key}")
            continue

        if key in news_dict:
            matched_news = news_dict[key]
            response_data.append(matched_news)
        else:
            print(f"No match found for key {key}")

    return response_data


@app.get("/get_by_polarity/{polarity}")
async def get_by_polarity(polarity: str):
    with open(SCRAPPED_NEWS_PATH, "+r", encoding="utf-8") as json_file:
        noticias = json.load(json_file)
    results = [item for item in noticias if item["polarity"] == polarity]
    if not results:
        raise HTTPException(status_code=404, detail="No se encontraron elementos con esa polaridad")
    return results


uvicorn.run(app, host="0.0.0.0", port=12000)