from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import sys

from app import db


courses_enrolled = db.Table('courses_enrolled',
    db.Column('course_id', db.ForeignKey('course.id')),
    db.Column('student_id', db.ForeignKey('student.id')),
    db.Column('completed', db.Boolean, default=False)
)

# Create a Many-to-Many relation b/w students and lessons
lessons_completed = db.Table('lessons_completed',
    db.Column('lesson_id', db.ForeignKey('lesson.id')),
    db.Column('student_id', db.ForeignKey('student.id')),
    db.Column('completed', db.Boolean, default=False)
)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String)

    courses_enrolled = db.relationship('Course',
        secondary='courses_enrolled',
        primaryjoin=(courses_enrolled.c.student_id == id),
        backref=db.backref('students', lazy='dynamic'),
        lazy='dynamic'
    )

    lessons_completed = db.relationship('Lesson',
        secondary='lessons_completed',
        primaryjoin=(lessons_completed.c.student_id == id),
        backref=db.backref('students', lazy='dynamic'),
        lazy='dynamic'
    )

    def hash_password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def generate_auth_token(self, expiration):
        return jwt.encode(
            {"id": self.id, 'exp': datetime.datetime.now() + datetime.timedelta(seconds=expiration)},
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )

    @staticmethod
    def verify_auth_token(token):
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        except:
            print(sys.exc_info())
            return None
        
        return Student.query.get(data['id'])


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(255), nullable=False)
    long_description = db.Column(db.String, nullable=False)
    short_description = db.Column(db.String(255), nullable=False)
    modules = db.relationship('Module', backref='course', lazy='dynamic')

    def format(self):
        return {
            "id": self.id,
            "name": self.name,
            "long_description": self.long_description,
            "short_description": self.short_description
        }


    def __repr__(self):
        return f'<Course: {self.name}>'


class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    lessons = db.relationship('Lesson', backref='module', lazy='dynamic')

    def format(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }

    def __repr__(self):
        return f'<Module: {self.name}>'


class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(255), nullable=False)
    content = db.Column(db.String, nullable=False)
    status = db.Column(db.Boolean, nullable=False, default=False)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))

    def format(self):
        return {
            "id": self.id,
            "name": self.name,
            "content": self.content,
            "status": self.status
        }

    def __repr__(self):
        return f'<Lesson: {self.name}>'

