from builtins import range
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Khởi tạo WebDriver
driver = webdriver.Chrome()

for i in range(65, 91):
    url = "https://en.wikipedia.org/wiki/List_of_painters_by_name_beginning_with_%22" + chr(i) + "%22"
    try:
        # Mở trang
        driver.get(url)

        # Đợi một chút để trang tải
        time.sleep(3)

        # Lấy ra tất cả các thẻ ul
        painter_links = driver.find_elements(By.XPATH, "//div[@id='mw-content-text']//div[contains(@class,'div-col')]//li//a")
        titles = [tag.get_attribute("title") for tag in painter_links]
        # In ra title
        for title in titles[:5]:
            print(title)
    except:
        print("Error!")

# Đóng WebDriver
driver.quit()
