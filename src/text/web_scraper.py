import requests
from bs4 import BeautifulSoup
import streamlit as st

@st.cache_data(show_spinner=False, ttl=3600)
def extract_url_content(url):
    try:
        # Giảm timeout xuống 5s và dùng lxml parser (cực nhanh bằng C/C++) thay vì html.parser
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.content, 'lxml')
        
        title = soup.title.string if soup.title else ""
        paragraphs = soup.find_all('p')
        text_content = " ".join([p.text for p in paragraphs])
        
        # Cắt bớt lượng text (lấy 3000 ký tự đầu tiên) để tải nhẹ qua mạng
        return title, text_content[:3000]
    except Exception as e:
        return "", f"Lỗi khi truy xuất URL: {str(e)}"
