import pytesseract
from PIL import Image
import os

# Cấu hình đường dẫn Tesseract (Tùy biến cho Windows)
tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
if os.path.exists(tesseract_cmd):
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

def extract_text_from_image(image_bytes):
    """
    Sử dụng Tesseract OCR để trích xuất văn bản từ hình ảnh ở chế độ Ngoại tuyến.
    """
    try:
        img = Image.open(image_bytes)
        
        # Tiền xử lý ảnh để OCR đọc tốt hơn (Đặc biệt là ảnh chụp màn hình)
        from PIL import ImageEnhance, ImageOps
        
        # 1. Phóng to ảnh lên 3 lần (Upscale) để chữ không bị vỡ hạt
        new_size = (img.width * 3, img.height * 3)
        img_resized = img.resize(new_size, Image.Resampling.LANCZOS)
        
        # 2. Chuyển sang ảnh xám
        gray_img = img_resized.convert('L')
        
        # 3. Tăng độ tương phản lên gấp 2 lần
        enhancer = ImageEnhance.Contrast(gray_img)
        contrast_img = enhancer.enhance(2.0)
        
        # Ép đường dẫn tessdata qua biến môi trường để tránh lỗi nhận diện thư mục trên Windows
        os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR\tessdata'
        
        # Sử dụng ngôn ngữ tiếng Việt (vie)
        text = pytesseract.image_to_string(contrast_img, lang='vie')
        return text.strip()
    except Exception as e:
        # Tránh lỗi UnicodeEncodeError trên console Windows cp1252
        error_msg = str(e).encode('ascii', 'ignore').decode('ascii')
        print(f"OCR Error: {error_msg}")
        return f"ERROR: {str(e)}"
