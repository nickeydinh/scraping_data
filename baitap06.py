from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import re

######################################################
# I. Khoi tao DataFrame rong
all_links = []
d = pd.DataFrame({'name': [], 'birth': [], 'death': [], 'nationality': []})

######################################################
# II. Lay ra tat ca duong dan (Links)
# Chay thu voi chu cai 'P' (Ma ASCII 80)
for i in range(80, 81): 
    driver = webdriver.Chrome()
    url = "https://en.wikipedia.org/wiki/List_of_painters_by_name_beginning_with_%22" + chr(i) + "%22"
    
    try:
        print("------------------------------------------------")
        print("Dang truy cap: " + url)
        driver.get(url)
        time.sleep(3)

        # 1. Lay tat ca cac the ul tren trang
        ul_tags = driver.find_elements(By.TAG_NAME, "ul")
        
        # 2. THUAT TOAN TIM DANH SACH DUNG (Tim ul co nhieu li nhat)
        chosen_ul = None
        max_items = 0

        for ul in ul_tags:
            try:
                li_list = ul.find_elements(By.TAG_NAME, "li")
                if len(li_list) > max_items:
                    max_items = len(li_list)
                    chosen_ul = ul
            except:
                pass

        print(f"Da tim thay danh sach chua {max_items} dong.")

        # 3. Lay link (Da sua lai de an toan hon)
        if chosen_ul:
            li_tags = chosen_ul.find_elements(By.TAG_NAME, "li")
            
            # --- SU DUNG VONG LAP AN TOAN ---
            for tag in li_tags:
                try:
                    # Co gang tim the <a> ben trong the <li>
                    a_tag = tag.find_element(By.TAG_NAME, "a")
                    link = a_tag.get_attribute("href")
                    all_links.append(link)
                except:
                    # Neu dong nay khong co link thi bo qua, khong bao loi
                    pass
            # --------------------------------
            
        else:
            print("Khong tim thay danh sach nao phu hop!")

    except Exception as e:
        print(f"Loi o buoc 1: {e}")

    driver.quit()

print(f"Tong cong tim duoc: {len(all_links)} link.")

#######################################################
# III. Lay thong tin chi tiet tung hoa si
count = 0
for link in all_links:
    # --- CHAY THU 4 NGUOI DE TEST (XOA DE CHAY HET) ---
    if count > 3:
        break
    count += 1
    # --------------------------------------------------

    print(f"[{count}] Dang cao du lieu tu: {link}")
    
    try:
        driver = webdriver.Chrome()
        driver.get(link)
        time.sleep(2)

        # Lay ten
        try:
            name = driver.find_element(By.TAG_NAME, "h1").text
        except:
            name = ""

        # Lay ngay sinh
        try:
            birth_element = driver.find_element(By.XPATH, "//th[text()='Born']/following-sibling::td")
            birth = re.findall(r'[0-9]{1,2}\s+[A-Za-z]+\s+[0-9]{4}', birth_element.text)[0]
        except:
            birth = ""
            
        # Lay ngay mat
        try:
            death_element = driver.find_element(By.XPATH, "//th[text()='Died']/following-sibling::td")
            death = re.findall(r'[0-9]{1,2}\s+[A-Za-z]+\s+[0-9]{4}', death_element.text)[0]
        except:
            death = ""

        # Lay quoc tich
        try:
            nationality_element = driver.find_element(By.XPATH, "//th[text()='Nationality']/following-sibling::td")
            nationality = nationality_element.text
        except:
            nationality = ""
        
        # Ghi vao DataFrame
        painter = {'name': name, 'birth': birth, 'death': death, 'nationality': nationality}
        painter_df = pd.DataFrame([painter])
        d = pd.concat([d, painter_df], ignore_index=True)
        
        driver.quit()
        
    except:
        driver.quit()
        pass

##################
# IV. Xuat ra Excel
print("\nKet qua:")
print(d)

file_name = 'Painters_Final.xlsx'
d.to_excel(file_name, index=False)
print('Xong!')