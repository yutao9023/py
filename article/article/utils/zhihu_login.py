import requests
import time
import json
from selenium import webdriver
cookie = {}
session = requests.session()

driver = webdriver.Chrome()
driver.get('https://www.shanbay.com/web/account/login')

driver.find_element_by_xpath('//*[@name="username"]').send_keys('yutao1')
driver.find_element_by_xpath('//*[@name="password"]').send_keys('161016')
time.sleep(7)
driver.find_element_by_xpath('//*[@type="submit"]').click()

cookies = driver.get_cookies()
print(cookies)
# for item in cookies:
#     cookie[item.get('name')] = item.get('value')
#
# with open('cookie.txt','w',encoding='utf-8') as f:
#     f.write(json.dumps(cookie))
# print(cookie)