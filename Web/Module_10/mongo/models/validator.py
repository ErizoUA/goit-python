from abc import ABC, abstractmethod
from datetime import date

from email_validator import validate_email, EmailNotValidError
from phonenumbers import parse, format_number, PhoneNumberFormat, NumberParseException

from .custom_exceptions import WrongNameFormat


class IValidator(ABC):

    @abstractmethod
    def validate(self, value):
        ...


class NameValidator(IValidator):

    def validate(self, name):
        if len(name) < 1:
            raise WrongNameFormat(name)
        else:
            return name


class PhoneValidator(IValidator):

    def validate(self, phone):

        while True:
            try:
                phone = parse(phone)
                phone = format_number(phone, PhoneNumberFormat.INTERNATIONAL)

            except NumberParseException as e:
                print(str(e))
                phone = input("Enter as +380XX XXX-XX-XX. Phone: ")
                continue
            else:
                break

        return phone


class EmailValidator(IValidator):

    def validate(self, email):
        try:
            v = validate_email(email)
            email = v["email"]

            return email

        except EmailNotValidError as e:
            print(str(e))


class AddressValidator(IValidator):

    def validate(self, address):
        return address


class BirthdayValidator(IValidator):

    def validate(self, birthday):

        while True:
            try:
                birthday = date.fromisoformat(birthday)
            except ValueError:
                birthday = input('Wrong birthday format. Enter as yyyy-mm-dd: ')
                continue
            else:
                break

        return birthday.strftime('%Y-%m-%d')
