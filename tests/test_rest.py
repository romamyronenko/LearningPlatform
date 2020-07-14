import json
import pytest

from app import app, db


@pytest.fixture
def get_db():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    db.create_all()
    yield None
    db.drop_all()


def test_empty_db(get_db):
    r = app.test_client().get('/rest/users')
    assert r.data == b'[]\n'


def test_add_role(get_db):
    r1 = app.test_client().post('/rest/roles', data={'name': 'Student'})
    r2 = app.test_client().get('/rest/roles')
    assert r1.data == b'{\n    "name": "Student"\n}\n'
    assert r2.data == b'[\n    {\n        "name": "Student"\n    }\n]\n'


def test_add_user(get_db):
    app.test_client().post('/rest/roles', data={'name': 'Student'})
    app.test_client().post('/rest/roles', data={'name': 'Teacher'})