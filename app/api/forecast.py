from datetime import datetime, date, timedelta

import requests
from flask import request, current_app

from app import db
from app.api import api
from app.api.helpers import geocode, reverse_geocode, daterange
from app.models.City import City
from app.models.DailyWeather import DailyWeather
from app.models.WeatherStatus import WeatherStatus


def get_forecast(city):
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
            precipitation=day.get('rain', 0),
            wind_speed=day['wind_speed'],
        )
        day_db.save_to_db()


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
            get_forecast(city)
            daily = db.session.query(DailyWeather).filter_by(city_id=city.id, date=single_date).first()
        data['forecast'].append(daily.to_day())

    return data
