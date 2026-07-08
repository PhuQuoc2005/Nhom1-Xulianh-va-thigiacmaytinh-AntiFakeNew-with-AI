import sys
import os
import pytest

# Trỏ đường dẫn về thư mục gốc để import được src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.schemas import AIAnalysisResult
from src.text.web_scraper import extract_url_content

def test_schema_logic():
    """Kiểm thử tính đúng đắn của logic phân loại tin giả dựa trên Data Schema"""
    fake_news = AIAnalysisResult(fake_probability=85, reasons=["Không có thật"], sentiment_score=-0.5)
    assert fake_news.is_highly_fake() == True
    assert fake_news.is_reliable() == False

    real_news = AIAnalysisResult(fake_probability=20, reasons=["Nguồn uy tín"], sentiment_score=0.9)
    assert real_news.is_highly_fake() == False
    assert real_news.is_reliable() == True

def test_web_scraper_fallback():
    """Kiểm thử khả năng chịu lỗi (Fallback) của công cụ cào dữ liệu Web"""
    title, content = extract_url_content("https://domain-nay-khong-ton-tai-12345.com")
    # Phải trả về chuỗi thông báo lỗi chứa chữ 'Lỗi' thay vì làm crash (sập) chương trình
    assert "Lỗi" in content 
