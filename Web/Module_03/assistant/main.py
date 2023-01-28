from models.dbs import AddressBook, Diary
from tools import autocompletion as ui
from tools import sorting

from help import helper

CLI_UI = '''
CMD HELPER: 1.Add 2.View 3.Search 4.Find 5.Sort 6.Update 7.Delete 8.Reset 9.Birthdays 10. Help 11.Exit
'''


def cli():

    addr = AddressBook('contacts.data')
    addr.db_load()
    diary = Diary('notes.data')
    diary.db_load()

    print(CLI_UI)
    choice = ''
    while choice != 'exit':
        choice = ui.autocomplete()
        match choice:
            case 'add_contact':
                print(addr.add.__doc__)
                addr.db_save(addr.add())
            case 'add_note':
                print(diary.add.__doc__)
                diary.db_save(diary.add())
            case 'view_contacts':
                print(addr.view.__doc__)
                addr.view()
            case 'view_notes':
                print(diary.view.__doc__)
                diary.view()
            case 'search_contacts':
                print(addr.search.__doc__)
                addr.search()
            case 'search_notes':
                print(diary.search.__doc__)
                diary.search()
            case 'find_contact':
                print(addr.find_by_name.__doc__)
                addr.find_by_name()
            case 'update_contact':
                print(addr.update.__doc__)
                addr.update()
            case 'update_note':
                print(diary.update.__doc__)
                diary.update()
            case 'delete_contact':
                print(addr.delete.__doc__)
                addr.delete()
            case 'delete_notes':
                print(diary.delete.__doc__)
                diary.delete()
            case 'reset_contacts':
                print(addr.reset.__doc__)
                addr.reset()
            case 'reset_notes':
                print(diary.reset.__doc__)
                diary.reset()
            case 'sort_files':
                print(sorting.perform.__doc__)
                sorting.perform()
            case 'birthdays':
                print(addr.get_birthdays.__doc__)
                addr.get_birthdays()
            case 'help':
                print(helper.__doc__)
                helper()
            case 'exit':
                print("Exiting...")
            case _:
                print("Invalid choice.")


if __name__ == '__main__':
    cli()
