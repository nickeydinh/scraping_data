from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# 1. Khởi tạo
driver = webdriver.Chrome()

# 2. Truy cập trang
url = r"https://en.wikipedia.org/wiki/List_of_painters_by_name_beginning_with_%22P%22"
driver.get(url)
time.sleep(5) 


print("Đang quét dữ liệu...")

# Lấy tất cả thẻ a nằm trong danh sách của phần nội dung chính
painter_links = driver.find_elements(By.XPATH, "//div[@id='mw-content-text']//div[contains(@class,'div-col')]//li//a")

# Nếu XPath trên không ra (do wiki đổi format), dùng cái tổng quát hơn này:
if len(painter_links) == 0:
    print("Không tìm thấy thẻ a trong div-col, thử dùng XPath tổng quát hơn...")
    painter_links = driver.find_elements(By.XPATH, "//div[@id='mw-content-text']//ul//li//a")

print(f"Tìm thấy {len(painter_links)} họa sĩ.")


for tag in painter_links[:10]:
    print( tag.get_attribute("title"))
    print( tag.get_attribute("href"))
    

driver.quit()