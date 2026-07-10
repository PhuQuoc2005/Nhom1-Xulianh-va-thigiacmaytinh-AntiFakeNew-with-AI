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
        image_scan_mode = st.radio("Chọn phương pháp phân tích ảnh:", ["Gemini AI (Chuyên Sâu)", "Thuật toán ELA (Computer Vision)"], horizontal=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.image(uploaded_file, caption="Ảnh gốc", use_container_width=True)
        with col2:
            if "ELA" in image_scan_mode:
                with st.spinner("Đang soi lỗi Pixel bằng thuật toán ELA..."):
                    uploaded_file.seek(0)
                    ela_img = compute_ela(uploaded_file)
                    if ela_img:
                        st.image(ela_img, caption="Ảnh ELA (Vệt sáng = Bị chỉnh sửa)", use_container_width=True)
            else:
                st.info("Chế độ AI: Máy tính sẽ tự động đọc cấu trúc ngầm của bức ảnh.")
    
    if st.button("🚀 Bắt Đầu Quét", type="primary"):
        if uploaded_file is not None:
            if "ELA" in image_scan_mode:
                st.info("Chế độ ELA: Máy tính sẽ tìm kiếm các vùng pixel bị nén bất thường do can thiệp bằng phần mềm chỉnh sửa ảnh (như Photoshop).")
                with st.spinner("⏳ Đang tính toán Error Level Analysis và đẩy qua Mạng Nơ-ron (CNN)..."):
                    from src.image.ela_processor import compute_ela
                    uploaded_file.seek(0)
                    ela_img = compute_ela(uploaded_file)
                    
                    if ela_img:
                        from src.models.ela_cnn import predict_ela
                        fake_prob = predict_ela(ela_img)
                        
                        if fake_prob is not None:
                            # Tích hợp OCR và NLP Offline
                            from src.image.ocr_processor import extract_text_from_image
                            from src.text.nlp_processor import predict_text_fake_news
                            
                            extracted_text = extract_text_from_image(uploaded_file)
                            
                            if extracted_text and extracted_text.startswith("ERROR:"):
                                st.error(f"⚠️ Lỗi cấu hình Tesseract OCR: {extracted_text.replace('ERROR:', '').strip()}\n\nVui lòng kiểm tra lại xem Tesseract đã được cài đặt đúng đường dẫn chưa!")
                                extracted_text = "" # Xóa text lỗi để tiếp tục luồng bình thường
                            
                            if extracted_text and len(extracted_text.strip()) > 5:
                                text_length = len(extracted_text.strip())
                                st.info(f"📝 Đã bóc tách được văn bản (OCR) - Độ dài {text_length} ký tự:\n{extracted_text[:100]}...")
                                fake_prob_nlp = predict_text_fake_news(extracted_text)
                                
                                # Cân bằng trọng số động (Dynamic Weighting)
                                if text_length > 30:
                                    # Phát hiện nhiều chữ -> Ảnh màn hình web/báo chí
                                    st.warning("🔄 Tự động kích hoạt Cân bằng Trọng số Động (Dynamic Weighting): Hệ thống dồn 80% trọng số vào thuật toán Ngôn ngữ (NLP) vì phát hiện đây là ảnh chụp màn hình có chứa chữ (tránh báo động giả từ thanh Menu giao diện).")
                                    final_prob = (fake_prob * 0.2) + (fake_prob_nlp * 0.8)
                                else:
                                    # Ít chữ -> Ảnh tự nhiên
                                    final_prob = (fake_prob * 0.6) + (fake_prob_nlp * 0.4)
                                    
                                reasons = [
                                    "Đã phân tích cấu trúc điểm ảnh bằng Thuật toán CNN-ELA (Ngoại tuyến).",
                                    f"Mạng Nơ-ron (CNN) chấm {round(fake_prob, 2)}% xác suất Pixel bị đứt gãy/cắt ghép.",
                                    f"Mô hình Ngôn ngữ (NLP) chấm {round(fake_prob_nlp, 2)}% xác suất Nội dung là tin giả mạo."
                                ]
                            else:
                                final_prob = fake_prob
                                reasons = [
                                    "Đã phân tích các điểm ảnh bằng Mạng Nơ-ron CNN-ELA (Ngoại tuyến).",
                                    "Mạng Nơ-ron Tích chập (CNN) phát hiện bất thường." if fake_prob > 50 else "CNN chưa tìm thấy dấu vết cắt ghép lộ liễu.",
                                    "Tesseract OCR không tìm thấy văn bản hợp lệ trong bức ảnh."
                                ]
                                
                                
                            res = {
                                "fake_probability": round(final_prob, 2),
                                "reasons": reasons,
                                "sentiment_score": 0.0
                            }
                        else:
                            res = {
                                "fake_probability": 0,
                                "reasons": ["⚠️ Mô hình ELA CNN chưa được huấn luyện! Vui lòng chạy file train_ela_model.py."],
                                "sentiment_score": 0.0
                            }
                    else:
                        res = {
                            "fake_probability": 0,
                            "reasons": ["⚠️ Không thể phân tích ELA cho bức ảnh này (định dạng không được hỗ trợ hoặc file bị lỗi)."],
                            "sentiment_score": 0.0
                        }
            else:
                with st.spinner("⏳ AI đang phân tích cấu trúc điểm ảnh... Vui lòng đợi trong giây lát!"):
                    res = analyze_real_fake_image(uploaded_file, custom_api_key=custom_api_key)
                
            display_results(res, "Hình Ảnh", is_offline=("ELA" in image_scan_mode))
            
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
                    with st.spinner("⏳ Mô hình Trí tuệ Nhân tạo Ngôn ngữ (NLP) đang phân tích câu chữ..."):
                        from src.text.nlp_processor import predict_text_fake_news
                        fake_prob_nlp = predict_text_fake_news(input_text.strip())
                        res = {
                            "fake_probability": fake_prob_nlp,
                            "reasons": [
                                "Phân tích cú pháp và ngữ nghĩa bằng mô hình Machine Learning NLP (Ngoại tuyến).",
                                "Văn bản có giọng điệu và từ khóa đặc trưng của tin giả (Clickbait/Fake News)." if fake_prob_nlp > 50 else "Nội dung văn bản khá trung lập và đáng tin cậy."
                            ],
                            "sentiment_score": 0.0
                        }
                    
                    display_results(res, "Bài Viết (Học máy)", is_offline=True)
                    
                    prob = res.get("fake_probability", 50)
                    if prob < 30:
                        st.balloons()
                    add_to_history("Văn Bản (TF-IDF)", "Đoạn văn", prob)
            else:
                loading_text = "⏳ Đang truy xuất URL, bóc tách dữ liệu và cho AI suy luận..." if is_url else "⏳ AI đang tìm kiếm đối chiếu sự thật trên mạng..."
                
                with st.spinner(loading_text):
                    res, snippet = analyze_real_fake_news(input_text, is_url=is_url, custom_api_key=custom_api_key)
                
            display_results(res, "Đường dẫn URL" if is_url else "Văn Bản", is_offline=False)
            
            prob = res.get("fake_probability", 50)
            if prob < 30:
                st.balloons()
            
            if not ("LỖI QUÁ TẢI" in res.get("reasons", [""])[0] or "Lỗi hệ thống" in res.get("reasons", [""])[0]):
                add_to_history("Đường Dẫn" if is_url else "Văn Bản", snippet, prob)
                
        else:
            st.warning("⚠️ Vui lòng nhập văn bản, URL hoặc tải lên hình ảnh trước khi phân tích!")
