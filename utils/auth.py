import streamlit as st
import time
from utils.db import init_supabase

def check_auth():
    """Protect pages and provide a SaaS-level authentication experience."""
    if "user_logged_in" not in st.session_state:
        st.session_state.user_logged_in = False
    if "guest_mode" not in st.session_state:
        st.session_state.guest_mode = False
    if "user_email" not in st.session_state:
        st.session_state.user_email = None

    if st.session_state.user_logged_in or st.session_state.guest_mode:
        return

    st.markdown(
        """
        <div style="text-align: center; padding: 2rem 0;">
            <h1 style="font-size: 2.5rem; color: #0f172a; margin-bottom: 0.5rem;">مرحباً بك في Stat Suite Pro 🚀</h1>
            <p style="color: #475569; font-size: 1.1rem;">قم بتسجيل الدخول لحفظ تحليلاتك وتقاريرك السابقة، أو تابع كزائر للتجربة السريعة.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        auth_tab1, auth_tab2 = st.tabs(["تسجيل الدخول", "إنشاء حساب"])
        supabase = init_supabase()

        with auth_tab1:
            st.markdown("### 🔐 تسجيل الدخول")
            with st.form("login_form"):
                email = st.text_input("البريد الإلكتروني")
                password = st.text_input("كلمة المرور", type="password")
                submitted = st.form_submit_button("تسجيل الدخول", type="primary", use_container_width=True)

                if submitted:
                    if not supabase:
                        st.error("لم يتم إعداد قاعدة البيانات. يرجى المتابعة كزائر.")
                    else:
                        with st.spinner("جاري التحقق..."):
                            try:
                                response = supabase.auth.sign_in_with_password({"email": email, "password": password})
                                st.session_state.user_logged_in = True
                                st.session_state.user_email = response.user.email
                                st.success("✅ تم الدخول بنجاح! جاري تحويلك...")
                                time.sleep(1)
                                st.rerun()
                            except Exception as e:
                                st.error("❌ بيانات الدخول غير صحيحة.")

        with auth_tab2:
            st.markdown("### 👤 إنشاء حساب جديد")
            with st.form("signup_form"):
                new_email = st.text_input("البريد الإلكتروني")
                new_password = st.text_input("كلمة المرور", type="password")
                signup_submitted = st.form_submit_button("إنشاء حساب", type="primary", use_container_width=True)

                if signup_submitted:
                    if not supabase:
                        st.error("لم يتم إعداد قاعدة البيانات. يرجى المتابعة كزائر.")
                    else:
                        with st.spinner("جاري التسجيل..."):
                            try:
                                response = supabase.auth.sign_up({"email": new_email, "password": new_password})
                                st.success("✅ تم التسجيل بنجاح! يرجى تأكيد بريدك الإلكتروني (إذا كان مفعلاً) أو تسجيل الدخول.")
                            except Exception as e:
                                st.error(f"❌ حدث خطأ أثناء التسجيل: {str(e)}")

        st.markdown("<br><hr>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #475569;'>أو الدخول السريع</p>", unsafe_allow_html=True)
        
        # Google Login Simulation
        if st.button("🌐 Continue with Google", use_container_width=True):
            st.info("⚠️ تم تعطيل Google OAuth مؤقتاً لعدم توفر الـ Client ID في إعدادات Supabase. يرجى استخدام الايميل أو متابعة كزائر.")
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🚀 متابعة كزائر (Guest Mode)", use_container_width=True, type="secondary"):
            st.session_state.guest_mode = True
            st.success("تم تفعيل وضع الزائر! لن يتم حفظ بياناتك في السحابة.")
            time.sleep(1)
            st.rerun()

    st.stop()
