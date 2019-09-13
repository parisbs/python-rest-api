import pytest

from config import Test
from rest_api import create_api
from rest_api import db as _db


@pytest.fixture(scope='session', name='app')
def fixture_app():
    app = create_api(Test)
    context = app.app_context()
    context.push()
    yield app
    context.pop()


@pytest.fixture(scope='session', name='db')
def fixture_db(app):
    _db.app = app
    _db.create_all()
    yield _db
    _db.drop_all()


@pytest.fixture(scope='function', name='session')
def fixture_session(db):
    connection = db.engine.connect()
    transaction = connection.begin()
    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)
    db.session = session
    yield session
    transaction.rollback()
    connection.close()
    session.remove()


@pytest.fixture(autouse=True)
def patch_factory_db_session(monkeypatch, session):
    factories = ['UserFactory']
    for factory in factories:
        path = ('tests.unit.factories.'
                '{}._meta.sqlalchemy_session').format(factory)
        monkeypatch.setattr(path, session)


@pytest.fixture(autouse=True)
def patch_verify_oauth2_token(monkeypatch):
    user = {
        'iss': 'https://accounts.google.com',
        'aud': 'client1',
        'sub': '1',
    }
    path = 'google.oauth2.id_token.verify_oauth2_token'
    monkeypatch.setattr(path, lambda token, request: user)
