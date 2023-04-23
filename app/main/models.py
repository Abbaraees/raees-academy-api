from app import db


courses_enrolled = db.Table('courses_enrolled',
    db.Column('course_id', db.ForeignKey('course.id')),
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

