from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB Atlas Connection
client = MongoClient("mongodb+srv://akshitamishra421:UBuVS7KHJkhOY6v5@cluster0.3crbjxf.mongodb.net/")
db = client["aded_database"]
collection = db["users"]

@app.post("/register")
async def register_user(request: Request):
    data = await request.json()
    result = collection.insert_one(data)
    return {"message": "User registered", "id": str(result.inserted_id)}
