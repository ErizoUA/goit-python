from .fields import Name, Address, Phone, Email, Birthday


class Person:

    def __init__(self,
                 name: Name = None,
                 address: Address = None,
                 phone: Phone = None,
                 email: Email = None,
                 birthday: Birthday = None):

        self.name = name
        self.address = address
        self.phone = phone
        self.email = email
        self.birthday = birthday

    def __str__(self):
        return f"{self.name}, {self.address}, {self.phone}, {self.email}, {self.birthday}"
