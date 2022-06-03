from datetime import timedelta

from app import db
from app.api.owm import geocode, reverse_geocode
from app.models.City import City


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


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)
