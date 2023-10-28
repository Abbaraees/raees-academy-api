from flask import Blueprint, g

from app.main.authentication import  auth
from app.main.errors import unauthorized

bp = Blueprint('learn', __name__)

@bp.before_request
@auth.login_required
def before_request():
    if not g.current_user:
        return unauthorized("Invalid credentials")


from app.learn import routes