from selenium import webdriver
from selenium.webdriver.common.by import By 
import time
import pandas as pd 
import re

# Khởi tạo WebDriver
driver = webdriver.Chrome()

# SỬA 1: Link đúng chính tả
url = "https://en.wikipedia.org/wiki/Dirck_van_Baburen"
driver.get(url)
time.sleep(2)

# Lấy tên họa sĩ
try:
    name = driver.find_element(By.TAG_NAME, "h1").text
except:
    name = ""

# Lấy ngày sinh
try: 
    birth_element = driver.find_element(By.XPATH, "//th[text()='Born']/following-sibling::td")
    birth_text = birth_element.text
    # SỬA 2: Regex chuẩn hơn
    birth = re.findall(r'[0-9]{1,2}\s+[A-Za-z]+\s+[0-9]{4}', birth_text)[0]
except:
    birth = ""

# Lấy ngày mất
try: 
    death_element = driver.find_element(By.XPATH, "//th[text()='Died']/following-sibling::td")
    death_text = death_element.text
    # SỬA 2: Regex chuẩn hơn
    death = re.findall(r'[0-9]{1,2}\s+[A-Za-z]+\s+[0-9]{4}', death_text)[0]
except:
    death = ""

# Lấy quốc tịch
try:
    # Lưu ý: Một số trang dùng 'Citizenship' thay vì 'Nationality', nên kiểm tra kỹ nếu vẫn rỗng
    nationality_element = driver.find_element(By.XPATH, "//th[text()='Citizenship']/following-sibling::td")
    nationality = nationality_element.text
except:
    nationality = ""

# Tạo dictionary
painter = {
    'name': name,
    'birth': birth,  
    'death': death,
    'nationality': nationality
}

# Tạo DataFrame
painters_df = pd.DataFrame([painter])

# In kết quả
print(painters_df)

# Đóng trình duyệt
driver.quit()