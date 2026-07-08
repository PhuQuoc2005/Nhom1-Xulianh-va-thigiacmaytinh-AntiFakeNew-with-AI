from duckduckgo_search import DDGS
import streamlit as st

@st.cache_data(show_spinner=False, ttl=3600)
def search_cross_check(query):
    try:
        # Giảm max_results xuống 2 để giảm thiểu thời gian chờ API của DuckDuckGo
        results = DDGS().text(query, max_results=2)
        search_text = ""
        for r in results:
            search_text += f"- Nguồn: {r.get('href')}\n  Tiêu đề: {r.get('title')}\n  Trích dẫn: {r.get('body')}\n\n"
        return search_text
    except Exception as e:
        return f"Lỗi tìm kiếm: {str(e)}"
