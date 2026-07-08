# 1. Nguyên Tắc và Cấu Trúc (Principles & Architecture)

## 1.1. Feature-based Architecture
Thay vì nhồi nhét tất cả vào một file `app.py` khổng lồ, toàn bộ dự án đã được đập đi xây lại thành mô hình Modular phân cấp sâu:
- `app/`: Chứa thuần tuý UI (Streamlit Components, CSS).
- `src/`: Chứa lõi Logic xử lý (AI, Image, Text).
- `data/` & `docs/`: Chứa dữ liệu và tài liệu độc lập.

## 1.2. Nguyên tắc Code chung cho 6 thành viên
1. **Không code đè (No Override):** Mỗi người làm việc trong thư mục/file của mình.
2. **Kế thừa & Import:** Khi cần dữ liệu từ module khác, gọi hàm thông qua `import src.xxx`, tuyệt đối không copy-paste lại code.
3. **Luôn bắt lỗi (Try-Catch):** Mọi hàm API, Request qua mạng đều phải có Try-Catch để không làm hỏng giao diện tổng của Streamlit.
