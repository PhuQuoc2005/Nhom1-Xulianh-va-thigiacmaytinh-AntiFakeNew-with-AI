import torch
import torch.nn as nn
import torch.nn.functional as F

class ELACNN(nn.Module):
    """
    Mạng Nê-ron Tích chập (CNN) được nâng cấp chống 'Dying ReLU'.
    Sử dụng BatchNorm để ổn định phân phối, LeakyReLU tránh sập nơ-ron,
    và Dropout để giảm thiểu Overfitting trên tập dữ liệu nhỏ.
    """
    def __init__(self):
        super(ELACNN, self).__init__()
        # Lớp Convolution 1
        self.conv1 = nn.Conv2d(3, 32, kernel_size=5, padding=2)
        self.bn1 = nn.BatchNorm2d(32)
        self.pool1 = nn.MaxPool2d(2, 2)
        
        # Lớp Convolution 2
        self.conv2 = nn.Conv2d(32, 64, kernel_size=5, padding=2)
        self.bn2 = nn.BatchNorm2d(64)
        self.pool2 = nn.MaxPool2d(2, 2)
        
        # Lớp Convolution 3
        self.conv3 = nn.Conv2d(64, 128, kernel_size=5, padding=2)
        self.bn3 = nn.BatchNorm2d(128)
        self.pool3 = nn.MaxPool2d(2, 2)
        
        # Lớp Dropout chống Overfitting
        self.dropout = nn.Dropout(0.5)
        
        # Lớp kết nối (Fully Connected)
        self.fc1 = nn.Linear(128 * 16 * 16, 256)
        self.fc2 = nn.Linear(256, 2)
        
        # Hàm kích hoạt LeakyReLU
        self.leaky_relu = nn.LeakyReLU(0.1)
        
    def forward(self, x):
        x = self.pool1(self.leaky_relu(self.bn1(self.conv1(x))))
        x = self.pool2(self.leaky_relu(self.bn2(self.conv2(x))))
        x = self.pool3(self.leaky_relu(self.bn3(self.conv3(x))))
        
        x = x.view(-1, 128 * 16 * 16) # Duỗi phẳng (Flatten) ma trận
        x = self.dropout(x) # Rơi rụng ngẫu nhiên 50% nơ-ron
        x = self.leaky_relu(self.fc1(x))
        x = self.fc2(x)
        return x

def predict_ela(ela_img_pil):
    """
    Sử dụng ELA CNN đã train để dự đoán.
    Trả về xác suất % là ảnh Fake (bị cắt ghép).
    """
    import os
    from torchvision import transforms
    
    model_path = os.path.join(os.path.dirname(__file__), "weights", "ela_cnn.pth")
    if not os.path.exists(model_path):
        return None

    model = ELACNN()
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu'), weights_only=True))
    model.eval()

    transform = transforms.Compose([
        transforms.Resize((128, 128)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
    ])

    input_tensor = transform(ela_img_pil).unsqueeze(0)
    with torch.no_grad():
        output = model(input_tensor)
        probs = torch.nn.functional.softmax(output, dim=1)
        fake_prob = probs[0][1].item() * 100
    
    return round(fake_prob, 2)
