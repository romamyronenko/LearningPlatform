from flask_restful import Resource, reqparse
from . import db, api
from . import models

parser = reqparse.RequestParser()
parser.add_argument('username')
parser.add_argument('name')
parser.add_argument('password')
parser.add_argument('role')


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
            db.session.commit()
        if args['password'] is not None:
            user.password = args['password']

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
        print(args)
        if not args['username']:
            return 'username is empty', 400
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


api.add_resource(UserListApi, '/rest/users')
api.add_resource(UserApi, '/rest/users/<id>')
