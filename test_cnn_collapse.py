from src.models.ela_cnn import predict_ela
from PIL import Image
import numpy as np

# Tạo một ảnh RGB ngẫu nhiên
dummy_img = Image.fromarray(np.random.randint(0, 255, (128, 128, 3), dtype=np.uint8))
prob = predict_ela(dummy_img)
print(f"Dummy Image CNN Prob: {prob}")

# Tạo ảnh đen toàn tập
black_img = Image.new('RGB', (128, 128), color = 'black')
prob_black = predict_ela(black_img)
print(f"Black Image CNN Prob: {prob_black}")
