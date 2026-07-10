# Nhóm 1 - Đồ án Xử lý ảnh và Thị giác máy tính: Trợ lý AI Chống Tin Giả (Anti Fake News with AI)

Dự án này là một hệ thống AI đa phương thức giúp nhận diện tin giả (Fake News) và hình ảnh bị cắt ghép (Image Forgery). Tài liệu dưới đây mô tả toàn bộ vòng đời phát triển phần mềm (SDLC) của dự án từ khâu khảo sát yêu cầu đến khi kiểm thử toàn diện.

---

## 1. User's Requirement (Yêu cầu người dùng)
Trong thời đại bùng nổ mạng xã hội, người dùng liên tục tiếp xúc với các luồng thông tin và hình ảnh được lan truyền với tốc độ chóng mặt. 
**Vấn đề:** 
- Người dùng không có khả năng phân biệt tin tức thật/giả được cắt ghép tinh vi.
- Hình ảnh bị chỉnh sửa (Photoshop) để thay đổi ngữ cảnh hoặc ngụy tạo bằng chứng giả.
- Cần một công cụ "All-in-one" dễ sử dụng, tải ảnh hoặc copy văn bản vào là nhận ngay kết quả phân tích có cơ sở.

## 2. Tìm Features (Xác định các tính năng cốt lõi)
Từ bài toán trên, hệ thống cần các tính năng sau:
- **Phân tích Văn bản (Text NLP):** Đánh giá tính giật gân, độ tin cậy của đoạn văn bản tin tức.
- **Phân tích Hình ảnh Cắt ghép (Image Forgery Detection):** Phát hiện các vùng ảnh bị can thiệp kỹ thuật số bằng thuật toán ELA (Error Level Analysis).
- **Trích xuất văn bản từ ảnh (OCR):** Nếu người dùng tải lên một ảnh chụp màn hình bài báo, hệ thống phải tự động đọc chữ trong ảnh để phân tích nội dung.
- **Trí tuệ nhân tạo tạo sinh (GenAI Integration):** Đóng vai trò chuyên gia tổng hợp, đưa ra kết luận cuối cùng (bằng % Fake) và giải thích lý do bằng ngôn ngữ tự nhiên.

## 3. Scope, Out of Scope & Edge Cases

### In Scope (Trong phạm vi dự án)
- Hỗ trợ văn bản tiếng Việt.
- Xử lý định dạng ảnh phổ biến (JPG, PNG).
- Phát hiện cắt ghép ảnh kỹ thuật số (Splicing, Copy-Move) trên nền ảnh nén JPEG.
- Giao diện Web tương tác trực quan (Streamlit).

### Out of Scope (Ngoài phạm vi)
- Xử lý Video (Deepfake video) và Âm thanh giả mạo (Voice cloning).
- Cào dữ liệu theo thời gian thực (Real-time Live Scraping) từ toàn bộ mạng Internet.
- Phân tích hàng loạt (Batch processing) hàng ngàn file cùng lúc.

### Edge Cases (Các trường hợp ngoại lệ/Rủi ro)
- **Nén ảnh nhiều lần (Social Media Compression):** Ảnh tải về từ Facebook/Zalo bị nén mạnh làm mất dấu vết ELA. (Giải pháp: Huấn luyện mô hình với ảnh đã mô phỏng nén).
- **Rate Limit API:** API của AI (Gemini) bị giới hạn số lần gọi. (Giải pháp: Chuyển đổi Model sang phiên bản có Quota cao hơn, tích hợp cơ chế Fallback Heuristic).
- **Văn bản châm biếm (Sarcasm):** AI có thể hiểu lầm các bài báo mang tính trào phúng là tin giả giật gân.

## 4. Tech Solution (Giải pháp công nghệ)
- **Frontend / UI:** [Streamlit](https://streamlit.io/) (Python) - Cho phép xây dựng Web App nhanh chóng và trực quan.
- **Backend Core:** Python 3.13.
- **Computer Vision:** OpenCV (`cv2`), Pillow (`PIL`).
- **Deep Learning Framework:** PyTorch (Sử dụng cho mô hình Mạng nơ-ron chập CNN).
- **NLP / OCR:** Pytesseract (Optical Character Recognition), Scikit-Learn.
- **LLM API:** Google Generative AI (`gemini-3.1-flash-lite`).

## 5. Logic và AI Solution (Kiến trúc & Giải pháp AI)

### A. System Logic Pipeline (Luồng xử lý)
1. **Input:** Nhận Image hoặc Text từ người dùng qua Web UI.
2. **Routing:**
   - Nếu là Image: Gọi `Image Processor` -> Tính toán ELA -> Nếu có chữ, chạy OCR.
   - Nếu là Text: Đưa thẳng vào `NLP Processor`.
3. **Core Analysis:** Gọi các Model Học máy (CNN cho ảnh, ML cho văn bản) để lấy điểm kỹ thuật số (Technical Score).
4. **AI Synthesis:** Đóng gói toàn bộ *Technical Score*, *Văn bản*, *Bản đồ ELA* gửi qua API cho bộ não **Gemini**.
5. **Output:** Trả về JSON chứa `% Fake Probability`, `Reasons` (Giải thích chi tiết) và hiển thị lên UI.

### B. AI Solution
- **Image ELA CNN:** Sử dụng mạng nơ-ron chập (CNN) được thiết kế riêng để học các bất thường ở mức điểm ảnh (Pixel compression artifacts) sinh ra từ quá trình lưu ảnh JPEG nhiều lần tại các vùng bị PTS.
- **GenAI / LLM:** Sử dụng `Gemini 3.1 Flash Lite` làm "Bộ não ra quyết định". Khai thác khả năng Multimodal (Đa phương thức) để kết hợp đánh giá văn bản và thị giác cùng lúc.

## 6. Plan (Kế hoạch Triển khai)
- **Phase 1 (Khung xương):** Xây dựng kho lưu trữ Git, thiết lập môi trường ảo (`venv`), thiết kế UI/UX trên Streamlit.
- **Phase 2 (Xử lý Ảnh):** Cài đặt thuật toán chuyển đổi ELA, thiết lập luồng OCR cơ bản.
- **Phase 3 (Train AI):** Cào dữ liệu báo chính thống, tự động hóa việc tạo Fake News (Data Augmentation), huấn luyện mô hình ELA-CNN và NLP.
- **Phase 4 (Tích hợp & Tinh chỉnh):** Nối API Gemini, xử lý lỗi Exception (API Key lỗi, Rate limit, đụng độ bộ nhớ khi đọc file).

## 7. Implement (Quá trình Thực thi thực tế)
Quá trình thực thi dự án gặp nhiều thách thức và đã được giải quyết bằng các kỹ thuật sau:
- **Data Augmentation NLP:** Áp dụng phương án tự động đọc tin Thật (từ VnExpress), dùng LLM tự bóp méo, thêm từ ngữ giật gân để đẻ ra tin Giả tương ứng -> Tạo bộ Dataset chất lượng.
- **Data Augmentation Image:** Code hàm random JPEG Compression (Quality 30-60) ngay trong quá trình train ELA CNN để AI "quen" với việc đọc ảnh chất lượng thấp.
- **Lỗi File Handle & Encoding:** Sửa lỗi `UnicodeEncodeError` khi in log tiếng Việt trên Windows và lỗi khóa file tạm `PermissionError` bằng cú pháp Context Manager `with`.
- **Chuyển đổi Mô hình AI động:** Xây dựng cơ chế đổi Model linh hoạt (`ai_engine.py`) để đối phó với Google API Rate Limits (Chuyển đổi giữa Gemini 2.5 Flash và 3.1 Flash Lite).

## 8. Test (Kiểm thử toàn diện)

### A. Test Model Level (Kiểm thử cấp độ Mô hình)
- **ELA CNN Training:** Mô hình được huấn luyện qua 30 Epochs.
  - *Kết quả cuối:* Loss hội tụ ở mức thấp (~0.24), **Accuracy đạt 90.61%**. Mô hình nhận diện rất tốt các bức ảnh cắt ghép tinh vi ngay cả khi bị nén.
- **NLP Model:** Đạt độ bao phủ tốt nhờ bộ dữ liệu Augmentation sát với văn phong báo chí Việt Nam.

### B. Test Full Pipeline (Kiểm thử End-to-End)
- **Khả năng chống chịu lỗi (Fault Tolerance):**
  - Cố tình nhập API Key sai hoặc đợi khi Google Rate Limit -> Hệ thống không bị crash (Sập) mà tự động nhảy sang hàm `fallback_heuristic_scan`, quét thủ công bằng từ khóa và báo lỗi lịch sự ra giao diện.
- **Luồng Upload Ảnh:**
  - Tải một bức ảnh chế (Meme/Fake news facebook) lên hệ thống -> Nhánh ELA chạy mượt mà -> Nhánh OCR tự bóc tách chữ trong ảnh -> Chuyển giao toàn bộ cho AI phân tích -> Kết xuất ra tỷ lệ Fake chính xác cùng lý do cảnh báo rõ ràng.
- **Tối ưu hóa UX:** Code được clean, loại bỏ các Warning của Streamlit (`use_container_width` deprecated, thiếu `label`), đảm bảo Web App chạy "Sạch" trên Console.

---
*Dự án hoàn thiện sẵn sàng cho nghiệm thu & báo cáo đồ án.*
