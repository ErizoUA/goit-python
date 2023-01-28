from datetime import datetime

from .custom_exceptions import WrongNameFormat
from .print_interface import ViewAllAddressBook
from database.models import Person, ContactPerson
from database.db import session
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

    queryset = session.query(Person.name).select_from(Person).filter(Person.name == name).first()

    if not queryset:
        person = Person(name=name, birthday=birthday)
        session.add(person)
        session.commit()

        person_id = session.query(Person.id).select_from(Person).filter(
            Person.name == name)
        contact = ContactPerson(address=address, phone=phone, email=email,
                                person_id=person_id)
        session.add(contact)
        session.commit()
        session.close()
    else:
        print("Contact already exist")


def find_by_name():
    """
    Searching contact in address book by full- or part name and printing found record as a formatted table
    """
    name = input("Enter the searching name: ")
    name = f'%{name}%'
    queryset = session.query(Person.name,
                             ContactPerson.address,
                             ContactPerson.phone,
                             ContactPerson.email,
                             Person.birthday).join(ContactPerson).filter(
        Person.name.like(name)).all()
    session.close()

    if queryset:
        ViewAllAddressBook(queryset).print_table()

    else:
        print("Contacts not found")


def find_by_address():
    """
    Searching contact in address book by full- or part address and printing found record as a formatted table
    """
    address = input("Enter the searching address: ")
    address = f'%{address}%'
    queryset = session.query(Person.name,
                             ContactPerson.address,
                             ContactPerson.phone,
                             ContactPerson.email,
                             Person.birthday).join(ContactPerson).filter(
        ContactPerson.address.like(address)).all()
    session.close()

    if queryset:
        ViewAllAddressBook(queryset).print_table()

    else:
        print("Contacts not found")


def find_by_email():
    """
    Searching contact in address book by full- or part email and printing found record as a formatted table
    """
    email = input("Enter the searching email: ")
    email = f'%{email}%'
    queryset = session.query(Person.name,
                             ContactPerson.address,
                             ContactPerson.phone,
                             ContactPerson.email,
                             Person.birthday).join(ContactPerson).filter(
        ContactPerson.email.like(email)).all()
    session.close()

    if queryset:
        ViewAllAddressBook(queryset).print_table()

    else:
        print("Contacts not found")


def find_by_phone():
    """
    Searching contact in address book by full- or part phone and printing found record as a formatted table
    """
    phone = input("Enter the searching phone: ")
    phone = f'%{phone}%'
    queryset = session.query(Person.name,
                             ContactPerson.address,
                             ContactPerson.phone,
                             ContactPerson.email,
                             Person.birthday).join(ContactPerson).filter(
        ContactPerson.phone.like(phone)).all()
    session.close()

    if queryset:
        ViewAllAddressBook(queryset).print_table()

    else:
        print("Contacts not found")


def update():
    """
    Updating record in address book. You can change one field or all ones immediately
    """
    name_find = input("Enter the name: ")
    queryset = session.query(Person.name,
                             ContactPerson.address,
                             ContactPerson.phone,
                             ContactPerson.email,
                             Person.birthday,
                             Person.id).join(ContactPerson).filter(
        Person.name == name_find).first()

    name, address, phone, email, birthday, person_id = queryset
    if name_find == name:
        print("Found. Enter new details and keep empty fields if no any changes")
        name_, address_, phone_, email_, birthday_ = get_details()

        name = name_ or name
        address = address_ or address
        phone = phone_ or phone
        email = email_ or email
        birthday = birthday_ or birthday

        session.query(Person).filter(Person.name == name_find).update(
            {'name': name,
             'birthday': birthday})
        session.query(ContactPerson).filter(ContactPerson.person_id == person_id).update(
            {'address': address,
             'phone': phone,
             'email': email}
        )
        session.commit()
        session.close()
        print("Address book successfully updated")
    else:
        print("Contact not found")


def get_birthdays():
    """
    Printing contacts which have birthday in 7 days
    """

    gap_days = 7
    current_date = datetime.now().date()
    result = {}

    queryset = session.query(Person.name,
                             Person.birthday).join(ContactPerson).all()
    session.close()

    for name, birthday in queryset:
        if birthday is None:
            continue

        try:
            mappedbday = birthday.replace(year=current_date.year)
        except ValueError:
            # 29 February cannot be mapped to non-leap year. Choose 28-Feb instead
            mappedbday = birthday.replace(year=current_date.year, day=28)

        if 0 <= (mappedbday - current_date).days < gap_days:
            try:
                result[mappedbday.strftime('%A')].append(name)
            except KeyError:
                result[mappedbday.strftime('%A')] = [name]
        elif current_date.weekday() == 0:
            if -2 <= (mappedbday - current_date).days < 0:
                try:
                    result[current_date.strftime('%A')].append(name)
                except KeyError:
                    result[current_date.strftime('%A')] = [name]

    if not result:
        print('There are no birthdays in 7 days')
    else:
        for day, names in result.items():
            print(f"{', '.join(names)} has birthday on {day}")


def view():
    """
    Printing whole address book as a formatted table
    """
    queryset = session.query(Person.name,
                             ContactPerson.address,
                             ContactPerson.phone,
                             ContactPerson.email,
                             Person.birthday).join(ContactPerson).all()
    session.close()

    if queryset:
        ViewAllAddressBook(queryset).print_table()
    else:
        print("No match contacts in database")


def remove():
    """
    Deleting record in addressbook by name
    """
    name_input = input("Enter the name to delete: ")

    name, person_id = session.query(Person.name, Person.id).filter(
        Person.name == name_input).first()

    queryset = session.query(Person).filter(Person.name == name)
    queryset_contact = session.query(ContactPerson).filter(ContactPerson.person_id == person_id)

    if name_input == name:
        queryset.delete()
        queryset_contact.delete()
        session.commit()
        session.close()
        print("Contact was deleted")
    else:
        print("Contact not found in the addressbook")
