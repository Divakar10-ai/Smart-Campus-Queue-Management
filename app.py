import streamlit as st
from database import init_database
from modules.admin import admin_page
from modules.student import student_page
from modules.analytics import analytics_page
from modules.reports import reports_page

st.set_page_config(
    page_title="Smart Queue Management System",
    page_icon="SQ",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_database()

# ---------- Styling ----------
st.markdown("""
<style>
    .stApp { background: #f6f8fb; }
    [data-testid="stSidebar"] { background: #111827; }
    [data-testid="stSidebar"] * { color: #f9fafb !important; }
    .main-title { font-size: 32px; font-weight: 700; color: #111827; margin-bottom: 4px; }
    .subtitle { color: #6b7280; margin-bottom: 24px; }
    .card {
        background: white; padding: 20px; border-radius: 12px;
        border: 1px solid #e5e7eb; margin-bottom: 16px;
    }
    .metric-label { color:#6b7280; font-size:13px; }
    .metric-value { color:#111827; font-size:28px; font-weight:700; }
    .token {
        font-size: 52px; font-weight: 800; text-align:center;
        color:#111827; padding:18px; border:2px solid #2563eb;
        border-radius:14px; background:#eff6ff;
    }
    div.stButton > button {
        border-radius: 8px; font-weight: 600; min-height: 42px;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## Smart Queue")
    st.caption("Campus Queue Management")
    st.divider()

    role = st.radio(
        "Module",
        ["Student", "Admin", "Analytics", "Reports"],
        index=0
    )
    st.divider()
    st.caption("Smart Campus Queue Management System")
    st.caption("SQLite • Streamlit • Prediction")

if role == "Student":
    student_page()
elif role == "Admin":
    admin_page()
elif role == "Analytics":
    analytics_page()
else:
    reports_page()
