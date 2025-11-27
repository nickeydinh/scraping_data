from selenium import webdriver
from selenium.webdriver.common.by import By
import time

#tao driver de bat dau dieu khien
driver = webdriver.Chrome()

#mo mot trang web
driver.get("https://gomotungkinh.com/")
time.sleep(10)  #cho trang web load

try:
    while True:
        driver.find_element(By.ID, "bonk").click()
        time.sleep(2)  #cho trang web load
except:
    driver.quit()