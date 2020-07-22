import pytest
import os
from api_app import create_app
from api_app.db import init_db, init_engine
from random import randint
from config import Config
from api_app.db import Base
from api_app.models import User


@pytest.fixture()
def client():

    db_name = f'test_{randint(0, 999999)}'
    #os.system(f"psql -c 'create database {db_name};'")
    db_path = f'postgresql:///insuranceapi_test'
    app = create_app({"TESTING": True, "DATABASE": db_path})

    with app.test_client() as client:
        yield client
    from api_app.db import engine
    User.__table__.drop(engine)
    #os.system(f"psql -c 'drop database {db_name};'")

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username="test", password="test"):
        return self._client.post(
            "/auth/login", data={"username": username, "password": password}
        )

    def logout(self):
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client):
    return AuthActions(client)


def test_base(client):
    registration = {"username": "Niklas35",
                    "password": "something",
                    "email": "niklas.dehio63@gmail.com"}
    rv1 = client.post('/register', json=registration)
    print('rv:', rv1.data)
    rv2 = client.post('/register', json=registration)
    print('rv:', rv2.data)
    assert b'Successfully registered and logged in.' == rv1.data
    assert b'Username is already taken.' == rv2.data

def test_get_recommendation(client, auth):
    auth.login()
    registration = {"username": "Niklas35",
                    "password": "something",
                    "email": "niklas.dehio63@gmail.com"}
    rv1 = client.post('/register', json=registration)
    assert b'Successfully registered and logged in.' == rv1.data
    auth.login()