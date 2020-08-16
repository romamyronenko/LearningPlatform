import jwt
import copy
from werkzeug.security import check_password_hash
import base64
import pytest
from app import app, db, models
from app import schemas
from tests import data


def get_user_id(username):
    return models.User.query.filter_by(username=username).first().id


def get_publication_id(name):
    return models.Publication.query.filter_by(name=name).first().id


def get_group_id(name):
    return models.Group.query.filter_by(name=name).first().id


def get_user_password(username):
    for i in data.users:
        if i['username'] == username:
            return i['password']


def get_token(user_data):
    credentials = base64.b64encode(bytes(f'{user_data["username"]}:{user_data["password"]}', 'utf-8')).decode('utf-8')
    user = app.test_client().get('/login', headers={'Authorization': f'Basic {credentials}'})
    return user.json['token']


@pytest.fixture
def get_db():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    db.create_all()
    yield None
    db.drop_all()


@pytest.fixture
def add_admin():
    db.session.add(models.Role(**data.roles[0]))
    db.session.add(models.User(**data.users[0]))
    db.session.commit()
    return get_token(data.users[0])


@pytest.fixture
def add_users():
    for user in data.users:
        db.session.add(models.User(**user))
    db.session.commit()

    users = schemas.UserSchema(many=True).dump(models.User.query.all())
    for i in range(len(users)):
        users[i]['password'] = get_user_password(users[i]['username'])
    return users


@pytest.fixture
def add_publications():
    publications = copy.deepcopy(data.publications)
    for publication in publications:
        publication['user_id'] = get_user_id(publication['username'])
        del publication['username']
        db.session.add(models.Publication(**publication))
    db.session.commit()

    return schemas.PublicationSchema(many=True).dump(models.Publication.query.all())


def test_empty_db(get_db):
    r = app.test_client().get('/rest/users')
    assert r.json == []


def test_get_role(get_db):
    for role in data.roles:
        db.session.add(models.Role(**role))
    db.session.commit()

    r = app.test_client().get('/rest/roles')
    assert r.json == data.roles


def test_add_role(get_db, add_admin):
    r1 = app.test_client().post('/rest/roles', json=data.roles[1], headers={'X-Api-Key': add_admin})
    r2 = app.test_client().get('/rest/roles')
    r3 = app.test_client().get('/rest/roles/Student')
    assert r1.json == data.roles[1]
    assert r2.json == [data.roles[0], data.roles[1]]
    assert r3.json == data.roles[1]


def test_remove_role(get_db, add_admin):
    db.session.add(models.Role('Teacher'))
    db.session.commit()

    r = app.test_client().delete('/rest/roles/Teacher', headers={'X-Api-Key': add_admin})
    assert r.status_code == 204
    assert data.roles[2] not in app.test_client().get('/rest/roles').json


def test_get_user(get_db):
    for user in data.users:
        db.session.add(models.User(**user))
    db.session.commit()

    r = app.test_client().get('/rest/users').json
    for i in range(len(data.users)):
        for j in data.users[i]:
            if j != 'password':
                assert r[i][j] == data.users[i][j]
            else:
                assert check_password_hash(r[i][j], data.users[i][j])


def test_add_user(get_db, add_admin):
    for i in data.roles:
        app.test_client().post('/rest/roles', json=i, headers={'X-Api-Key': add_admin})
    for i in data.users:
        app.test_client().post('/rest/users', json=i)
    r = app.test_client().get('/rest/users').json
    for i in range(len(data.users)):
        for j in data.users[i]:
            if j != 'password':
                assert r[i][j] == data.users[i][j]
            else:
                assert check_password_hash(r[i][j], data.users[i][j])


def test_remove_user(get_db):
    db.session.add(models.Role(**data.roles[2]))
    db.session.add(models.User(**data.users[2]))
    db.session.commit()

    credentials = base64.b64encode(bytes(f'{data.users[2]["username"]}:{data.users[2]["password"]}',
                                         encoding='utf-8')).decode('utf-8')
    user = app.test_client().get('/login', headers={'Authorization': f'Basic {credentials}'})

    r = app.test_client().delete(f'/rest/users/{get_user_id(data.users[2]["username"])}',
                                 headers={'X-Api-Key': user.json['token']})
    assert r.status_code == 204
    assert models.User.query.filter_by(username=data.users[2]['username']).first() is None


def test_get_publications_status(get_db):
    for status in data.publications_status:
        db.session.add(models.PublicationStatus(**status))
    db.session.commit()

    r = app.test_client().get('/rest/publications_status')
    assert r.json == data.publications_status


def test_add_publications_status(get_db, add_admin):
    r1 = app.test_client().post('/rest/publications_status',
                                json=data.publications_status[0],
                                headers={'X-Api-Key': add_admin})
    r2 = app.test_client().get('/rest/publications_status')
    r3 = app.test_client().get(f'/rest/publications_status/{data.publications_status[0]["name"]}')
    assert r1.json == data.publications_status[0]
    assert r2.json == [data.publications_status[0]]
    assert r3.json == data.publications_status[0]


def test_remove_publications_status(get_db, add_admin):
    db.session.add(models.PublicationStatus('Open'))
    db.session.commit()

    r = app.test_client().delete('/rest/publications_status/Open', headers={'X-Api-Key': add_admin})
    assert r.status_code == 204
    assert data.publications_status[0] not in app.test_client().get('/rest/publications_status').json


def test_add_publication(get_db, add_users):
    publications = copy.deepcopy(data.publications)
    for i in publications:
        i['user_id'] = get_user_id(i['username'])
        del i['username']
        db.session.add(models.Publication(**i))
        app.test_client().post('/rest/publications', json=i, headers={'X-Api-Key': get_token(data.users[1])})

    pubs = schemas.PublicationSchema(many=True).dump(models.Publication.query.all())
    for i in range(len(pubs)):
        del pubs[i]['date']
        del pubs[i]['id']
    assert pubs == publications


def test_remove_publication(get_db, add_users):
    publication = copy.copy(data.publications[0])
    publication['user_id'] = get_user_id(publication['username'])
    del publication['username']
    db.session.add(models.Publication(**publication))
    db.session.commit()

    app.test_client().delete('/rest/publications/1', headers={'X-Api-Key': get_token(data.users[2])})  # not owner
    pub_data = schemas.PublicationSchema(many=True).dump(models.Publication.query.all())
    del pub_data[0]['date']
    del pub_data[0]['id']
    r1 = app.test_client().delete('/rest/publications/1', headers={'X-Api-Key': get_token(data.users[1])})  # owner

    assert r1.status_code == 204
    assert pub_data == [publication]
    assert not models.Publication.query.all()


def test_add_publication_permission_student(get_db, add_users, add_publications):
    user_id = get_user_id(data.publications_permissions_student[0]['username'])
    publication_id = get_publication_id(data.publications_permissions_student[0]['publication_name'])
    publication_permission_student = {'publication_id': publication_id,
                                      'user_id': user_id}
    r1 = app.test_client().post('/rest/publications_permissions_students',
                               json=publication_permission_student,
                               headers={'X-Api-Key': get_token(data.users[0])})

    r2 = app.test_client().post('/rest/publications_permissions_students',
                               json=publication_permission_student,
                               headers={'X-Api-Key': get_token(data.users[1])})

    r3 = app.test_client().get('/rest/publications', headers={'X-Api-Key': get_token(data.users[4])})
    assert r1.status_code == 400
    assert r2.status_code == 201
    assert r2.json['user_id'] == user_id
    assert r2.json['publication_id'] == publication_id
    assert r3.json == add_publications


def test_remove_publication_permission_student(get_db, add_users, add_publications):
    pps = data.publications_permissions_student[0]
    user_id = get_user_id(pps['username'])
    publication_id = get_publication_id(pps['publication_name'])
    publication_permission_student = {'publication_id': publication_id,
                                      'user_id': user_id}
    db.session.add(models.PublicationPermissionStudent(**publication_permission_student))
    db.session.commit()

    r1 = app.test_client().delete('/rest/publications_permissions_students/1', headers={'X-Api-Key': get_token(data.users[1])})
    assert r1.status_code == 204
    assert not app.test_client().get('/rest/publications_permissions_students').json


def test_add_group(get_db, add_users):
    group = copy.copy(data.groups[0])
    group['user_id'] = get_user_id(group['username'])
    del group['username']
    r = app.test_client().post('/rest/groups', json=group, headers={'X-Api-Key': get_token(data.users[1])})
    assert r.json['name'] == group['name']
    assert r.json['user_id'] == group['user_id']
    assert r.status_code == 201


def test_remove_group(get_db, add_users):
    group = copy.copy(data.groups[0])
    group['user_id'] = get_user_id(group['username'])
    del group['username']
    db.session.add(models.Group(**group))
    db.session.commit()

    r = app.test_client().delete('/rest/groups/1', headers={'X-Api-Key': get_token(data.users[1])})
    assert r.status_code == 204
    assert not app.test_client().get('/rest/groups').json


def test_add_group_student(get_db, add_users):
    group = copy.copy(data.groups[0])
    group['user_id'] = get_user_id(group['username'])
    del group['username']
    db.session.add(models.Group(**group))
    db.session.commit()

    gs = copy.copy(data.groups_students[0])
    gs['group_id'] = get_group_id(gs['group_name'])
    gs['user_id'] = get_user_id(gs['username'])
    del gs['group_name']
    del gs['username']
    r1 = app.test_client().post('/rest/group_student', json=gs, headers={'X-Api-Key': get_token(data.users[1])})
    assert r1.status_code == 201


def test_remove_group_student(get_db, add_users):
    group = copy.copy(data.groups[0])
    group['user_id'] = get_user_id(group['username'])
    del group['username']
    db.session.add(models.Group(**group))
    db.session.commit()

    gs = copy.copy(data.groups_students[0])
    gs['group_id'] = get_group_id(gs['group_name'])
    gs['user_id'] = get_user_id(gs['username'])
    del gs['group_name']
    del gs['username']
    db.session.add(models.GroupStudent(**gs))
    db.session.commit()

    r = app.test_client().delete('/rest/group_student/1', headers={'X-Api-Key': get_token(data.users[1])})
    assert r.status_code == 204
    assert not app.test_client().get('/rest/group_student').json


def test_add_publication_permission_group(get_db, add_users, add_publications):
    group = copy.copy(data.groups[0])
    group['user_id'] = get_user_id(group['username'])
    del group['username']
    db.session.add(models.Group(**group))
    db.session.commit()

    ppg = copy.copy(data.publications_permissions_group[0])
    ppg['group_id'] = get_group_id(ppg['group_name'])
    ppg['publication_id'] = get_publication_id(ppg['publication_name'])
    del ppg['group_name']
    del ppg['publication_name']
    r1 = app.test_client().post('/rest/publications_permissions_groups',
                                json=ppg,
                                headers={'X-Api-Key': get_token(data.users[1])})

    assert r1.status_code == 201


def test_remove_publication_permission_group(get_db, add_users, add_publications):
    group = copy.copy(data.groups[0])
    group['user_id'] = get_user_id(group['username'])
    del group['username']
    db.session.add(models.Group(**group))
    db.session.commit()

    ppg = copy.copy(data.publications_permissions_group[0])
    ppg['group_id'] = get_group_id(ppg['group_name'])
    ppg['publication_id'] = get_publication_id(ppg['publication_name'])
    del ppg['group_name']
    del ppg['publication_name']

    db.session.add(models.PublicationPermissionGroup(**ppg))
    db.session.commit()
    r1 = app.test_client().delete('/rest/publications_permissions_groups/1',
                                  headers={'X-Api-Key': get_token(data.users[1])})
    assert r1.status_code == 204
    assert not app.test_client().get('/rest/publications_permissions_groups').json


def test_add_task(get_db, add_users):
    r1 = app.test_client().post('/rest/tasks', json=dict(), headers={'X-Api-Key': get_token(data.users[1])})
    assert r1.status_code == 201


def test_remove_task(get_db, add_users):
    task = copy.copy(data.tasks[0])
    task['user_id'] = get_user_id(task['username'])
    del task['username']
    db.session.add(models.Task(**task))
    db.session.commit()

    r1 = app.test_client().delete('/rest/tasks/1', headers={'X-Api-Key': get_token(data.users[1])})

    assert r1.status_code == 204
    assert not app.test_client().get('/rest/tasks').json


def test_add_rating_fields(get_db, add_users):
    group = copy.copy(data.groups[0])
    group['user_id'] = get_user_id(group['username'])
    del group['username']
    db.session.add(models.Group(**group))
    db.session.commit()

    rf = copy.copy(data.rating_fields[0])
    r1 = app.test_client().post('/rest/rating_fields',
                                json=rf,
                                headers={'X-Api-Key': get_token(data.users[1])})
    rf['id'] = 1
    assert r1.status_code == 201
    assert r1.json == rf


def test_remove_rating_fields(get_db, add_users):
    group = copy.copy(data.groups[0])
    group['user_id'] = get_user_id(group['username'])
    del group['username']
    db.session.add(models.Group(**group))
    db.session.commit()

    rf = copy.copy(data.rating_fields[0])
    db.session.add(models.RatingFields(**rf))
    db.session.commit()

    r1 = app.test_client().delete('/rest/rating_fields/1', headers={'X-Api-Key': get_token(data.users[1])})

    assert r1.status_code == 204
    assert not app.test_client().get('/rest/rating_fields').json


def test_add_rating_list():
    pass


def test_remove_rating_list():
    pass


def test_add_question_type():
    pass


def test_remove_question_type():
    pass


def test_add_question():
    pass


def test_remove_question():
    pass


def test_add_tests():
    pass


def test_remove_tests():
    pass


def test_add_answers():
    pass


def test_remove_answers():
    pass
