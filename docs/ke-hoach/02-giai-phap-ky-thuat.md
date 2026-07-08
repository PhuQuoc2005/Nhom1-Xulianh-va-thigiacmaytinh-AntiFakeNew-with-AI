# 2. Giải Pháp Kỹ Thuật (Tech Solution)

## 2.1. Công nghệ sử dụng
- **Framework UI:** `Streamlit` (Python).
- **Ngôn ngữ:** `Python 3.10+`.
- **Thư viện Web Scraping:** `requests`, `BeautifulSoup4` (sử dụng `lxml` parser siêu tốc).
- **Thư viện Tìm kiếm:** `duckduckgo_search`.
- **Thư viện Xử lý ảnh:** `Pillow`.
- **Kiến trúc:** Feature-based Modular Architecture (Tách bạch UI, AI, Scraping, Search, Image).

## 2.2. Giải pháp Trí tuệ nhân tạo (AI Solution)
- **Mô hình cốt lõi:** Dùng `Gemini 2.5 Flash` qua SDK `google-generativeai`.
- **Tối ưu tốc độ (Performance):** Bật chế độ `Native JSON Mode` của Gemini để ép model trả về JSON tinh khiết, cắt giảm hàng triệu thao tác xử lý chuỗi so với Markdown.
- **Logic xử lý chữ (Text/URL):**
  - Prompt Engineering yêu cầu trả về định dạng `JSON`.
  - Bơm kết quả từ Web Scraping và DuckDuckGo vào prompt (RAG - Retrieval-Augmented Generation) để cung cấp kiến thức nền (context) chuẩn xác theo thời gian thực cho LLM.
- **Logic xử lý ảnh (Vision):**
  - Đẩy trực tiếp bytes hình ảnh lên Gemini.
  - Sử dụng Multi-modal Prompt để soi dấu hiệu chỉnh sửa Photoshop/AI Generator.

## 2.3. Caching & Tối ưu luồng
- Ứng dụng tích cực `@st.cache_data` cho Web Scraping và DDG Search để lưu bộ nhớ đệm. Bất kỳ URL hay Text nào quét trùng lại sẽ được hoàn thành trong 0.1 giây.
