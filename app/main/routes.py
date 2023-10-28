from flask import g, request
from app.main import bp
from app.main.models import Course, Student
from .authentication import auth


@bp.route('/test')
def test():
    return {
        "message": "Testing"
    }

@bp.route('/tokens/', methods=['POST'])
def get_token():
    data = request.get_json()
    if data['email'] == '' or data['password'] == '':
        return {
            "error": "unauthorized",
            'message': 'INvalid credentials'
        }
    
    user = Student.query.filter_by(email=data['email']).first()
    if user is None or not user.verify_password(data['password']):
        return {
            "error": "unauthorized",
            'message': 'INvalid credentials'
        }
    
    return {
        'token': user.generate_auth_token(expiration=3600),
        'expiration': 3600
    }


@bp.route('/courses')
@auth.login_required
def get_courses():
    courses = Course.query.all()
    return {
        "success": True,
        "data": [course.format() for course in courses]
    }


@bp.route('/courses/<int:id>')
def get_course(id):
    course = Course.query.filter_by(id=id).first_or_404()
    formated = course.format()
    formated["modules"] = [module.format() for module in course.modules.all()]
    return {
        "success": True,
        "data": formated,
    }


@bp.route('/courses/enrolled')
def enrolled_courses():
    student = Student.query.filter_by(id=1).first()
    courses = student.courses_enrolled.all()

    return {
        "success": True,
        "data": [course.format() for course in courses]
    }
