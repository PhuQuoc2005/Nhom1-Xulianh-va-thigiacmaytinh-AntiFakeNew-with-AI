import easyocr
import os

# Khởi tạo mô hình OCR một lần duy nhất (Singleton) để tránh load lại nhiều lần gây giật lag
reader = None

def get_ocr_reader():
    global reader
    if reader is None:
        # Load ngôn ngữ Tiếng Việt ('vi') và Tiếng Anh ('en'). Chạy bằng CPU (gpu=False)
        reader = easyocr.Reader(['vi', 'en'], gpu=False)
    return reader

def extract_text_from_image(image_file):
    """
    Sử dụng công nghệ Nhận dạng ký tự quang học (OCR) để lột chữ từ hình ảnh.
    """
    try:
        r = get_ocr_reader()
        
        # Đọc dữ liệu dạng byte từ file ảnh của Streamlit
        image_bytes = image_file.read()
        
        # Đưa con trỏ file về vị trí 0 để các hàm khác (như st.image) còn vẽ được ảnh lên web
        image_file.seek(0)
        
        # Nhận diện chữ (detail=0 chỉ lấy text, không lấy tọa độ khung hình)
        result = r.readtext(image_bytes, detail=0)
        
        # Ghép các mảng chữ lại thành 1 đoạn văn bản hoàn chỉnh
        extracted_text = " ".join(result)
        return extracted_text
        
    except Exception as e:
        print(f"Lỗi khi chạy OCR: {e}")
        return ""
