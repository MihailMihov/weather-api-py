from app.models import db
from app.models.WeatherStatus import WeatherStatus


class DailyWeather(db.Model):
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), primary_key=True, nullable=False)
    date = db.Column(db.Date, primary_key=True, nullable=False)
    weather_status_id = db.Column(db.Integer, db.ForeignKey('weather_status.id'), nullable=False)
    # weather_status = db.relationship('WeatherStatus', )
    day_temp = db.Column(db.Float)
    day_temp_feels = db.Column(db.Float)
    night_temp = db.Column(db.Float)
    night_temp_feels = db.Column(db.Float)
    clouds = db.Column(db.Integer)
    humidity = db.Column(db.Integer)
    precipitation = db.Column(db.Float)
    wind_speed = db.Column(db.Float)
    sunset = db.Column(db.DateTime)
    sunrise = db.Column(db.DateTime)

    def __repr__(self):
        return f'<DailyWeather {self.city_id} {self.date}>'

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def to_day(self):
        weather_status = WeatherStatus.query(self.weather_status_id).get()
        data = {
            'day': {
                'temp': self.day_temp,
                'temp_feels_like': self.day_temp_feels
            },
            'night': {
                'temp': self.night_temp,
                'temp_feels_like': self.night_temp_feels
            },
            'other': {
                'humidity': self.humidity,
                'clouds': self.clouds,
                'precipitation': self.precipitation,
                'wind_speed': self.wind_speed
            },
            'status': {
                'description': weather_status.description,
                'icon': weather_status.icon,
                'background': weather_status.background
            },
            'sunrise': self.sunrise,
            'sunset': self.sunset
        }
        return data
