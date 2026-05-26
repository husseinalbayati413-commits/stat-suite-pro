"""
Download App Page
"""
import streamlit as st
from utils.theme import apply_theme, render_header

st.set_page_config(page_title="تحميل التطبيق", page_icon="icon.png", layout="wide")
apply_theme()
render_header()

st.title("📥 تحميل تطبيق الأندرويد")
st.markdown(
    """
    <div class="hero-card rtl-app">
        <h2>قم بتحميل تطبيق Stat Suite Pro على هاتفك</h2>
        <p>يمكنك الآن الاستمتاع بجميع ميزات التحليل الإحصائي مباشرة من هاتفك الأندرويد.</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.info("سيتم توفير رابط تحميل ملف الـ APK هنا قريباً بعد رفع التطبيق إلى المتجر أو توفير رابط مباشر.")

from utils.theme import render_footer
render_footer()
