from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import re # Dùng để xử lý chuỗi và làm sạch dữ liệu

# --- CẤU HÌNH ---
URL = "https://www.reddit.com/"
WAIT_TIMEOUT = 30 # Thời gian chờ tối đa cho các phần tử ban đầu (giảm từ 120 cho thực tế)
TARGET_POSTS = 10 # Mục tiêu số lượng bài viết cần thu thập
SCROLL_PAUSE_TIME = 2 # Thời gian chờ sau mỗi lần cuộn để nội dung mới tải

# Khởi tạo WebDriver
# Vui lòng đảm bảo ChromeDriver/tương đương đã được thiết lập đúng
# Sử dụng 'options' nếu cần thiết (ví dụ: chạy ẩn)
driver = webdriver.Chrome()

def extract_post_data(post_element):
    """Trích xuất dữ liệu từ một phần tử shreddit-post/article."""
    data = {}
    try:
        # 1. Tiêu đề (lấy từ thuộc tính 'post-title' của shreddit-post)
        title = post_element.get_attribute("post-title")
        data['title'] = title.strip() if title else "Không tìm thấy tiêu đề"

        # 2. Link bài viết (permalink) - Rất quan trọng để theo dõi các bài viết đã xử lý
        data['link'] = post_element.get_attribute("permalink") or "Không tìm thấy link"

        # 3. Score (Điểm upvote/downvote)
        score = post_element.get_attribute("score")
        data['score'] = score.strip() if score else "N/A"
        
        # 4. Số comment
        comments = post_element.get_attribute("comment-count") 
        data['comments'] = comments.strip() if comments else "N/A"
        
        # 5. Người đăng bài (author) và Subreddit
        data['subreddit'] = post_element.get_attribute("subreddit-name") or "N/A"
        author = post_element.get_attribute("author")
        data['author'] = author.strip() if author else "Ẩn danh"

    except Exception as e:
        # Trong trường hợp lỗi, vẫn trả về link nếu có để tránh lặp lại
        data['error'] = f"Lỗi khi trích xuất: {e}"

    return data

try:
    print(f"Đang truy cập: {URL}")
    driver.get(URL)

    # 1. Chờ cho thẻ <shreddit-feed> tải xong (là dấu hiệu trang đã ổn định)
    wait = WebDriverWait(driver, WAIT_TIMEOUT)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "shreddit-post")))

    print("Đã tải xong trang chính. Bắt đầu thu thập bài viết...")

    all_posts_data = []
    # Dùng set để lưu trữ các permalink đã được xử lý, đảm bảo tính duy nhất
    processed_links = set() 
    
    # Biến theo dõi chiều cao cuộn cuối cùng để phát hiện khi hết nội dung
    last_height = driver.execute_script("return document.body.scrollHeight")

    while len(all_posts_data) < TARGET_POSTS:
        print(f"\n--- Tiến trình: Đã thu thập {len(all_posts_data)}/{TARGET_POSTS} bài viết ---")

        # 1. Lấy lại tất cả các post đã tải
        shreddit_posts = driver.find_elements(By.TAG_NAME, "shreddit-post")
        
        newly_processed_count = 0

        # 2. Duyệt qua các post, chỉ xử lý những post mới (dựa trên permalink)
        for post in shreddit_posts:
            permalink = post.get_attribute("permalink")
            
            # Kiểm tra xem bài viết có link và link chưa được xử lý không
            if permalink and permalink not in processed_links:
                post_data = extract_post_data(post)
                all_posts_data.append(post_data)
                processed_links.add(permalink)
                newly_processed_count += 1
                
                # In thông tin bài viết đã thu thập
                idx = len(all_posts_data)
                print(f" [OK] Bài #{idx} - {post_data['title']} (r/{post_data['subreddit']})")

                if len(all_posts_data) >= TARGET_POSTS:
                    break # Đã đạt mục tiêu

        if len(all_posts_data) >= TARGET_POSTS:
            break # Thoát khỏi vòng lặp while

        # 3. Nếu chưa đủ, thực hiện cuộn trang để tải thêm nội dung
        if newly_processed_count == 0 and len(shreddit_posts) > 0:
            # Nếu không tìm thấy bài viết mới nào trong lần lặp này (có thể do lỗi tải),
            # vẫn tiếp tục cuộn nếu chưa đạt mục tiêu.
            pass
        
        # Cuộn xuống cuối trang
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Chờ để trang tải nội dung mới
        time.sleep(SCROLL_PAUSE_TIME)
        
        # Kiểm tra xem có nội dung mới được tải không
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        if new_height == last_height:
            print("Không thể cuộn thêm (chiều cao trang không đổi). Dừng thu thập.")
            break # Dừng vòng lặp nếu không thể cuộn thêm
        
        last_height = new_height # Cập nhật chiều cao cuộn cuối

    print("\n" + "=" * 50)
    print(f"*** THU THẬP HOÀN TẤT: Đã lấy {len(all_posts_data)}/{TARGET_POSTS} bài viết. ***")
    print("=" * 50)
    
    # In ra danh sách kết quả cuối cùng
    for idx, post_data in enumerate(all_posts_data, start=1):
        print(f"\nBài viết #{idx}:")
        print(f" Tiêu đề: {post_data['title']}")
        print(f" Subreddit: r/{post_data['subreddit']}")
        print(f" Người đăng: u/{post_data['author']}")
        print(f" Score: {post_data['score']}, Comments: {post_data['comments']}")
        print(f" Link: {post_data['link']}")


except TimeoutException:
    print(f"Lỗi: Đã hết thời gian chờ ({WAIT_TIMEOUT} giây) để tải trang hoặc tìm phần tử chính.")
except Exception as e:
    print(f"Đã xảy ra lỗi không xác định: {e}")

finally:
    # Đảm bảo WebDriver luôn đóng, dù có lỗi xảy ra hay không. 
    driver.quit()
    print("\nWebDriver đã đóng.")