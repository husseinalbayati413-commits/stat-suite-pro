"""
Privacy Policy Page
"""
import streamlit as st
from utils.theme import apply_theme, render_header

st.set_page_config(page_title="شروط الأحكام وسياسة الخصوصية", page_icon="icon.png", layout="wide")
apply_theme()
render_header()

st.title("🛡️ شروط الأحكام وسياسة الخصوصية")
st.markdown(
    """
    <div class="feature-card rtl-app">
        <h3>شروط الاستخدام</h3>
        <p>هذا التطبيق مقدم كأداة تعليمية وعملية لتحليل البيانات. استخدامك للتطبيق يعني موافقتك على إخلاء مسؤولية المطور عن أي أضرار أو قرارات تُتخذ بناءً على النتائج الإحصائية.</p>

        <h3>سياسة الخصوصية</h3>
        <p>نحن في Stat Suite Pro (المطور: حسين حيدر) نلتزم بحماية خصوصية بياناتك.</p>
        
        <h3>جمع البيانات واستخدامها</h3>
        <p>التطبيق يعمل بالكامل لمعالجة بياناتك وقت الجلسة. نحن لا نقوم بتخزين ملفاتك، أو بياناتك، أو نتائج تحليلاتك على خوادمنا بشكل دائم.</p>
        
        <h3>أمان البيانات</h3>
        <p>تتم معالجة البيانات عبر بروتوكولات آمنة وتُحذف بمجرد إنهاء الجلسة أو إغلاق التطبيق.</p>
        
        <h3>التواصل</h3>
        <p>للتواصل والاستفسارات والدعم، يرجى مراسلتنا عبر البريد الإلكتروني:<br/>
        <a href="mailto:Husseinalbayati413@gmail.com">Husseinalbayati413@gmail.com</a></p>
    </div>
    """,
    unsafe_allow_html=True
)

from utils.theme import render_footer
render_footer()
