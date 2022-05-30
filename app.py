import http

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


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

    # day_temp =
    # day_feels_temp =
    # night_temp =
    # night_feels_temp =
    # wind_speed =
    # humidity =
    # clouds =
    # sunset =
    # sunrise =

    def __repr__(self):
        return f'<DailyWeather {self.city_id} {self.date}>'


@app.route('/health')
def health():
    return http.HTTPStatus.OK, 'OK'


if __name__ == '__main__':
    app.run()
