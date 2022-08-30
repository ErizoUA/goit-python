from collections import UserDict
from datetime import datetime as dt
import re


class CustomException(Exception):
    pass


class WrongPhoneNumber(CustomException):
    def __init__(self, phone, message="Phone number is not correct. Enter as +380(XX)XXX-XX-XX"):
        self.phone = phone
        self.message = message

    def __str__(self):
        return f'{self.phone} -> {self.message}'


class WrongBirthdayFormat(CustomException):
    def __init__(self, birthday, message="Wrong birthday format. Enter as DD.MM.YYYY"):
        self.birthday = birthday
        self.message = message

    def __str__(self):
        return f'{self.birthday} -> {self.message}'


class Field:
    def __init__(self, value: str):
        self.value = value

    def __repr__(self):
        return f'{self.value}'


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        self.__value = None
        super().__init__(value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if re.match(r'[+380]{0,4}\(?\w{2,3}\)?\w{3}-?\w{2}-?\w{2}', value):
            self.__value = value
        else:
            raise WrongPhoneNumber(value)


class Birthday(Field):
    def __init__(self, value):
        self.__value = None
        super().__init__(value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        try:
            dt.strptime(value, '%d.%m.%Y')
            self.__value = value
        except ValueError:
            raise WrongBirthdayFormat(value)


class Record:
    def __init__(self, name: Name, phones: Phone = None, birthday: Birthday = None):
        self.name = name
        self.phones = [] if phones is None else [str(phones)]
        self.birthday = str(birthday)

    def __repr__(self):
        return f'{self.name}, {self.phones}, {self.birthday}'

    def add_phone(self, phone_number: Phone) -> None:
        self.phones.append(str(phone_number))

    def del_phone(self, phone_number: str) -> None:
        try:
            self.phones.remove(phone_number)
        except ValueError:
            print(f'Phone number {phone_number} does not exist')

    def change_phone(self, old_number: str, new_number: Phone) -> None:
        try:
            self.phones.remove(old_number)
            self.phones.append(str(new_number))
        except ValueError:
            print(f'Old number {old_number} does not exist')

    def days_to_birthday(self):

        birthday = dt.strptime(self.birthday, '%d.%m.%Y')
        try:
            date = birthday.replace(year=dt.now().year)
        except ValueError:
            date = birthday.replace(year=dt.now().year, day=date.day - 1)

        if date.date() > dt.now().date():
            return f'{(date.date() - dt.now().date()).days} days'
        else:
            return f'{(date.replace(year=dt.now().year + 1).date() - dt.now().date()).days} days'


class AddressBook(UserDict):

    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def iterator(self, quantity=10):
        count = 0
        for person in iter(self.data.values()):
            while count < quantity:
                count += 1
                yield person
                break

    def find_name(self, symbols: str):

        for name, contact in self.data.items():
            if symbols.lower() in name:
                print(contact)

    def find_phone(self, number: int):
        for contact in self.data.values():
            for numbers in contact.phones:
                if str(number) in numbers:
                    print(contact)
