import requests
import pandas as pd
import matplotlib.pyplot as plt

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
            'wind_direction': data['wind']['deg'],  # Wind direction in degrees
            'clouds': data['clouds']['all'],  # Cloud cover percentage
            'visibility': data.get('visibility', 'N/A'),  # Visibility in meters
            'precipitation': data.get('rain', {}).get('1h', 0),  # Rainfall in last hour (if any)
            'pressure': data['main']['pressure'],  # Atmospheric pressure in hPa
            'weather_alerts': data.get('alerts', 'No alerts')  # Severe weather alerts (if any)
        }
        return weather
    else:
        return {"error": response.json().get("message", "An error occurred")}

def fetch_and_print_weather(city, api_key):
    weather_info = get_weather(city, api_key)

    if 'error' in weather_info:
        print(weather_info['error'])
    else:
        print(f"Weather in {weather_info['city']}:")
        print(f"Temperature: {weather_info['temperature']}°C")
        print(f"Description: {weather_info['description']}")
        print(f"Humidity: {weather_info['humidity']}%")
        print(f"Wind Speed: {weather_info['wind_speed']} m/s")
        print(f"Wind Direction: {weather_info['wind_direction']}°")
        print(f"Cloud Cover: {weather_info['clouds']}%")
        print(f"Visibility: {weather_info['visibility']} meters")
        print(f"Precipitation (last hour): {weather_info['precipitation']} mm")
        print(f"Pressure: {weather_info['pressure']} hPa")
        print(f"Weather Alerts: {weather_info['weather_alerts']}")
        print("\n")  # Adds a line break for better readability

          # Convert the weather data to a DataFrame
        df = pd.DataFrame([weather_info])
        print("\nWeather Data as DataFrame:")
        print(df)

        # Save weather data to CSV
        df.to_csv(f'{city}_weather_data.csv', index=False)
        print(f"\nWeather data for {city} saved as CSV.")

          # Visualize weather data
        features = ['Temperature (°C)', 'Humidity (%)', 'Wind Speed (m/s)']
        values = [weather_info['temperature'], weather_info['humidity'], weather_info['wind_speed']]

        # Create a bar chart for weather data
        plt.figure(figsize=(8, 5))
        plt.bar(features, values, color='skyblue', edgecolor='black')

        # Add title and labels
        plt.title(f"Weather Data for '{weather_info['city']}'")
        plt.ylabel('Value')

        # Show the plot
        plt.show()

def main():
    API_KEY = "677a7b68cc7faf7f866737c8aa306185"  # Replace with your OpenWeatherMap API key
    city = input("Enter city name: ")  # Take city name as input

    # Fetch and print weather information for the entered city
    fetch_and_print_weather(city, API_KEY)

if __name__ == "__main__":
    main()
