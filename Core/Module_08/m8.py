from collections import defaultdict
from datetime import datetime as dt
from datetime import timedelta as td
from typing import Dict, List

from dict_birthdays import generate_users


def sort_birthdays_per_week(users: List[Dict]) -> List[Dict]:
    actual_users = []

    for person in users:
        name, date = person['name'], person['birthday']

        try:
            date = date.replace(year=dt.now().year)
        except ValueError:
            date = date.replace(year=dt.now().year, day=date.day - 1)

        if dt.now() < date <= dt.now() + td(7):
            actual_users.append({'name': name, 'birthday': date})

    return actual_users


def weekends_to_monday(users: List[Dict]) -> List[Dict]:
    actual_users = []

    for person in users:
        name, date = person['name'], person['birthday']

        if date.weekday() in (5, 6):
            date += td(7 - date.weekday())
            actual_users.append({'name': name, 'birthday': date})
        else:
            actual_users.append({'name': name, 'birthday': date})

    return actual_users


def birthdays_to_print(users: List[Dict]) -> None:
    birthdays_list_to_print = defaultdict(list)

    for person in users:
        name, date = person['name'], person['birthday']
        birthdays_list_to_print[date].append(name)

    for date, names in birthdays_list_to_print.items():
        print(f"{date.strftime('%A')}: {', '.join(names)}")


def get_birthdays_per_week(users: List[Dict]) -> None:

    actual_users_birthday = sort_birthdays_per_week(users)
    actual_users_birthday = weekends_to_monday(actual_users_birthday)
    birthdays_to_print(actual_users_birthday)


get_birthdays_per_week(generate_users())
