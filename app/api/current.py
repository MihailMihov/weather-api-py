import requests
from flask import current_app, request

from app.api import api


def get_current_weather(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather" \
          f"?appid={current_app.config['OPENWEATHERMAP_API_KEY']}" \
          f"&lat={lat}" \
          f"&lon={lon}"
    return requests.get(url).json()


@api.route('/current')
def current():
    if 'lat' not in request.args or 'lon' not in request.args:
        return "Record not found", 400
    return get_current_weather(request.args.get('lat'), request.args.get('lon'))
