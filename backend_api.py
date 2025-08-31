from flask import Flask, jsonify
from flask_cors import CORS
import pymongo
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("MONGO_DB")
COLLECTION_NAME = os.getenv("MONGO_COLLECTION")

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Connect to MongoDB
client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

@app.route('/api/sensor-data', methods=['GET'])
def get_sensor_data():
    """Get all sensor data from MongoDB"""
    try:
        # Get all documents, sorted by timestamp descending
        data = list(collection.find({}, {'_id': 0}).sort('timestamp', -1))
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/latest-data', methods=['GET'])
def get_latest_data():
    """Get the latest sensor reading"""
    try:
        latest = collection.find_one({}, {'_id': 0}, sort=[('timestamp', -1)])
        return jsonify(latest)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/")
def home():
    return jsonify({"message": "Hello SoilSense API with Flask!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
