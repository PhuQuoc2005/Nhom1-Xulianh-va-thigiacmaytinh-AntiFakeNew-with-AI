# 3. Triển Khai (Deployment)

## 3.1. Cài đặt Môi trường
- Đảm bảo bạn đang ở thư mục gốc của dự án `fake-news-detector`.
- Chạy lệnh cài đặt môi trường ảo:
  ```bash
  python -m venv venv
  .\venv\Scripts\pip install -r requirements.txt
  ```

## 3.2. Cấu hình
- File `.streamlit/config.toml` đã được cấu hình sẵn Dark Mode mặc định, không cần sửa đổi.
- API Key được gắn mặc định trong code, nhưng người dùng có thể linh hoạt điền Key riêng ở giao diện Sidebar.

## 3.3. Khởi chạy Ứng dụng
Chỉ cần chạy duy nhất script khởi động ở thư mục gốc:
```bash
python run_app.py
```
Script này sẽ tự động nạp PYTHONPATH và kích hoạt máy chủ Streamlit trên cổng `8501`.
