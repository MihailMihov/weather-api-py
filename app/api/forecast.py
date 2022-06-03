from flask import request
from flask_cors import cross_origin

from app.api import api
from app.api.cache import get_forecast
from app.api.helpers import get_parameters, get_city


@api.route('/forecast')
@cross_origin()
def forecast():
    (city_name, lat, lon) = get_parameters(request.args)
    if city_name is None:
        return "Bad request", 400

    city = get_city(city_name, lat, lon)

    data = {
        'city': {
            'name': city.name
        },
        'forecast': get_forecast(city)
    }

    return data
