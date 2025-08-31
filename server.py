import os
from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from dotenv import load_dotenv

# Load env variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("MONGO_DB", "IoT_DB")
COLLECTION_NAME = os.getenv("MONGO_COLLECTION", "sensor_data")

# Connect to MongoDB Atlas
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# FastAPI app
app = FastAPI()

# Data model for sensor readings
class SensorData(BaseModel):
    device_id: str
    sensor: str
    value: float
    unit: str

@app.post("/add-reading")
def add_reading(data: SensorData):
    doc = data.dict()
    collection.insert_one(doc)
    return {"status": "success", "inserted": doc}

@app.get("/get-readings")
def get_readings(limit: int = 5):
    docs = list(collection.find().sort("_id", -1).limit(limit))
    for d in docs:
        d["_id"] = str(d["_id"])  # convert ObjectId to string
    return {"readings": docs}
