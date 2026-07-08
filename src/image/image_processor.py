import PIL.Image
from src.inference.ai_engine import call_gemini_analysis
import streamlit as st

def analyze_real_fake_image(image_bytes, custom_api_key=None):
    img = PIL.Image.open(image_bytes)
    prompt = "Hãy phân tích hình ảnh này xem có dấu hiệu chỉnh sửa, giả mạo (photoshop, deepfake, AI generated) hay không. Chỉ ra các bất thường về ánh sáng, pixel, hoặc bối cảnh nếu có."
    res = call_gemini_analysis(prompt, image=img, custom_api_key=custom_api_key)
    return res
