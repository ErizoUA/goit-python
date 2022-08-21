from collections import UserDict


class Field:
    def __init__(self, value: str):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, phones: str):
        self.phones = phones

    def __repr__(self):
        return f'{self.phones}'


class Record:
    def __init__(self, name: Name, phones: Phone = None):
        self.name = name
        self.phones = [] if phones is None else [str(phones)]

    def __repr__(self):
        return f'{self.phones}'

    def add_phone(self, phone_number: str) -> None:
        self.phones.append(phone_number)

    def del_phone(self, phone_number: str) -> None:
        try:
            self.phones.remove(phone_number)
        except ValueError:
            print(f'Phone number {phone_number} does not exist')

    def change_phone(self, old_number: str, new_number: str) -> None:
        try:
            self.phones.remove(old_number)
            self.phones.append(new_number)
        except ValueError:
            print(f'Old number {old_number} does not exist')


class AddressBook(UserDict):

    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record
