import requests
import psycopg2

# PostgreSQL Database Connection
db_config = {
    'host': 'localhost',           # Change to your PostgreSQL host
    'user': 'postgres',       # Replace with your PostgreSQL username
    'password': 'postgres',   # Replace with your PostgreSQL password
    'database': 'weather_db'       # Replace with your database name
}

# Connect to PostgreSQL
connection = psycopg2.connect(**db_config)
cursor = connection.cursor()

# OpenWeather API Key
API_KEY = "677a7b68cc7faf7f866737c8aa306185"  # Replace with your OpenWeatherMap API key

# Function to get weather data from OpenWeather API
def get_weather(city_name, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city_name,
        'appid': api_key,
        'units': 'metric'  # Use 'imperial' for Fahrenheit
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        weather = {
            'city': data['name'],
            'temperature': data['main']['temp'],  # Current temperature in Celsius
            'description': data['weather'][0]['description'],  # General weather condition
            'humidity': data['main']['humidity'],  # Humidity percentage
            'wind_speed': data['wind']['speed'],  # Wind speed in m/s
            'clouds': data['clouds']['all'],  # Cloud cover percentage
            'visibility': data.get('visibility', 'N/A'),  # Visibility in meters
            'precipitation': data.get('rain', {}).get('1h', 0),  # Rainfall in last hour (if any)
            'pressure': data['main']['pressure']  # Atmospheric pressure in hPa
        }
        return weather
    else:
        return {"error": response.json().get("message", "An error occurred")}

# Function to save weather data to PostgreSQL
def save_weather_to_db(city, api_key):
    # Get weather data for the city
    weather_info = get_weather(city, api_key)

    if 'error' in weather_info:
        print(weather_info['error'])
    else:
        # Insert weather data into PostgreSQL database
        insert_query = """
        INSERT INTO weather_data (city, temperature, description, humidity, wind_speed, clouds, visibility, precipitation, pressure)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            weather_info['city'],
            weather_info['temperature'],
            weather_info['description'],
            weather_info['humidity'],
            weather_info['wind_speed'],
            weather_info['clouds'],
            weather_info['visibility'],
            weather_info['precipitation'],
            weather_info['pressure']
        ))
        connection.commit()

        print(f"Weather data for '{weather_info['city']}' inserted into the database.")

# Main function to execute the weather data fetching and saving to DB
def main():
    city = input("Enter city name: ")  # Take city name as input

    # Save weather data to PostgreSQL
    save_weather_to_db(city, API_KEY)

# Run the main function
if __name__ == "__main__":
    main()

    # Close the PostgreSQL connection
    cursor.close()
    connection.close()
