import google.generativeai as genai
import json
import time
import streamlit as st

DEFAULT_API_KEY = ""
current_api_key = DEFAULT_API_KEY
model = None

def init_model(api_key):
    global model, current_api_key
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            'gemini-2.5-flash',
            generation_config={"response_mime_type": "application/json"}
        )
        current_api_key = api_key
    except Exception as e:
        pass

# Khởi tạo lần đầu
init_model(DEFAULT_API_KEY)

def fallback_heuristic_scan(prompt, image=None):
    if image is not None:
        return {
            "fake_probability": 50,
            "reasons": ["⚠️ LỖI QUÁ TẢI (RATE LIMIT): API Google đã đạt giới hạn.", "Không thể quét hình ảnh bằng thuật toán thủ công (chỉ áp dụng cho văn bản). Vui lòng thêm API Key riêng."],
            "sentiment_score": 0.0
        }
        
    fake_keywords = ["tin giả", "không đúng sự thật", "bác bỏ", "sai sự thật", "lừa đảo", "chưa được kiểm chứng", "đính chính", "tin đồn thất thiệt"]
    real_keywords = ["xác nhận", "công bố chính thức", "sự thật là", "đã bắt giữ", "đúng sự thật"]
    
    prompt_lower = prompt.lower()
    score = 50
    reasons = ["⚠️ CHẾ ĐỘ QUÉT THỦ CÔNG (Do AI quá tải):"]
    
    found_fake = False
    for kw in fake_keywords:
        if kw in prompt_lower:
            score += 15
            reasons.append(f"- Phát hiện từ khóa cảnh báo rủi ro: '{kw}'")
            found_fake = True
            
    for kw in real_keywords:
        if kw in prompt_lower:
            score -= 10
            reasons.append(f"- Phát hiện từ khóa đáng tin cậy: '{kw}'")
            
    if not found_fake:
        reasons.append("- Không tìm thấy từ khóa cảnh báo rủi ro cao nào trong kết quả tra cứu.")
        
    score = max(5, min(95, score))
    
    return {
        "fake_probability": score,
        "reasons": reasons,
        "sentiment_score": 0.0
    }

def call_gemini_analysis(prompt, image=None, custom_api_key=None):
    global current_api_key
    
    # Cập nhật API Key Động (Dynamic Key)
    if custom_api_key and custom_api_key.strip() != "" and custom_api_key != current_api_key:
        init_model(custom_api_key.strip())
    elif (not custom_api_key or custom_api_key.strip() == "") and current_api_key != DEFAULT_API_KEY:
        init_model(DEFAULT_API_KEY)

    if not model:
        return {"fake_probability": 50, "reasons": ["AI chưa được khởi tạo."], "sentiment_score": 0.0}
    
    system_prompt = """
    Bạn là chuyên gia phân tích và nhận diện tin giả (Fake News) cấp cao.
    Hãy phân tích thông tin được cung cấp (văn bản, kết quả tìm kiếm đối chiếu hoặc hình ảnh).
    BẮT BUỘC TRẢ VỀ JSON hợp lệ theo đúng cấu trúc sau:
    {
        "fake_probability": <số nguyên từ 0 đến 100, thể hiện % khả năng đây là tin giả>,
        "reasons": ["Lý do 1", "Lý do 2"],
        "sentiment_score": <số thập phân từ -1.0 đến 1.0, -1 là tiêu cực/kích động, 1 là tích cực>
    }
    Hãy cực kỳ khách quan. Nếu có nguồn đối chiếu chỉ ra nội dung này là giả, hãy tăng fake_probability.
    """
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            if image:
                response = model.generate_content([system_prompt + "\n\n" + prompt, image])
            else:
                response = model.generate_content(system_prompt + "\n\n" + prompt)
                
            text = response.text
            data = json.loads(text.strip())
            
            return {
                "fake_probability": data.get("fake_probability", 50),
                "reasons": data.get("reasons", ["AI đã phân tích nhưng không đưa ra lý do cụ thể."]),
                "sentiment_score": data.get("sentiment_score", 0.0)
            }
        except Exception as e:
            error_msg = str(e)
            
            # Xử lý tự động thử lại (Auto-Retry) khi bị lỗi 429 Quota Exceeded
            if "429" in error_msg or "Quota exceeded" in error_msg:
                if attempt < max_retries - 1:
                    wait_time = 20 # Đợi 20 giây rồi thử lại
                    st.toast(f"API đang bận. Hệ thống sẽ tự động thử lại sau {wait_time}s (Lần {attempt+1}/{max_retries-1})...", icon="⏳")
                    time.sleep(wait_time)
                    continue
                else:
                    return fallback_heuristic_scan(prompt, image)
                
            return fallback_heuristic_scan(prompt, image)
