from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
async def welcome():
    return {"message": "Hello World"}