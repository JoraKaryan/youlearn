import requests
import json

def get_weather_openweathermap(city, api_key):
    """
    Fetch weather using OpenWeatherMap API
    Requires free API key from openweathermap.org
    """
    base_url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        return f"""OpenWeatherMap Weather Report:
City: {data['name']}
Temperature: {data['main']['temp']}°C
Feels Like: {data['main']['feels_like']}°C
Condition: {data['weather'][0]['description']}
Humidity: {data['main']['humidity']}%
Wind Speed: {data['wind']['speed']} m/s"""
    
    except Exception as e:
        return f"OpenWeatherMap API Error: {str(e)}"

def get_weather_wttr(city):
    """
    Fetch weather using wttr.in (no API key required)
    """
    try:
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        current = data['current_condition'][0]
        
        return f"""wttr.in Weather Report:
City: {city}
Temperature: {current['temp_C']}°C
Feels Like: {current['FeelsLikeC']}°C
Condition: {current['weatherDesc'][0]['value']}
Humidity: {current['humidity']}%
Wind Speed: {current['windspeedKmph']} km/h"""
    
    except Exception as e:
        return f"wttr.in API Error: {str(e)}"

def get_weather_weatherapi(city, api_key):
    """
    Fetch weather using WeatherAPI (free tier available)
    Requires free API key from weatherapi.com
    """
    base_url = 'http://api.weatherapi.com/v1/current.json'
    params = {
        'key': api_key,
        'q': city
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        return f"""WeatherAPI Report:
City: {data['location']['name']}
Temperature: {data['current']['temp_c']}°C
Feels Like: {data['current']['feelslike_c']}°C
Condition: {data['current']['condition']['text']}
Humidity: {data['current']['humidity']}%
Wind Speed: {data['current']['wind_kph']} km/h"""
    
    except Exception as e:
        return f"WeatherAPI Error: {str(e)}"

def main():
    print("Weather Information Retrieval")
    print("----------------------------")
    city = input("Enter city name: ")
    
    print("\nAttempting multiple weather sources:")
    
    # Option 1: wttr.in (No API key)
    print("\n1. Free wttr.in Service:")
    print(get_weather_wttr(city))
    
    # Note about other methods requiring API keys
    print("\nNote: For more reliable results, you can:")
    print("1. Get a free API key from OpenWeatherMap")
    print("2. Get a free API key from WeatherAPI")
    print("3. Replace the placeholders in the script")

if __name__ == "__main__":
    main()