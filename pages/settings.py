"""
Settings Page
"""
import os
import sys
import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.theme import apply_theme, render_header
from utils.session import init_session

st.set_page_config(page_title="الإعدادات", page_icon="icon.png", layout="wide")
init_session()
apply_theme()
render_header()

st.markdown("## ⚙️ الإعدادات الشاملة (Settings)")
st.info("قم بتخصيص تفضيلات التطبيق. يتم حفظ الإعدادات تلقائياً في جلستك الحالية.")

col1, col2 = st.columns(2)

with col1:
    st.session_state.app_language = st.selectbox(
        "اللغة (Language)", 
        ["العربية", "English"], 
        index=0 if st.session_state.get("app_language", "العربية") == "العربية" else 1
    )
    
    st.session_state.app_theme = st.selectbox(
        "المظهر (Theme)", 
        ["Professional Light (الافتراضي)", "Dark Mode (قريباً)"], 
        index=0
    )

with col2:
    st.session_state.plot_type = st.selectbox(
        "نوع الرسوم البيانية", 
        ["Plotly Interactive (تفاعلي)", "Matplotlib (ثابت)"], 
        index=0 if st.session_state.get("plot_type", "Plotly Interactive (تفاعلي)") == "Plotly Interactive (تفاعلي)" else 1
    )
    
    st.session_state.auto_save = st.toggle(
        "الحفظ التلقائي للنتائج (Auto Save)", 
        value=st.session_state.get("auto_save", True)
    )

st.markdown("---")
st.markdown("### 💾 مسح البيانات")
if st.button("🗑️ مسح بيانات الجلسة الحالية", use_container_width=True):
    st.session_state.clear()
    st.success("تم مسح جميع البيانات والنتائج من الجلسة الحالية بنجاح!")
    st.rerun()

st.success("✅ جميع الإعدادات مفعلة ويتم حفظها تلقائياً.")

from utils.theme import render_footer
render_footer()
