from addressbook import AddressBook
from tools import autocompletion as ui
from tools import sorting


def cli():
    """
    Comparing inputted command with existing ones
    and performing correspondent command
    :return: None
    """
    app = AddressBook('contacts.data')
    choice = ''
    while choice != 'exit':
        print(app)
        choice = ui.autocomplete()
        match choice:
            case 'add':
                print(app.add.__doc__)
                app.add()
            case 'add_notes':
                print(app.add_note.__doc__)
                app.add_note()
            case 'view_all':
                print(app.view_all.__doc__)
                app.view_all()
            case 'view_all_notes':
                print(app.view_all_notes.__doc__)
                app.view_all_notes()
            case 'search':
                print(app.search.__doc__)
                app.search()
            case 'search_notes':
                print(app.search_notes.__doc__)
                app.search_notes()
            case 'find':
                print(app.find.__doc__)
                app.find()
            case 'update':
                print(app.update.__doc__)
                app.update()
            case 'update_notes':
                print(app.update_notes.__doc__)
                app.update_notes()
            case 'delete':
                print(app.delete.__doc__)
                app.delete()
            case 'delete_notes':
                print(app.delete_notes.__doc__)
                app.delete_notes()
            case 'reset':
                print(app.reset.__doc__)
                app.reset()
            case 'reset_notes':
                print(app.reset_notes.__doc__)
                app.reset_notes()
            case 'file_sort':
                print(sorting.perform.__doc__)
                sorting.perform()
            case 'sort_birthday':
                print(app.get_birthdays.__doc__)
                app.get_birthdays()
            case 'help':
                print(app.help.__doc__)
                app.help()
            case 'exit':
                print("Exiting...")
            case _:
                print("Invalid choice.")


if __name__ == '__main__':
    cli()
