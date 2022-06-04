from datetime import datetime, date, timedelta

import requests
from flask import request, current_app

from app import db
from app.api import api
from app.api.helpers import geocode, reverse_geocode, daterange, source_forecast
from app.models.City import City
from app.models.DailyWeather import DailyWeather
from app.models.WeatherStatus import WeatherStatus


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
        'forecast': []
    }

    start_date = date.today()
    end_date = start_date + timedelta(days=5)
    for single_date in daterange(start_date, end_date):
        daily = db.session.query(DailyWeather).filter_by(city_id=city.id, date=single_date).first()
        if daily is None:
            source_forecast(city)
            daily = db.session.query(DailyWeather).filter_by(city_id=city.id, date=single_date).first()
        data['forecast'].append(daily.to_day())

    return data
