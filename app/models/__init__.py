from flask import Blueprint
from app import db

models = Blueprint('models', __name__)

from app.models import City, WeatherStatus, DailyWeather
