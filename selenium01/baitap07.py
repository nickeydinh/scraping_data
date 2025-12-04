from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1. Thiết lập URL và Khởi tạo WebDriver
URL = "https://vi.wikipedia.org/wiki/Danh_s%C3%A1ch_tr%C6%B0%E1%BB%9Dng_%C4%91%E1%BA%A1i_h%E1%BB%8Dc,_h%E1%BB%8Dc_vi%E1%BB%87n_v%C3%A0_cao_%C4%91%E1%BA%B3ng_t%E1%BA%A1i_Vi%E1%BB%87t_Nam"

# Cấu hình Chrome Options để chạy ẩn (Headless)
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)
all_table_data = [] # Danh sách chứa dữ liệu của tất cả các bảng

print(f"Bắt đầu truy cập trang: {URL}")

try:
    driver.get(URL)
    
    # Đợi cho một bảng bất kỳ tải xong
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "wikitable"))
    )

    # 2. Định vị tất cả các bảng
    tables = driver.find_elements(By.TAG_NAME, 'table')
    print(f"Tìm thấy tổng cộng {len(tables)} bảng trên trang.")

    # 3. Lặp qua từng bảng
    for table_index, table in enumerate(tables):
        table_name = f"Bảng #{table_index + 1}"
        print(f"\n--- Xử lý {table_name} ---")
        
        # Lấy tất cả các hàng <tr> trong bảng
        # Sử dụng XPath để tìm tr trong tbody hoặc thead (vì wikitable có thể có cả 2)
        rows = table.find_elements(By.XPATH, ".//tr")
        
        if not rows:
            print("  Không tìm thấy hàng nào trong bảng này. Bỏ qua.")
            continue
            
        table_data = []
        
        # 4. Lặp qua từng hàng (<tr>)
        for row_index, row in enumerate(rows):
            # Lấy tất cả các ô dữ liệu (td) và ô tiêu đề (th) trong hàng
            cells = row.find_elements(By.XPATH, "./th | ./td")
            
            if not cells:
                continue # Bỏ qua hàng rỗng
            
            row_data = []
            
            # 5. Xử lý logic chiết xuất cho từng ô (cell)
            for cell in cells:
                cell_value = ""
                
                # Tìm thẻ <a> bên trong ô
                try:
                    anchor_tag = cell.find_element(By.TAG_NAME, "a")
                    
                    # Ưu tiên lấy thuộc tính 'title'
                    title_content = anchor_tag.get_attribute("title")
                    
                    if title_content:
                        cell_value = title_content.strip()
                    else:
                        # Nếu không có title, lấy text của thẻ <a>
                        cell_value = anchor_tag.text.strip()
                        
                except:
                    # Trường hợp không có thẻ <a> (hoặc thẻ td không phải là link)
                    # Lấy text trực tiếp của ô
                    cell_value = cell.text.strip()
                
                # Xử lý các trường hợp rác như [a], [b],... trong Wikipedia
                import re
                cell_value = re.sub(r'\[\w\]', '', cell_value).strip()
                
                row_data.append(cell_value)

            table_data.append(row_data)
            
        all_table_data.append({
            "name": table_name,
            "data": table_data
        })
        print(f"  Đã chiết xuất {len(table_data)} hàng dữ liệu.")

    XPATH_TO_OLS = "//ol[position() <= last() - 2]"
    ol_elements = driver.find_elements(By.XPATH, XPATH_TO_OLS)
    
    if not ol_elements:
        print("Không tìm thấy các thẻ <ol> theo yêu cầu.")
    else:
        print(f"Đã tìm thấy {len(ol_elements)} thẻ <ol>.")
        
        for ol_index, ol in enumerate(ol_elements):
            print(f"--- Xử lý <ol> thứ {ol_index + 1} ---")
            
            # Lấy tất cả các thẻ <li> con trực tiếp hoặc gián tiếp bên trong <ol> này
            list_items = ol.find_elements(By.XPATH, ".//li")  
            for li in list_items:
                print(li.text)
    print("\n--- HOÀN TẤT TRUY XUẤT DỮ LIỆU ---")
    
    # In ra một phần của kết quả để kiểm tra
    # for table_result in all_table_data:
    #     print(f"\n✨ {table_result['name']} ({len(table_result['data'])} hàng):")
    #     # In 3 hàng đầu tiên (chỉ mục 0, 1, 2) của mỗi bảng để xem cấu trúc
    #     for row in table_result['data'][:3]:
    #         print(f"  {row}")

except Exception as e:
    print(f"\nĐã xảy ra lỗi: {e}")

finally:
    driver.quit()
    print("\nĐã đóng trình duyệt.")