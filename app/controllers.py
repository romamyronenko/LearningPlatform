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

    def delete(self, id):
        user = models.User.query.filter_by(id=id).first()
        db.session.delete(user)
        db.session.commit()
        return '', 204


class UserListApi(Resource):
    def post(self):
        """Add new User"""
        args = parser.parse_args()
        val = validate(args, ('username', 'name', 'password', 'role'))
        if val[0]:
            return val
        db.session.add(models.User(*val[1]))
        db.session.commit()

        return args['username'], 201

    def get(self):
        """Return a list of Users"""
        users = models.User.query.all()
        return {user.id: {'username': user.username,
                          'name': user.name,
                          'role': user.role} for user in users}


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

    def delete(self, id):
        group = models.Group.query.filter_by(id=id).first()
        db.session.delete(group)
        db.session.commit()
        return '', 204


class GroupListApi(Resource):
    def post(self):
        args = parser.parse_args()
        val = validate(args, ('name', 'teacher_id'))
        if val[0]:
            return val
        db.session.add(models.Group(*val[1]))
        db.session.commit()
        return args['name'], 201

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

    def delete(self, id):
        publication = models.Publication.query.filter_by(id=id).first()
        db.session.delete(publication)
        db.session.commit()
        return '', 204


class PublicationListApi(Resource):
    def post(self):
        args = parser.parse_args()

        val = validate(args, ('teacher_id', 'name', 'status', 'content'))
        if val[0]:
            return val
        db.session.add(models.Publication(*val[1]))
        db.session.commit()
        return args['name'], 201

    def get(self):
        publications = models.Publication.query.all()
        return {publication.id: {'teacher_id': publication.teacher_id,
                                 'name': publication.name,
                                 'status': publication.status,
                                 'content': publication.content,
                                 'date': str(publication.date)} for publication in publications}


api.add_resource(UserListApi, '/rest/users')
api.add_resource(UserApi, '/rest/users/<id>')
api.add_resource(GroupListApi, '/rest/groups')
api.add_resource(GroupApi, '/rest/groups/<id>')
api.add_resource(PublicationListApi, '/rest/publications')
api.add_resource(PublicationApi, '/rest/publications/<id>')
