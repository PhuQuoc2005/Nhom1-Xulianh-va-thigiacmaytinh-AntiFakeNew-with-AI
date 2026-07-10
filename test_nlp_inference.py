import os
from src.text.nlp_processor import predict_text_fake_news

text = "Cảnh báo khẩn cấp ! Vừa phát hiện đĩa bay người ngoài hành tinh đang đi dạo ở Hồ Gươm, Hà Nội. Mọi người tuyệt đối không ra đường. Hãy chia sẻ bài viết này để nhận ngay 500 triệu đồng vào tài khoản!"

prob = predict_text_fake_news(text)
print(f"NLP Probability for text: {prob}%")
