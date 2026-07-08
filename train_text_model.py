import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
import joblib
import os

def main():
    print("🚀 Bắt đầu quá trình Huấn Luyện (Training) Mô hình Học Máy cho Văn bản...")
    print("Thuật toán: TF-IDF + Random Forest (Rừng ngẫu nhiên)")
    
    csv_path = os.path.join("data", "text", "vn_fake_news_dataset.csv")
    if not os.path.exists(csv_path):
        print(f"❌ LỖI: Không tìm thấy file {csv_path}")
        return
        
    # 1. Đọc dữ liệu
    df = pd.read_csv(csv_path)
    print(f"✅ Đã tải thành công {len(df)} bài báo (tin tức).")
    
    X = df['text']
    y = df['label'] # 0: Thật, 1: Giả
    
    # 2. Chia tập Train/Test (80% để học, 20% để thi thử)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 3. Tạo Pipeline (Ống dẫn: Từ văn bản -> Ma trận TF-IDF -> Rừng ngẫu nhiên)
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=5000, ngram_range=(1, 2))),
        ('rf', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    
    print("⏳ Đang huấn luyện mô hình (Quá trình này cực kỳ nhanh trên CPU)...")
    pipeline.fit(X_train, y_train)
    
    # 4. Đánh giá chấm điểm học sinh (AI)
    acc = pipeline.score(X_test, y_test)
    print(f"✅ Hoàn tất! Độ chính xác trên tập kiểm tra ẩn (Accuracy): {acc * 100:.2f}%")
    
    # 5. Lưu bộ não AI
    weights_dir = os.path.join("src", "models", "weights")
    os.makedirs(weights_dir, exist_ok=True)
    
    save_path = os.path.join(weights_dir, "text_ml.pkl")
    joblib.dump(pipeline, save_path)
    
    print(f"🎉 Đã lưu bộ não AI (Machine Learning) tại: {save_path}")
    print("Bây giờ bạn có thể lên giao diện Web để thử nghiệm quét tin tức bằng thuật toán tự chế này!")

if __name__ == "__main__":
    main()
