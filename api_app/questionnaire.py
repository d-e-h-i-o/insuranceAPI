from api_app.validation import OneOf, String, Boolean, Email, Integer, PayloadError
from collections import defaultdict
from flask import jsonify


class Questionnaire:
    """Validates and saves the payload and gives a insurance validation."""
    first_name = String(minsize=1, maxsize=64)
    address = String(minsize=1, maxsize=64)
    occupation = OneOf('Employed', 'Student', 'Self-Employed')
    email_address = Email()
    children = Boolean()
    num_children = Integer(minvalue=0, maxvalue=25)
    insurance = defaultdict(list)

    def __init__(self, **kwargs):
        """Validates and initialises the questionnaire data."""

        if not kwargs:
            raise PayloadError('''Invalid data. Must be of type application/json and contain the following fields:
                  'first_name': String,
                  'address': String,
                  'occupation': String(OneOf('Employed', 'Student', 'Self-Employed')),
                  'email_address': String,
                  'children': Boolean,
                  'num_children': Optional(int)
                ''')
        try:
            self.first_name = kwargs.get('first_name', None)
            self.address = kwargs.get('address', None)
            self.occupation = kwargs.get('occupation', None)
            self.email_address = kwargs.get('email_address', None)
            self.children = kwargs.get('children', None)
            self.num_children = kwargs.get('num_children', 0)
        except ValueError as e:
            raise PayloadError(str(e))

    def __repr__(self):
        return f'{self.__class__.__name__}({self.first_name!r}, {self.address!r}, {self.occupation!r})'

    def recommendation(self):
        return jsonify('Health insurance.')
