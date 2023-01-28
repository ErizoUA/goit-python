import models.addressbook


def helper():
    """
    I'm a personal assistant. I'm able to keep an address book & a diary, to sort files.
    You can use next functions:
    """
    functions = {'add_contact': models.addressbook.add,
                 'view_contacts': models.addressbook.view,
                 'find_contacts_by_name': models.addressbook.find_by_name,
                 'find_contacts_by_address': models.addressbook.find_by_address,
                 'find_contacts_by_email': models.addressbook.find_by_email,
                 'find_contacts_by_phone': models.addressbook.find_by_phone,
                 'update_contact': models.addressbook.update,
                 'delete_contact': models.addressbook.remove,
                 'birthdays': models.addressbook.get_birthdays,
                 }

    for name, function in functions.items():
        print(name)
        print(f'\t{function.__doc__}')
