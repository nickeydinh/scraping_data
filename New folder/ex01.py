import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
import time

# đường dẫn đến file thực thi gecko driver
gecko_driver_path = r'C:\Users\Admin\Documents\HK1B-2025\OSDS\scraping_data\New folder\geckodriver.exe'

#khởi tạo đối tượng Service cho gecko driver
Ser = Service(gecko_driver_path)

#tạo tùy chọn
options = webdriver.FirefoxOptions()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'

#thiết lập firefox chỉ hiện thị giao diện
options.headless = False

#khoi tao driver
driver = webdriver.Firefox(service=Ser, options=options)

#tao url
url = 'http://pythonscraping.com/pages/javascript/ajaxDemo.html'

#truy cap
driver.get(url)

#in ra noi dung
print("Berfore AJAX call: ========================\n")
print(driver.page_source)

#tam dung 3 giay
time.sleep(3)

#in lai
print("After AJAX call: ========================\n")
print(driver.page_source)

#dong trinh duyet
driver.quit()