import requests
from bs4 import BeautifulSoup
import pandas as pd
import html
import re
import random

# Danh sách nguồn báo Chính thống
rss_urls = [
    "https://vnexpress.net/rss/tin-moi-nhat.rss",
    "https://tuoitre.vn/rss/tin-moi-nhat.rss",
    "https://thanhnien.vn/rss/home.rss"
]

csv_path = 'data/text/vn_fake_news_dataset.csv'

# Các từ khóa giật gân để thêm thắt vào tin thật
fake_prefixes = ["Sốc:", "Khẩn cấp:", "Cảnh báo:", "Chấn động:", "Tin mật:", "Tuyệt mật:", "Lộ tẩy:"]
fake_suffixes = ["Hãy chia sẻ bài viết này ngay!", "Nguy hiểm chết người!", "Sắp tận thế rồi!", 
                 "Gây ung thư lập tức!", "Nhận ngay 500 triệu đồng!", "Thực hư ra sao?"]
fake_injections = ["do người ngoài hành tinh đứng sau", "bị yểm bùa", "vì ăn nhầm thuốc độc", 
                   "gây chấn động giới tỷ phú", "có liên quan đến kho báu nghìn tỷ"]

def clean_html(raw_html):
    if not raw_html: return ""
    soup = BeautifulSoup(raw_html, "html.parser")
    text = soup.get_text(separator=" ")
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def distort_to_fake(real_text):
    """
    Biến đổi một bản tin thật thành tin giả mang tính giật gân
    """
    # Thay đổi các con số nhỏ thành con số khổng lồ (VD: 5 -> 50000)
    def replace_number(match):
        num_str = match.group()
        try:
            num = int(num_str.replace('.', '').replace(',', ''))
            return str(num * random.choice([10, 100, 1000, 10000]))
        except:
            return num_str

    distorted = re.sub(r'\b\d{1,4}\b', replace_number, real_text)
    
    # Thêm tiền tố giật gân
    if random.random() > 0.3:
        distorted = f"{random.choice(fake_prefixes)} {distorted}"
        
    # Chèn các cụm từ phi lý vào giữa câu (thay dấu chấm hoặc phẩy bằng cụm từ)
    if random.random() > 0.5:
        distorted = distorted.replace(". ", f" {random.choice(fake_injections)}. ", 1)
        
    # Thêm hậu tố câu like, share
    if random.random() > 0.4:
        distorted = f"{distorted} {random.choice(fake_suffixes)}"
        
    return distorted

print("🚀 Bắt đầu cào dữ liệu báo Chính Thống và Tự động sinh Tin Giả...")
new_data = []

headers = {'User-Agent': 'Mozilla/5.0'}

for url in rss_urls:
    try:
        print(f"Đang quét nguồn: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        
        # Dùng xml parser để tránh lỗi parse html
        soup = BeautifulSoup(response.content, "xml")
        items = soup.find_all('item')
        
        for item in items:
            title = item.find('title').text if item.find('title') else ""
            desc = item.find('description').text if item.find('description') else ""
            
            # Làm sạch dữ liệu
            clean_title = clean_html(title)
            # Trong một số RSS, description chứa cục HTML <img>, ta cần dọn dẹp
            clean_desc = clean_html(desc)
            
            real_text = f"{clean_title}. {clean_desc}".strip()
            
            if len(real_text) > 20:
                # 1. Lưu lại bản Gốc là Tin Thật (Nhãn 0)
                new_data.append({"text": real_text, "label": 0})
                
                # 2. Xào nấu bản Gốc thành Tin Giả (Nhãn 1)
                fake_text = distort_to_fake(real_text)
                new_data.append({"text": fake_text, "label": 1})
                
    except Exception as e:
        print(f"❌ Lỗi khi cào {url}: {e}")

df_new = pd.DataFrame(new_data).drop_duplicates()

if len(df_new) > 0:
    df_new.to_csv(csv_path, mode='a', header=False, index=False, encoding='utf-8')
    print(f"🎉 Đã cào và biến tấu thành công {len(df_new)} bài báo ({(len(df_new)//2)} Thật, {(len(df_new)//2)} Giả) vào {csv_path}!")
else:
    print("⚠️ Không lấy được bài báo nào.")
