from app.main import bp


@bp.route('/health')
def health():
    return {}
