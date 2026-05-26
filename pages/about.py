import os
import sys
import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.theme import apply_theme, render_header
from utils.session import init_session

st.set_page_config(page_title="About Platform", page_icon="icon.png", layout="wide")
init_session()
apply_theme()
render_header()

st.markdown("## 🧠 About Stat Suite Pro")

st.markdown("""
<div class="feature-card rtl-app">
<h3>نبذة عن المنصة</h3>
<p>Stat Suite Pro منصة تعليمية وعملية لتحليل البيانات، الإحصاء التطبيقي، الانحدار، وتعلم الآلة.</p>
<p>تم تصميمها لتكون مناسبة للباحثين والطلبة ومحللي البيانات مع واجهة واضحة ومتجاوبة.</p>
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
c1.metric("التحليل الإحصائي", "متقدم")
c2.metric("الانحدار", "خطي ومتعدد")
c3.metric("التقارير", "PDF + CSV + JSON")

st.markdown("""
### الفئات المستهدفة
- الباحثون وطلاب الدراسات العليا
- مشاريع التخرج والتقارير الجامعية
- محللو البيانات والمدربون
- من يريد واجهة سهلة لإجراء اختبارات إحصائية بسرعة

### التقنيات المستخدمة
- Streamlit
- Pandas / NumPy / SciPy
- statsmodels / scikit-learn
- Plotly / ReportLab
""")


from utils.theme import render_footer
render_footer()
