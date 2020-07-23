import pytest
from api_app import create_app
from api_app.models import User


@pytest.fixture()
def client():
    db_path = f'postgresql:///insuranceapi_test'
    app = create_app({"TESTING": True, "DATABASE": db_path})

    with app.test_client() as client:
        yield client
    from api_app.db import engine
    User.__table__.drop(engine)


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def register(self, username="test", email='test@test.com', password="password"):
        return self._client.post(
            "/register", json={"username": username, "email": email, "password": password}
        )

    def login(self, username="test", password="password"):
        return self._client.post(
            "/auth/login", json={"username": username, "password": password}
        )

    def logout(self):
        return self._client.get("/auth/logout")


@pytest.fixture()
def auth(client):
    return AuthActions(client)


@pytest.fixture(scope='module')
def client_torture():
    db_path = f'postgresql:///insuranceapi_test'
    app = create_app({"TESTING": True, "DATABASE": db_path})

    with app.test_client() as client:
        yield client
    from api_app.db import engine
    User.__table__.drop(engine)


@pytest.fixture(scope='module')
def auth_torture(client_torture):
    return AuthActions(client_torture)
