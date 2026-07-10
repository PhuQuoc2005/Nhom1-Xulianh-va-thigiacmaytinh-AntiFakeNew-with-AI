import os
from PIL import Image, ImageChops, ImageEnhance

def compute_ela(image_path_or_file, quality=90):
    """
    Tạo ảnh ELA (Error Level Analysis) từ ảnh gốc.
    Nhận diện vùng ảnh bị cắt ghép dựa trên độ nén JPEG.
    """
    try:
        original = Image.open(image_path_or_file).convert('RGB')
        
        # Lưu ảnh tạm với mức độ nén nhất định (Quality=90)
        temp_filename = "temp_ela_compression.jpg"
        original.save(temp_filename, 'JPEG', quality=quality)
        
        # Mở ảnh vừa nén
        with Image.open(temp_filename) as temp_img:
            compressed = temp_img.convert('RGB')
        
        # Tính toán độ chênh lệch (Error) giữa ảnh gốc và ảnh nén
        ela_image = ImageChops.difference(original, compressed)
        
        # Tăng cường độ sáng (Brightness) để mắt người dễ nhìn thấy vết ghép
        extrema = ela_image.getextrema()
        max_diff = max([ex[1] for ex in extrema])
        if max_diff == 0:
            max_diff = 1
        scale = 255.0 / max_diff
        
        ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)
        
        # Dọn dẹp file tạm
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
            
        return ela_image
    except Exception as e:
        print(f"Error processing ELA: {e}")
        return None
