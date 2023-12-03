import unittest
import pymysql
import requests
from pymysql import IntegrityError


class BackendTestCase(unittest.TestCase):

    def test_backend(self):

        requests.post('http://127.0.0.1:5000/users/1', json={"user_name":"john"})

        res = requests.get('http://127.0.0.1:5000/users/1')
        self.assertEqual(res.status_code,200)
        self.assertEqual(res.json()['user_name'], 'john')

        conn = pymysql.connect(host='127.0.0.1', port=3306, user='user', password='password', db='mydb')
        conn.autocommit(True)
        cursor = conn.cursor()

        try:
            cursor.execute(f"SELECT name FROM mydb.users WHERE id='1'")
            self.assertEqual(cursor.fetchone()[0], 'john')
        except IntegrityError as e:
            print('no such user_id')
        finally:
            cursor.close()
            conn.close()


if __name__ == '__main__':
    unittest.main()