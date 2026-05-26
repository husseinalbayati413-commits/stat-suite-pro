"""
Privacy Policy Page
"""
import streamlit as st
from utils.theme import apply_theme, render_header

st.set_page_config(page_title="سياسة الخصوصية", page_icon="🛡️", layout="wide")
apply_theme()
render_header()

st.title("🛡️ سياسة الخصوصية")
st.markdown(
    """
    <div class="feature-card rtl-app">
        <h3>مقدمة</h3>
        <p>نحن في Stat Suite Pro (المطور: حسين حيدر) نلتزم بحماية خصوصية بياناتك.</p>
        
        <h3>جمع البيانات واستخدامها</h3>
        <p>التطبيق يعمل بالكامل لمعالجة بياناتك وقت الجلسة. نحن لا نقوم بتخزين ملفاتك، أو بياناتك، أو نتائج تحليلاتك على خوادمنا بشكل دائم.</p>
        
        <h3>أمان البيانات</h3>
        <p>تتم معالجة البيانات عبر بروتوكولات آمنة وتُحذف بمجرد إنهاء الجلسة أو إغلاق التطبيق.</p>
    </div>
    """,
    unsafe_allow_html=True
)

from utils.theme import render_footer
render_footer()
