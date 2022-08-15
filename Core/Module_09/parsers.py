from collections import namedtuple
import re
from typing import Dict, Callable

import handler


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
        return handler.handler_hello()
    raise ValueError('Entered command is wrong')


@input_error
def parser_add(user_input: str):
    User = namedtuple('User', ('command', 'name', 'contact'))
    args = user_input.split(' ')
    args = list(filter(lambda x: len(x) > 0, args))

    if len(args) != 3:
        raise ValueError('Entered command is wrong')

    user = User(*args)
    return handler.handler_add(user.name, user.contact)


@input_error
def parser_change(user_input: str):
    User = namedtuple('User', ('command', 'name', 'contact'))
    args = user_input.split(' ')
    args = list(filter(lambda x: len(x) > 0, args))

    if len(args) != 3:
        raise ValueError('Entered command is wrong')

    user = User(*args)
    return handler.handler_change(user.name, user.contact)


@input_error
def parser_phone(user_input: str):
    User = namedtuple('User', ('command', 'name'))
    args = user_input.split(' ')
    args = list(filter(lambda x: len(x) > 0, args))

    if len(args) != 2:
        raise ValueError('Entered command is wrong')

    user = User(*args)
    return handler.handler_phone(user.name)


@input_error
def parser_show_all(user_input: str):
    if user_input == 'show all':
        return handler.handler_show_all()
    raise ValueError('Entered command is wrong')


@input_error
def parser_exit(user_input: str):
    if user_input in ('good bye', 'close', 'exit'):
        return handler.handler_exit()

    raise ValueError('Entered command is wrong')


@input_error
def parser_user_input(user_input: str):
    parsers: Dict[str, Callable] = {
        'hello': parser_hello,
        'add': parser_add,
        'change': parser_change,
        'phone': parser_phone,
        'show all': parser_show_all,
        'good bye': parser_exit,
        'close': parser_exit,
        'exit': parser_exit
    }

    for item in parsers.keys():
        if re.match(item, user_input):
            return parsers.get(item)(user_input)

    raise ValueError('Unknown command')
