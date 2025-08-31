import serial
import pymongo
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("MONGO_DB")
COLLECTION_NAME = os.getenv("MONGO_COLLECTION")

# 🔹 Connect to MongoDB
client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# 🔹 Connect to Arduino serial port
# Change COM6 to your actual port (check in Arduino IDE -> Tools -> Port)
arduino = serial.Serial(port="COM6", baudrate=9600, timeout=2)
time.sleep(2)  # wait for Arduino to reset

print("✅ Connected to Arduino & MongoDB")

while True:
    try:
        line = arduino.readline().decode("utf-8").strip()
        if line:
            print("📥 Received:", line)

            # Expected format: "Temperature: 25°C | Humidity: 60% | Soil Moisture: 40%"
            try:
                parts = line.replace("°C", "").replace("%", "").split("|")
                temp = float(parts[0].split(":")[1])
                hum = float(parts[1].split(":")[1])
                soil = float(parts[2].split(":")[1])

                # Create document
                doc = {
                    "temperature": temp,
                    "humidity": hum,
                    "soil_moisture": soil,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                }

                # Insert into MongoDB
                collection.insert_one(doc)
                print("✅ Saved to MongoDB:", doc)

            except Exception as e:
                print("⚠️ Parsing error:", e)

    except KeyboardInterrupt:
        print("❌ Stopped by user")
        break
