from werkzeug.security import generate_password_hash
from flask_restful import Resource, reqparse
from flask import request, g
from marshmallow.exceptions import ValidationError
from . import db, api
from . import models
from . import auth
from . import schemas


class CustomResource(Resource):
    check_role = None
    check_user_id = False

    def get(self, **kwargs):
        schema = self.schema()
        value = self.model.query.filter_by(**kwargs).first()
        if value is None:
            return {}
        return schema.dump(value)

    def put(self, **kwargs):
        schema = self.schema()
        value = self.model.query.filter_by(**kwargs).first()
        if value is None:
            return 'not found', 404

        try:
            if 'password' in request.json:
                request.json['password'] = generate_password_hash(request.json['password'])
            value = schema.load(request.json, instance=value, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400
        db.session.add(value)
        db.session.commit()
        return schema.dump(value)

    @auth.token_required
    def delete(self, **kwargs):
        if self.check_role is not None and self.check_role != g.user.role:
            return 'user is not a ' + str(g.user.role), 405
        if self.check_user_id and str(kwargs['id']) != str(g.user.id):
            print('dds', kwargs['id'], g.user.id)
            return 'permissions denied', 406
        value = self.model.query.filter_by(**kwargs).first()
        if not value:
            return 'value is not exists', 403
        db.session.delete(value)
        db.session.commit()
        return 'Successfully deleted', 204


class CustomListResource(Resource):
    add_user_id = False
    check_role = None
    
    @auth.token_required
    def post(self):
        if self.add_user_id:
            request.json['user_id'] = g.user.id

        if self.check_role is not None and self.check_role != g.user.role:
            return 'user is not a ' + str(g.user.role), 405
        schema = self.schema()
        try:
            value = schema.load(request.json, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400
        db.session.add(value)
        db.session.commit()
        return schema.dump(value), 201

    def get(self):
        schema = self.schema(many=True)
        values = self.model.query.all()
        return schema.dump(values)


class RoleApi(CustomResource):
    check_role = 'Admin'
    model = models.Role
    schema = schemas.RoleSchema


class RoleListApi(CustomListResource):
    check_role = 'Admin'
    model = models.Role
    schema = schemas.RoleSchema


class UserApi(CustomResource):
    model = models.User
    schema = schemas.UserSchema
    check_user_id = True


class UserListApi(CustomListResource):
    model = models.User
    schema = schemas.UserSchema

    def post(self):
        schema = self.schema()
        try:
            value = schema.load(request.json, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400
        db.session.add(value)
        db.session.commit()
        return schema.dump(value), 201


class PublicationStatusApi(CustomResource):
    check_role = 'Admin'
    model = models.PublicationStatus
    schema = schemas.PublicationStatusSchema


class PublicationStatusListApi(CustomListResource):
    check_role = 'Admin'
    model = models.PublicationStatus
    schema = schemas.PublicationStatusSchema


class GroupApi(CustomResource):
    model = models.Group
    schema = schemas.GroupSchema


class GroupListApi(CustomListResource):
    check_role = 'Teacher'
    model = models.Group
    schema = schemas.GroupSchema


class PublicationApi(CustomResource):
    model = models.Publication
    schema = schemas.PublicationSchema


class PublicationListApi(CustomListResource):
    add_user_id = True
    model = models.Publication
    schema = schemas.PublicationSchema


class GroupStudentApi(CustomResource):
    model = models.GroupStudent
    schema = schemas.GroupStudentSchema


class GroupStudentListApi(CustomListResource):
    model = models.GroupStudent
    schema = schemas.GroupStudentSchema


class PublicationPermissionStudentApi(CustomResource):
    model = models.PublicationPermissionStudent
    schema = schemas.PublicationPermissionStudentSchema


class PublicationPermissionStudentListApi(CustomListResource):
    model = models.PublicationPermissionStudent
    schema = schemas.PublicationPermissionStudentSchema


class PublicationPermissionGroupApi(CustomResource):
    model = models.PublicationPermissionGroup
    schema = schemas.PublicationPermissionGroupSchema


class PublicationPermissionGroupListApi(CustomListResource):
    model = models.PublicationPermissionGroup
    schema = schemas.PublicationPermissionGroupSchema


class TaskApi(CustomResource):
    model = models.Task
    schema = schemas.TaskSchema


class TaskListApi(CustomListResource):
    model = models.Task
    schema = schemas.TaskSchema


class RatingFieldsApi(CustomResource):
    model = models.RatingFields
    schema = schemas.RatingFieldsSchema


class RatingFieldsListApi(CustomListResource):
    model = models.RatingFields
    schema = schemas.RatingFieldsSchema


class RatingListApi(CustomResource):
    model = models.RatingList
    schema = schemas.RatingListSchema


class RatingListListApi(CustomListResource):
    model = models.RatingList
    schema = schemas.RatingListSchema


class QuestionTypeApi(CustomResource):
    model = models.QuestionType
    schema = schemas.QuestionTypeSchema


class QuestionTypeListApi(CustomListResource):
    model = models.QuestionType
    schema = schemas.QuestionTypeSchema


class QuestionApi(CustomResource):
    model = models.Question
    schema = schemas.QuestionSchema


class QuestionListApi(CustomListResource):
    model = models.Question
    schema = schemas.QuestionSchema


class TestsApi(CustomResource):
    model = models.Tests
    schema = schemas.TestsSchema


class TestsListApi(CustomListResource):
    model = models.Tests
    schema = schemas.TestsSchema


class AnswersApi(CustomResource):
    model = models.Answers
    schema = schemas.AnswersSchema


class AnswersListApi(CustomListResource):
    model = models.Answers
    schema = schemas.AnswersSchema


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
