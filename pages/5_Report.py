"""
Page 5 — Report Export & Session Management
"""
import os
import sys
import json
from datetime import datetime

import pandas as pd
import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.theme import apply_theme, render_header
from utils.session import init_session, reset_session, export_session, import_session
from utils.pdf_report import build_pdf_report
from utils.data_utils import summary_dict

st.set_page_config(page_title="Report", page_icon="📄", layout="wide")
init_session()
apply_theme()
render_header()

st.markdown("## 📄 Report & Downloads — التقارير والتنزيل")

tab1, tab2, tab3 = st.tabs([
    "📑 سجل النتائج",
    "📄 تقرير PDF",
    "💾 الجلسة والملفات",
])

with tab1:
    st.subheader("سجل النتائج التحليلية")
    logs = st.session_state.results_log
    if not logs:
        st.info("لا توجد نتائج محفوظة بعد. شغّل التحليلات أولاً من صفحات Statistics أو Machine Learning.")
    else:
        st.write(f"**عدد النتائج:** {len(logs)}")
        for i, r in enumerate(logs, 1):
            with st.expander(f"{i}. [{r['category']}] {r['title']} · {r['timestamp']}"):
                st.json(r["content"])

        if st.button("🗑️ مسح كل النتائج"):
            st.session_state.results_log = []
            st.success("✅ تم مسح السجل")
            st.rerun()

        flat_rows = []
        for r in logs:
            row = {
                "category": r["category"],
                "title": r["title"],
                "timestamp": r["timestamp"],
            }
            for k, v in r["content"].items():
                row[k] = v if isinstance(v, (str, int, float, bool)) else json.dumps(v, ensure_ascii=False)
            flat_rows.append(row)
        df_logs = pd.DataFrame(flat_rows)

        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                "⬇️ تنزيل النتائج CSV",
                df_logs.to_csv(index=False).encode("utf-8-sig"),
                file_name="analysis_results.csv",
                mime="text/csv",
            )
        with col2:
            st.download_button(
                "⬇️ تنزيل النتائج JSON",
                json.dumps(logs, ensure_ascii=False, indent=2, default=str),
                file_name="analysis_results.json",
                mime="application/json",
            )

with tab2:
    st.subheader("توليد تقرير PDF احترافي")
    project_name = st.text_input("اسم المشروع", value=st.session_state.project_name)
    st.session_state.project_name = project_name

    a, b, c = st.columns(3)
    a.metric("الملف الحالي", st.session_state.filename or "—")
    b.metric("عدد النتائج", len(st.session_state.results_log))
    c.metric("نماذج ML", len(st.session_state.ml_models))

    if st.button("📄 إنشاء التقرير", type="primary"):
        if st.session_state.df is None:
            st.error("⚠️ لا توجد بيانات محملة")
        else:
            try:
                with st.spinner("جاري إنشاء تقرير PDF..."):
                    pdf_bytes = build_pdf_report(
                        project_name=project_name,
                        filename=st.session_state.filename or "dataset",
                        df_summary=summary_dict(st.session_state.df),
                        results_log=st.session_state.results_log,
                        figures=st.session_state.figures,
                    )
                st.success("✅ تم إنشاء التقرير بنجاح")
                st.download_button(
                    "⬇️ تنزيل التقرير PDF",
                    pdf_bytes,
                    file_name=f"{project_name.replace(' ', '_')}_report.pdf",
                    mime="application/pdf",
                )
            except Exception as e:
                st.error(f"خطأ أثناء إنشاء التقرير: {e}")

with tab3:
    st.subheader("تنزيل الملفات وحفظ الجلسة")

    if st.session_state.df is not None:
        st.download_button(
            "⬇️ تنزيل البيانات الحالية CSV",
            st.session_state.df.to_csv(index=False).encode("utf-8-sig"),
            file_name=f"current_{st.session_state.filename or 'dataset'}.csv",
            mime="text/csv",
        )
    else:
        st.info("لا توجد بيانات حالية للتنزيل")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 💾 تصدير الجلسة")
        if st.button("إنشاء ملف الجلسة"):
            try:
                session_blob = export_session()
                st.download_button(
                    "⬇️ تنزيل ملف الجلسة .statpro",
                    session_blob.encode(),
                    file_name=f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.statpro",
                    mime="text/plain",
                )
            except Exception as e:
                st.error(f"خطأ: {e}")

    with col2:
        st.markdown("### 📥 استيراد جلسة")
        uploaded_session = st.file_uploader("ملف .statpro", type=["statpro", "txt"])
        if uploaded_session and st.button("استعادة الجلسة"):
            try:
                import_session(uploaded_session.read().decode())
                st.success("✅ تمت استعادة الجلسة")
                st.rerun()
            except Exception as e:
                st.error(f"خطأ: {e}")

    st.markdown("---")
    st.markdown("### ⚠️ منطقة الخطر")
    if st.button("🗑️ مسح الجلسة بالكامل"):
        reset_session()
        st.success("✅ تم مسح كل شيء")
        st.rerun()
