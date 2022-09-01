from collections import namedtuple
from pickle import dump, load
from pprint import pprint
from typing import Dict, Callable, Union

from contact_book import *


def handler_hello():
    return "How can I help you?"


def handler_create(name_user: str, phone_user: Union[str, None], birthday_user: Union[str, None]):

    name = Name(name_user)

    if birthday_user is None:
        phone = Phone(phone_user)
        record = Record(name, phone)
    else:
        phone = Phone(phone_user)
        birthday = Birthday(birthday_user)
        record = Record(name, phone, birthday)

    address_book.add_record(record)
    return 'Contact was added'


def handler_add(name_user: str, new_number: str):

    for name, contact in address_book.items():
        if name == name_user:
            new_number = Phone(new_number)
            contact.add_phone(new_number)

    return 'Phone was added'


def handler_change(old_number: str, new_number: str):

    for contact in address_book.values():
        for numbers in contact.phones:
            if old_number in numbers:
                new_number = Phone(new_number)
                contact.change_phone(old_number, new_number)

    return 'Phone was changed'


def handler_del(phone: str):
    for contact in address_book.values():
        for numbers in contact.phones:
            if phone in numbers:
                contact.del_phone(phone)

    return 'Phone was deleted'


def handler_birthday(name_user: str):
    for name, contact in address_book.items():
        if name == name_user:
            return contact.days_to_birthday()


def handler_find(user_input: Union[str, int]):

    if user_input.isdigit():
        return address_book.find_phone(user_input)

    return address_book.find_name(user_input)


def handler_show_all():
    if not len(address_book):
        return 'Contact book is empty'

    return address_book


def handler_iterator(num: str):

    if num is None:
        return address_book.iterator()

    if num.isdigit():
        return address_book.iterator(int(num))

    return 'Wrong command'


def handler_exit():

    with open('db.bin', 'wb') as file_db:
        dump(address_book, file_db)
        print('phonebook has been saved successfully')

    raise SystemExit('Good bye!')


def input_error(func):
    def wrapper(user_input):
        try:
            return func(user_input)
        except ValueError as error:
            return str(error)

    return wrapper


@input_error
def parser_hello(user_input: str):
    if user_input == 'hello':
        return handler_hello()
    raise ValueError('Entered command is wrong')


@input_error
def parser_create(user_input: str):
    User = namedtuple('User', ('command', 'name', 'phones', 'birthday'))
    args = user_input.split(' ')
    args = list(filter(lambda x: len(x) > 0, args))

    if len(args) < 2:
        raise ValueError('Entered command is wrong')

    while len(args) < 4:
        args.append(None)

    user = User(*args)
    return handler_create(user.name, user.phones, user.birthday)


@input_error
def parser_add(user_input: str):
    User = namedtuple('User', ('command', 'name', 'number'))
    args = user_input.split(' ')
    args = list(filter(lambda x: len(x) > 0, args))

    if len(args) != 3:
        raise ValueError('Entered command is wrong')

    user = User(*args)
    return handler_add(user.name, user.number)


@input_error
def parser_change(user_input: str):
    User = namedtuple('User', ('command', 'old_number', 'new_number'))
    args = user_input.split(' ')
    args = list(filter(lambda x: len(x) > 0, args))

    if len(args) != 3:
        raise ValueError('Entered command is wrong')

    user = User(*args)
    return handler_change(user.old_number, user.new_number)


@input_error
def parser_del(user_input: str):
    User = namedtuple('User', ('command', 'phone'))
    args = user_input.split(' ')
    args = list(filter(lambda x: len(x) > 0, args))

    if len(args) != 2:
        raise ValueError('Entered command is wrong')

    user = User(*args)
    return handler_del(user.phone)


@input_error
def parser_birthday(user_input: str):
    User = namedtuple('User', ('command', 'name'))
    args = user_input.split(' ')
    args = list(filter(lambda x: len(x) > 0, args))

    if len(args) != 2:
        raise ValueError('Entered command is wrong')

    user = User(*args)
    return handler_birthday(user.name)


@input_error
def parser_find(user_input: str):
    User = namedtuple('User', ('command', 'symbols'))
    args = user_input.split(' ')
    args = list(filter(lambda x: len(x) > 0, args))

    if len(args) != 2:
        raise ValueError('Entered command is wrong')

    user = User(*args)

    return handler_find(user.symbols)


@input_error
def parser_show_all(user_input: str):
    if user_input == 'show all':
        return handler_show_all()

    raise ValueError('Entered command is wrong')


@input_error
def parser_iterator(user_input: str):
    User = namedtuple('User', ('command', 'number'))
    args = user_input.split(' ')
    args = list(filter(lambda x: len(x) > 0, args))

    if len(args) > 2:
        raise ValueError('Entered command is wrong')

    while len(args) < 2:
        args.append(None)

    user = User(*args)

    return handler_iterator(user.number)


@input_error
def parser_exit(user_input: str):
    if user_input in ('good bye', 'close', 'exit'):
        return handler_exit()

    raise ValueError('Entered command is wrong')


@input_error
def parser_user_input(user_input: str):
    parsers: Dict[str, Callable] = {
        'hello': parser_hello,
        'create': parser_create,
        'add': parser_add,
        'change': parser_change,
        'del': parser_del,
        'show all': parser_show_all,
        'good bye': parser_exit,
        'close': parser_exit,
        'exit': parser_exit,
        'birthday': parser_birthday,
        'find': parser_find,
        'iterator': parser_iterator
    }

    for item in parsers.keys():
        if re.match(item, user_input):
            return parsers.get(item)(user_input)

    raise ValueError('Unknown command')


def main():

    while True:
        user_input = input('\nEnter Command: ').lower().strip()
        try:
            result = parser_user_input(user_input)
            pprint(result)
        except (WrongPhoneNumber, WrongBirthdayFormat) as error:
            print(error)
            continue
        except SystemExit as error:
            print(error)
            break


if __name__ == '__main__':
    address_book = AddressBook()

    try:
        with open('db.bin', 'rb') as file:
            address_book = load(file)
    except FileNotFoundError:
        pass

    main()
