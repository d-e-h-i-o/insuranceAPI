import pytest
import os
from api_app import create_app
from api_app.db import init_db, init_engine
from random import randint
from config import Config
from api_app.db import Base
from api_app.models import User
import json


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


@pytest.fixture
def auth(client):
    return AuthActions(client)


