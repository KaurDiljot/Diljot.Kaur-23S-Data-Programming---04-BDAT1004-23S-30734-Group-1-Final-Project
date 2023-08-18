from flask import Flask, render_template, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Replace the connection string with your MongoDB Atlas connection string
connection_string = "mongodb+srv://diljotkaur:taj1818@weather.c8nlppu.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string)
db = client["weather_db"]
collection = db["weather_collection"]

@app.route('/')
def index():
    weather_data = collection.find_one(sort=[('_id', -1)])
    all_weather_data = list(collection.find({}, {'_id': 0}).sort('_id', -1))
    return render_template('index.html', weather_data=weather_data, all_weather_data=all_weather_data)
@app.route('/api/get_all_weather_data', methods=['GET'])
def get_all_weather_data():
    data = list(collection.find({}, {'_id': 0}))
    return jsonify(data)  # Return the data as JSON response

if __name__ == "__main__":
    app.run(debug=True)
