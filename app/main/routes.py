from app.main import bp
from app.main.models import Course, Student


@bp.route('/test')
def test():
    return '<h1>Testing</h1>'


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


@bp.route('/courses/enrolled')
def enrolled_courses():
    student = Student.query.filter_by(id=1).first()
    courses = student.courses_enrolled.all()

    return {
        "success": True,
        "data": [course.format() for course in courses]
    }
