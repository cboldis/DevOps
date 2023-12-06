import json
import unittest
import pymysql
import requests
from flask import jsonify
from pymysql import IntegrityError
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By


class CombinedTestCase(unittest.TestCase):
    """
        combined testing: make sure that the insert/update of user is done correctly in the DB and that a new ID is being generated
    """
    def test_backend(self):

        try:

            conn = pymysql.connect(host='127.0.0.1', port=3306, user='user', password='password', db='mydb')
            conn.autocommit(True)
            cursor = conn.cursor()

            cursor.execute("SELECT * from test_config")
            row = cursor.fetchone()
            url = row[0]
            username = row[2]
            print(username)

            cursor.execute("SELECT max(id) from users")
            nextid = cursor.fetchone()[0] + 1

            requests.post('http://127.0.0.1:5000/users/'+str(nextid), json={"user_name": username})

            res = requests.get('http://127.0.0.1:5000/users/'+str(nextid))
            self.assertEqual(res.status_code,200)
            self.assertEqual(res.json()['user_name'], username)



            try:
                cursor.execute(f"SELECT name FROM mydb.users WHERE id='{nextid}'")
                self.assertEqual(cursor.fetchone()[0], username)
            except IntegrityError as e:
                print('no such user_id')
            finally:
                cursor.close()
                conn.close()

            driver = webdriver.Chrome()
            driver.get(url+str(nextid))
            try:
                self.assertEqual(driver.find_element(By.ID, value="user").text, username)
            except NoSuchElementException:
                print('user doesnt exist')

            driver.close()
            driver.quit()

        except AssertionError:
            raise Exception('test failed')

if __name__ == '__main__':
    unittest.main()
