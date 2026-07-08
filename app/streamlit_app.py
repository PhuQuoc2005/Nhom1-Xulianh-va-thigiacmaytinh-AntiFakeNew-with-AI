import sys
import os

# Cấu hình PYTHONPATH để Python nhận diện được thư mục gốc của dự án
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from app.ui_components import load_custom_css, render_header, display_results, render_sidebar
from src.text.web_scraper import extract_url_content
from src.text.search_engine import search_cross_check
from src.inference.ai_engine import call_gemini_analysis
from src.image.image_processor import analyze_real_fake_image
from src.image.ela_processor import compute_ela

st.set_page_config(page_title="Nhóm 1 - Xử Lý Ảnh Và Thị Giác Máy Tính - Anti Fake News Project", page_icon="🕵️", layout="wide")

if "query_history" not in st.session_state:
    st.session_state.query_history = []

def add_to_history(q_type, snippet, prob):
    st.session_state.query_history.insert(0, {"type": q_type, "snippet": snippet, "prob": prob})
    if len(st.session_state.query_history) > 10:
        st.session_state.query_history.pop()

load_custom_css()
render_header()
custom_api_key = render_sidebar(st.session_state.query_history)

# Chia layout chính để form ra giữa thay vì tràn toàn màn hình
_, col_main, _ = st.columns([1, 2, 1])

with col_main:
    def analyze_real_fake_news(content: str, is_url: bool = False, custom_api_key: str = None):
        search_results = ""
        extracted_text = content
        title = ""
        
        if is_url:
            title, extracted_text = extract_url_content(content)
            search_query = title if title else extracted_text[:100]
            search_results = search_cross_check(search_query)
        else:
            search_results = search_cross_check(extracted_text[:100])
                
        prompt = f"""
        Hãy phân tích nội dung sau để xem nó có phải tin giả không:
        Nội dung cần phân tích:
        {extracted_text[:2000]}
        
        Kết quả tìm kiếm chéo trên Internet (dùng để đối chiếu sự thật):
        {search_results}
        """
        
        snippet = title if title else (content[:60] + "..." if len(content) > 60 else content)
        return call_gemini_analysis(prompt, custom_api_key=custom_api_key), snippet
    
    st.write("") 
    
    input_text = st.text_area(
        "Văn bản hoặc Link bài báo:", 
        height=160, 
        placeholder="Nhập nội dung văn bản hoặc dán đường dẫn (VD: https://vnexpress.net/...) vào đây...",
        label_visibility="collapsed"
    )
    
    uploaded_file = st.file_uploader("Hoặc tải lên một hình ảnh:", type=["jpg", "png", "jpeg", "webp"])
    
    image_scan_mode = "Gemini AI"
    if uploaded_file is not None:
        image_scan_mode = st.radio("Chọn phương pháp phân tích ảnh:", ["Gemini AI (Chuyên Sâu)", "Thuật toán ELA (Computer Vision)"], horizontal=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.image(uploaded_file, caption="Ảnh gốc", use_container_width=True)
        with col2:
            if "ELA" in image_scan_mode:
                with st.spinner("Đang soi lỗi Pixel bằng thuật toán ELA..."):
                    ela_img = compute_ela(uploaded_file)
                    if ela_img:
                        st.image(ela_img, caption="Ảnh ELA (Vệt sáng = Bị chỉnh sửa)", use_container_width=True)
            else:
                st.info("Chế độ AI: Máy tính sẽ tự động đọc cấu trúc ngầm của bức ảnh.")
    
    if st.button("🚀 Bắt Đầu Quét", type="primary"):
        if uploaded_file is not None:
            if "ELA" in image_scan_mode:
                st.warning("🚧 Mô hình ELA-CNN hiện đang chờ được nạp dữ liệu (Dataset) để Huấn luyện. Tạm thời trả về kết quả phân tích ELA bằng mắt thường.")
                res = {
                    "fake_probability": 50,
                    "reasons": [
                        "Thuật toán ELA đã làm nổi bật các điểm ảnh (pixel) bị nén bất thường.", 
                        "👉 HÃY NHÌN VÀO BỨC ẢNH ELA PHÍA TRÊN: Nếu có một vùng nào đó SÁNG RỰC lên khác biệt hoàn toàn so với xung quanh, đó chính là phần bị ghép/photoshop!"
                    ],
                    "sentiment_score": 0.0
                }
            else:
                with st.spinner("⏳ AI đang phân tích cấu trúc điểm ảnh... Vui lòng đợi trong giây lát!"):
                    res = analyze_real_fake_image(uploaded_file, custom_api_key=custom_api_key)
                
            display_results(res, "Hình Ảnh")
            
            prob = res.get("fake_probability", 50)
            if prob < 30:
                st.balloons()
            # Tránh lưu lỗi vào lịch sử
            if not ("LỖI QUÁ TẢI" in res.get("reasons", [""])[0] or "Lỗi hệ thống" in res.get("reasons", [""])[0]):
                add_to_history("Hình Ảnh", uploaded_file.name, prob)
                
        elif input_text.strip():
            is_url = input_text.strip().startswith("http://") or input_text.strip().startswith("https://")
            loading_text = "⏳ Đang truy xuất URL, bóc tách dữ liệu và cho AI suy luận..." if is_url else "⏳ AI đang tìm kiếm đối chiếu sự thật trên mạng..."
            
            with st.spinner(loading_text):
                res, snippet = analyze_real_fake_news(input_text, is_url=is_url, custom_api_key=custom_api_key)
                
            display_results(res, "Đường dẫn URL" if is_url else "Văn Bản")
            
            prob = res.get("fake_probability", 50)
            if prob < 30:
                st.balloons()
            
            if not ("LỖI QUÁ TẢI" in res.get("reasons", [""])[0] or "Lỗi hệ thống" in res.get("reasons", [""])[0]):
                add_to_history("Đường Dẫn" if is_url else "Văn Bản", snippet, prob)
                
        else:
            st.warning("⚠️ Vui lòng nhập văn bản, URL hoặc tải lên hình ảnh trước khi phân tích!")
