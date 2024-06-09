import pytest
from app import create_app, db


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True

    with app.app_context():
        db.create_all()
        yield app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    res = "home page"
    assert res in response.data.decode('utf-8')


def test_register_route(client):
    data = {"username": "luffy000", "password": "iam@KINGOFPIRATES"}
    response = client.post('/register', json=data)
    assert response.status_code == 201


def test_login_route(client):
    data = {"username": "luffy000", "password": "iam@KINGOFPIRATES"}
    response = client.post('/login', json=data)
    assert response.status_code == 200