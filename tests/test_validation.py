import json

def test_base(client):
    registration = {"username": "Niklas35",
                    "password": "something",
                    "email": "niklas.dehio63@gmail.com"}
    rv1 = client.post('/register', json=registration)
    rv2 = client.post('/register', json=registration)
    assert b'Successfully registered and logged in.' == rv1.data
    assert b'{"error":"Username is already taken."}\n' == rv2.data

def test_get_recommendation(client, auth):
    auth.login()
    registration = {"username": "Niklas35",
                    "password": "something",
                    "email": "niklas.dehio63@gmail.com"}
    rv1 = client.post('/register', json=registration)
    assert b'Successfully registered and logged in.' == rv1.data
    auth.login()

def test_validation_recommendation_empty(client, auth):
    auth.login()
    payload = {}
    rv = client.post('/recommendation', json=payload)
    assert rv.status_code == 401

def test_validation_recommendation_first_name(client, auth):
    auth.register()
    payload = {
      "first_name": "Niklas",
      "address": "Musterweg 21",
      "occupation": "Employed",
      "email_address": "niklas.dehio@gmail.com",
      "children": False
    }
    rv = client.post('/recommendation', json=payload)
    assert rv.status_code == 200