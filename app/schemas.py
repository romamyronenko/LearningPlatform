from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow.exceptions import ValidationError
from flask import request, g
from . import models
from marshmallow import validates


class RoleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = models.Role
        load_instance = True


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = models.User
        load_instance = True
        include_fk = True

    @validates('role')
    def is_teacher(self, value):
        if value == 'Admin':
            raise ValidationError('permissions denied')


class PublicationStatusSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = models.PublicationStatus
        load_instance = True
        include_fk = True


class PublicationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = models.Publication
        load_instance = True
        include_fk = True

    @validates('user_id')
    def is_teacher(self, value):
        if models.User.query.filter_by(id=value).first().role != 'Teacher':
            raise ValidationError('user is not a teacher')


class GroupSchema(SQLAlchemyAutoSchema):
    class Meta:
        load_instance = True
        include_fk = True
        model = models.Group

    @validates('user_id')
    def is_teacher(self, value):
        if models.User.query.filter_by(id=value).first().role != 'Teacher':
            raise ValidationError('user is not a teacher')


class GroupStudentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = models.GroupStudent


class PublicationPermissionStudentSchema(SQLAlchemyAutoSchema):
    class Meta:
        load_instance = True
        include_fk = True
        model = models.PublicationPermissionStudent

    @validates('publication_id')
    def is_teacher(self, value):
        if models.Publication.query.filter_by(id=value).first().id != g.user.id:
            raise ValidationError('permissions denied')


class PublicationPermissionGroupSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = models.PublicationPermissionGroup


class TaskSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = models.Task


class RatingFieldsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = models.RatingFields


class RatingListSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = models.RatingList


class QuestionTypeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = models.QuestionType


class QuestionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = models.Question


class TestsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = models.Tests


class AnswersSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = models.Answers

