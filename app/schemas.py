from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from . import models


class RoleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = models.Role
        load_instance = True


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = models.User
        load_instance = True
        include_fk = True


class PublicationStatusSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = models.PublicationStatus


class PublicationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = models.Publication


class GroupSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = models.Group


class GroupStudentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = models.GroupStudent


class PublicationPermissionStudentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = models.PublicationPermissionStudent


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

