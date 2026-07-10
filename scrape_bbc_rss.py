import requests
from bs4 import BeautifulSoup
import pandas as pd
import html
import re

rss_urls = [
    "https://feeds.bbci.co.uk/vietnamese/rss.xml",
    "https://www.rfa.org/vietnamese/rss2.xml" # Thêm RFA để lấy thêm văn phong tương tự
]

csv_path = 'data/text/vn_fake_news_dataset.csv'

def clean_html(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")
    text = soup.get_text(separator=" ")
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

print("🚀 Bắt đầu cào dữ liệu từ BBC Tiếng Việt và các nguồn tương tự...")
new_data = []

for url in rss_urls:
    try:
        print(f"Đang quét nguồn: {url}")
        # Fake User-Agent để tránh bị block
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        items = soup.findAll('item')
        
        for item in items:
            title = item.find('title').text if item.find('title') else ""
            desc = item.find('description').text if item.find('description') else ""
            
            clean_title = clean_html(title)
            clean_desc = clean_html(desc)
            
            full_text = f"{clean_title}. {clean_desc}".strip()
            
            if len(full_text) > 20:
                # Gắn nhãn 1 (Tin giả / Theo yêu cầu hệ thống)
                new_data.append({"text": full_text, "label": 1})
                
    except Exception as e:
        print(f"❌ Lỗi khi cào {url}. Nguyên nhân có thể do mạng bị chặn (Block): {e}")

df_new = pd.DataFrame(new_data).drop_duplicates()

print(f"✅ Đã cào thành công {len(df_new)} bài báo.")

if len(df_new) > 0:
    df_new.to_csv(csv_path, mode='a', header=False, index=False, encoding='utf-8')
    print(f"🎉 Đã dán nhãn [1] và nạp {len(df_new)} bài báo vào {csv_path}!")
else:
    print("⚠️ Không lấy được bài báo nào. Vui lòng kiểm tra lại kết nối mạng (Có thể cần bật VPN).")
