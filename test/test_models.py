import pytest
from app import create_app, db, utils
from app.models import User


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    yield app


@pytest.fixture
def database(app):
    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()


def test_create_test_instance(app, database):
    salt, hashed_password = utils.compute_sha256('password')
    test_instance = User(username='test_user', salt=salt, hashed_password=hashed_password)
    database.session.add(test_instance)
    database.session.commit()
    queried_test_instance = User.query.filter_by(username='test_user').first()
    assert queried_test_instance is not None
    assert queried_test_instance.username == 'test_user'
    assert queried_test_instance.hashed_password == hashed_password



