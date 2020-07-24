from flask_restful import Resource, reqparse
from . import db, api
from . import models
from . import auth

parser = reqparse.RequestParser()
parser.add_argument('username')
parser.add_argument('name')
parser.add_argument('password')
parser.add_argument('role')
parser.add_argument('teacher_id')
parser.add_argument('status')
parser.add_argument('content')
parser.add_argument('group_id')
parser.add_argument('student_id')
parser.add_argument('publication_id')
parser.add_argument('task_id')
parser.add_argument('field_name')
parser.add_argument('required')
parser.add_argument('mark')
parser.add_argument('number')
parser.add_argument('question')
parser.add_argument('correct_answer')
parser.add_argument('type')
parser.add_argument('max_mark')


def validate(args, names):
    for i in names:
        if not args[i]:
            return i + ' is empty', 400
        if i == 'teacher_id':
            if models.User.query.filter_by(id=args[i]).first().role != 'Teacher':
                return 'user is not a teacher', 406
    return '', [args[i] for i in names]


class CustomResource(Resource):
    def get(self, **kwargs):
        value = self.model.query.filter_by(**kwargs).first()
        if value is None:
            return {}
        # value.__dict__['name'] - return value of column `name`
        return {i: value.__dict__[i] for i in self.model.__table__.columns.keys()}

    def put(self):
        pass

    def delete(self, **kwargs):
        db.session.delete(self.model.query.filter_by(**kwargs).first())
        db.session.commit()
        return 'Successfully deleted', 204


class CustomListResource(Resource):
    def post(self):
        p_args = parser.parse_args()
        val = self.validate(p_args)
        if val[0]:
            return val

        db.session.add(self.model(*val[1]))
        db.session.commit()
        return {i: j for i, j in zip(self.fields, val[1])}, 201

    def get(self):
        values = self.model.query.all()
        # table.__table__.columns.keys() - return list of column names
        return [{i: str(value.__dict__[i]) for i in self.model.__table__.columns.keys()} for value in values]


class RoleApi(CustomResource):
    model = models.Role


class RoleListApi(CustomListResource):
    model = models.Role
    fields = ('name',)

    def validate(self, values):
        roles = [i.name for i in self.model.query.all()]
        for i in self.fields:
            if i == 'name':
                if not values[i]:
                    return 'name is empty', 411
                if values[i] in roles:
                    return 'role is exists', 411
                if len(values[i]) < 2:
                    return 'name too short', 411
                if len(values[i]) > 30:
                    return 'name too long', 411
        return '', [values[i] for i in self.fields]


class UserApi(CustomResource):
    model = models.User


class UserListApi(CustomListResource):
    model = models.User
    fields = ('username', 'name', 'password', 'role')


class PublicationStatusApi(CustomResource):
    model = models.PublicationStatus


class PublicationStatusListApi(CustomListResource):
    model = models.PublicationStatus
    fields = ('name', )


class GroupApi(CustomResource):
    model = models.Group


class GroupListApi(CustomListResource):
    model = models.Group
    fields = ('name', 'teacher_id')


class PublicationApi(CustomResource):
    model = models.Publication


class PublicationListApi(CustomListResource):
    model = models.Publication
    fields = ('teacher_id', 'name', 'status', 'content')


class GroupStudentApi(CustomResource):
    model = models.GroupStudent


class GroupStudentListApi(CustomListResource):
    model = models.GroupStudent
    fields = ('group_id', 'student_id')


class PublicationPermissionStudentApi(CustomResource):
    model = models.PublicationPermissionStudent


class PublicationPermissionStudentListApi(CustomListResource):
    model = models.PublicationPermissionStudent
    fields = ('publication_id', 'student_id')


class PublicationPermissionGroupApi(CustomResource):
    model = models.PublicationPermissionGroup


class PublicationPermissionGroupListApi(CustomListResource):
    model = models.PublicationPermissionGroup
    fields = ('publication_id', 'group_id')


class TaskApi(CustomResource):
    model = models.Task


class TaskListApi(CustomListResource):
    model = models.Task
    fields = ('teacher_id',)


class RatingFieldsApi(CustomResource):
    model = models.RatingFields


class RatingFieldsListApi(CustomListResource):
    model = models.RatingFields
    fields = ('task_id', 'group_id', 'field_name', 'required')


class RatingListApi(CustomResource):
    model = models.RatingList


class RatingListListApi(CustomListResource):
    model = models.RatingList
    fields = ('student_id', 'field_id', 'mark')


class QuestionTypeApi(CustomResource):
    model = models.QuestionType


class QuestionTypeListApi(CustomListResource):
    model = models.QuestionType
    fields = ('name',)


class QuestionApi(CustomResource):
    model = models.Question


class QuestionListApi(CustomListResource):
    model = models.Question
    fields = ('task_id', 'number', 'question', 'correct_answer', 'type', 'max_mark')


class TestsApi(CustomResource):
    model = models.Tests


class TestsListApi(CustomListResource):
    model = models.Tests
    fields = ('question_id', 'answer')


class AnswersApi(CustomResource):
    model = models.Answers


class AnswersListApi(CustomListResource):
    model = models.Answers
    fields = ('question_id', 'answer', 'student_id')


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
