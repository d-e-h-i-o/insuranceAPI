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

    def __init__(self, first_name, address, occupation, email_address, children, num_children=0):
        try:
            self.first_name = first_name
            self.address = address
            self.occupation = occupation
            self.email_address = email_address
            self.children = children
            self.num_children = num_children
        except ValueError as e:
            print(e)
            raise PayloadError(str(e))
        except TypeError as e:
            print(e)
            raise PayloadError('''Invalid data. Must be of format:
                              "first_name": String,
                              "address": String,
                              "occupation": String(OneOf('Employed', 'Student', 'Self-Employed')),
                              "email_address": String,
                              "children": Boolean,
                              "num_children": Optional(int)
                                ''')

    def __repr__(self):
        return f'{self.__class__.__name__}({self.first_name!r}, {self.address!r}, {self.occupation!r})'

    def recommendation(self):
        return 'Health insurance.'
