from validation import OneOf, String, Boolean, Email, Integer
from collections import defaultdict


class Questionnaire:
    first_name = String(minsize=1, maxsize=64)
    address = String(minsize=1, maxsize=64)
    occupation = OneOf('Employed', 'Student', 'Self-Employed')
    email_address = Email()
    children = Boolean()
    num_children = Integer(minvalue=0, maxvalue=25)
    insurance = defaultdict(list)

    def __init__(self, first_name, address, occupation, email_address, children, num_children=0):
        self.first_name = first_name
        self.address = address
        self.occupation = occupation
        self.email_address = email_address
        self.children = children
        self.num_children = num_children

    def __repr__(s):
        return f'{s.__class__.__name__}({s.first_name!r}, {s.address!r}, {s.occupation!r})'

    def recommendation(self):
        return 'Health insurance.'
