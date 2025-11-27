from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

url = "https://en.wikipedia.org/wiki/List_of_painters_by_name_beginning_with_%22P%22"
driver.get(url)

time.sleep(5)  # cho trang web load
ul_tags = driver.find_elements(By.TAG_NAME, "ul")
print(f"Số lượng thẻ ul tìm thấy: {len(ul_tags)}")
ul_painter = ul_tags[20]
li_tags = ul_painter.find_elements(By.TAG_NAME, "li")

#tao danh sach links
links = [tag.find_element(By.TAG_NAME, "a").get_attribute('href') for tag in li_tags]
print(f"Số lượng link tìm thấy: {len(links)}")
#tao danh sach titles
titels = [tag.find_element(By.TAG_NAME, "a").get_attribute('title') for tag in li_tags]

#in ra url va title
for title, link in zip(titels, links):
    print(f"Title: {title}, Link: {link}")
driver.quit()