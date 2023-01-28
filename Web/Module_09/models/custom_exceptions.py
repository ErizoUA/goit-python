class CustomException(Exception):
    ...


class WrongNameFormat(CustomException):
    def __init__(self, name, message="Name must be at least 1 letter"):
        self.name = name
        self.message = message

    def __str__(self):
        return f'{self.name} -> {self.message}'
