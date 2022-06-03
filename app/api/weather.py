from flask import request

from app.api import api
from app.api.cache import get_forecast
from app.api.helpers import get_parameters, get_city
from app.api.owm import source_current_weather


@api.route('/weather')
def weather():
    (city_name, lat, lon) = get_parameters(request.args)
    if city_name is None:
        return "Bad request", 400

    city = get_city(city_name, lat, lon)

    data = {
        'city': {
            'name': city.name
        },
        'current': source_current_weather(lat, lon),
        'forecast': get_forecast(city)
    }
    return data
