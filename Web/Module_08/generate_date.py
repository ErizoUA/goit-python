import datetime
from faker import Faker


fake = Faker()


def gen_dates(start, finish):
    dates_list = []

    while len(dates_list) < 3000:
        fake_date = fake.date()
        date = datetime.datetime.strptime(fake_date, "%Y-%m-%d").date()
        if start.date() < date < finish.date():
            dates_list.append(date)
        else:
            continue

    return dates_list
