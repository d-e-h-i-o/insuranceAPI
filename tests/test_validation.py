

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
    assert rv1.data == b'Successfully registered and logged in.'
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

    payload = {
        "first_name": 1,
        "address": "Musterweg 21",
        "occupation": "Employed",
        "email_address": "niklas.dehio@gmail.com",
        "children": False
    }
    rv = client.post('/recommendation', json=payload)
    assert rv.status_code == 422
    assert rv.data == b'{"error":"Expected a str for \'first_name\'."}\n'

    payload = {
        "address": "Musterweg 21",
        "occupation": "Employed",
        "email_address": "niklas.dehio@gmail.com",
        "children": False
    }
    rv = client.post('/recommendation', json=payload)
    assert rv.status_code == 422
    assert rv.data == b'{"error":"Field \'first_name\' is missing."}\n'

def test_validation_recommendation_address(client, auth):
    auth.register()
    payload = {
        "first_name": "Niklas",
        "address": 1,
        "occupation": "Employed",
        "email_address": "niklas.dehio@gmail.com",
        "children": False
    }
    rv = client.post('/recommendation', json=payload)
    assert rv.status_code == 422
    assert rv.data == b'{"error":"Expected a str for \'address\'."}\n'

    payload = {
        "first_name": "Niklas",
        "occupation": "Employed",
        "email_address": "niklas.dehio@gmail.com",
        "children": False
    }
    rv = client.post('/recommendation', json=payload)
    assert rv.status_code == 422
    assert rv.data == b'{"error":"Field \'address\' is missing."}\n'