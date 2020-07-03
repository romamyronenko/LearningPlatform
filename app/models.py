from werkzeug.security import generate_password_hash
from app import db


class Role(db.Model):
    name = db.Column(db.VARCHAR(30), primary_key=True)

    users = db.relationship('User', backref='role', lazy='dynamic')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.VARCHAR(30), unique=True)
    name = db.Column(db.VARCHAR(255))
    password = db.Column(db.String(94))
    role = db.Column(db.VARCHAR(30), db.ForeignKey(Role.name))

    publications = db.relationship('Publication', backref='publication_teacher', lazy='dynamic')
    groups = db.relationship('Group', backref='group_teacher', lazy='dynamic')
    group_students = db.relationship('GroupStudent', backref='group_student', lazy='dynamic')
    pub_permission_students = db.relationship("PublicationPermissionStudent", backref='pub_permission_student',
                                              lazy='dynamic')
    tasks = db.relationship('Task', backref='task', lazy='dynamic')
    rating_lists = db.relationship('RatingList', backref='rating_list', lazy='dynamic')
    answers = db.relationship('Answers', backref='answer', lazy='dynamic')



class PublicationStatus(db.Model):
    name = db.Column(db.VARCHAR(30), primary_key=True)

    publications = db.relationship('Publication', backref='publication_status', lazy='dynamic')


class Publication(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey(User.id))
    name = db.Column(db.String)
    status = db.Column(db.VARCHAR(30), db.ForeignKey(PublicationStatus.name))
    content = db.Column(db.Text)
    date = db.Column(db.Date)

    pub_permission_students = db.relationship("PublicationPermissionStudent", backref='pub_permission_student',
                                              lazy='dynamic')
    pub_permission_groups = db.relationship("PublicationPermissionGroup", backref='pub_permission_group',
                                            lazy='dynamic')


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.VARCHAR(30))
    teacher_id = db.Column(db.Integer, db.ForeignKey(User.id))

    group_students = db.relationship('GroupStudent', backref='group_student', lazy='dynamic')
    pub_permission_groups = db.relationship("PublicationPermissionGroup", backref='pub_permission_group',
                                            lazy='dynamic')
    rating_fields = db.relationship('RatingFields', backref='rating_field', lazy='dynamic')


class GroupStudent(db.Model):
    student_id = db.Column(db.Integer, db.ForeignKey(User.id))
    group_id = db.Column(db.Integer, db.ForeignKey(Group.id))


class PublicationPermissionStudent(db.Model):
    publication_id = db.Column(db.Integer, db.ForeignKey(Publication.id))
    student_id = db.Column(db.Integer, db.ForeignKey(User.id))


class PublicationPermissionGroup(db.Model):
    publication_id = db.Column(db.Integer, db.ForeignKey(Publication.id))
    group_id = db.Column(db.Integer, db.ForeignKey(Group.id))


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey(User.id))
    max_mark = db.Column(db.Integer)

    rating_fields = db.relationship('RatingFields', backref='rating_field', lazy='dynamic')
    questions = db.relationship('Question', backref='question', lazy='dynamic')


class RatingFields(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.Integer, db.ForeignKey(Task.id))
    group_id = db.Column(db.Integer, db.ForeignKey(Group.id))
    field_name = db.Column(db.VARCHAR(30))
    required = db.Column(db.Boolean)

    rating_lists = db.relationship('RatingList', backref='rating_list', lazy='dynamic')


class RatingList(db.Model):
    student_id = db.Column(db.Integer, db.ForeignKey(User.id))
    field_id = db.Column(db.Integer, db.ForeignKey(RatingFields.id))
    mark = db.Column(db.Integer)


class QuestionType(db.Model):
    name = db.Column(db.VARCHAR(30))

    questions = db.relationship('Question', backref='question', lazy='dynamic')


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.Integer, db.ForeignKey(Task.id))
    number = db.Column(db.Integer)
    question = db.Column(db.Text)
    correct_answer = db.Column(db.Text)
    type = db.Column(db.VARCHAR(30), db.ForeignKey(QuestionType.name))
    max_mark = db.Column(db.Integer)

    tests = db.relationship('Tests', backref='test', lazy='dynamic')
    answers = db.relationship('Answers', backref='answer', lazy='dynamic')


class Tests(db.Model):
    question_id = db.Column(db.Integer, db.ForeignKey(Question.id))
    answer = db.Column(db.Text)


class Answers(db.Model):
    question_id = db.Column(db.Integer, db.ForeignKey(Question.id))
    answer = db.Column(db.Text)
    student_id = db.Column(db.Integer, db.ForeignKey(User.id))
    file_path = db.Column(db.String)
    mark = db.Column(db.Integer)
