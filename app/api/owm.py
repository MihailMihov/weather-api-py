from datetime import datetime

import requests
from flask import current_app

from app import db
from app.models.DailyWeather import DailyWeather
from app.models.WeatherStatus import WeatherStatus


def geocode(city):
    url = f"https://api.openweathermap.org/geo/1.0/direct" \
          f"?appid={current_app.config['OPENWEATHERMAP_API_KEY']}" \
          f"&q={city}" \
          f"&limit=1"
    response = requests.get(url).json()
    return response[0]['name'], response[0]['lat'], response[0]['lon']


def reverse_geocode(lat, lon):
    url = f"https://api.openweathermap.org/geo/1.0/reverse" \
          f"?appid={current_app.config['OPENWEATHERMAP_API_KEY']}" \
          f"&lat={lat}" \
          f"&lon={lon}" \
          f"&limit=1"
    response = requests.get(url).json()
    return response[0]['name'], response[0]['lat'], response[0]['lon']


def source_current_weather(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather" \
          f"?appid={current_app.config['OPENWEATHERMAP_API_KEY']}" \
          f"&lat={lat}" \
          f"&lon={lon}"
    response = requests.get(url).json()

    current = {
        'temp': {
            'temp': response['main']['temp'],
            'feels_like': response['main']['feels_like']
        },
        'other': {
            'humidity': response['main']['humidity'],
            'clouds': response['clouds']['all'],
            'wind_speed': response['wind']['speed'],
        },
        'status': {
            'description': response['weather'][0]['description'],
            # TODO: Return full link for icon field
            'icon': response['weather'][0]['icon'],
            # TODO: Implement background images for each status type
            'image': 'unimplemented'
        }
    }

    return current


def source_forecast(city):
    url = f"https://api.openweathermap.org/data/3.0/onecall" \
          f"?appid={current_app.config['OPENWEATHERMAP_API_KEY']}" \
          f"&exclude=current,hourly,minutely,alerts" \
          f"&lat={city.lat}" \
          f"&lon={city.lon}"
    response = requests.get(url).json()
    days = response['daily']
    for day in days:
        weather_status_id = day['weather'][0]['id']
        weather_status = db.session.query(WeatherStatus).filter_by(id=weather_status_id).first()
        if weather_status is None:
            weather_status = WeatherStatus(id=day['weather'][0]['id'],
                                           description=day['weather'][0]['description'],
                                           icon=day['weather'][0]['icon'])
            weather_status.save_to_db()
        day_db = DailyWeather(
            city_id=city.id,
            date=datetime.utcfromtimestamp(day['dt']),
            weather_status_id=weather_status_id,
            day_temp=day['temp']['day'],
            day_temp_feels=day['feels_like']['day'],
            night_temp=day['temp']['night'],
            night_temp_feels=day['feels_like']['night'],
            clouds=day['clouds'],
            humidity=day['humidity'],
            precipitation=day.get('pop', 0),
            wind_speed=day['wind_speed'],
        )
        day_db.save_to_db()
