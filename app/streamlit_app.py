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
        "", 
        height=160, 
        placeholder="Nhập nội dung văn bản hoặc dán đường dẫn (VD: https://vnexpress.net/...) vào đây...",
        label_visibility="collapsed"
    )
    
    text_scan_mode = "Gemini AI"
    if input_text.strip():
        text_scan_mode = st.radio("Chọn phương pháp phân tích văn bản:", ["Gemini AI (Phân tích ngữ cảnh sâu)", "Mô hình Học máy (TF-IDF + Random Forest)"], horizontal=True)
    
    uploaded_file = st.file_uploader("Hoặc tải lên một hình ảnh:", type=["jpg", "png", "jpeg", "webp"])
    
    image_scan_mode = "Gemini AI"
    if uploaded_file is not None:
        image_scan_mode = st.radio("Chọn phương pháp phân tích ảnh:", ["Gemini AI (Chuyên Sâu)", "Thuật toán ELA (Computer Vision)", "Đọc chữ trong ảnh (OCR + Máy học)"], horizontal=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.image(uploaded_file, caption="Ảnh gốc", use_container_width=True)
        with col2:
            if "ELA" in image_scan_mode:
                with st.spinner("Đang soi lỗi Pixel bằng thuật toán ELA..."):
                    ela_img = compute_ela(uploaded_file)
                    if ela_img:
                        st.image(ela_img, caption="Ảnh ELA (Vệt sáng = Bị chỉnh sửa)", use_container_width=True)
            elif "OCR" in image_scan_mode:
                st.info("Chế độ OCR: Máy tính sẽ tự động đọc chữ (Text) bên trong bức ảnh của bạn mà không cần mạng Internet.")
            else:
                st.info("Chế độ AI: Máy tính sẽ tự động đọc cấu trúc ngầm của bức ảnh.")
    
    if st.button("🚀 Bắt Đầu Quét", type="primary"):
        if uploaded_file is not None:
            if "ELA" in image_scan_mode:
                st.info("Chế độ ELA: Máy tính sẽ tìm kiếm các vùng pixel bị nén bất thường do can thiệp bằng phần mềm chỉnh sửa ảnh (như Photoshop).")
                with st.spinner("⏳ Đang tính toán Error Level Analysis và đẩy qua Mạng Nơ-ron (CNN)..."):
                    from src.image.ela_processor import compute_ela
                    ela_img = compute_ela(uploaded_file)
                    
                    if ela_img:
                        from src.models.ela_cnn import predict_ela
                        fake_prob = predict_ela(ela_img)
                        
                        if fake_prob is not None:
                            res = {
                                "fake_probability": fake_prob,
                                "reasons": [
                                    "Đã phân tích các điểm ảnh bằng Thuật toán ELA.",
                                    "Mạng Nơ-ron Tích chập (CNN) được huấn luyện trên bộ dữ liệu MKLab Quốc tế đã phát hiện cấu trúc ảnh bất thường." if fake_prob > 50 else "Mạng Nơ-ron Tích chập (CNN) chưa tìm thấy dấu hiệu ảnh bị cắt ghép lộ liễu."
                                ],
                                "sentiment_score": 0.0
                            }
                        else:
                            res = {
                                "fake_probability": 0,
                                "reasons": ["⚠️ Mô hình ELA CNN chưa được huấn luyện! Vui lòng chạy file train_ela_model.py."],
                                "sentiment_score": 0.0
                            }
            elif "OCR" in image_scan_mode:
                with st.spinner("⏳ Đang sử dụng công nghệ EasyOCR để lột chữ tiếng Việt từ hình ảnh..."):
                    from src.image.ocr_processor import extract_text_from_image
                    extracted_text = extract_text_from_image(uploaded_file)
                
                if not extracted_text.strip():
                    res = {
                        "fake_probability": 0,
                        "reasons": ["⚠️ Không tìm thấy chữ viết rõ ràng nào trong bức ảnh này!", "Công nghệ OCR yêu cầu hình ảnh phải chứa văn bản (Ví dụ: ảnh chụp màn hình bài báo, status Facebook)."],
                        "sentiment_score": 0.0
                    }
                else:
                    with st.spinner("⏳ Đang đưa chữ vào Mô hình Học máy tự train (TF-IDF)..."):
                        from src.models.text_ml_model import predict_text
                        res = predict_text(extracted_text)
                        res["reasons"].insert(0, f"**Văn bản OCR đọc được từ ảnh:**\n\n> *{extracted_text}*")
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
            
            if "TF-IDF" in text_scan_mode:
                if is_url:
                    st.error("❌ Mô hình TF-IDF Cổ điển chỉ hỗ trợ phân tích đoạn văn bản trực tiếp. Vui lòng copy nội dung bài báo dán vào đây, hoặc chuyển sang dùng Gemini AI để đọc Link!")
                else:
                    with st.spinner("⏳ Mô hình Học máy đang tính toán tần suất từ vựng (TF-IDF)..."):
                        from src.models.text_ml_model import predict_text
                        res = predict_text(input_text.strip())
                    
                    display_results(res, "Bài Viết (Học máy)")
                    
                    prob = res.get("fake_probability", 50)
                    if prob < 30:
                        st.balloons()
                    add_to_history("Văn Bản (TF-IDF)", "Đoạn văn", prob)
            else:
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
