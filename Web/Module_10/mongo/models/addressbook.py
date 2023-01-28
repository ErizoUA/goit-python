from datetime import datetime

from mongoengine.errors import ValidationError, NotUniqueError

from .custom_exceptions import WrongNameFormat
from .models import Contact
from .print_interface import ViewAllAddressBook
from .validator import EmailValidator, NameValidator, PhoneValidator, AddressValidator, BirthdayValidator


def get_details():

    while True:
        name = input("Name: ")

        try:
            name = NameValidator().validate(name)
        except WrongNameFormat as e:
            print(e)
            continue
        else:
            break

    address = input("Address: ")
    if address:
        address = AddressValidator().validate(address)
    else:
        address = None

    phone = input("Phone: ")
    if phone:
        phone = PhoneValidator().validate(phone)
    else:
        phone = None

    email = input("Email: ")
    if email:
        email = EmailValidator().validate(email)
    else:
        email = None

    birthday = input("Birthday [format yyyy-mm-dd]: ")
    if birthday:
        birthday = BirthdayValidator().validate(birthday)
    else:
        birthday = None

    return name, address, phone, email, birthday


def add():
    """
    Adding contact to the address book with fields: name, address, phone, email, birthday
    """
    name, address, phone, email, birthday = get_details()

    try:
        contact = Contact(name=name,
                          address=address,
                          phone=phone,
                          email=email,
                          birthday=birthday).save()

        to_print = f'{contact.name=}, {contact.address=}, {contact.phone=}, {contact.email=}, {contact.birthday=}'
        print(f'Contact with {to_print} was added')

    except ValidationError:
        print('Inserted data are not valid. Try again')

    except NotUniqueError:
        print('Contact with such name already exist')


def find_by_name():
    """
    Searching contacts in address book by full- or part name and printing found records as a formatted table
    """
    name = input("Enter the searching name: ")

    contacts = Contact.objects(name__contains=name)

    if contacts:
        ViewAllAddressBook(contacts).print_table()

    else:
        print("Contacts not found")


def find_by_address():
    """
    Searching contacts in address book by full- or part address and printing found records as a formatted table
    """
    address = input("Enter the searching address: ")

    contacts = Contact.objects(address__contains=address)

    if contacts:
        ViewAllAddressBook(contacts).print_table()

    else:
        print("Contacts not found")


def find_by_email():
    """
    Searching contacts in address book by full- or part email and printing found records as a formatted table
    """
    email = input("Enter the searching email: ")

    contacts = Contact.objects(email__contains=email)

    if contacts:
        ViewAllAddressBook(contacts).print_table()

    else:
        print("Contacts not found")


def find_by_phone():
    """
    Searching contacts in address book by full- or part phone and printing found records as a formatted table
    """
    phone = input("Enter the searching phone: ")

    contacts = Contact.objects(phone__contains=phone)

    if contacts:
        ViewAllAddressBook(contacts).print_table()

    else:
        print("Contacts not found")


def update():
    """
    Updating record in address book. You can change one field or all ones immediately
    """
    name_find = input("Enter the name: ")

    contact = Contact.objects(name=name_find).first()

    if contact:
        print("Found. Enter new details and keep empty fields if no any changes")
        name, address, phone, email, birthday = get_details()

        name = name or contact.name

        if not address:
            try:
                address = contact.address
            except AttributeError:
                address = None

        if not phone:
            try:
                phone = contact.phone
            except AttributeError:
                phone = None

        if not email:
            try:
                email = contact.email
            except AttributeError:
                email = None

        if not birthday:
            try:
                birthday = contact.birthday
            except AttributeError:
                birthday = None

        contact.update(name=name,
                       address=address,
                       phone=phone,
                       email=email,
                       birthday=birthday)

        print("Contact was successfully updated")
    else:
        print("Contact not found")


def get_birthdays():
    """
    Printing contacts which have birthday in 7 days
    """
    gap_days = 7
    current_date = datetime.now()
    result = {}

    contacts = Contact.objects()

    for contact in contacts:

        if not contact.birthday:
            continue
        else:
            bday = contact.birthday

        try:
            mappedbday = bday.replace(year=current_date.year)
        except ValueError:
            # 29 February cannot be mapped to non-leap year. Choose 28-Feb instead
            mappedbday = bday.replace(year=current_date.year, day=28)

        if 0 <= (mappedbday - current_date).days < gap_days:
            try:
                result[mappedbday.strftime('%A')].append(contact.name)
            except KeyError:
                result[mappedbday.strftime('%A')] = [contact.name]
        elif current_date.weekday() == 0:
            if -2 <= (mappedbday - current_date).days < 0:
                try:
                    result[current_date.strftime('%A')].append(contact.name)
                except KeyError:
                    result[current_date.strftime('%A')] = [contact.name]

    for day, names in result.items():
        print(f"{', '.join(names)} has birthday on {day}")


def view():
    """
    Printing whole address book as a formatted table
    """
    contact = Contact.objects()

    if contact:
        ViewAllAddressBook(contact).print_table()


def remove():
    """
    Deleting record in address book by name
    """
    name = input("Enter the name to delete: ")
    contact = Contact.objects(name=name)

    if contact:
        contact.delete()
        print("Contact was deleted")
    else:
        print("Contact not found in the address book")
