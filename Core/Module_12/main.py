from contact_book import *
from gen_users import generate_users
from pprint import pprint
from pickle import dump, load

if __name__ == '__main__':
    address_book = AddressBook()

    for contact in generate_users():
        name = Name(contact.get('name'))
        phone = Phone(contact.get('phone'))
        birthday = Birthday(contact.get('birthday'))
        record = Record(name, phone, birthday)
        address_book.add_record(record)

    print('standard address book')
    pprint(address_book)

    with open('db.bin', 'wb') as file:
        dump(address_book, file)

    with open('db.bin', 'rb') as file:
        address_book = load(file)

    print('\naddressbook after deserialize')
    pprint(address_book)

    name = Name('Valerii')
    tel = Phone('+38(050)111-11-11')
    birthday = Birthday('20.08.2022')
    record = Record(name, tel, birthday)
    address_book.add_record(record)

    with open('db.bin', 'wb') as file:
        dump(address_book, file)

    with open('db.bin', 'rb') as file:
        address_book = load(file)

    print('\nnew addressbook after deserialize')
    pprint(address_book)

    print('\nfind name')
    address_book.find_name('v')

    print('\nfind phone')
    address_book.find_phone(99)
