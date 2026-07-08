# 1. Tổng Quan Dự Án (Project Overview)

## 1.1. User's requirement (Yêu cầu người dùng)
- Xây dựng một ứng dụng web có giao diện to, rõ, đẹp mắt (Premium UI) bằng phong cách Dark Mode/Glassmorphism.
- Cho phép người dùng nhập Văn bản, dán Link (URL) bài báo hoặc tải hình ảnh lên để kiểm tra.
- Tự động trích xuất nội dung từ URL.
- Ứng dụng AI để phân tích sự thật, đưa ra phần trăm tin giả và lý do chi tiết.
- Kiến trúc phải được chia nhỏ để 6 lập trình viên có thể làm việc song song không bị xung đột (conflict).

## 1.2. Tìm features (Các tính năng cốt lõi)
1. **Web Scraping:** Tự động truy xuất và bóc tách nội dung HTML từ URL.
2. **Cross-checking (Fact-check):** Tự động tìm kiếm chéo thông tin trên mạng Internet qua DuckDuckGo để lấy bằng chứng.
3. **AI Text Analysis:** Ứng dụng LLM phân tích văn bản kết hợp bằng chứng từ DuckDuckGo để suy luận logic, đưa ra lý do và phân tích cảm xúc (Sentiment).
4. **AI Vision Analysis:** Ứng dụng Computer Vision (Gemini 2.5) để nhận diện cấu trúc điểm ảnh, độ rọi, ánh sáng của hình ảnh phát hiện manipulation.
5. **Unified Dashboard UI & History:** Giao diện Streamlit hợp nhất một luồng, tự động nhận diện loại dữ liệu nhập vào (Text/URL/Image), lưu trữ lịch sử quét cục bộ và cho phép chỉnh sửa API Key động.

## 1.3. Scope, Out of scope, Edge cases
**Scope (Phạm vi dự án):**
- Phát hiện tin giả dựa trên suy luận logic ngôn ngữ và dữ liệu đối chiếu trên web.
- Hỗ trợ tiếng Việt và các ngôn ngữ phổ biến.
- Hỗ trợ ảnh tĩnh (JPG, PNG, WEBP).

**Out of scope (Ngoài phạm vi):**
- Phân tích Video (Deepfake Video) chưa được hỗ trợ trong phiên bản này.
- Phân tích các URL yêu cầu đăng nhập (Paywall, Mạng xã hội private).
- Khả năng xử lý hơn 1000 request/phút (do giới hạn API rate limit của bản miễn phí).

**Edge cases (Trường hợp ngoại lệ xử lý):**
- **URL hỏng hoặc không có quyền truy cập:** Hệ thống tự động báo lỗi kết nối và chuyển sang phân tích trên chuỗi URL tĩnh.
- **LLM bị nghẽn (API Timeout/Rate Limit 429):** Hệ thống có cơ chế Auto-Retry tự động chờ 20 giây, nếu kiệt quệ sẽ thông báo thân thiện trên giao diện UI để người dùng đổi Key.
- **Ảnh không chứa metadata:** AI Vision chuyển sang soi mức điểm ảnh (pixel level) thay vì metadata.
