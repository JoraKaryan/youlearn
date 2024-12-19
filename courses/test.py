import requests

def get_weather(city):
    """
    Fetch current weather information for a given city using OpenWeatherMap API
    Note: You'll need to sign up for a free API key at https://openweathermap.org/
    """
    # IMPORTANT: Replace 'YOUR_API_KEY' with your actual OpenWeatherMap API key
    API_KEY = 'YOUR_API_KEY'
    BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'
    
    # Parameters for the API request
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'  # Use metric for Celsius
    }
    
    try:
        # Send GET request to the API
        response = requests.get(BASE_URL, params=params)
        
        # Raise an exception for bad responses
        response.raise_for_status()
        
        # Parse the JSON response
        weather_data = response.json()
        
        # Extract relevant information
        temp = weather_data['main']['temp']
        feels_like = weather_data['main']['feels_like']
        description = weather_data['weather'][0]['description']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']
        
        # Format and return the weather information
        return f"""
Weather in {city}:
Temperature: {temp}°C
Feels Like: {feels_like}°C
Conditions: {description.capitalize()}
Humidity: {humidity}%
Wind Speed: {wind_speed} m/s
"""
    
    except requests.RequestException as e:
        return f"Error fetching weather data: {e}"

def main():
    # Example usage
    city = input("Enter a city name: ")
    print(get_weather(city))

if __name__ == "__main__":
    main()
