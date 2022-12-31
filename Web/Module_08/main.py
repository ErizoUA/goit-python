from dz import dz, welcome
import sys
import mariadb
from create import create_db, create_tables, use_db
from tables import teachers, subjects, groups, students, grades
from insert_data import insert_datas
from queries import q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12


def create_database(conn):
    create_db(conn)
    use_db(conn)

    tables_db = [teachers, subjects, groups, students, grades]
    for table in tables_db:
        create_tables(conn, table)

    insert_datas(conn)


def do_query(query, cur):

    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()


def main(conn):
    print(dz)
    print(welcome)

    with conn:

        while True:

            cur = conn.cursor()
            query = 'q' + input('Number: ')
            match query:
                case 'q1':
                    do_query(q1, cur)
                case 'q2':
                    do_query(q2, cur)
                case 'q3':
                    do_query(q3, cur)
                case 'q4':
                    do_query(q4, cur)
                case 'q5':
                    do_query(q5, cur)
                case 'q6':
                    do_query(q6, cur)
                case 'q7':
                    do_query(q7, cur)
                case 'q8':
                    do_query(q8, cur)
                case 'q9':
                    do_query(q9, cur)
                case 'q10':
                    do_query(q10, cur)
                case 'q11':
                    do_query(q11, cur)
                case 'q12':
                    do_query(q12, cur)
                case _:
                    break


if __name__ == "__main__":
    try:
        connection = mariadb.connect(
            host="localhost",
            port=3306,
            user="root",
            password="03111983")
    except mariadb.Error as e:
        print(f"Error connecting to the database: {e}")
        sys.exit(1)

    create_database(connection)
    main(connection)
