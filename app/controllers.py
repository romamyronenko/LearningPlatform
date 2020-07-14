from flask_restful import Resource, reqparse
from . import db, api
from . import models

parser = reqparse.RequestParser()
parser.add_argument('username')
parser.add_argument('name')
parser.add_argument('password')
parser.add_argument('role')
parser.add_argument('teacher_id')
parser.add_argument('status')
parser.add_argument('content')


def validate(args, names):
    for i in names:
        if not args[i]:
            return i + ' is empty', 400
    return '', [args[i] for i in names]


def delete_wrapper(f):
    def wrapper(*args, **kwargs):
        db.session.delete(f(*args, **kwargs))
        db.session.commit()
        return '', 204
    return wrapper


def post_wrapper(f):
    def wrapper(*args, **kwargs):
        names, table = f(*args, **kwargs)
        p_args = parser.parse_args()
        val = validate(p_args, names)
        if val[0]:
            return val

        db.session.add(table(*val[1]))
        db.session.commit()
        return p_args['name'], 201
    return wrapper


def get_wrapper(many=True):
    """
    Wrapper for get method
    if many = False return one value by condition
    else return all values
    """
    def func(f):
        def wrapper(*args, **kwargs):
            if not many:
                table, condition = f(*args, **kwargs)
                value = table.query.filter_by(**condition).first()
                # value.__dict__[name] - return value of column `name`
                return {i: value.__dict__[i] for i in table.__table__.columns.keys()}

            table = f(*args, **kwargs)
            values = table.query.all()
            # table.__table__.columns.keys() - return list of column names
            return [{i: value.__dict__[i] for i in table.__table__.columns.keys()} for value in values]
        return wrapper
    return func


class RoleApi(Resource):
    @get_wrapper(many=False)
    def get(self, name):
        return models.Role, {'name': name}

    def put(self, name):
        pass

    @delete_wrapper
    def delete(self, name):
        return models.Role.query.filter_by(name=name).first()


class RoleListApi(Resource):
    @post_wrapper
    def post(self):
        return ('name',), models.Role

    @get_wrapper()
    def get(self):
        return models.Role


class UserApi(Resource):
    @get_wrapper(many=False)
    def get(self, id):
        return models.User, {'id': id}

    def put(self, id):
        user = models.User.query.filter_by(id=id).first()
        args = parser.parse_args()
        if args['username'] is not None:
            user.username = args['username']
        if args['name'] is not None:
            user.name = args['name']
        if args['password'] is not None:
            user.password = args['password']
        db.session.commit()

        return {user.id: {'username': user.username,
                          'name': user.name,
                          'role': user.role}}

    @delete_wrapper
    def delete(self, id):
        return models.User.query.filter_by(id=id).first()


class UserListApi(Resource):
    @post_wrapper
    def post(self):
        """Add new User"""
        return ('username', 'name', 'password', 'role'), models.User

    @get_wrapper()
    def get(self):
        """Return a list of Users"""
        return models.User


class PublicationStatusApi(Resource):
    @get_wrapper(many=False)
    def get(self, name):
        return models.PublicationStatus, {'name': name}

    def put(self, name):
        pass

    @delete_wrapper
    def delete(self, name):
        return models.PublicationStatus.query.filter_by(name=name).first()


class PublicationStatusListApi(Resource):
    @post_wrapper
    def post(self):
        return ('name',), models.PublicationStatus

    @get_wrapper()
    def get(self):
        return models.PublicationStatus


class GroupApi(Resource):
    @get_wrapper(many=False)
    def get(self, id):
        return models.Group, {'id': id}

    def put(self, id):
        group = models.Group.query.filter_by(id=id).first()
        args = parser.parse_args()
        if args['name'] is not None:
            group.name = args['name']

        return {group.id: {'name': group.name,
                           'teacher_id': group.teacher_id}}

    @delete_wrapper
    def delete(self, id):
        return models.Group.query.filter_by(id=id).first()


class GroupListApi(Resource):
    @post_wrapper
    def post(self):
        return ('name', 'teacher_id'), models.Group

    @get_wrapper()
    def get(self):
        return models.Group


class PublicationApi(Resource):
    @get_wrapper(many=False)
    def get(self, id):
        return models.Publication, {'id': id}

    def put(self, id):
        publication = models.Publication.query.filter_by(id=id).first()
        args = parser.parse_args()
        if args['name'] is not None:
            publication.name = args['name']
        if args['status'] is not None:
            publication.status = args['status']
        if args['content'] is not None:
            publication.content = args['content']

        return {publication.id: {'teacher_id': publication.teacher_id,
                                 'name': publication.name,
                                 'status': publication.status,
                                 'content': publication.content,
                                 'date': str(publication.date)}}

    @delete_wrapper
    def delete(self, id):
        return models.Publication.query.filter_by(id=id).first()


class PublicationListApi(Resource):
    @post_wrapper
    def post(self):
        return ('teacher_id', 'name', 'status', 'content'), models.Publication

    @get_wrapper()
    def get(self):
        return models.Publication


class GroupStudentApi(Resource):
    @get_wrapper(many=False)
    def get(self, id):
        return models.GroupStudent, {'id': id}

    def put(self, id):
        gr_st = models.GroupStudent.query.filter_by(id=id).first()
        # pass
        return {gr_st.id: {'student_id': gr_st.student_id,
                           'group_id': gr_st.group_id}}

    @delete_wrapper
    def delete(self, id):
        return models.GroupStudent.query.filter_by(id=id).first()


class GroupStudentListApi(Resource):
    @post_wrapper
    def post(self):
        return ('group_id', 'student_id'), models.GroupStudent

    @get_wrapper()
    def get(self):
        return models.GroupStudent


class PublicationPermissionStudentApi(Resource):
    @get_wrapper(many=False)
    def get(self, id):
        return models.PublicationPermissionStudent, {'id': id}

    def put(self, id):
        pass

    @delete_wrapper
    def delete(self, id):
        return models.PublicationPermissionStudent.query.filter_by(id=id).first()


class PublicationPermissionStudentListApi(Resource):
    @post_wrapper
    def post(self):
        return ('publication_id', 'student_id'), models.PublicationPermissionStudent

    @get_wrapper()
    def get(self):
        return models.PublicationPermissionStudent


class PublicationPermissionGroupApi(Resource):
    @get_wrapper(many=False)
    def get(self, id):
        return models.PublicationPermissionGroup, {'id': id}

    def put(self, id):
        pass

    @delete_wrapper
    def delete(self, id):
        return models.PublicationPermissionGroup.query.filter_by(id=id).first()


class PublicationPermissionGroupListApi(Resource):
    @post_wrapper
    def post(self):
        return ('publication_id', 'group_id'), models.PublicationPermissionGroup

    @get_wrapper()
    def get(self):
        return models.PublicationPermissionGroup


class TaskApi(Resource):
    @get_wrapper(many=False)
    def get(self, id):
        return models.Task, {'id': id}

    def put(self, id):
        pass

    @delete_wrapper
    def delete(self, id):
        return models.Task.query.filter_by(id=id).first()


class TaskListApi(Resource):
    @post_wrapper
    def post(self):
        return ('teacher_id',), models.Task

    @get_wrapper()
    def get(self):
        return models.Task


class RatingFieldsApi(Resource):
    @get_wrapper(many=False)
    def get(self, id):
        return models.RatingFields, {'id': id}

    def put(self, id):
        pass

    @delete_wrapper
    def delete(self, id):
        return models.RatingFields.query.filter_by(id=id).first()


class RatingFieldsListApi(Resource):
    @post_wrapper
    def post(self):
        return ('task_id', 'group_id', 'field_name', 'required'), models.RatingFields

    @get_wrapper()
    def get(self):
        return models.RatingFields


class RatingListApi(Resource):
    @get_wrapper(many=False)
    def get(self, id):
        return models.RatingList, {'id': id}

    def put(self, id):
        pass

    @delete_wrapper
    def delete(self, id):
        return models.RatingList.query.filter_by(id=id).first()


class RatingListListApi(Resource):
    @post_wrapper
    def post(self):
        return ('student_id', 'field_id', 'mark'), models.RatingList

    @get_wrapper()
    def get(self):
        return models.RatingList


class QuestionTypeApi(Resource):
    @get_wrapper(many=False)
    def get(self, name):
        return models.QuestionType, {'name': name}

    def put(self, name):
        pass

    @delete_wrapper
    def delete(self, name):
        return models.QuestionType.query.filter_by(name=name).first()


class QuestionTypeListApi(Resource):
    @post_wrapper
    def post(self):
        return ('name',), models.QuestionType

    @get_wrapper()
    def get(self):
        return models.QuestionType


class QuestionApi(Resource):
    @get_wrapper(many=False)
    def get(self, id):
        return models.Question, {'id': id}

    def put(self, id):
        pass

    @delete_wrapper
    def delete(self, id):
        return models.Question.query.filter_by(id=id).first()


class QuestionListApi(Resource):
    @post_wrapper
    def post(self):
        return ('task_id', 'number', 'question', 'correct_answer', 'type', 'max_mark'), models.Question

    @get_wrapper()
    def get(self):
        return models.Question


class TestsApi(Resource):
    @get_wrapper(many=False)
    def get(self, id):
        return models.Tests, {'id': id}

    def put(self, id):
        pass

    @delete_wrapper
    def delete(self, id):
        return models.Tests.query.filter_by(id=id).first()


class TestsListApi(Resource):
    @post_wrapper
    def post(self):
        return ('question_id', 'answer'), models.Tests

    @get_wrapper()
    def get(self):
        return models.Tests


class AnswersApi(Resource):
    @get_wrapper(many=False)
    def get(self, id):
        return models.Answers, {'id': id}

    def put(self, id):
        pass

    @delete_wrapper
    def delete(self, id):
        return models.Answers.query.filter_by(id=id).first()


class AnswersListApi(Resource):
    @post_wrapper
    def post(self):
        return ('question_id', 'answer', 'student_id'), models.Answers

    @get_wrapper()
    def get(self):
        return models.Answers


api.add_resource(RoleApi, '/rest/roles/<name>')
api.add_resource(RoleListApi, '/rest/roles')
api.add_resource(UserApi, '/rest/users/<id>')
api.add_resource(UserListApi, '/rest/users')
api.add_resource(PublicationStatusApi, '/rest/publications_status/<name>')
api.add_resource(PublicationStatusListApi, '/rest/publications_status')
api.add_resource(GroupApi, '/rest/groups/<id>')
api.add_resource(GroupListApi, '/rest/groups')
api.add_resource(PublicationApi, '/rest/publications/<id>')
api.add_resource(PublicationListApi, '/rest/publications')
api.add_resource(GroupStudentApi, '/rest/group_student/<id>')
api.add_resource(GroupStudentListApi, '/rest/group_student')
api.add_resource(PublicationPermissionStudentApi, '/rest/publications_permissions_students/<id>')
api.add_resource(PublicationPermissionStudentListApi, '/rest/publications_permissions_students')
api.add_resource(PublicationPermissionGroupApi, '/rest/publications_permissions_groups/<id>')
api.add_resource(PublicationPermissionGroupListApi, '/rest/publications_permissions_groups')
api.add_resource(TaskApi, '/rest/tasks/<id>')
api.add_resource(TaskListApi, '/rest/tasks')
api.add_resource(RatingFieldsApi, '/rest/rating_fields/<id>')
api.add_resource(RatingFieldsListApi, '/rest/rating_fields')
api.add_resource(RatingListApi, '/rest/rating_lists/<id>')
api.add_resource(RatingListListApi, '/rest/rating_lists')
api.add_resource(QuestionTypeApi, '/rest/question_types/<name>')
api.add_resource(QuestionTypeListApi, '/rest/question_types')
api.add_resource(QuestionApi, '/rest/questions/<id>')
api.add_resource(QuestionListApi, '/rest/questions')
api.add_resource(TestsApi, '/rest/tests/<id>')
api.add_resource(TestsListApi, '/rest/tests')
api.add_resource(AnswersApi, '/rest/answers/<id>')
api.add_resource(AnswersListApi, '/rest/answers')
