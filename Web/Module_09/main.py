from tools import autocompletion as ui

from help import helper
import models.addressbook


CLI_UI = '''
CMD HELPER: 1.Add 2.View 3.Update 4.Delete 5.Find 6.Birthdays 7. Help 8.Exit
'''


def cli():

    print(CLI_UI)

    choice = ''
    while choice != 'exit':
        choice = ui.autocomplete()
        match choice:
            case 'add_contact':
                print(models.addressbook.add.__doc__)
                models.addressbook.add()
            case 'view_contacts':
                print(models.addressbook.view.__doc__)
                models.addressbook.view()
            case 'find_contacts_by_name':
                print(models.addressbook.find_by_name.__doc__)
                models.addressbook.find_by_name()
            case 'find_contacts_by_address':
                print(models.addressbook.find_by_address.__doc__)
                models.addressbook.find_by_address()
            case 'find_contacts_by_email':
                print(models.addressbook.find_by_email.__doc__)
                models.addressbook.find_by_email()
            case 'find_contacts_by_phone':
                print(models.addressbook.find_by_phone.__doc__)
                models.addressbook.find_by_phone()
            case 'update_contact':
                print(models.addressbook.update.__doc__)
                models.addressbook.update()
            case 'delete_contact':
                print(models.addressbook.remove.__doc__)
                models.addressbook.remove()
            case 'birthdays':
                print(models.addressbook.get_birthdays.__doc__)
                models.addressbook.get_birthdays()
            case 'help':
                print(helper.__doc__)
                helper()
            case 'exit':
                print("Exiting...")
            case _:
                print("Invalid choice.")


if __name__ == '__main__':
    cli()
