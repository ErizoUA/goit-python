from calendar import Calendar
from datetime import datetime
from random import randint


def generate_users():
    users = []

    for num in range(1, 500):
        year = randint(1922, 2021)
        month = randint(1, 12)
        day = randint(1, max(Calendar().itermonthdays(year, month)))
        name = f'User_{num}'
        users.append({'name': name, 'birthday': datetime(year, month, day)})

    return users
