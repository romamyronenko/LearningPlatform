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


class RoleApi(Resource):
    def get(self, name):
        role = models.Role.query.filter_by(name=name).first()
        return role.name

    def put(self, name):
        pass

    @delete_wrapper
    def delete(self, name):
        return models.Role.query.filter_by(name=name).first()


class RoleListApi(Resource):
    @post_wrapper
    def post(self):
        return ('name',), models.Role

    def get(self):
        roles = models.Role.query.all()
        return [role.name for role in roles]


class UserApi(Resource):
    def get(self, id):
        user = models.User.query.filter_by(id=id).first()
        return {user.id: {'username': user.username,
                          'name': user.name,
                          'role': user.role}}

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

    def get(self):
        """Return a list of Users"""
        users = models.User.query.all()
        return {user.id: {'username': user.username,
                          'name': user.name,
                          'role': user.role} for user in users}


class PublicationStatusApi(Resource):
    def get(self, name):
        publication_status = models.PublicationStatus.query.filter_by(name=name).first()
        return publication_status.name

    def put(self, name):
        pass

    @delete_wrapper
    def delete(self, name):
        return models.PublicationStatus.query.filter_by(name=name).first()


class PublicationStatusListApi(Resource):
    @post_wrapper
    def post(self):
        return ('name',), models.PublicationStatus

    def get(self):
        pubs = models.PublicationStatus.query.all()
        return [pub.name for pub in pubs]


class GroupApi(Resource):
    def get(self, id):
        group = models.Group.query.filter_by(id=id).first()
        return {group.id: {'name': group.name,
                           'teacher_id': group.teacher_id}}

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

    def get(self):
        groups = models.Group.query.all()
        return {group.id: {'name': group.name,
                           'teacher_id': group.teacher_id} for group in groups}


class PublicationApi(Resource):
    def get(self, id):
        publication = models.Publication.query.filter_by(id=id).first()
        return {publication.id: {'teacher_id': publication.teacher_id,
                                 'name': publication.name,
                                 'status': publication.status,
                                 'content': publication.content,
                                 'date': str(publication.date)}}

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

    def get(self):
        publications = models.Publication.query.all()
        return {publication.id: {'teacher_id': publication.teacher_id,
                                 'name': publication.name,
                                 'status': publication.status,
                                 'content': publication.content,
                                 'date': str(publication.date)} for publication in publications}


class GroupStudentApi(Resource):
    def get(self, id):
        gr_st = models.GroupStudent.query.filter_by(id=id).first()
        return {gr_st.id: {'student_id': gr_st.student_id,
                           'group_id': gr_st.group_id}}

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

    def get(self):
        gr_sts = models.GroupStudent.query.all()
        return {gr_st.id: {'student_id': gr_st.student_id,
                           'group_id': gr_st.group_id} for gr_st in gr_sts}


class PublicationPermissionStudentApi(Resource):
    def get(self, id):
        pass

    def put(self, id):
        pass

    @delete_wrapper
    def delete(self, id):
        return models.PublicationPermissionStudent.query.filter_by(id=id).first()


class PublicationPermissionStudentListApi(Resource):
    @post_wrapper
    def post(self):
        return ('publication_id', 'student_id'), models.PublicationPermissionStudent

    def get(self):
        pass


class PublicationPermissionGroupApi(Resource):
    def get(self, id):
        pass

    def put(self, id):
        pass

    @delete_wrapper
    def delete(self, id):
        return models.PublicationPermissionGroup.query.filter_by(id=id).first()


class PublicationPermissionGroupListApi(Resource):
    @post_wrapper
    def post(self):
        return ('publication_id', 'group_id'), models.PublicationPermissionGroup

    def get(self):
        pass


class TaskApi(Resource):
    def get(self, id):
        pass

    def put(self, id):
        pass

    @delete_wrapper
    def delete(self, id):
        return models.Task.query.filter_by(id=id).first()


class TaskListApi(Resource):
    @post_wrapper
    def post(self):
        return ('teacher_id',), models.Task

    def get(self):
        pass


class RatingFieldsApi(Resource):
    def get(self, id):
        pass

    def put(self, id):
        pass

    @delete_wrapper
    def delete(self, id):
        return models.RatingFields.query.filter_by(id=id).first()


class RatingFieldsListApi(Resource):
    @post_wrapper
    def post(self):
        return ('task_id', 'group_id', 'field_name', 'required'), models.RatingFields

    def get(self):
        pass


class RatingListApi(Resource):
    def get(self, id):
        pass

    def put(self, id):
        pass

    @delete_wrapper
    def delete(self, id):
        return models.RatingList.query.filter_by(id=id).first()


class RatingListListApi(Resource):
    @post_wrapper
    def post(self):
        return ('student_id', 'field_id', 'mark'), models.RatingList

    def get(self):
        pass


class QuestionTypeApi(Resource):
    def get(self, id):
        pass

    def put(self, id):
        pass

    @delete_wrapper
    def delete(self, name):
        return models.QuestionType.query.filter_by(name=name).first()


class QuestionTypeListApi(Resource):
    @post_wrapper
    def post(self):
        return ('name',), models.QuestionType

    def get(self):
        pass


class QuestionApi(Resource):
    def get(self, id):
        pass

    def put(self, id):
        pass

    @delete_wrapper
    def delete(self, id):
        return models.Question.query.filter_by(id=id).first()


class QuestionListApi(Resource):
    @post_wrapper
    def post(self):
        return ('task_id', 'number', 'question', 'correct_answer', 'type', 'max_mark'), models.Question

    def get(self):
        pass


class TestsApi(Resource):
    def get(self, id):
        pass

    def put(self, id):
        pass

    @delete_wrapper
    def delete(self, id):
        return models.Tests.query.filter_by(id=id).first()


class TestsListApi(Resource):
    @post_wrapper
    def post(self):
        return ('question_id', 'answer'), models.Tests

    def get(self):
        pass


class AnswersApi(Resource):
    def get(self, id):
        pass

    def put(self, id):
        pass

    @delete_wrapper
    def delete(self, id):
        return models.Answers.query.filter_by(id=id).first()


class AnswersListApi(Resource):
    @post_wrapper
    def post(self):
        return ('question_id', 'answer', 'student_id'), models.Answers

    def get(self):
        pass


api.add_resource(RoleListApi, '/rest/roles')
api.add_resource(RoleApi, '/rest/roles/<name>')
api.add_resource(UserListApi, '/rest/users')
api.add_resource(UserApi, '/rest/users/<id>')
api.add_resource(GroupListApi, '/rest/groups')
api.add_resource(GroupApi, '/rest/groups/<id>')
api.add_resource(PublicationListApi, '/rest/publications')
api.add_resource(PublicationApi, '/rest/publications/<id>')
