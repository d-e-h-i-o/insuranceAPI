def test_authentification_register(client):
    rv = client.post(
        "/register", json={"username": "test", "email": "test@test.com", "password": "password"}
    )
    assert rv.status_code == 200


def test_authentification_register_double(client):
    rv = client.post(
        "/register", json={"username": "test", "email": "test@test.com", "password": "password"}
    )
    assert rv.status_code == 200

    rv = client.post(
        "/register", json={"username": "test", "email": "test@test.com", "password": "password"}
    )
    assert rv.status_code == 422
    assert rv.data == b'{"error":"Username is already taken."}\n'


def test_authentification_login(client, auth):
    auth.register()
    auth.logout()
    rv = client.post(
        "/login", json={"username": "test", "password": "password"}
    )
    assert rv.status_code == 200


def test_authentification_logout(client, auth):
    auth.register()
    rv = client.get(
        "/logout"
    )
    assert rv.status_code == 200


def test_authentification_register_wrong_args(client):
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
