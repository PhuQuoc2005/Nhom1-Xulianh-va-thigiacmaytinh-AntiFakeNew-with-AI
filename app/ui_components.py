import streamlit as st

def load_custom_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"]  {
            font-family: 'Poppins', sans-serif !important;
        }

        .stApp {
            background: #0f172a; /* Slate 900 */
        }

        h1 {
            text-align: center;
            background: linear-gradient(to right, #818cf8, #c084fc, #38bdf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 4rem !important;
            font-weight: 800;
            letter-spacing: -1.5px;
            padding-top: 2.5rem;
            margin-bottom: 0.5rem;
            animation: fadeInDown 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .subtitle {
            text-align: center;
            color: #94a3b8;
            font-size: 1.3rem;
            font-weight: 400;
            margin-bottom: 3.5rem;
            animation: fadeInUp 1s cubic-bezier(0.4, 0, 0.2, 1);
        }

        /* Khung nhập liệu (Text Area) */
        .stTextArea textarea {
            font-family: 'Poppins', sans-serif !important;
            font-size: 1.15rem !important;
            padding: 1.8rem !important;
            border-radius: 24px !important;
            background-color: rgba(30, 41, 59, 0.7) !important; /* Slate 800 */
            border: 1px solid #334155 !important;
            color: #f8fafc !important;
            box-shadow: inset 0 2px 4px 0 rgba(0, 0, 0, 0.2);
            transition: all 0.4s ease;
            backdrop-filter: blur(10px);
        }
        .stTextArea textarea:focus {
            background-color: #1e293b !important;
            border-color: #6366f1 !important;
            box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.2), 0 20px 40px -10px rgba(0, 0, 0, 0.3) !important;
            transform: translateY(-3px);
        }

        /* Nút bấm */
        .stButton>button {
            width: 100%;
            height: 70px;
            font-size: 1.3rem;
            font-weight: 700;
            border-radius: 24px;
            background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%);
            color: white;
            border: none;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            margin-top: 1.5rem;
            box-shadow: 0 10px 25px -5px rgba(79, 70, 229, 0.5);
            text-transform: uppercase;
            letter-spacing: 1.5px;
        }
        .stButton>button:hover {
            transform: translateY(-6px) scale(1.02);
            box-shadow: 0 20px 35px -5px rgba(79, 70, 229, 0.6);
            background: linear-gradient(135deg, #4338ca 0%, #2563eb 100%);
            color: white;
        }
        
        img {
            border-radius: 24px;
            box-shadow: 0 20px 40px -10px rgba(0,0,0,0.5);
            transition: transform 0.4s ease;
        }
        img:hover {
            transform: scale(1.015);
        }

        /* Các lớp CSS cho Điểm số trong Popup */
        .score-high { color: #fb7185; font-size: 70px; font-weight: 800; line-height: 1; text-shadow: 0 10px 20px rgba(251, 113, 133, 0.3);}
        .score-mid { color: #fbbf24; font-size: 70px; font-weight: 800; line-height: 1; text-shadow: 0 10px 20px rgba(251, 191, 36, 0.3);}
        .score-low { color: #34d399; font-size: 70px; font-weight: 800; line-height: 1; text-shadow: 0 10px 20px rgba(52, 211, 153, 0.3);}

        /* Popup Dialog Tweak */
        div[data-testid="stDialog"] {
            border-radius: 24px !important;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5) !important;
            border: 1px solid rgba(255,255,255,0.1);
            background: rgba(15, 23, 42, 0.95);
            backdrop-filter: blur(20px);
        }

        @keyframes fadeInDown {
            from { opacity: 0; transform: translateY(-30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
    """, unsafe_allow_html=True)

def render_header():
    st.markdown("<h1>Anti Fake News Project</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Thực hiện bởi: Nhóm 1 - Xử Lý Ảnh Và Thị Giác Máy Tính</p>", unsafe_allow_html=True)

@st.dialog("✨ Kết Quả Phân Tích", width="large")
def show_result_popup(result, analysis_type, is_offline=False):
    prob = result.get("fake_probability", 50)
    
    st.markdown(f"<h3 style='color: #cbd5e1; font-weight: 500; font-size: 1.2rem; margin-bottom: 2rem;'>Khảo sát đối tượng: <span style='color: #f8fafc; font-weight: 700;'>{analysis_type}</span></h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.3])
    with col1:
        st.markdown("<p style='color: #cbd5e1; font-weight: 600; margin-bottom: 0px;'>Nguy cơ giả mạo:</p>", unsafe_allow_html=True)
        if prob > 50:
            st.markdown(f"<span class='score-high'>{prob}%</span>", unsafe_allow_html=True)
            st.error("🚨 KHẢ NĂNG CAO LÀ GIẢ MẠO / CẮT GHÉP")
        elif prob == 50:
            st.markdown(f"<span class='score-mid'>{prob}%</span>", unsafe_allow_html=True)
            st.warning("⚠️ CẦN KIỂM CHỨNG THÊM")
        else:
            st.markdown(f"<span class='score-low'>{prob}%</span>", unsafe_allow_html=True)
            st.success("✅ NỘI DUNG ĐÁNG TIN CẬY")
            
        st.progress(prob / 100.0)
        
    with col2:
        if is_offline:
            st.markdown("<h4 style='color: #f8fafc; font-weight: 700; margin-bottom: 1rem;'>⚙️ Phân Tích Bằng Trí Tuệ Nhân Tạo (Hệ thống Cục bộ - CNN & NLP):</h4>", unsafe_allow_html=True)
        else:
            st.markdown("<h4 style='color: #f8fafc; font-weight: 700; margin-bottom: 1rem;'>📋 Phân Tích Logic Bằng Siêu AI (Gemini Cloud):</h4>", unsafe_allow_html=True)
        for r in result.get("reasons", []):
            st.markdown(f"<p style='color: #94a3b8; line-height: 1.7; font-size: 1.05rem;'>• {r}</p>", unsafe_allow_html=True)
            
    st.divider()
    
    sentiment = result.get("sentiment_score", 0)
    st.markdown("<h4 style='color: #f8fafc; font-weight: 700;'>🎭 Chỉ số Cảm xúc (Sentiment):</h4>", unsafe_allow_html=True)
    if sentiment > 0.3:
        st.success(f"Văn phong Tích cực & Lạc quan (Điểm: {sentiment})")
    elif sentiment < -0.3:
        st.error(f"Văn phong Tiêu cực & Kích động dư luận (Điểm: {sentiment})")
    else:
        st.info(f"Văn phong Trung lập & Khách quan (Điểm: {sentiment})")

def display_results(result, analysis_type, is_offline=False):
    show_result_popup(result, analysis_type, is_offline)

def render_sidebar(history):
    with st.sidebar:
        st.markdown("<h2 style='color: #f8fafc; font-weight: 700; margin-bottom: 1rem;'>⚙️ Cấu Hình Hệ Thống</h2>", unsafe_allow_html=True)
        custom_key = st.text_input("🔑 Gemini API Key (Tùy chọn):", type="password", placeholder="Nhập API Key để dùng riêng...", help="Nếu API Key mặc định bị quá tải, bạn có thể nhập Key của riêng bạn vào đây để vượt giới hạn.")
        
        st.markdown("<hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
        st.markdown("<h2 style='color: #f8fafc; font-weight: 700; margin-bottom: 1.5rem;'>🕒 Lịch Sử Quét</h2>", unsafe_allow_html=True)
        if not history:
            st.info("Chưa có lịch sử. Các bài báo hoặc hình ảnh bạn quét sẽ hiển thị ở đây để tránh quét lại.")
        else:
            for item in history:
                prob = item["prob"]
                
                # Determine color based on probability
                if prob > 50:
                    color = "#ef4444" # Red
                    icon = "🚨"
                elif prob == 50:
                    color = "#f59e0b" # Yellow
                    icon = "⚠️"
                else:
                    color = "#10b981" # Green
                    icon = "✅"
                
                st.markdown(f"""
                <div style="
                    background: rgba(30, 41, 59, 0.7); 
                    border-left: 4px solid {color};
                    padding: 1rem;
                    border-radius: 12px;
                    margin-bottom: 1rem;
                    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                ">
                    <p style="color: #94a3b8; font-size: 0.85rem; margin-bottom: 0.5rem; text-transform: uppercase; font-weight: 600;">{icon} {item['type']} <span style="float:right; color: {color};">{prob}%</span></p>
                    <p style="color: #f8fafc; font-size: 0.95rem; margin-bottom: 0; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; font-weight: 500;">{item['snippet']}</p>
                </div>
                """, unsafe_allow_html=True)
        return custom_key
