from contact_book import *


if __name__ == '__main__':
    address_book = AddressBook()

    name = Name('Valerii')
    tel = Phone('+38(050)111-11-11')
    record = Record(name, tel)
    address_book.add_record(record)
    print(repr(address_book), end='\n\n')

    record.add_phone('+38(099)222-22-22')
    print(repr(address_book), end='\n\n')

    record.del_phone('+38(099)222-22-22')
    print(repr(address_book), end='\n\n')

    record.change_phone('+38(050)111-11-11', '+38(063)333-33-33')
    print(repr(address_book), end='\n\n')
