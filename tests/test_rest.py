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
    assert r.data == b'{}\n'


def test_add_user():
    r = app.test_client().post('/rest/users')
