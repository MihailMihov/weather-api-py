import requests
from flask import request, current_app

from app.main import main


@main.route('/health')
def health():
    return {}


def get_current_weather(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather" \
          f"?appid={current_app.config['OPENWEATHERMAP_API_KEY']}" \
          f"&lat={lat}" \
          f"&lon={lon}"
    return requests.get(url).json()


@main.route('/current')
def current():
    if 'lat' not in request.args or 'lon' not in request.args:
        return "Record not found", status.HTTP_400_BAD_REQUEST
    return get_current_weather(request.args.get('lat'), request.args.get('lon'))
