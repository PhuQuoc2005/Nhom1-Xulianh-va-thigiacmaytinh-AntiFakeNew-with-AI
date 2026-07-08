import easyocr
import os

# Khởi tạo mô hình OCR một lần duy nhất (Singleton) để tránh load lại nhiều lần gây giật lag
reader = None

import sys

def get_ocr_reader():
    global reader
    if reader is None:
        # Tắt in ra console (cả stdout và stderr) để tránh lỗi progress bar chứa ký tự lạ của easyocr khi tải model
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')
        try:
            # Load ngôn ngữ Tiếng Việt ('vi') và Tiếng Anh ('en'). Chạy bằng CPU (gpu=False)
            reader = easyocr.Reader(['vi', 'en'], gpu=False)
        finally:
            sys.stdout.close()
            sys.stderr.close()
            sys.stdout = old_stdout
            sys.stderr = old_stderr
    return reader

def extract_text_from_image(image_file):
    """
    Sử dụng công nghệ Nhận dạng ký tự quang học (OCR) để lột chữ từ hình ảnh.
    """
    try:
        r = get_ocr_reader()
        
        # QUAN TRỌNG: Đưa con trỏ file về 0 TRƯỚC KHI đọc, vì Streamlit có thể đã đọc file này ở bước trước (st.image)
        image_file.seek(0)
        # Đọc dữ liệu dạng byte từ file ảnh của Streamlit
        image_bytes = image_file.read()
        
        # Đưa con trỏ file về vị trí 0 lại để các hàm khác (nếu có) vẫn dùng được
        image_file.seek(0)
        
        # Nhận diện chữ (detail=0 chỉ lấy text, không lấy tọa độ khung hình)
        result = r.readtext(image_bytes, detail=0)
        
        # Ghép các mảng chữ lại thành 1 đoạn văn bản hoàn chỉnh
        extracted_text = " ".join(result)
        return extracted_text
        
    except Exception as e:
        with open("ocr_error.log", "w", encoding="utf-8") as f:
            f.write(str(e))
        return ""
