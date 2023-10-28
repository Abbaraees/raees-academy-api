from flask import g, request
from app.main import bp
from app.main.models import Course, Student
from .authentication import auth
from .errors import unauthorized


@bp.route('/test')
def test():
    return {
        "message": "Testing"
    }
