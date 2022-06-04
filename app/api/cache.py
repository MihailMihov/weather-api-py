from datetime import date, timedelta

from app import db
from app.api.helpers import daterange
from app.api.owm import source_forecast
from app.models.DailyWeather import DailyWeather


def get_forecast(city):
    forecast = []
    start_date = date.today()
    end_date = start_date + timedelta(days=5)
    for single_date in daterange(start_date, end_date):
        daily = db.session.query(DailyWeather).filter_by(city_id=city.id, date=single_date).first()
        if daily is None:
            source_forecast(city)
            daily = db.session.query(DailyWeather).filter_by(city_id=city.id, date=single_date).first()
        forecast.append(daily.to_day())
    return forecast
