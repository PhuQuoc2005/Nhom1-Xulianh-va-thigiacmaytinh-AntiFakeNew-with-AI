import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle
import os

def train_nlp_model():
    print("🚀 Bắt đầu huấn luyện bộ não ngôn ngữ AI (NLP)...")
    
    # 1. Đọc dữ liệu
    csv_path = 'data/text/vn_fake_news_dataset.csv'
    if not os.path.exists(csv_path):
        print(f"❌ Không tìm thấy file {csv_path}")
        return
        
    df = pd.read_csv(csv_path)
    # Loại bỏ các dòng bị lỗi null nếu có
    df = df.dropna(subset=['text', 'label'])
    
    texts = df['text'].astype(str).tolist()
    labels = df['label'].astype(int).tolist()
    
    print(f"✅ Đã tải {len(texts)} bài báo (Thật/Giả).")
    
    # 2. Tiền xử lý & Vector hóa ngôn ngữ (TF-IDF)
    # Chuyển đổi ngôn ngữ con người thành ma trận số học
    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
    X = vectorizer.fit_transform(texts)
    y = labels
    
    # Chia tập dữ liệu: 80% để học, 20% để thi thử
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 3. Huấn luyện mô hình Logistic Regression
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    
    # 4. Đánh giá (Thi thử)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"✅ Độ chính xác (Accuracy) của Mô hình NLP: {acc * 100:.2f}%")
    
    # 5. Lưu mô hình vào thư mục weights
    save_dir = 'src/models/weights'
    os.makedirs(save_dir, exist_ok=True)
    
    with open(os.path.join(save_dir, 'text_vectorizer.pkl'), 'wb') as f:
        pickle.dump(vectorizer, f)
        
    with open(os.path.join(save_dir, 'text_nlp_model.pkl'), 'wb') as f:
        pickle.dump(model, f)
        
    print(f"🎉 Huấn luyện thành công! Đã lưu não NLP tại: {save_dir}")

if __name__ == "__main__":
    train_nlp_model()
