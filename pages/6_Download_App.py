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

apk_path = "StatSuitePro.apk"
if os.path.exists(apk_path):
    with open(apk_path, "rb") as file:
        btn = st.download_button(
            label="📲 تحميل التطبيق (APK)",
            data=file,
            file_name="StatSuitePro.apk",
            mime="application/vnd.android.package-archive"
        )
    st.success("اضغط على الزر أعلاه لتنزيل التطبيق وتثبيته على هاتفك.")
else:
    st.info("لم يتم رفع ملف التطبيق (APK) حتى الآن. (للمطور: قم ببناء التطبيق باستخدام Android Studio وارفع ملف StatSuitePro.apk إلى المستودع).")


from utils.theme import render_footer
render_footer()
