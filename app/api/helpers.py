from datetime import timedelta, datetime

from app import db
from app.api.owm import geocode, reverse_geocode
from app.models.City import City

from app import db
from app.models.DailyWeather import DailyWeather
from app.models.WeatherStatus import WeatherStatus


def get_parameters(args):
    lat = args.get('lat')
    lon = args.get('lon')
    city_name = args.get('city')
    if lat is not None and lon is not None and city_name is not None:
        city_name = None
    if city_name is not None:
        (city_name, lat, lon) = geocode(city_name)
    elif lat is not None and lon is not None:
        (city_name, lat, lon) = reverse_geocode(lat, lon)
    else:
        city_name = None

    return city_name, lat, lon


def get_city(city_name, lat, lon):
    city = db.session.query(City).filter_by(name=city_name).first()
    if city is None:
        city = City(name=city_name, lat=lat, lon=lon)
        city.save_to_db()
    return city


def source_current_weather(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather" \
          f"?appid={current_app.config['OPENWEATHERMAP_API_KEY']}" \
          f"&lat={lat}" \
          f"&lon={lon}"
    return requests.get(url).json()


def source_forecast(city):
    url = f"https://api.openweathermap.org/data/3.0/onecall" \
          f"?appid={current_app.config['OPENWEATHERMAP_API_KEY']}" \
          f"&exclude=current,hourly,minutely,alerts" \
          f"&lat={city.lat}" \
          f"&lon={city.lon}"
    response = requests.get(url).json()
    data = []
    for day in response['daily']:
        weather_status = day['weather'][0]
        weather_status_db = db.session.query(WeatherStatus).filter_by(id=weather_status['id']).first()
        if weather_status_db is None:
            weather_status_db = WeatherStatus(id=weather_status['id'],
                                              description=weather_status['description'],
                                              icon=weather_status['icon'])
            weather_status_db.save_to_db()
        day_db = DailyWeather(
            city_id=city.id,
            date=datetime.utcfromtimestamp(day['dt']),
            weather_status_id=weather_status['id'],
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
        data.append(day_db.to_day())
    return data


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)
