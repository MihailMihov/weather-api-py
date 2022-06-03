from flask import request

from app import db
from app.api import api
from app.api.cache import get_forecast
from app.api.owm import geocode, reverse_geocode
from app.models.City import City


@api.route('/forecast')
def forecast():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    city_name = request.args.get('city')
    if lat is not None and lon is not None and city_name is not None:
        return "Too many parameters", 400
    if city_name is not None:
        (city_name, lat, lon) = geocode(city_name)
    elif lat is not None and lon is not None:
        (city_name, lat, lon) = reverse_geocode(lat, lon)
    else:
        return "Missing required parameters", 400

    city = db.session.query(City).filter_by(name=city_name).first()
    if city is None:
        city = City(name=city_name, lat=lat, lon=lon)
        city.save_to_db()

    data = {
        'city': {
            'name': city.name
        },
        'forecast': get_forecast(city)
    }

    return data
