import datetime
from random import randint, choices
import string
import sys

from faker import Faker
import mariadb

from generate_date import gen_dates


def insert_datas(conn):

    subjects = ['Modern History', 'Economics', 'Probability theory',
                'Literature of Middle Ages', 'Philosophy']

    groups = [f'{"".join(choices(string.ascii_uppercase, k=2))}-{randint(1,9)}' for _ in range(3)]

    fake = Faker()
    cur = conn.cursor()

    number_of_teachers = 3
    number_of_students = 30

    def insert_teachers():
        teachers = []

        for _ in range(number_of_teachers):
            teachers.append(fake.name())

        sql_teachers = 'INSERT teachers(name) VALUES (?)'
        cur.executemany(sql_teachers, list(zip(teachers, )))

    def insert_subjects():
        sql_subj = 'INSERT subjects(name, teacher_id) VALUES (?, ?)'
        cur.executemany(sql_subj, list(zip(
            subjects, iter(randint(1, number_of_teachers) for _ in range(len(subjects))))))

    def insert_groups():
        sql_groups = 'INSERT groups(name) VALUES (?)'
        cur.executemany(sql_groups, list(zip(groups, )))

    def insert_students():
        students = []

        for _ in range(number_of_students):
            students.append(fake.name())

        sql_students = 'INSERT students(name, group_id) VALUES (?,?)'
        cur.executemany(sql_students, list(zip(students, iter(randint(1, len(groups)) for _ in range(len(students))))))

    def insert_grades():
        finish = datetime.datetime.now()
        start = finish - datetime.timedelta(days=6 * 30)
        dates = gen_dates(start, finish)

        grades = []

        for date in dates:

            id_subj = randint(1, len(subjects))
            id_st = randint(1, number_of_students)
            grade = (id_st, id_subj, date, randint(1, 5))
            grades.append(grade)

        sql_ratings = 'INSERT grades(student_id, subject_id, date_of, grade) VALUES (?, ?, ?, ?)'
        cur.executemany(sql_ratings, grades)

    try:
        insert_teachers()
        insert_subjects()
        insert_groups()
        insert_students()
        insert_grades()

    except mariadb.Error as e:
        print(f"Error inserting datas: {e}")
        conn.rollback()
        conn.close()
        sys.exit(1)

    conn.commit()
