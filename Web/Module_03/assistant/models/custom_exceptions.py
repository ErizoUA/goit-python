class CustomException(Exception):
    ...


# class WrongPhoneNumber(CustomException):
#     def __init__(self, phone, message="Phone number is not correct. Enter as +380(XX)XXX-XX-XX"):
#         self.phone = phone
#         self.message = message
#
#     def __str__(self):
#         return f'{self.phone} -> {self.message}'


# class WrongBirthdayFormat(CustomException):
#     def __init__(self, birthday, message="Wrong birthday format. Enter as yyyy-mm-dd"):
#         self.birthday = birthday
#         self.message = message
#
#     def __str__(self):
#         return f'{self.birthday} -> {self.message}'


class WrongNameFormat(CustomException):
    def __init__(self, name, message="Name must be at least 1 letter"):
        self.name = name
        self.message = message

    def __str__(self):
        return f'{self.name} -> {self.message}'
