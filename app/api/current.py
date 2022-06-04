from flask import request

from app.api import api
from app.api.helpers import geocode, source_current_weather


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
    response = source_current_weather(lat, lon)
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
            'icon': response['weather'][0]['icon'],
            # TODO: Implement background images for each status type
            'image': 'unimplemented'
        }
    }
    return data
