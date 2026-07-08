import os
import subprocess
import sys

def main():
    print("Dang khoi dong AI Fake News Detector...")
    
    # Thiết lập PYTHONPATH tự động chĩa về thư mục gốc
    root_dir = os.path.dirname(os.path.abspath(__file__))
    os.environ["PYTHONPATH"] = root_dir
    
    # Đường dẫn tới tệp khởi động của giao diện
    app_path = os.path.join(root_dir, "app", "streamlit_app.py")
    
    # Chạy Streamlit
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", app_path])
    except KeyboardInterrupt:
        print("\n🛑 Đã tắt máy chủ.")

if __name__ == "__main__":
    main()
