from flask import g
from app.learn import bp
from app.main.models import Course, Student
from app.main.authentication import auth

@bp.route('/courses')
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


@bp.route('/courses/my')
def enrolled_courses():
    courses = g.current_user.courses_enrolled.all()

    return {
        "success": True,
        "data": [course.format() for course in courses],
        "count": len(courses)
    }
