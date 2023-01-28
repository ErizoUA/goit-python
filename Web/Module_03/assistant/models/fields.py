from abc import ABC
from typing import List

from .validator import EmailValidator, NameValidator, PhoneValidator, AddressValidator, BirthdayValidator
from .validator import NoteValidator, TagValidator


class IField(ABC):
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return self.value


class Name(IField):

    def __init__(self, name: str):
        super().__init__(name)
        self.value = NameValidator().validate(name)


class Phone(IField):

    def __init__(self, phone: str):
        super().__init__(phone)
        self.value = PhoneValidator().validate(phone)


class Email(IField):

    def __init__(self, email: str):
        super().__init__(email)
        self.value = EmailValidator().validate(email)


class Address(IField):

    def __init__(self, address: str):
        super().__init__(address)
        self.value = AddressValidator().validate(address)


class Birthday(IField):

    def __init__(self, birthday: str):
        super().__init__(birthday)
        self.value = BirthdayValidator().validate(birthday)


class NoteText(IField):

    def __init__(self, text: str):
        super().__init__(text)
        self.value = NoteValidator().validate(text)


class Tag:

    def __init__(self, tag: List[str]):
        self.value = TagValidator().validate(tag)

    def __str__(self):
        return self.value
