from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from pygments.formatters.html import webify

driver = webdriver.Chrome()

url = 'https://en.wikipedia.org/wiki/List_of_painters_by_name'
driver.get(url)
# Mở full màn hình 
driver.maximize_window()
time.sleep(20)  # cho trang web load


tags = driver.find_elements(By.XPATH,"//a[contains(@title, 'List of painters')]")
links = [tag.get_attribute('href') for tag in tags]

#xuat thong tin
for link in links:
    print(link)

driver.quit()
