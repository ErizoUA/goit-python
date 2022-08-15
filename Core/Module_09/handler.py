from contacts import user_contacts


def handler_hello():
    return "How can I help you?"


def handler_add(name: str, number: str):

    if number == user_contacts.get(name):
        return 'Contact already exists'

    if name in user_contacts.keys():
        return 'Such name already exists'

    if number in user_contacts.values():
        return 'Such number already exists'

    user_contacts[name] = number
    return 'Contact was added'


def handler_change(name: str, number: str):
    if number == user_contacts.get(name):
        return 'Contact already exists'

    if name not in user_contacts.keys() and number not in user_contacts.values():
        user_contacts[name] = number
        return 'It is a new contact. Contact was added'

    if number in user_contacts.values():
        return 'Such number already exists'

    user_contacts[name] = number
    return 'Contact was changed'


def handler_phone(name: str):
    return user_contacts.get(name, 'Such contact is absent')


def handler_show_all():
    if not len(user_contacts):
        return 'Contact book is empty'

    contacts_to_print = ''
    for name, number in user_contacts.items():
        contacts_to_print += f'{name}: {number}\n'
    return contacts_to_print


def handler_exit():
    raise SystemExit('Good bye!')
