from app.api import api


@api.route('/weather')
def weather():
    return {}
