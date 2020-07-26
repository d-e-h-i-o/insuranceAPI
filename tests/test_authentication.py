def test_authentication_register(client):
    rv = client.post(
        "/register", json={"username": "test", "email": "test@test.com", "password": "password"}
    )
    assert rv.status_code == 201


def test_authentication_register_double(client, auth):
    rv1 = auth.register()
    auth.logout()
    rv2 = auth.register()
    assert b'"Successfully registered and logged in."\n' == rv1.data
    assert b'{"error":"Username is already taken."}\n' == rv2.data


def test_authentication_login(client, auth):
    auth.register()
    auth.logout()
    rv = client.post(
        "/login", json={"username": "test", "password": "password"}
    )
    assert rv.status_code == 200


def test_authentication_logout(client, auth):
    auth.register()
    rv = client.get(
        "/logout"
    )
    assert rv.status_code == 200


def test_authentication_register_wrong_args(client):
    rv = client.post(
        "/register", json={"username": "test", "email": "test@test.com", "password": "p"}
    )
    assert rv.status_code == 422
    assert rv.data == b'{"error":"Password must be at least 6 characters long."}\n'

    rv = client.post(
        "/register", json={"email": "test@test.com", "password": "password"}
    )
    assert rv.status_code == 422
    assert rv.data == b'{"error":"Field \'_username\' is missing."}\n'

    rv = client.post(
        "/register", json={"username": "test", "password": "password"}
    )
    assert rv.status_code == 422
    assert rv.data == b'{"error":"Field \'_email\' is missing."}\n'

    rv = client.post(
        "/register", json={"username": "test", "email": "test@test.com"}
    )
    assert rv.status_code == 422
    assert rv.data == b'{"error":"Field \'password\' is missing."}\n'
