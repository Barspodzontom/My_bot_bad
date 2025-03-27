import openmeteo_requests
import time
import requests_cache
import pandas as pd
from retry_requests import retry
#from handlers.fsm_weather import *


params = {'latitude':47.31, 'longitude':37.89,
"current": ["temperature_2m",
                 "is_day",
                   "precipitation",
                     "surface_pressure",
                       "wind_speed_10m",
                         "wind_direction_10m"],
    "forecast_days": 3,
    "hourly": "temperature_2m"}

long = params['longitude']
def get_local_time_from_longitude(long):
  utc_offset_hours = round(long / 15)
  current_timestamp = time.time()
  adjusted_timestamp = current_timestamp + (utc_offset_hours * 3600)
  local_time = time.gmtime(adjusted_timestamp)

  return time.strftime("%Y-%m-%d %H:%M:%S", local_time)


def meteo():
  # Setup the Open-Meteo API client with cache and retry on error
  cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
  retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
  openmeteo = openmeteo_requests.Client(session = retry_session)

  url = "https://api.open-meteo.com/v1/forecast"

  responses = openmeteo.weather_api(url, params=params)

  # Process first location. Add a for-loop for multiple locations or weather models
  response = responses[0]

  # Current values. The order of variables needs to be the same as requested.
  current = response.Current()

  current_temperature_2m = current.Variables(0).Value()

  current_is_day = current.Variables(1).Value()

  current_precipitation = current.Variables(2).Value()

  current_surface_pressure = current.Variables(3).Value()

  current_wind_speed_10m = current.Variables(4).Value()

  current_wind_direction_10m = current.Variables(5).Value()

  return (f"""\nТекущее время: {get_local_time_from_longitude(params['longitude'])}\n
  Координаты: {response.Latitude()}°N {response.Longitude()}°E\n
  Высота над уровнем моря: {response.Elevation()} m asl\n
  Текущая температура: {current_temperature_2m:0.2f} °C\n
  Время суток: {'День' if current_is_day else 'Ночь' }\n  
  Количество осадков: {current_precipitation} mm\n
  Атмосферное давление: {int(current_surface_pressure*100/133.322)} bar\n
  Скорость ветра: {current_wind_speed_10m:0.1f} м/с\n
  Направление ветра: {current_wind_direction_10m:0.2f}°\n\n""")


print(meteo())