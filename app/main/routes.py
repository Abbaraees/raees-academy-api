from app.main import bp


@bp.route('/test')
def test():
    return '<h1>Testing</h1>'