from datetime import timedelta

import requests
from flask import current_app


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


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)
