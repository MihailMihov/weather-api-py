from app import db


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f'<City {self.name}>'


class WeatherStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, unique=True, nullable=False)
    icon = db.Column(db.Text, nullable=False)
    background = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<WeatherStatus {self.description}>'


class DailyWeather(db.Model):
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), primary_key=True, nullable=False)
    date = db.Column(db.Date, primary_key=True, nullable=False)
    weather_status_id = db.Column(db.Integer, db.ForeignKey('weather_status.id'), nullable=False)

    day_temp = db.Column(db.Float)
    day_temp_feels = db.Column(db.Float)
    night_temp = db.Column(db.Float)
    night_temp_feels = db.Column(db.Float)
    clouds = db.Column(db.Integer)
    humidity = db.Column(db.Integer)
    wind_speed = db.Column(db.Float)
    sunset = db.Column(db.DateTime)
    sunrise = db.Column(db.DateTime)

    def __repr__(self):
        return f'<DailyWeather {self.city_id} {self.date}>'
