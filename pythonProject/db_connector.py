import pydoc
from datetime import datetime

import pymysql
from pymysql import IntegrityError
from pypika import Table, Query, Database

schema_name = 'mydb'


def insert(name, user_id):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='user', password='password', db=schema_name)
    conn.autocommit(True)
    cursor = conn.cursor()


    try:
        prepstmt = "INSERT INTO users (id, name, creation_date) VALUES (%s, %s, %s)"
        cursor.execute(prepstmt, (user_id, name, str(datetime.now())))
    except IntegrityError as e:
        cursor.execute("SELECT max(id) from users")
        nextid = cursor.fetchone()[0] + 1

        prepstmt = "INSERT INTO users (id, name, creation_date) VALUES (%s, %s, %s)"
        cursor.execute(prepstmt, (nextid, name, str(datetime.now())))
    finally:
        cursor.close()
        conn.close()
    return 0


def update(name, user_id):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='user', password='password', db=schema_name)
    conn.autocommit(True)
    cursor = conn.cursor()

    try:
        users = Table('users')

        q = Query.update(users).set(users.name, name).where(users.id == int(user_id))

        query = q.get_sql(quote_char=None)
        cursor.execute(query)

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
        users = Table('users')

        q = Query.from_(users).delete().where(users.id == int(user_id))

        query = q.get_sql(quote_char=None)
        cursor.execute(query)

        if cursor.rowcount == 0:
            return -1
    except IntegrityError as e:
        return -1
    finally:
        cursor.close()
        conn.close()
    return 0


def get_user_name(user_id):
    """
        Params:
          x and b are numbers (int or float)
        Returns:
          the sum of x and y.
    """
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='user', password='password', db=schema_name)
    conn.autocommit(True)
    cursor = conn.cursor()

    try:
        users = Table('users')

        q = Query.from_(users).select(users.name).where(users.id == int(user_id))

        query = q.get_sql(quote_char=None)
        cursor.execute(query)

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



