from werkzeug.security import generate_password_hash
import datetime
from app import db


class Role(db.Model):
    name = db.Column(db.VARCHAR(30), primary_key=True)

    def __init__(self, name, **kwargs):
        self.name = name

    def __repr__(self):
        return f'Role({self.name})'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.VARCHAR(30), unique=True)
    name = db.Column(db.VARCHAR(255))
    password = db.Column(db.String(94))
    role = db.Column(db.VARCHAR(30), db.ForeignKey(Role.name))

    def __init__(self, username, name, password, role):
        self.username = username
        self.name = name
        self.password = generate_password_hash(password)
        self.role = role

    def __repr__(self):
        return f'User({self.id}, {self.username}, {self.name}, {self.role})'


class PublicationStatus(db.Model):
    name = db.Column(db.VARCHAR(30), primary_key=True)

    def __init__(self, name):
        self.name = name


class Publication(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    name = db.Column(db.Text)
    status = db.Column(db.VARCHAR(30), db.ForeignKey(PublicationStatus.name))
    content = db.Column(db.Text)
    date = db.Column(db.Date)

    def __init__(self, user_id, name, status, content):
        self.user_id = user_id
        self.name = name
        self.status = status
        self.content = content
        self.date = datetime.date.today()


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.VARCHAR(30))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

    def __repr__(self):
        return f'Group({self.id}, {self.name}, {self.user_id})'


class GroupStudent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    group_id = db.Column(db.Integer, db.ForeignKey(Group.id))

    def __init__(self, user_id, group_id):
        self.user_id = user_id
        self.group_id = group_id


class PublicationPermissionStudent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    publication_id = db.Column(db.Integer, db.ForeignKey(Publication.id))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    def __init__(self, publication_id, user_id):
        self.publication_id = publication_id
        self.user_id = user_id


class PublicationPermissionGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    publication_id = db.Column(db.Integer, db.ForeignKey(Publication.id))
    group_id = db.Column(db.Integer, db.ForeignKey(Group.id))

    def __init__(self, publication_id, group_id):
        self.publication_id = publication_id
        self.group_id = group_id


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    max_mark = db.Column(db.Integer)

    def __init__(self, user_id):
        self.user_id = user_id


class RatingFields(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.Integer, db.ForeignKey(Task.id))
    group_id = db.Column(db.Integer, db.ForeignKey(Group.id))
    field_name = db.Column(db.VARCHAR(30))
    required = db.Column(db.Boolean)

    def __init__(self, task_id, group_id, field_name, required):
        self.task_id = task_id
        self.group_id = group_id
        self.field_name = field_name
        self.required = bool(required)


class RatingList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    field_id = db.Column(db.Integer, db.ForeignKey(RatingFields.id))
    mark = db.Column(db.Integer)

    def __init__(self, user_id, field_id, mark):
        self.user_id = user_id
        self.field_id = field_id
        self.mark = int(mark)


class QuestionType(db.Model):
    name = db.Column(db.VARCHAR(30), primary_key=True)

    def __init__(self, name):
        self.name = name


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.Integer, db.ForeignKey(Task.id))
    number = db.Column(db.Integer)
    question = db.Column(db.Text)
    correct_answer = db.Column(db.Text)
    type = db.Column(db.VARCHAR(30), db.ForeignKey(QuestionType.name))
    max_mark = db.Column(db.Integer)

    def __init__(self, task_id, number, question, correct_answer, type, max_mark):
        self.task_id = task_id
        self.number = int(number)
        self.question = question
        self.correct_answer = correct_answer
        self.type = type
        self.max_mark = int(max_mark)


class Tests(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_id = db.Column(db.Integer, db.ForeignKey(Question.id))
    answer = db.Column(db.Text)

    def __init__(self, question_id, answer):
        self.question_id = question_id
        self.answer = answer


class Answers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey(Question.id))
    answer = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    def __init__(self, question_id, answer, user_id):
        self.question_id = question_id
        self.answer = answer
        self.user_id = user_id
