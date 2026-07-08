import os
import urllib.request
import time

def download_images():
    print("🚀 Bắt đầu cào dữ liệu ảnh từ MKLab Dataset...")
    
    txt_file = os.path.join("data", "mklab_dataset", "set_images.txt")
    if not os.path.exists(txt_file):
        print(f"❌ LỖI: Không tìm thấy file {txt_file}. Đảm bảo bạn đã clone repo.")
        return
        
    real_dir = os.path.join("data", "images", "real")
    fake_dir = os.path.join("data", "images", "fake")
    os.makedirs(real_dir, exist_ok=True)
    os.makedirs(fake_dir, exist_ok=True)
    
    # Đọc file set_images.txt
    with open(txt_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    real_count = 0
    fake_count = 0
    max_per_class = 20 # Tải 20 ảnh mỗi loại để Demo cho nhanh (do nhiều link từ 2015 đã chết)
    
    # Bỏ qua dòng header đầu tiên
    for line in lines[1:]:
        if real_count >= max_per_class and fake_count >= max_per_class:
            break
            
        parts = line.strip().split('\t')
        if len(parts) >= 3:
            img_id = parts[0]
            url = parts[1]
            label = parts[2] # 'real' hoặc 'fake'
            
            if label == 'real' and real_count < max_per_class:
                target_dir = real_dir
            elif label == 'fake' and fake_count < max_per_class:
                target_dir = fake_dir
            else:
                continue
                
            file_path = os.path.join(target_dir, f"{img_id}.jpg")
            if os.path.exists(file_path):
                if label == 'real': real_count += 1
                else: fake_count += 1
                continue
                
            # Thử tải ảnh (Bỏ qua lỗi 404/403 do web cũ)
            try:
                # Giả lập trình duyệt để tránh bị block
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=5) as response:
                    with open(file_path, 'wb') as out_file:
                        out_file.write(response.read())
                
                print(f"✅ Đã tải: {img_id}.jpg vào thư mục {label}")
                if label == 'real': real_count += 1
                else: fake_count += 1
                
                time.sleep(0.5) # Tránh bị chặn IP
            except Exception as e:
                # Link chết thì bỏ qua
                print(f"❌ Link hỏng ({img_id}): {url}")
                pass
                
    print(f"\n🎉 HOÀN TẤT! Tải được {real_count} ảnh THẬT và {fake_count} ảnh GIẢ.")
    
    # Nếu ít quá (do web chết hết), copy bừa ảnh hoa để mô hình không bị crash khi train
    if real_count < 2 or fake_count < 2:
        print("⚠️ Cảnh báo: Tải được quá ít ảnh (Các link MKLab 2015 đa số đã die). Đang dùng ảnh Dummy (hoa) để chữa cháy.")
        from PIL import Image, ImageDraw
        dummy_path = r'venv\Lib\site-packages\sklearn\datasets\images\flower.jpg'
        if os.path.exists(dummy_path):
            img = Image.open(dummy_path).convert('RGB')
            for i in range(5):
                img.save(os.path.join(real_dir, f"dummy_real_{i}.jpg"), 'JPEG')
                
                # Tạo ảnh giả (vẽ hinh vuong)
                fake_img = img.copy()
                draw = ImageDraw.Draw(fake_img)
                draw.rectangle([100+i, 100+i, 200+i, 200+i], fill='black')
                fake_img.save(os.path.join(fake_dir, f"dummy_fake_{i}.jpg"), 'JPEG', quality=95)
            print("✅ Đã tạo 5 ảnh Thật/Giả bằng công nghệ chữa cháy.")

if __name__ == "__main__":
    download_images()
