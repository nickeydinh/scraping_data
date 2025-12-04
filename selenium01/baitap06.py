from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd
import re
import string

# 1. CẤU HÌNH CHẾ ĐỘ HEADLESS ⚙️
chrome_options = Options()
# Bật chế độ headless (chạy ngầm)
chrome_options.add_argument("--headless=new") 
# Các tùy chọn bổ sung quan trọng cho Headless
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")

######################################################
base_url = "https://en.wikipedia.org/wiki/List_of_painters_by_name_beginning_with_%22{}%22"

# Tạo ExcelWriter để ghi nhiều sheet
writer = pd.ExcelWriter("painters.xlsx", engine="xlsxwriter")

# 2. KHỞI TẠO DRIVER MỘT LẦN VỚI CẤU HÌNH HEADLESS
driver = webdriver.Chrome(options=chrome_options)
print("Đang chạy Selenium ở chế độ nền (Headless Mode)...")

try: # Dùng try...finally để đảm bảo driver.quit() luôn được gọi
    for letter in string.ascii_uppercase: # A-Z
        url = base_url.format(letter)
        
        # Bỏ driver = webdriver.Chrome() ở đây
        driver.get(url)
        print(f"\n--- Đang xử lý chữ cái: {letter} ---")
        time.sleep(2)

        # Tránh tìm tất cả ul_tags lặp lại, chỉ tìm ul chính xác hơn nếu có thể
        # ul_tags = driver.find_elements(By.TAG_NAME, "ul")
        
        # Thử tìm ul dựa trên id hoặc class nếu có, nếu không tiếp tục dùng index 19
        ul_tags = driver.find_elements(By.TAG_NAME, "ul")
        dem = 1
        
        # Chỉ số 19 hoạt động với trang Wikipedia này (có thể thay đổi)
        if len(ul_tags) > 19:
            ul = ul_tags[19]
            li_list = ul.find_elements(By.TAG_NAME, "li")

            pattern = r"^(.*?) \((?:.*?, )?(\d{4})(?:–(\d{4}))?\), (.*)"
            data = []
            
            print(f"Có {len(li_list)} họa sĩ")
            for tag in li_list:
                match = re.match(pattern, tag.text)
                if match:
                    # Bỏ print(dem) trong vòng lặp nhỏ này để giảm output
                    dem += 1
                    
                    name_raw, birth, death, details_raw = match.groups()
                    name = name_raw.strip()
                    
                    # Tách Quốc tịch: lấy từ đầu tiên
                    nationality_parts = details_raw.split(' ',1)
                    nationality = nationality_parts[0].strip()
                    
                    # Bỏ print chi tiết từng họa sĩ để giảm output khi chạy nền
                    # print(f"Tên: {name}, Năm sinh: {birth}, Năm mất: {death}, Quốc tịch: {nationality}")
                    
                    data.append({
                        "Name": name,
                        "Birth": birth,
                        "Death": death if death else "N/A", # Xử lý năm mất có thể None
                        "Nationality": nationality
                    })
            
            # Chuyển sang DataFrame và ghi vào sheet theo chữ cái
            if data:
                df = pd.DataFrame(data)
                df.to_excel(writer, sheet_name=letter, index=False)
    
finally:
    # 3. ĐÓNG DRIVER KHI XONG HOẶC GẶP LỖI
    driver.quit()
    
# Lưu file Excel
writer.close()
print("\nĐã hoàn tất quá trình cào dữ liệu.")
print("Đã lưu dữ liệu vào painters.xlsx với mỗi sheet là một chữ cái A-Z")