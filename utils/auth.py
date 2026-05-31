import streamlit as st
import time

def check_auth():
    """Protect pages with a password."""
    if "user_logged_in" not in st.session_state:
        st.session_state.user_logged_in = False
        
    if not st.session_state.user_logged_in:
        st.markdown("## 🔒 تسجيل الدخول مطلوب")
        st.info("هذه الصفحة محمية. يرجى إدخال كلمة المرور للوصول إلى أدوات التحليل والإحصاء.")
        
        pwd = st.text_input("كلمة المرور:", type="password", key="login_password")
        if st.button("تسجيل الدخول", type="primary"):
            # Strong password required by user
            if pwd == "StatPro@2026!":
                st.session_state.user_logged_in = True
                st.success("تم تسجيل الدخول بنجاح! جاري تحويلك...")
                time.sleep(1)
                st.rerun()
            else:
                st.error("كلمة المرور غير صحيحة.")
        st.stop()
