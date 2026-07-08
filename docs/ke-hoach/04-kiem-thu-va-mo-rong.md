# 4. Kiểm Thử và Mở Rộng (Testing & Scaling)

## 4.1. Test Model Level (Kiểm thử mức độ Mô hình AI)
- Đưa 10 bài báo chính thống từ VnExpress (có kiểm chứng): Model phải trả về dưới 30% tin giả.
- Đưa 10 tin đồn thất thiệt từ Facebook: Model phải đọc được bằng chứng từ DuckDuckGo và đẩy tỷ lệ lên trên 70%.
- Cung cấp ảnh do Midjourney/AI tạo: Model Vision phải phát hiện ra bất thường cấu trúc ánh sáng/pixel.

## 4.2. Test Full Pipeline (Kiểm thử luồng hệ thống End-to-End)
- Dán URL -> UI có hiện loading không? -> Scraper có lấy được chữ không? -> AI có trả về JSON không? -> Giao diện có render phần trăm hiển thị chuẩn màu (Đỏ/Vàng/Xanh) không?
- Lịch sử quét có được lưu vào Sidebar không?
- Giả lập ngắt kết nối Internet: Ứng dụng không được sập hoàn toàn (Crash) mà phải báo lỗi bằng giao diện thông báo của Streamlit.
- Bấm liên tục (Spam) để dính lỗi 429 Rate Limit: Ứng dụng phải hiện bảng chờ 20s (Auto-Retry) thay vì Crash mã đỏ.

## 4.3. Kế Hoạch Mở Rộng
- **Database:** Tích hợp PostgreSQL/MongoDB thay thế cho Session State để lưu lịch sử quét lâu dài.
- **User Auth:** Tích hợp đăng nhập để giới hạn Rate Limit theo User thay vì chia sẻ chung 1 API Key.
