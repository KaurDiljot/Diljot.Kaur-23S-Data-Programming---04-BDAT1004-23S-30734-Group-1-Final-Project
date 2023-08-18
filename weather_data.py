import requests
import time
from pymongo import MongoClient 
import datetime

API_KEY = "ee2b9cfa5010e247ed73be17fe5ee81d"

def acquire_and_store_weather(location):
    # Acquire Data from the OpenWeatherMap API
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        temperature = data.get("main", {}).get("temp", "N/A")
        temperature_feels_like = data.get("main", {}).get("feels_like", "N/A")
        humidity = data.get("main", {}).get("humidity", "N/A")
        wind_speed = data.get("wind", {}).get("speed", "N/A")
        weather_description = data.get("weather", [])[0].get("description", "N/A") 
        
        # Store Data in MongoDB
        client = MongoClient("mongodb+srv://diljotkaur:taj1818@weather.c8nlppu.mongodb.net/?retryWrites=true&w=majority")
        db = client["weather_db"]
        collection = db["weather_collection"]
        current_time = datetime.datetime.now() 
        weather_document = {
            "location": location,
            "temperature": temperature,
            "temperature_feels_like":temperature_feels_like,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "weather_description" :weather_description,
            "recorded_at": datetime.datetime.now()
        }
        
        collection.insert_one(weather_document)
        print(f"Weather data for {location} stored in the database.")
    else:
        print("Failed to fetch weather data.")

def main():
    while True:
        location = "Barrie"  # Location: Barrie, Ontario, Canada
        acquire_and_store_weather(location)
        time.sleep(24 * 60 * 60)  # Wait for 24 hours
if __name__ == "__main__":
    main()