from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
import time
import pandas as pd
import getpass

driver = webdriver.Chrome()



url = 'https://www.reddit.com/r/boysitinh/submit/'
driver.get(url)
time.sleep(10)
# Nhap thong tin nguoi dung
# my_email = input('Please provide your email:')
# my_password = getpass.getpass('Please provide your password:')
my_email = 'FriendlyCharity9130'
my_password = 'dinhquockhanh8888'

actionChains = ActionChains(driver)
time.sleep(20)


for i in range(6):
    actionChains.key_down(Keys.TAB).perform()
    
actionChains.send_keys(my_email).perform()
actionChains.key_down(Keys.TAB).perform()

actionChains.send_keys(my_password + Keys.ENTER).perform()

time.sleep(5)
wait = WebDriverWait(driver, 10)
# 1. Bắt đầu bằng cách lấy focus cho phần tử đầu tiên trên trang (ví dụ: body)
# driver.find_element(By.TAG_NAME, 'body').click()

for i in range(18):
    actionChains.key_down(Keys.TAB).perform()
    time.sleep(0.5)
# 3. Gửi chuỗi phím này
actionChains.send_keys("title ne").perform()
time.sleep(2)

# 4. Gửi 1 lần Tab nữa để di chuyển đến trường Body (giả sử là lần nhấn thứ 18)
for i in range(2):
    actionChains.key_down(Keys.TAB).perform()
time.sleep(2)
actionChains.send_keys("body ne").perform()
time.sleep(5)
btn = driver.find_element(By.ID, 'submit-post-button')
btn.click()
time.sleep(7)
driver.quit()