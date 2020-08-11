import jwt
from werkzeug.security import check_password_hash
import base64
import pytest
from app import app, db, models

roles = [
    {'name': 'Admin'},
    {'name': 'Student'},
    {'name': 'Teacher'}]

users = [
    {
        'username': 'admin',
        'name': 'Admin',
        'role': 'Admin',
        'password': 'admin'
    },
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

publications_status = [
    {'name': 'Open'},
    {'name': 'Close'}
]


@pytest.fixture
def get_db():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    db.create_all()
    yield None
    db.drop_all()


@pytest.fixture
def add_admin():
    db.session.add(models.Role('Admin'))
    db.session.add(models.User(**users[0]))
    db.session.commit()
    credentials = base64.b64encode(b'admin:admin').decode('utf-8')
    admin = app.test_client().get('/login', headers={'Authorization': f'Basic {credentials}'})
    return admin.json['token']


def test_empty_db(get_db):
    r = app.test_client().get('/rest/users')
    assert r.json == []


def test_get_role(get_db):
    for role in roles:
        db.session.add(models.Role(**role))
    db.session.commit()

    r = app.test_client().get('/rest/roles')
    assert r.json == roles


def test_add_role(get_db, add_admin):
    r1 = app.test_client().post('/rest/roles', json=roles[1], headers={'X-Api-Key': add_admin})
    r2 = app.test_client().get('/rest/roles')
    r3 = app.test_client().get('/rest/roles/Student')
    assert r1.json == roles[1]
    assert r2.json == [roles[0], roles[1]]
    assert r3.json == roles[1]


def test_remove_role(get_db, add_admin):
    db.session.add(models.Role('Teacher'))
    db.session.commit()

    r = app.test_client().delete('/rest/roles/Teacher', headers={'X-Api-Key': add_admin})
    assert r.status_code == 204
    assert roles[2] not in app.test_client().get('/rest/roles').json


def test_get_user(get_db):
    for user in users:
        db.session.add(models.User(**user))
    db.session.commit()

    r = app.test_client().get('/rest/users').json
    for i in range(len(users)):
        for j in users[i]:
            if j != 'password':
                assert r[i][j] == users[i][j]
            else:
                assert check_password_hash(r[i][j], users[i][j])


def test_add_user(get_db, add_admin):
    for i in roles:
        app.test_client().post('/rest/roles', json=i, headers={'X-Api-Key': add_admin})
    for i in users:
        app.test_client().post('/rest/users', json=i)
    r = app.test_client().get('/rest/users').json
    for i in range(len(users)):
        for j in users[i]:
            if j != 'password':
                assert r[i][j] == users[i][j]
            else:
                assert check_password_hash(r[i][j], users[i][j])


def test_remove_user(get_db):
    db.session.add(models.Role(**roles[2]))
    db.session.add(models.User(**users[2]))
    db.session.commit()

    credentials = base64.b64encode(bytes(f'{users[2]["username"]}:{users[2]["password"]}', encoding='utf-8')).decode('utf-8')
    user = app.test_client().get('/login', headers={'Authorization': f'Basic {credentials}'})

    r = app.test_client().delete('/rest/users/1', headers={'X-Api-Key': user.json['token']})
    assert r.status_code == 204
    assert models.User.query.filter_by(username=users[2]['username']).first() is None


def test_get_publications_status(get_db):
    for status in publications_status:
        db.session.add(models.PublicationStatus(**status))
    db.session.commit()

    r = app.test_client().get('/rest/publications_status')
    assert r.json == publications_status


def test_add_publications_status(get_db, add_admin):
    r1 = app.test_client().post('/rest/publications_status', json=publications_status[0], headers={'X-Api-Key': add_admin})
    r2 = app.test_client().get('/rest/publications_status')
    r3 = app.test_client().get('/rest/publications_status/Open')
    assert r1.json == publications_status[0]
    assert r2.json == [publications_status[0]]
    assert r3.json == publications_status[0]


def test_remove_publications_status(get_db, add_admin):
    db.session.add(models.PublicationStatus('Open'))
    db.session.commit()

    r = app.test_client().delete('/rest/publications_status/Open', headers={'X-Api-Key': add_admin})
    assert r.status_code == 204
    assert publications_status[0] not in app.test_client().get('/rest/publications_status').json
