import json


def test_recommendation_employed(client, auth):
    auth.register()
    payload = {
        "first_name": "Niklas",
        "address": "Some street",
        "occupation": "Employed",
        "email_address": "test.mustermann@gmail.com",
        "children": False
    }
    rv = client.post(
            "/recommendation", json=payload
        )
    assert rv.status_code == 200
    recommendation = json.loads(rv.data)
    assert 'Job' in recommendation['needed']


def test_recommendation_many_children(client, auth):
    auth.register()
    payload = {
        "first_name": "Niklas",
        "address": "Some street",
        "occupation": "Student",
        "email_address": "test.mustermann@gmail.com",
        "children": True,
        "num_children": 10
    }
    rv = client.post(
            "/recommendation", json=payload
        )
    assert rv.status_code == 200
    recommendation = json.loads(rv.data)
    assert 'Household content' in recommendation['needed']
    assert 'Job' not in recommendation['needed']
    assert not recommendation['optional']