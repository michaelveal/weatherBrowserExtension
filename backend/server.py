import requests
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)  # Create a Flask app

API_KEY = "342f332dd47791c622414afd6f44a7d2"  # Your OpenWeatherMap API key

# Function to get latitude and longitude from location name using Geocoding API
def get_lat_lon(location):
    location = location.strip()  # Remove any leading or trailing spaces
    # Construct the Geocoding API URL
    geocode_url = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={API_KEY}"
    response = requests.get(geocode_url)  # Make a request to the Geocoding API
    data = response.json()  # Parse the response JSON data
    
    # Print debug information
    print(f"Geocode API URL: {geocode_url}")
    print(f"Geocode API Response Status Code: {response.status_code}")
    print(f"Geocode API Response: {response.text}")
    
    if response.status_code == 200 and data:  # Check if the request was successful and data is not empty
        return data[0]['lat'], data[0]['lon']  # Return latitude and longitude
    else:
        return None, None  # Return None if coordinates could not be retrieved

# Function to get current weather data
def get_current_weather(lat, lon):
    # Construct the current weather API URL
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={API_KEY}"
    response = requests.get(weather_url)  # Make a request to the current weather API
    return response.json()  # Return the response JSON data

# Function to get 5-day weather forecast using 3-hour forecast endpoint
def get_forecast(lat, lon):
    # Construct the 5-day forecast API URL
    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid={API_KEY}"
    response = requests.get(forecast_url)  # Make a request to the forecast API
    data = response.json()  # Parse the response JSON data
    
    # Print debug information for the forecast
    print(f"Forecast API URL: {forecast_url}")
    print(f"Forecast API Response Status Code: {response.status_code}")
    print(f"Forecast API Response: {response.text}")
    
    return data  # Return the response JSON data

# Route to get current weather data
@app.route('/current_weather', methods=['GET'])
def current_weather():
    location = request.args.get('location')  # Get the location from the request arguments
    lat, lon = get_lat_lon(location)  # Get the latitude and longitude for the location
    if lat is None or lon is None:  # Check if coordinates could not be retrieved
        return jsonify({"error": "Could not retrieve location coordinates"}), 400  # Return an error response
    
    weather_data = get_current_weather(lat, lon)  # Get the current weather data
    return jsonify(weather_data)  # Return the weather data as a JSON response

# Route to get 5-day weather forecast
@app.route('/forecast', methods=['GET'])
def forecast():
    location = request.args.get('location')  # Get the location from the request arguments
    lat, lon = get_lat_lon(location)  # Get the latitude and longitude for the location
    if lat is None or lon is None:  # Check if coordinates could not be retrieved
        return jsonify({"error": "Could not retrieve location coordinates"}), 400  # Return an error response
    
    forecast_data = get_forecast(lat, lon)  # Get the forecast data
    return jsonify(forecast_data)  # Return the forecast data as a JSON response

# Main block to run the Flask app
if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app in debug mode
