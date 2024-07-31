from langchain.agents import tool
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from typing import Dict, Any, Optional

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

@tool
def get_weather_data(latitude: float, longitude: float) -> Dict[str, Any]:
    """
    Fetches weather data from the Open-Meteo API and returns the weather details as a dictionary.
    
    Args:
    latitude (float): The latitude of the location
    longitude (float): The longitude of the location
    
    Returns:
    Dict[str, Any]: A dictionary containing current weather data
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "is_day", "precipitation", "rain", "showers", "snowfall", "weather_code", "cloud_cover", "pressure_msl", "surface_pressure", "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m"],
        "forecast_days": 1
    }
    try:
        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]
        current = response.Current()
        current_weather = {
          "temperature_2m": current.Variables(0).Value(),
          "relative_humidity_2m": current.Variables(1).Value(),
          "apparent_temperature": current.Variables(2).Value(),
          "is_day": current.Variables(3).Value(),
          "precipitation": current.Variables(4).Value(),
          "rain": current.Variables(5).Value(),
          "showers": current.Variables(6).Value(),
          "snowfall": current.Variables(7).Value(),
          "weather_code": current.Variables(8).Value(),
          "cloud_cover": current.Variables(9).Value(),
          "pressure_msl": current.Variables(10).Value(),
          "surface_pressure": current.Variables(11).Value(),
          "wind_speed_10m": current.Variables(12).Value(),
          "wind_direction_10m": current.Variables(13).Value(),
          "wind_gusts_10m": current.Variables(14).Value()
        }
        return current_weather
    except Exception as e:
        return {"error": str(e)}

def get_weather_info(info_type: str, latitude: float, longitude: float) -> str:
    """
    Helper function to get specific weather information.
    
    Args:
    info_type (str): The type of weather information to retrieve
    latitude (float): The latitude of the location
    longitude (float): The longitude of the location
    
    Returns:
    str: Formatted weather information
    """
    weather_data = get_weather_data.invoke({"latitude": latitude,"longitude": longitude})
    if "error" in weather_data:
        return f"Error fetching weather data: {weather_data['error']}"
    
    info_mapping = {
        "temperature": ("temperature_2m", "Temperature", "°C"),
        "humidity": ("relative_humidity_2m", "Relative Humidity", "%"),
        "apparent_temperature": ("apparent_temperature", "Apparent Temperature", "°C"),
        "precipitation": ("precipitation", "Precipitation", "mm"),
        "rain": ("rain", "Rain", "mm"),
        "showers": ("showers", "Showers", "mm"),
        "snowfall": ("snowfall", "Snowfall", "cm"),
        "weather_code": ("weather_code", "Weather Code", ""),
        "cloud_cover": ("cloud_cover", "Cloud Cover", "%"),
        "pressure_msl": ("pressure_msl", "Pressure at Mean Sea Level", "hPa"),
        "surface_pressure": ("surface_pressure", "Surface Pressure", "hPa"),
        "wind_speed": ("wind_speed_10m", "Wind Speed at 10m", "km/h"),
        "wind_direction": ("wind_direction_10m", "Wind Direction at 10m", "°"),
        "wind_gusts": ("wind_gusts_10m", "Wind Gusts at 10m", "km/h")
    }
    
    if info_type in info_mapping:
        key, label, unit = info_mapping[info_type]
        return f"{label}: {weather_data.get(key, 'N/A')}{unit}"
    elif info_type == "day_night":
        return "It is currently day." if weather_data.get("is_day", 0) else "It is currently night."
    else:
        return f"Unknown information type: {info_type}"

@tool
def get_temperature(latitude: float, longitude: float) -> str:
    """
    Returns the temperature at 2 meters height for the specified location.
    """
    return get_weather_info("temperature", latitude, longitude)

@tool
def get_relative_humidity(latitude: float, longitude: float) -> str:
    """
    Returns the relative humidity at 2 meters height for the specified location.
    """
    return get_weather_info("humidity", latitude, longitude)

@tool
def get_apparent_temperature(latitude: float, longitude: float) -> str:
    """
    Returns the apparent temperature for the specified location.
    """
    return get_weather_info("apparent_temperature", latitude, longitude)

@tool
def get_day_or_night(latitude: float, longitude: float) -> str:
    """
    Returns whether it is currently day or night at the specified location.
    """
    return get_weather_info("day_night", latitude, longitude)

@tool
def get_precipitation(latitude: float, longitude: float) -> str:
    """
    Returns the precipitation level for the specified location.
    """
    return get_weather_info("precipitation", latitude, longitude)

@tool
def get_rain(latitude: float, longitude: float) -> str:
    """
    Returns the rain level for the specified location.
    """
    return get_weather_info("rain", latitude, longitude)

@tool
def get_showers(latitude: float, longitude: float) -> str:
    """
    Returns the showers level for the specified location.
    """
    return get_weather_info("showers", latitude, longitude)

@tool
def get_snowfall(latitude: float, longitude: float) -> str:
    """
    Returns the snowfall level for the specified location.
    """
    return get_weather_info("snowfall", latitude, longitude)

@tool
def get_weather_code(latitude: float, longitude: float) -> str:
    """
    Returns the weather code for the specified location.
    """
    return get_weather_info("weather_code", latitude, longitude)

@tool
def get_cloud_cover(latitude: float, longitude: float) -> str:
    """
    Returns the cloud cover percentage for the specified location.
    """
    return get_weather_info("cloud_cover", latitude, longitude)

@tool
def get_pressure_msl(latitude: float, longitude: float) -> str:
    """
    Returns the pressure at mean sea level for the specified location.
    """
    return get_weather_info("pressure_msl", latitude, longitude)

@tool
def get_surface_pressure(latitude: float, longitude: float) -> str:
    """
    Returns the surface pressure for the specified location.
    """
    return get_weather_info("surface_pressure", latitude, longitude)

@tool
def get_wind_speed(latitude: float, longitude: float) -> str:
    """
    Returns the wind speed at 10 meters height for the specified location.
    """
    return get_weather_info("wind_speed", latitude, longitude)

@tool
def get_wind_direction(latitude: float, longitude: float) -> str:
    """
    Returns the wind direction at 10 meters height for the specified location.
    """
    return get_weather_info("wind_direction", latitude, longitude)

@tool
def get_wind_gusts(latitude: float, longitude: float) -> str:
    """
    Returns the wind gusts at 10 meters height for the specified location.
    """
    return get_weather_info("wind_gusts", latitude, longitude)

@tool
def get_full_weather_report(latitude: float, longitude: float) -> str:
    """
    Returns a full weather report for the specified location.
    """
    weather_data = get_weather_data.invoke({"latitude": latitude,"longitude": longitude})
    if "error" in weather_data:
        return f"Error fetching weather data: {weather_data['error']}"
    
    report = get_weather_data.invoke({"latitude": latitude,"longitude": longitude})
    return str(report)

if __name__ == "__main__":
    print(get_temperature.invoke({"latitude": 58.1,"longitude": 47.5}))
    print(get_day_or_night.invoke({"latitude": 58.1,"longitude": 47.5}))
    print(get_relative_humidity.invoke({"latitude": 58.1,"longitude": 47.5}))
    print(get_full_weather_report.invoke({"latitude": 58.1,"longitude": 47.5}))
    print(get_apparent_temperature.invoke({"latitude": 58.1, "longitude": 47.5}))
    print(get_precipitation.invoke({"latitude": 58.1, "longitude": 47.5}))
    print(get_rain.invoke({"latitude": 58.1, "longitude": 47.5}))
    print(get_showers.invoke({"latitude": 58.1, "longitude": 47.5}))
    print(get_snowfall.invoke({"latitude": 58.1, "longitude": 47.5}))
    print(get_weather_code.invoke({"latitude": 58.1, "longitude": 47.5}))
    print(get_cloud_cover.invoke({"latitude": 58.1, "longitude": 47.5}))
    print(get_pressure_msl.invoke({"latitude": 58.1, "longitude": 47.5}))
    print(get_surface_pressure.invoke({"latitude": 58.1, "longitude": 47.5}))
    print(get_wind_speed.invoke({"latitude": 58.1, "longitude": 47.5}))
    print(get_wind_direction.invoke({"latitude": 58.1, "longitude": 47.5}))
    print(get_wind_gusts.invoke({"latitude": 58.1, "longitude": 47.5}))
