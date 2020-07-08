from flask_restful import Resource, reqparse
from . import db, api
from . import models

parser = reqparse.RequestParser()
parser.add_argument('username')
parser.add_argument('name')
parser.add_argument('password')
parser.add_argument('role')
parser.add_argument('teacher_id')


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
        if not args['username']:
            return 'username is empty', 400
        if not args['name']:
            return 'name is empty', 400
        if not args['password']:
            return 'password is empty', 400
        if not args['role']:
            return 'role is empty', 400
        db.session.add(models.User(args['username'],
                                   args['name'],
                                   args['password'],
                                   args['role']))
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
        print(args)
        if not args['name']:
            return 'name is empty', 400
        if not args['teacher_id']:
            return 'teacher_id is empty', 400
        db.session.add(models.Group(args['name'],
                                    args['teacher_id']))
        db.session.commit()
        return args['name'], 201

    def get(self):
        groups = models.Group.query.all()
        return {group.id: {'name': group.name,
                           'teacher_id': group.teacher_id} for group in groups}


api.add_resource(UserListApi, '/rest/users')
api.add_resource(UserApi, '/rest/users/<id>')
api.add_resource(GroupListApi, '/rest/groups')
api.add_resource(GroupApi, '/rest/groups/<id>')
