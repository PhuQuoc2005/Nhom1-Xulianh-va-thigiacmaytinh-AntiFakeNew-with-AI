import PIL.Image
from src.inference.ai_engine import call_gemini_analysis
import streamlit as st

def analyze_real_fake_image(image_bytes, custom_api_key=None):
    img = PIL.Image.open(image_bytes)
    prompt = """Hãy phân tích toàn diện bức ảnh này theo 2 bước:
1. Thị giác máy tính: Tìm các dấu hiệu chỉnh sửa, cắt ghép photoshop, deepfake hoặc AI generated.
2. Xử lý văn bản (OCR & Fact-check): Nếu trong ảnh có chứa bất kỳ đoạn chữ nào (tiêu đề báo, status mạng xã hội, tin nhắn...), hãy trích xuất đoạn chữ đó ra và ĐÁNH GIÁ XEM NỘI DUNG ĐÓ LÀ TIN THẬT HAY TIN GIẢ.
Hãy trả về kết quả phân tích rõ ràng."""
    res = call_gemini_analysis(prompt, image=img, custom_api_key=custom_api_key)
    return res
