import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
import joblib
import os

def main():
    print("Bat dau qua trinh Huan luyen (Training) Mo hinh Hoc May cho Van ban...")
    print("Thuat toan: TF-IDF + Random Forest (Rung ngau nhien)")
    
    csv_path = os.path.join("data", "text", "vn_fake_news_dataset.csv")
    if not os.path.exists(csv_path):
        print(f"❌ LỖI: Không tìm thấy file {csv_path}")
        return
        
    # 1. Đọc dữ liệu
    df = pd.read_csv(csv_path)
    print(f"Da tai thanh cong {len(df)} bai bao (tin tuc).")
    
    X = df['text']
    y = df['label'] # 0: Thật, 1: Giả
    
    # 2. Chia tập Train/Test (80% để học, 20% để thi thử)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 3. Tạo Pipeline (Ống dẫn: Từ văn bản -> Ma trận TF-IDF -> Rừng ngẫu nhiên)
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=5000, ngram_range=(1, 2))),
        ('rf', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    
    print("Dang huan luyen mo hinh (Qua trinh nay cuc ky nhanh tren CPU)...")
    pipeline.fit(X_train, y_train)
    
    # 4. Đánh giá chấm điểm học sinh (AI)
    acc = pipeline.score(X_test, y_test)
    print(f"Hoan tat! Do chinh xac tren tap kiem tra (Accuracy): {acc * 100:.2f}%")
    
    # 5. Lưu bộ não AI
    weights_dir = os.path.join("src", "models", "weights")
    os.makedirs(weights_dir, exist_ok=True)
    
    save_path = os.path.join(weights_dir, "text_ml.pkl")
    joblib.dump(pipeline, save_path)
    
    print(f"Da luu bo nao AI (Machine Learning) tai: {save_path}")
    print("Bay gio ban co the len giao dien Web de thu nghiem quet tin tuc bang thuat toan tu che nay!")

if __name__ == "__main__":
    main()
