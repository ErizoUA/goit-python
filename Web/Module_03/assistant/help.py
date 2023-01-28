from models.dbs import Diary, AddressBook
from tools import sorting


def helper():
    """
    I'm a personal assistant. I'm able to keep an address book & a diary, to sort files.
    You can use next functions:
    """
    functions = {'add_contact': AddressBook.add,
                 'add_note': Diary.add,
                 'view_contacts': AddressBook.view,
                 'view_notes': Diary.view,
                 'search_contacts': AddressBook.search,
                 'search_notes': Diary.search,
                 'find_contact': AddressBook.find_by_name,
                 'update_contact': AddressBook.update,
                 'update_notes': Diary.update,
                 'delete_contact': AddressBook.delete,
                 'delete_note': Diary.delete,
                 'reset_contacts': AddressBook.reset,
                 'reset_notes': Diary.reset,
                 'birthdays': AddressBook.get_birthdays,
                 'sort_files': sorting.perform
                 }
    for name, function in functions.items():
        print(name)
        print(f'\t{function.__doc__}')
