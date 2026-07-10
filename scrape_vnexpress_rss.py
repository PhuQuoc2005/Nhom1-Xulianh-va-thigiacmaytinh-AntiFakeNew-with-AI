import requests
from bs4 import BeautifulSoup
import pandas as pd
import html
import re

# Nguồn cấp dữ liệu RSS (Really Simple Syndication) của báo chính thống
rss_urls = [
    "https://vnexpress.net/rss/tin-moi-nhat.rss",
    "https://vnexpress.net/rss/thoi-su.rss",
    "https://vnexpress.net/rss/the-gioi.rss",
    "https://vnexpress.net/rss/phap-luat.rss",
    "https://thanhnien.vn/rss/home.rss",
    "https://thanhnien.vn/rss/thoi-su.rss"
]

csv_path = 'data/text/vn_fake_news_dataset.csv'

def clean_html(raw_html):
    """Xóa bỏ các thẻ HTML và link rác để lấy text thuần túy."""
    soup = BeautifulSoup(raw_html, "html.parser")
    text = soup.get_text(separator=" ")
    text = html.unescape(text)
    # Xóa các khoảng trắng thừa
    text = re.sub(r'\s+', ' ', text).strip()
    return text

print("🚀 Bắt đầu cào dữ liệu báo chí chính thống từ RSS...")
new_data = []

for url in rss_urls:
    try:
        print(f"Đang quét nguồn: {url}")
        response = requests.get(url, timeout=10)
        # Parse RSS Feed (Dùng html.parser thay vì xml để không cần cài thêm thư viện lxml)
        soup = BeautifulSoup(response.content, "html.parser")
        items = soup.findAll('item')
        
        for item in items:
            title = item.find('title').text if item.find('title') else ""
            desc = item.find('description').text if item.find('description') else ""
            
            clean_title = clean_html(title)
            clean_desc = clean_html(desc)
            
            # Gộp Tiêu đề và Mô tả làm một mẫu huấn luyện
            full_text = f"{clean_title}. {clean_desc}".strip()
            
            if len(full_text) > 20: # Lọc bỏ rác quá ngắn
                new_data.append({"text": full_text, "label": 0})
                
    except Exception as e:
        print(f"❌ Lỗi khi cào {url}: {e}")

# Loại bỏ trùng lặp nếu có
df_new = pd.DataFrame(new_data).drop_duplicates()

print(f"✅ Đã cào thành công {len(df_new)} bài báo chuẩn mực.")

if len(df_new) > 0:
    df_new.to_csv(csv_path, mode='a', header=False, index=False, encoding='utf-8')
    print(f"🎉 Đã nạp {len(df_new)} bài báo vào vũ khí {csv_path}!")
else:
    print("⚠️ Không tìm thấy bài báo mới nào.")
