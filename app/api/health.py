from app.api import api


@api.route('/health')
def health():
    return {}
