import pymysql
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

conn = pymysql.connect(host='127.0.0.1', port=3306, user='user', password='password', db='mydb')
conn.autocommit(True)
cursor = conn.cursor()

cursor.execute("SELECT * from test_config")
row = cursor.fetchone()
url=row[0]
username = row[2]

driver = webdriver.Chrome()

driver.get(url+"/1")
try:
    print(driver.find_element(By.ID, value="user").text)
except NoSuchElementException:
    print('user doesnt exist')


driver.close()
driver.quit()

cursor.close()
conn.close()

