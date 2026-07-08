# 2. Chi Tiết Nhiệm Vụ (Task Assignment)

Dự án có 6 module lõi, chia đều cho 6 thành viên trong nhóm:

### 🧑‍💻 Thành viên 1: `app/streamlit_app.py` (Điều phối & State)
- Chịu trách nhiệm viết luồng chạy chính, quản lý `st.session_state` (ví dụ: Lịch sử quét).
- Ráp nối các hàm từ thư mục `src/` vào luồng sự kiện của nút bấm.

### 🎨 Thành viên 2: `app/ui_components.py` (UI/UX)
- Chịu trách nhiệm viết HTML/CSS nội suy.
- Thiết kế các Dialog, Popup, Sidebar, Animation, đảm bảo giao diện đạt chuẩn Premium.

### 🧠 Thành viên 3: `src/inference/ai_engine.py` (AI Logic)
- Xây dựng Prompt cho LLM.
- Xử lý các mã lỗi của API (429 Rate Limit, Auto-Retry).
- Khởi tạo và thiết lập các Model AI (ví dụ: Gemini 2.5 Flash).

### 🕷️ Thành viên 4: `src/text/web_scraper.py` (Scraping)
- Viết thuật toán chui vào các trang báo mạng để bóc tách thẻ HTML.
- Tối ưu Parser (dùng lxml), xử lý timeout và Fake User-Agent.

### 🔍 Thành viên 5: `src/text/search_engine.py` (Fact Check Engine)
- Tích hợp DuckDuckGo API để tìm kiếm sự thật.
- Rút trích (Extract) những đoạn text có giá trị (body) từ công cụ tìm kiếm đưa vào RAG.

### 🖼️ Thành viên 6: `src/image/image_processor.py` (Computer Vision)
- Xử lý mảng byte ảnh đầu vào từ Streamlit (PIL Image).
- Gửi dữ liệu ảnh lên Vision Model để quét deepfake/photoshop.
