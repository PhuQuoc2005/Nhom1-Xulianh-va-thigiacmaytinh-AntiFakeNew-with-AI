import os
import pickle

# Tải trước bộ nhớ vào RAM để tăng tốc độ phân tích
vectorizer = None
nlp_model = None

save_dir = 'src/models/weights'
vectorizer_path = os.path.join(save_dir, 'text_vectorizer.pkl')
model_path = os.path.join(save_dir, 'text_nlp_model.pkl')

if os.path.exists(vectorizer_path) and os.path.exists(model_path):
    with open(vectorizer_path, 'rb') as f:
        vectorizer = pickle.load(f)
    with open(model_path, 'rb') as f:
        nlp_model = pickle.load(f)

def predict_text_fake_news(text):
    """
    Sử dụng mô hình AI NLP Ngoại tuyến để dự đoán xác suất tin giả.
    Đầu vào: Câu văn bản (Text).
    Đầu ra: Xác suất % là Tin giả (Float).
    """
    if not text or len(text.strip()) < 5:
        return 0.0 # Nếu văn bản quá ngắn, mặc định an toàn

    if vectorizer is None or nlp_model is None:
        print("Cảnh báo: Chưa tải được mô hình NLP. Vui lòng chạy train_text_nlp.py trước.")
        return 50.0

    try:
        # 1. Chuyển đổi text sang vector
        X_input = vectorizer.transform([text])
        
        # 2. Phân loại bằng Logistic Regression
        probs = nlp_model.predict_proba(X_input)[0]
        
        # 3. Lấy xác suất của class 1 (Tin giả)
        fake_prob = probs[1] * 100.0
        return round(fake_prob, 2)
    except Exception as e:
        print(f"Lỗi phân tích NLP Ngoại tuyến: {e}")
        return 50.0
