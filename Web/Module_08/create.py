import mariadb
import sys


def create_db(conn):
    cur = conn.cursor()

    try:
        cur.execute("DROP DATABASE IF EXISTS DZ8")
        cur.execute("CREATE DATABASE DZ8")
    except mariadb.Error as e:
        print(f"Error creating database: {e}")
        conn.rollback()
        conn.close()
        sys.exit(1)

    conn.commit()


def use_db(conn):
    cur = conn.cursor()

    try:
        cur.execute("USE DZ8")
    except mariadb.Error as e:
        print(f"Error using database: {e}")
        conn.close()
        sys.exit(1)


def create_tables(conn, table):
    cur = conn.cursor()

    try:
        cur.execute(table)
    except mariadb.Error as e:
        print(f"Error creating table {table}: {e}")
        conn.rollback()
        conn.close()
        sys.exit(1)

    conn.commit()
