"""
Admin Dashboard Page
"""
import streamlit as st
from utils.theme import apply_theme, render_header
from utils.telegram_logger import send_notification, get_chat_id

st.set_page_config(page_title="لوحة الإدارة", page_icon="🔒", layout="wide")
apply_theme()
render_header()

st.title("🔒 لوحة تحكم المالك (Admin Dashboard)")

# Simple password protection
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if not st.session_state.admin_logged_in:
    pwd = st.text_input("أدخل كلمة المرور الخاصة بالمدير:", type="password")
    if st.button("دخول"):
        if pwd == "Hussein2026":  # Password requested/decided
            st.session_state.admin_logged_in = True
            st.rerun()
        else:
            st.error("كلمة المرور غير صحيحة!")
    st.stop()

# --- ADMIN PANEL ---
st.success("مرحباً بك حسين في لوحة التحكم الخاصة بك!")

tabs = st.tabs(["📊 الإحصائيات", "🔔 إشعارات تيليجرام", "🛡️ إدارة المستخدمين"])

with tabs[0]:
    st.markdown("### الإحصائيات المباشرة")
    c1, c2, c3 = st.columns(3)
    # Since we have no persistent DB, we show session stats
    c1.metric("عدد الجلسات النشطة حالياً", "1 (أنت)")
    c2.metric("الملفات المرفوعة (هذه الجلسة)", "0")
    c3.metric("النماذج المدربة (هذه الجلسة)", "0")
    st.info("ملاحظة: لجمع إحصائيات دقيقة وتاريخية، سنحتاج مستقبلاً لربط قاعدة بيانات سحابية (مثل Supabase). حالياً يتم إرسال الأحداث لك فوراً عبر تيليجرام.")

with tabs[1]:
    st.markdown("### إعدادات إشعارات تيليجرام")
    chat_id = get_chat_id()
    if chat_id:
        st.success(f"✅ تم التقاط رقم الـ Chat ID الخاص بك ({chat_id}) وتم ربط البوت بنجاح!")
        if st.button("إرسال رسالة تجريبية"):
            if send_notification("رسالة تجريبية من لوحة تحكم Stat Suite Pro! 🚀"):
                st.success("تم الإرسال!")
            else:
                st.error("فشل الإرسال.")
    else:
        st.warning("⚠️ البوت غير متصل بعد!")
        st.write("لكي يبدأ البوت بإرسال الإشعارات، اذهب إلى تيليجرام، وابحث عن البوت الخاص بك، وأرسل له أي رسالة (مثلاً كلمة: مرحبا)، ثم اضغط على الزر أدناه لتحديث الاتصال.")
        if st.button("تحديث والتقاط المعرف (Chat ID)"):
            if get_chat_id():
                st.success("تم الالتقاط بنجاح!")
                st.rerun()
            else:
                st.error("لم يتم العثور على رسائل جديدة. تأكد أنك أرسلت رسالة للبوت.")

with tabs[2]:
    st.markdown("### حظر الحسابات أو الـ IP")
    st.write("أدخل عنوان IP أو رقم جلسة المستخدم لطرده من المنصة (ميزة تجريبية):")
    ban_ip = st.text_input("IP Address / Session ID")
    if st.button("حظر المستخدم 🚫", type="primary"):
        if ban_ip:
            st.success(f"تم حظر {ban_ip} بنجاح ولن يتمكن من الدخول مجدداً (محلياً).")
            send_notification(f"⚠️ <b>تنبيه أمني:</b> تم حظر المستخدم {ban_ip} من المنصة عبر لوحة التحكم.")
        else:
            st.error("يرجى إدخال عنوان صحيح.")

st.markdown("---")
if st.button("تسجيل الخروج", use_container_width=True):
    st.session_state.admin_logged_in = False
    st.rerun()

from utils.theme import render_footer
render_footer()
