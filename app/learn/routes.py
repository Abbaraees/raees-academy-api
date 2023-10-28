from flask import g, request, url_for
from app.learn import bp
from app.main.models import Course, Student, db
from app.main.authentication import auth
from app.main.errors import unauthorized

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


# Enroll a user in a course
@bp.route('/courses/enroll', methods=['POST'])
def enroll():

    #Get JSON data from the request
    data = request.get_json()
    
    if data.get('course_id'):
        course = Course.query.get_or_404(data.get('course_id'))

        if course in g.current_user.courses_enrolled:
            return unauthorized("Enrollment failed. The user is already enrolled in this course.")
        
        g.current_user.courses_enrolled.append(course)
        db.session.commit()

        return {
            'url': url_for('learn.get_course', id=course.id),
            'success': True,
            'message': "User successfully enrolled in the course.",
            "course_id": course.id
        }
    
    return {
            'success': False,
            'message': "Enrollment failed. Course ID is missing in the request.",
    }


# Unenroll user from a course
@bp.route('/courses/unenroll', methods=['POST'])
def unenroll():
    data = request.get_json()

    if data.get('course_id'):
        course = Course.query.get_or_404(data.get('course_id'))

        if course in g.current_user.courses_enrolled:
            g.current_user.courses_enrolled.remove(course)
            db.session.commit()

            return {
                'success': True,
                'message': "User successfully unenrolled from the course.",
                "course_id": course.id
            }
        else:
            return {
                'success': False,
                'message': "Unenrollment failed. The user is not enrolled in this course.",
            }
    else:
        return {
            'success': False,
            'message': "Unenrollment failed. Course ID is missing in the request.",
        }


@bp.route('/courses/<int:course_id>/modules/')
def get_course_modules(course_id):
    course = Course.query.get_or_404(course_id)
    modules = course.modules.all()

    return {
        "success": True,
        "data": [module.format() for module in modules],
        "count": len(modules)
    }

@bp.route('/courses/<int:course_id>/modules/<int:module_id>')
def get_module(course_id, module_id):
    course = Course.query.get_or_404(course_id)
    module = course.modules.filter_by(id=module_id).first_or_404()

    return {
        "success": True,
        "data": module.format(),
    }

@bp.route('/courses/<int:course_id>/modules/<int:module_id>/lessons/')
def get_module_lessons(course_id, module_id):
    course = Course.query.get_or_404(course_id)
    module = course.modules.filter_by(id=module_id).first_or_404()
    lessons = module.lessons.all()

    return {
        "success": True,
        "data": [lesson.format() for lesson in lessons],
        "count": len(lessons)
    }

@bp.route('/courses/<int:course_id>/modules/<int:module_id>/lessons/<int:lesson_id>/')
def get_lesson(course_id, module_id, lesson_id):
    course = Course.query.get_or_404(course_id)
    module = course.modules.filter_by(id=module_id).first_or_404()
    lesson = module.lessons.filter_by(id=lesson_id).first_or_404()

    return {
        "success": True,
        "data": lesson.format(True),
    }
