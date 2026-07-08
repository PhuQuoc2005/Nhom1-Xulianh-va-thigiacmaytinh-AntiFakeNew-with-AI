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
from PIL import Image

class ELADataset(torch.utils.data.Dataset):
    def __init__(self, image_paths, labels, transform=None):
        self.image_paths = image_paths
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        img_path = self.image_paths[idx]
        # Chạy thuật toán ELA ngay trong lúc đọc data
        ela_img = compute_ela(img_path)
        if ela_img is None:
            # Nếu lỗi, fallback về ảnh đen
            ela_img = Image.new('RGB', (128, 128), color='black')
        
        if self.transform:
            ela_img = self.transform(ela_img)
            
        label = self.labels[idx]
        return ela_img, label

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

    # Thu thập đường dẫn ảnh
    image_paths = []
    labels = []
    
    for filename in os.listdir(real_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_paths.append(os.path.join(real_dir, filename))
            labels.append(0) # 0 = Thật
            
    for filename in os.listdir(fake_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_paths.append(os.path.join(fake_dir, filename))
            labels.append(1) # 1 = Giả

    print(f"✅ Đã tải xong danh sách: {len(image_paths)} tấm ảnh.")
    
    # Tiền xử lý ảnh (Resize về 128x128 và biến thành Tensor)
    transform = transforms.Compose([
        transforms.Resize((128, 128)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
    ])
    
    dataset = ELADataset(image_paths, labels, transform=transform)
    dataloader = DataLoader(dataset, batch_size=8, shuffle=True) # Batch size nhỏ cho CPU
    
    # Khởi tạo Mô hình
    model = ELACNN()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    epochs = 30 # Tăng từ 5 lên 30 để AI cày cuốc cho đến khi thuộc lòng 200 ảnh
    print("🚀 Bắt đầu chạy Vòng lặp Học Máy (Epochs)...")
    for epoch in range(epochs):
        running_loss = 0.0
        correct = 0
        total = 0
        
        for i, data in enumerate(dataloader, 0):
            inputs, batch_labels = data
            
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, batch_labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += batch_labels.size(0)
            correct += (predicted == batch_labels).sum().item()
            
            print(f"\rEpoch [{epoch+1}/{epochs}] - Batch [{i+1}/{len(dataloader)}] - Loss: {loss.item():.4f}", end="")
            
        epoch_acc = 100 * correct / total
        print(f"\n✅ Hoàn tất Epoch {epoch+1} | Độ chính xác (Accuracy): {epoch_acc:.2f}% | Loss trung bình: {running_loss/len(dataloader):.4f}")
        
    # Lưu trí tuệ nhân tạo
    os.makedirs(os.path.join(os.path.dirname(__file__), "src", "models", "weights"), exist_ok=True)
    save_path = os.path.join(os.path.dirname(__file__), "src", "models", "weights", "ela_cnn.pth")
    torch.save(model.state_dict(), save_path)
    print(f"\n🎉 QUÁ TRÌNH HUẤN LUYỆN THÀNH CÔNG! Đã lưu 'não' của AI tại: {save_path}")

if __name__ == "__main__":
    main()
