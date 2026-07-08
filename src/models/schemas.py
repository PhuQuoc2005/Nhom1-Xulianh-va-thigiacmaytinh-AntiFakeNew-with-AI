from dataclasses import dataclass
from typing import List

@dataclass
class AIAnalysisResult:
    """
    Cấu trúc dữ liệu chuẩn (Data Schema) định nghĩa kết quả trả về từ Gemini.
    Giúp các thành viên làm UI và làm AI thống nhất được các trường dữ liệu (fields), 
    tránh việc gọi sai key của dictionary.
    """
    fake_probability: int
    reasons: List[str]
    sentiment_score: float

    def is_highly_fake(self) -> bool:
        """Kiểm tra nhanh xem tin này có rủi ro giả mạo cao không (>70%)"""
        return self.fake_probability > 70
        
    def is_reliable(self) -> bool:
        """Kiểm tra nhanh xem tin này có đáng tin cậy không (<40%)"""
        return self.fake_probability < 40
