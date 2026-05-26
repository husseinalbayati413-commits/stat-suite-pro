"""
Stat Suite Pro
Main landing page for the Streamlit multipage app.
"""
import streamlit as st
from utils.session import init_session

st.set_page_config(
    page_title="Stat Suite Pro | منصة التحليل الإحصائي",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_session()


st.sidebar.markdown("## 📊 Stat Suite Pro")
st.sidebar.caption("تحليل إحصائي احترافي · انحدار · تعلم آلة")


st.markdown(
    """
    <div class="hero-card rtl-app">
        <div class="hero-badge">نسخة احترافية محسّنة ومتوافقة مع الهاتف</div>
        <h1>منصة متكاملة للتحليل الإحصائي والانحدار</h1>
        <p>
            ارفع ملفك، نظّف البيانات، نفّذ الاختبارات الإحصائية، شغّل نماذج الانحدار،
            وصدّر تقرير PDF ونتائج قابلة للتحميل مباشرة من المتصفح أو الهاتف.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

c1, c2, c3, c4 = st.columns(4)
c1.metric("البيانات المحمّلة", "نعم" if st.session_state.get("df") is not None else "لا")
c2.metric("النتائج المسجلة", len(st.session_state.get("results_log", [])))
c3.metric("نماذج ML", len(st.session_state.get("ml_models", {})))
c4.metric("اسم المشروع", st.session_state.get("project_name", "Untitled"))

st.markdown("## ✨ ماذا أضفنا في النسخة الاحترافية؟")
feat1, feat2, feat3 = st.columns(3)

with feat1:
    st.markdown(
        """
        <div class="feature-card rtl-app">
            <h3>📂 إدارة بيانات احترافية</h3>
            <p>رفع CSV وExcel، تنظيف القيم المفقودة، حذف التكرار، تحويل الأنواع، وترميز الأعمدة الفئوية.</p>
            <p>إمكانية تنزيل البيانات المنظّفة مباشرة بصيغة CSV.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with feat2:
    st.markdown(
        """
        <div class="feature-card rtl-app">
            <h3>📈 إحصاء شامل + انحدار</h3>
            <p>إحصاء وصفي، فحص طبيعية التوزيع، فترات الثقة، الارتباط، T-Test، ANOVA، Chi-Square، كشف القيم الشاذة.</p>
            <p>انحدار خطي بسيط ومتعدد ومتعدد الحدود مع معاملات، قيم P، VIF، والبواقي.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with feat3:
    st.markdown(
        """
        <div class="feature-card rtl-app">
            <h3>📱 تجربة مناسبة للهاتف</h3>
            <p>بطاقات متجاوبة، تقليل الحشو، جداول ورسوم بعرض كامل، وأزرار تنزيل واضحة تعمل من الهاتف.</p>
            <p>واجهة ثنائية اللغة بصياغة عربية أوضح ومظهر أكثر احترافية.</p>
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
st.markdown(
    """
    <div class="footer-card rtl-app">
        <strong>Stat Suite Pro v2.0</strong><br/>
        مبني باستخدام Pandas · SciPy · statsmodels · scikit-learn · Plotly · Streamlit
    </div>
    """,
    unsafe_allow_html=True,
)
