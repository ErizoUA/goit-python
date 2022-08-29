from contact_book import *
from gen_users import generate_users


if __name__ == '__main__':
    address_book = AddressBook()

    name = Name('Valerii')
    tel = Phone('+38(050)111-11-11')
    birthday = Birthday('20.08.2022')
    record = Record(name, tel, birthday)
    address_book.add_record(record)
    print(repr(address_book), end='\n\n')

    print(record.days_to_birthday())

    for contact in generate_users():
        name = Name(contact.get('name'))
        phone = Phone(contact.get('phone'))
        birthday = Birthday(contact.get('birthday'))
        record = Record(name, phone, birthday)
        address_book.add_record(record)

    print(list(address_book.iterator(3)))
