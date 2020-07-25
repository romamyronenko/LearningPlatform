import json
from werkzeug.security import check_password_hash
import pytest
from app import app, db

roles = [
    {'name': 'Student'},
    {'name': 'Teacher'},
    {'name': 'Admin'}
]

users = [
    {
        'username': 'roma0221',
        'name': 'Roman',
        'role': 'Student',
        'password': 'fn23rh2892R'
    },
    {
        'username': 'bill_r',
        'name': 'Bill',
        'role': 'Teacher',
        'password': 'f23_#@dv'
    }
]


@pytest.fixture
def get_db():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    db.create_all()
    yield None
    db.drop_all()


def test_empty_db(get_db):
    r = app.test_client().get('/rest/users')
    assert r.json == []


def test_add_role(get_db):
    r1 = app.test_client().post('/rest/roles', data=roles[0])
    r2 = app.test_client().get('/rest/roles')
    r3 = app.test_client().get('/rest/roles/Student')
    assert r1.json == roles[0]
    assert r2.json == [roles[0]]
    assert r3.json == roles[0]


def test_remove_role(get_db):
    pass


def test_add_user(get_db):
    for i in roles:
        app.test_client().post('/rest/roles', data=i)

    for i in users:
        app.test_client().post('/rest/users', data=i)
    r = app.test_client().get('/rest/users').json
    for i in range(len(users)):
        for j in users[i]:
            if j != 'password':
                assert r[i][j] == users[i][j]
            else:
                assert check_password_hash(r[i][j], users[i][j])
