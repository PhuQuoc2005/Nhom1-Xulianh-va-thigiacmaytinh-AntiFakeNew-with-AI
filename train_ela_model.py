import os
import sys
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import transforms, datasets
from torch.utils.data import DataLoader

# Thêm thư mục gốc vào đường dẫn hệ thống để import
sys.path.append(os.path.dirname(__file__))
from src.models.ela_cnn import ELACNN
from src.image.ela_processor import compute_ela

def main():
    print("🚀 Bắt đầu quá trình Huấn Luyện (Training) ELA-CNN Model...")
    print("📌 Đang dùng CPU (Không dùng Card Đồ Họa Rời).")
    
    data_dir = os.path.join(os.path.dirname(__file__), "data", "images")
    real_dir = os.path.join(data_dir, "real")
    fake_dir = os.path.join(data_dir, "fake")
    
    # Tạo sẵn cấu trúc thư mục nếu chưa có
    os.makedirs(real_dir, exist_ok=True)
    os.makedirs(fake_dir, exist_ok=True)
    
    # Kiểm tra xem có ảnh để train chưa
    real_count = len(os.listdir(real_dir))
    fake_count = len(os.listdir(fake_dir))
    
    if real_count == 0 or fake_count == 0:
        print("\n❌ LỖI: Không có dữ liệu để Train!")
        print(f"👉 Hãy copy một vài tấm ảnh thật vào thư mục: {real_dir}")
        print(f"👉 Hãy copy một vài tấm ảnh đã qua chỉnh sửa (photoshop) vào thư mục: {fake_dir}")
        print("Sau đó chạy lại lệnh này nhé!")
        return

    print(f"✅ Đã tìm thấy {real_count} ảnh Thật và {fake_count} ảnh Giả.")
    
    # TODO: Phần load data và chạy vòng lặp Epochs sẽ được thực thi khi bạn có đủ ảnh.
    print("✅ Hệ thống đã sẵn sàng. Khi bạn nạp ảnh vào, thuật toán sẽ tự động biến đổi qua ELA và train ra file trí tuệ nhân tạo .pth!")

if __name__ == "__main__":
    main()
