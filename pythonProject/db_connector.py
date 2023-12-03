from datetime import datetime

import pymysql
from pymysql import IntegrityError

schema_name = 'mydb'


def insert(name, user_id):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='user', password='password', db=schema_name)
    conn.autocommit(True)
    cursor = conn.cursor()

    try:
        cursor.execute(f"INSERT into mydb.users (id, name, creation_date) VALUES ('{user_id}', '{name}', '{str(datetime.now())}')")
    except IntegrityError as e:
        cursor.execute("SELECT max(id) from users")
        nextid = cursor.fetchone()[0] + 1

        cursor.execute(f"INSERT into mydb.users (id, name, creation_date) VALUES ('{nextid}', '{name}', '{str(datetime.now())}')")
    finally:
        cursor.close()
        conn.close()
    return 0


def update(name, user_id):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='user', password='password', db=schema_name)
    conn.autocommit(True)
    cursor = conn.cursor()

    try:
        cursor.execute(f"UPDATE mydb.users SET name = '{name}' WHERE id='{user_id}'")
    except IntegrityError as e:
        return -1
    finally:
        cursor.close()
        conn.close()
    return 0


def delete(user_id):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='user', password='password', db=schema_name)
    conn.autocommit(True)
    cursor = conn.cursor()

    try:
        cursor.execute(f"DELETE FROM mydb.users WHERE id='{user_id}'")
        if cursor.rowcount == 0:
            return -1
    except IntegrityError as e:
        return -1
    finally:
        cursor.close()
        conn.close()
    return 0


def get_user_name(user_id):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='user', password='password', db=schema_name)
    conn.autocommit(True)
    cursor = conn.cursor()

    try:
        cursor.execute(f"SELECT name FROM mydb.users WHERE id='{user_id}'")
        if cursor.rowcount == 0:
            return -1
        else:
            name = cursor.fetchone()[0]
    except IntegrityError as e:
        return -1
    finally:
        cursor.close()
        conn.close()
    return name




