from hypothesis import given, settings
import hypothesis.strategies as st


@settings(deadline=None)
@given(first_name=st.characters(), address=st.characters(), occupation=st.characters(), email=st.characters(),
       children=st.booleans(), num_children=st.integers())
def test_torture_recommendation_(client_torture, auth_torture, first_name, address, occupation, email, children, num_children):
    """Tests whether the app can handle a wild range of inputs. The goal is to avoid having a 500 error code, but
    to provide specific error answers."""
    auth_torture.register()
    payload = {
        "first_name": first_name,
        "address": address,
        "occupation": occupation,
        "email_address": email,
        "children": children,
        "num_children": num_children
    }
    rv = client_torture.post('/recommendation', json=payload)
    assert rv.status_code in [201, 200, 422, 401]
