import pydoc
from datetime import datetime

import pymysql
from pymysql import IntegrityError
from pypika import Table, Query, Database

schema_name = 'mydb'


def insert(name, user_id):
    """
        method for adding a new user. if user id already exists, it updates the user name of the existing user
        Params:
          user id, user name
        Returns:
          0 for success
    """
    conn = get_db_connection()
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
    """
        method for updating the user name. if user id doesn't exist, it returns -1
        Params:
          user id, new user name
        Returns:
          0 for success
    """

    conn = get_db_connection()
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
    """
        method for deleting the user. if user id doesn't exist, it returns -1
        Params:
          user id
        Returns:
          0 for success
    """
    conn = get_db_connection()
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
        method for getting the user name. if user id doesn't exist, it returns -1
        Params:
          user id
        Returns:
          user name
    """
    conn = get_db_connection()
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

def get_db_connection():
    """
        method for getting the db connection
    :return:
        connection object
    """
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='user', password='password', db=schema_name)
    conn.autocommit(True)
    return conn


