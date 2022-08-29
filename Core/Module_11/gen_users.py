from calendar import Calendar
from random import randint
from string import ascii_uppercase


def generate_users():
    users = []

    for num in range(1, 11):
        year = randint(1922, 2021)
        month = randint(1, 12)
        day = randint(1, max(Calendar().itermonthdays(year, month)))
        first_letter = list(ascii_uppercase)[randint(0, 25)]
        name = f'{first_letter}_user_{num}'
        tel_code = f'+380({str(randint(1, 9))}{str(randint(1, 9))})'
        tel_number = f'{str(randint(0, 9)) * 3}-{str(randint(0, 9)) * 2}-{str(randint(0, 9)) * 2}'
        tel = tel_code + tel_number
        users.append({'name': name, 'birthday': f'{day}.{month}.{year}', 'phone': tel})

    return users
