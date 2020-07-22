from validation import OneOf, String, Boolean, Email, Integer, PayloadError
from collections import defaultdict


class Questionnaire:
    first_name = String(minsize=1, maxsize=64)
    address = String(minsize=1, maxsize=64)
    occupation = OneOf('Employed', 'Student', 'Self-Employed')
    email_address = Email()
    children = Boolean()
    num_children = Integer(minvalue=0, maxvalue=25)
    insurance = defaultdict(list)

    def __init__(self, **kwargs):
        try:
            self.first_name = kwargs['first_name'] if 'first_name' in kwargs else None
            self.address = kwargs['address'] if 'first_name' in kwargs else None
            self.occupation = kwargs['occupation'] if 'first_name' in kwargs else None
            self.email_address = kwargs['email_address'] if 'first_name' in kwargs else None
            self.children = kwargs['children'] if 'first_name' in kwargs else None
            self.num_children = kwargs['num_children'] if 'first_name' in kwargs else 0
        except ValueError as e:
            raise PayloadError(str(e))

    def __repr__(self):
        return f'{self.__class__.__name__}({self.first_name!r}, {self.address!r}, {self.occupation!r})'

    def recommendation(self):
        return 'Health insurance.'
