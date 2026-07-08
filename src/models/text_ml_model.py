import os
import joblib

def predict_text(text, model_path=None):
    """
    Sử dụng mô hình Học máy truyền thống (TF-IDF + Random Forest) để phân tích văn bản.
    """
    if model_path is None:
        model_path = os.path.join(os.path.dirname(__file__), "weights", "text_ml.pkl")
        
    if not os.path.exists(model_path):
        return {
            "fake_probability": 50,
            "reasons": [
                "⚠️ CHƯA CÓ TRÍ TUỆ NHÂN TẠO!", 
                "Bạn chưa huấn luyện mô hình Học máy cho Văn bản.", 
                "👉 Vui lòng chạy file `python train_text_model.py` để hệ thống tự học từ file CSV (Dataset) trước nhé."
            ],
            "sentiment_score": 0.0
        }
        
    try:
        # Tải mô hình đã train
        pipeline = joblib.load(model_path)
        
        # Dự đoán
        # pipeline.predict_proba trả về mảng xác suất [Xác suất Thật(0), Xác suất Giả(1)]
        proba = pipeline.predict_proba([text])[0]
        fake_prob = int(proba[1] * 100)
        
        reasons = [
            f"Mô hình Học máy Cổ điển (TF-IDF + Random Forest) đã phân tích tần suất từ vựng.",
            f"Dựa trên dữ liệu đã học, hệ thống chấm {fake_prob}% khả năng đây là tin giả."
        ]
        
        # Thêm đánh giá sâu hơn
        if fake_prob > 70:
            reasons.append("Phát hiện nhiều cụm từ có đặc trưng giống hệt với các bài viết lừa đảo/giật gân trong Dataset.")
        elif fake_prob < 30:
            reasons.append("Hành văn mang văn phong báo chí chính thống, đáng tin cậy.")
            
        return {
            "fake_probability": fake_prob,
            "reasons": reasons,
            "sentiment_score": 0.0
        }
    except Exception as e:
        return {
            "fake_probability": 50,
            "reasons": [f"Lỗi khi dự đoán bằng mô hình Học máy: {str(e)}"],
            "sentiment_score": 0.0
        }
