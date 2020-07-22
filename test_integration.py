import os
import tempfile
from random import randint
import pytest

from app import app, db


@pytest.fixture()
def client():
    app.config['TESTING'] = True
    db_name = f'test_{randint(0, 999999)}'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql:///{db_name}'
    os.system(f"psql -c 'create database {db_name};'")

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

    db.
    os.system(f"psql -c 'drop database {db_name};'")


def test_base(client):
    registration = {"username": "Niklas35",
                    "password": "something",
                    "email": "niklas.dehio63@gmail.com"}
    rv1 = client.post('/register', json=registration)
    print('rv:', rv1.data)
    rv2 = client.post('/register', json=registration)
    print('rv:', rv2.data)
    assert b'Successfully registered and logged in.' == rv1.data
    assert b'Already authenticated.' == rv2.data
