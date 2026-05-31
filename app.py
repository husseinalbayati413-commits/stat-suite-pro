"""
Stat Suite Pro
Main landing page for the Streamlit multipage app.
"""
import streamlit as st
from utils.session import init_session
from utils.theme import render_footer

st.set_page_config(
    page_title="Stat Suite Pro | منصة التحليل الإحصائي",
    page_icon="icon.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_session()


st.sidebar.markdown("## 📊 Stat Suite Pro")
st.sidebar.caption("تحليل إحصائي احترافي · انحدار · تعلم آلة")


st.markdown(
    """
    <div class="hero-card rtl-app" style="text-align: center; padding: 3rem 1rem;">
        <div class="hero-badge">Stat Suite Pro v2.0</div>
        <h1 style="font-size: 2.8rem; margin-bottom: 1rem;">المنصة الأولى لتحليل البيانات الإحصائية بضغطة زر</h1>
        <p style="font-size: 1.2rem; max-width: 800px; margin: 0 auto 2rem auto;">
            بديلك الأسرع والأذكى لبرامج SPSS و Excel. ارفع بياناتك، نفذ أعقد الاختبارات الإحصائية ونماذج الانحدار، واحصل على تقريرك جاهزاً في ثوانٍ معدودة.
        </p>
        <a href="Data_Lab" target="_self" style="background: linear-gradient(135deg, #4f46e5, #7c3aed); color: white; padding: 12px 30px; border-radius: 30px; text-decoration: none; font-weight: bold; font-size: 1.2rem; box-shadow: 0 10px 20px rgba(79,70,229,0.3);">🚀 ابدأ التحليل مجاناً الآن</a>
    </div>
    """,
    unsafe_allow_html=True,
)

c1, c2, c3, c4 = st.columns(4)
c1.metric("مستخدمين نشطين", "متصل")
c2.metric("دقة النماذج المدعومة", "99%")
c3.metric("سرعة المعالجة", "ثوانٍ")
c4.metric("الأمان والخصوصية", "تشفير كامل")

st.markdown("## 💡 لماذا تختار Stat Suite Pro؟ (بديل SPSS)")
feat1, feat2, feat3 = st.columns(3)

with feat1:
    st.markdown(
        """
        <div class="feature-card rtl-app">
            <h3>⚡ أسرع من Excel</h3>
            <p>لا داعي لكتابة معادلات معقدة أو ترتيب البيانات يدوياً. المنصة تقوم بتنظيف ومعالجة البيانات المفقودة تلقائياً بنقرة واحدة.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with feat2:
    st.markdown(
        """
        <div class="feature-card rtl-app">
            <h3>🧠 أذكى من SPSS</h3>
            <p>واجهة عصرية وبديهية تدعم اللغة العربية بالكامل، مع تقارير جاهزة قابلة للتنزيل بصيغة PDF تتضمن جميع الرسوم البيانية.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with feat3:
    st.markdown(
        """
        <div class="feature-card rtl-app">
            <h3>🤖 ذكاء اصطناعي وانحدار</h3>
            <p>ليست فقط للإحصاء الوصفي! تدعم المنصة خوارزميات تعلم الآلة، الانحدار الخطي والمتعدد، والتجميع (Clustering) المتقدم.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("## 🚀 مسار العمل المقترح")
step1, step2, step3, step4 = st.columns(4)
for col, title, text in [
    (step1, "1) Data Lab", "حمّل البيانات أو جرّب عينات جاهزة ثم افحص الجودة والأنواع والقيم المفقودة."),
    (step2, "2) Statistics", "نفّذ التحليل الإحصائي المتقدم، الارتباط، الاختبارات، والانحدار."),
    (step3, "3) ML & Visuals", "جرّب التنبؤ والتصنيف والتجميع والرسوم التفاعلية."),
    (step4, "4) Report", "نزّل تقرير PDF وملفات النتائج والجلسة والبيانات المنظفة."),
]:
    with col:
        st.markdown(
            f"""
            <div class="mini-card rtl-app">
                <h4>{title}</h4>
                <p>{text}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("## 📌 ملاحظات مهمة")
st.info(
    "• التطبيق متعدد الصفحات ويعمل من المتصفح، لذلك يمكن فتحه من الهاتف بسهولة.\n"
    "• كل صفحة تعرض أزرار تنزيل واضحة للنتائج والملفات.\n"
    "• صفحة Statistics أصبحت تشمل الجوانب الإحصائية الأساسية والمتقدمة والانحدار بشكل موسع."
)

st.markdown("---")
render_footer()
