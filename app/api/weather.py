from app.api import api
from app.api.forecast import forecast

@api.route('/weather')
def weather():
    data = {}
    current = current()
    forecast = forecast()
