import os
import sys
import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.theme import apply_theme, render_header
from utils.session import init_session

st.set_page_config(page_title="Settings", page_icon="⚙️", layout="wide")
init_session()
apply_theme()
render_header()

st.markdown("## ⚙️ Settings — الإعدادات")
st.info("هذه الصفحة حالياً تعريفية لتوضيح حالة المنصة. يمكن تطويرها لاحقاً لحفظ تفضيلات المستخدم بشكل دائم.")

col1, col2 = st.columns(2)
with col1:
    st.selectbox("اللغة", ["العربية", "English"], index=0, disabled=True)
    st.selectbox("النمط", ["Professional Light"], index=0, disabled=True)
with col2:
    st.selectbox("نوع الرسوم الافتراضي", ["Plotly Interactive"], index=0, disabled=True)
    st.toggle("Auto Save", value=True, disabled=True)

st.success("✅ الواجهة المتجاوبة للهاتف مفعّلة، وأزرار التنزيل متاحة داخل الصفحات الرئيسية.")
