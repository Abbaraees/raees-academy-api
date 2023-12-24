from flask import g, request
from flask_httpauth import HTTPBasicAuth
from .models import Student
from app.main import bp

auth = HTTPBasicAuth()

@auth.error_handler
def unauthorized():
    return {
        "error": "forbidden",
        "message": "Invalid credentials"
    }, 403


@auth.verify_password
def verify_password(email_or_token, password):
    authorization_header = request.headers.get('Authorization')
    
    if authorization_header is not None:
        token = authorization_header.split()[1]
        g.current_user = Student.verify_auth_token(token)
        g.token_used = True
        return g.current_user is not None

    if email_or_token == '':
        return False
    
    if password == '':
        g.current_user = Student.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None
    

    
    user = Student.query.filter_by(email=email_or_token).first()

    if not user:
        return False

    g.current_user = user
    g.token_used = False 

    return user.verify_password(password)


@bp.route('/tokens/', methods=['POST'])
def get_token():
    data = request.get_json()
    if data['email'] == '' or data['password'] == '':
        return unauthorized("Invalid credentials")
    
    user = Student.query.filter_by(email=data['email']).first()
    if user is None or not user.verify_password(data['password']):
        return unauthorized("Invalid credentials")
    
    return {
        'token': user.generate_auth_token(expiration=3600),
        'expiration': 3600
    }
