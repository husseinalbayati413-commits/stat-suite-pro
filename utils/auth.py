import streamlit as st
import time

def check_auth():
    """Protect pages with a password."""
    if "user_logged_in" not in st.session_state:
        st.session_state.user_logged_in = False
        
    if not st.session_state.user_logged_in:
        st.markdown("## 🔒 تسجيل الدخول مطلوب")
        st.info("هذه الصفحة محمية. يرجى إدخال كلمة المرور للوصول إلى أدوات التحليل والإحصاء.")
        
        with st.form("login_form"):
            pwd = st.text_input("كلمة المرور:", type="password")
            submitted = st.form_submit_button("تسجيل الدخول", type="primary")
            
            if submitted:
                if pwd == "StatPro@2026!":
                    st.session_state.user_logged_in = True
                    st.success("تم تسجيل الدخول بنجاح! جاري تحويلك...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("كلمة المرور غير صحيحة.")
        st.stop()
