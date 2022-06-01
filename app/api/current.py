import requests
from flask import current_app, request

from app.api import api
from app.api.helpers import geocode


def get_current_weather(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather" \
          f"?appid={current_app.config['OPENWEATHERMAP_API_KEY']}" \
          f"&lat={lat}" \
          f"&lon={lon}"
    return requests.get(url).json()


@api.route('/current')
def current():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    city = request.args.get('city')
    if lat is None or lon is None:
        if city is None:
            return "Missing required parameters", 400
        else:
            (lat_, lon_) = geocode(city)
            lat = lat_
            lon = lon_
    response = get_current_weather(lat, lon)
    data = {
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
            'item': response['weather'][0]['icon'],
            # TODO: Implement background images for each status type
            'image': 'unimplemented'
        }
    }
    return data
