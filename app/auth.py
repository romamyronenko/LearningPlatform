from werkzeug.security import check_password_hash
import jwt
from flask import request, jsonify, g
import datetime
from app import app, db
from . import models


@app.route('/login')
def login():
    auth = request.authorization
    user = db.session.query(models.User).filter_by(username=auth.get('username', '')).first()
    if user is None or not check_password_hash(user.password, auth.get('password', '')):
        return '', 401, {'WWW-Authenticate': 'Basic realm="Authentication required"'}
    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.datetime.now() + datetime.timedelta(hours=1)
    }, app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({'token': token.decode('utf-8')})


def token_required(f):
    def wrapper(self, *args, **kwargs):
        token = request.headers.get('X-Api-Key', '')
        if not token:
            return '', 401, {'WWW-Authenticate': 'Basic realm="Authentication required"'}
        try:
            user_id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['user_id']
        except (KeyError, jwt.ExpiredSignatureError):
            return '', 401, {'WWW-Authenticate': 'Basic realm="Authentication required"'}
        user = db.session.query(models.User).filter_by(id=user_id).first()
        if not user:
            return '', 401, {'WWW-Authenticate': 'Basic realm="Authentication required"'}
        # request.json['user_id'] = user_id
        g.user = user
        return f(self, *args, **kwargs)
    return wrapper
