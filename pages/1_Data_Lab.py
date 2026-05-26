"""
Page 1 — Data Lab
Load, inspect, clean, transform, and download datasets.
"""
import os
import sys

import numpy as np
import pandas as pd
import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.theme import apply_theme, render_header
from utils.session import init_session, add_result
from utils.data_utils import load_file, fill_missing

st.set_page_config(page_title="Data Lab", page_icon="📂", layout="wide")
init_session()
apply_theme()
render_header()

st.markdown("## 📂 Data Lab — مختبر البيانات")
st.caption("رفع البيانات، الفحص السريع، التنظيف، التحويل، والتنزيل")


def load_sample_dataset(name: str) -> pd.DataFrame:
    if name == "Iris":
        from sklearn.datasets import load_iris
        data = load_iris(as_frame=True)
        df = data.frame
        df["species"] = df["target"].map(dict(enumerate(data.target_names)))
        return df.drop(columns=["target"])
    if name in {"Tips", "Titanic"}:
        import seaborn as sns
        return sns.load_dataset(name.lower())
    raise ValueError("Unknown dataset")


def save_df_to_session(df: pd.DataFrame, filename: str):
    st.session_state.df = df
    st.session_state.df_original = df.copy()
    st.session_state.filename = filename


def profile_table(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({
        "العمود": df.columns,
        "النوع": df.dtypes.astype(str).values,
        "غير فارغ": df.notnull().sum().values,
        "فارغ": df.isnull().sum().values,
        "قيم فريدة": df.nunique(dropna=True).values,
        "النسبة المفقودة %": ((df.isnull().sum() / len(df)) * 100).round(2).values,
    })


summary1, summary2, summary3, summary4 = st.columns(4)
df_now = st.session_state.df
summary1.metric("البيانات المحمّلة", "نعم" if df_now is not None else "لا")
summary2.metric("الصفوف", 0 if df_now is None else df_now.shape[0])
summary3.metric("الأعمدة", 0 if df_now is None else df_now.shape[1])
summary4.metric("القيم المفقودة", 0 if df_now is None else int(df_now.isnull().sum().sum()))

tab1, tab2, tab3, tab4 = st.tabs([
    "📤 تحميل البيانات",
    "🔍 معاينة وفحص",
    "🧹 تنظيف",
    "🔄 تحويل وتنزيل",
])

with tab1:
    st.subheader("تحميل ملف البيانات")
    col1, col2 = st.columns([2, 1])

    with col1:
        uploaded = st.file_uploader("اختر ملف CSV أو Excel", type=["csv", "xls", "xlsx"])
        if uploaded:
            try:
                df = load_file(uploaded)
                save_df_to_session(df, uploaded.name)
                st.success(f"✅ تم تحميل {uploaded.name} بنجاح — {df.shape[0]} صف × {df.shape[1]} عمود")
                add_result("Data Lab", "Upload Dataset", {
                    "filename": uploaded.name,
                    "rows": int(df.shape[0]),
                    "columns": int(df.shape[1]),
                })
            except Exception as e:
                st.error(f"خطأ في قراءة الملف: {e}")

    with col2:
        st.markdown("### بيانات تجريبية")
        sample_choice = st.selectbox("اختر مجموعة", ["—", "Iris", "Tips", "Titanic"])
        if st.button("تحميل العينة"):
            try:
                if sample_choice != "—":
                    df = load_sample_dataset(sample_choice)
                    save_df_to_session(df, f"{sample_choice}.csv")
                    st.success(f"✅ تم تحميل بيانات {sample_choice}")
            except Exception as e:
                st.error(f"تعذر تحميل العينة: {e}")

with tab2:
    if st.session_state.df is None:
        st.info("⚠️ حمّل ملفاً أولاً من تبويب التحميل")
    else:
        df = st.session_state.df
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("الصفوف", df.shape[0])
        c2.metric("الأعمدة", df.shape[1])
        c3.metric("القيم المفقودة", int(df.isnull().sum().sum()))
        c4.metric("الحجم التقريبي KB", round(df.memory_usage(deep=True).sum() / 1024, 1))

        st.subheader("📌 أول 15 صف")
        st.dataframe(df.head(15), use_container_width=True)

        st.subheader("🧾 بروفايل الأعمدة")
        st.dataframe(profile_table(df), use_container_width=True)

        st.subheader("📊 إحصاء وصفي")
        st.dataframe(df.describe(include="all").T.fillna("—"), use_container_width=True)

with tab3:
    if st.session_state.df is None:
        st.info("⚠️ حمّل ملفاً أولاً")
    else:
        df = st.session_state.df.copy()
        st.subheader("تنظيف البيانات")

        left, right = st.columns(2)
        with left:
            strategy = st.radio(
                "استراتيجية معالجة القيم المفقودة",
                ["mean", "median", "zero", "drop"],
                format_func=lambda x: {
                    "mean": "المتوسط",
                    "median": "الوسيط",
                    "zero": "استبدال بصفر",
                    "drop": "حذف الصفوف الناقصة",
                }[x],
            )
            if st.button("تطبيق معالجة القيم المفقودة"):
                before = int(df.isnull().sum().sum())
                cleaned = fill_missing(df, strategy)
                st.session_state.df = cleaned
                after = int(cleaned.isnull().sum().sum())
                st.success(f"✅ تم التطبيق — قبل: {before} | بعد: {after}")
                add_result("Data Cleaning", "Missing Value Treatment", {
                    "strategy": strategy,
                    "missing_before": before,
                    "missing_after": after,
                })

        with right:
            duplicates = int(df.duplicated().sum())
            st.metric("الصفوف المكررة", duplicates)
            if st.button("حذف الصفوف المكررة"):
                before_rows = len(df)
                cleaned = df.drop_duplicates()
                st.session_state.df = cleaned
                removed = int(before_rows - len(cleaned))
                st.success(f"✅ تم حذف {removed} صف مكرر")
                add_result("Data Cleaning", "Remove Duplicates", {"removed_rows": removed})

        st.markdown("---")
        cols_to_drop = st.multiselect("أعمدة للحذف", df.columns.tolist())
        if cols_to_drop and st.button("حذف الأعمدة المحددة"):
            cleaned = df.drop(columns=cols_to_drop)
            st.session_state.df = cleaned
            st.success(f"✅ تم حذف: {', '.join(cols_to_drop)}")
            add_result("Data Cleaning", "Drop Columns", {"columns": ", ".join(cols_to_drop)})

        if st.button("🔄 استعادة البيانات الأصلية"):
            st.session_state.df = st.session_state.df_original.copy()
            st.success("✅ تمت استعادة النسخة الأصلية")

with tab4:
    if st.session_state.df is None:
        st.info("⚠️ حمّل ملفاً أولاً")
    else:
        df = st.session_state.df.copy()
        st.subheader("تحويل الأعمدة")

        col_to_convert = st.selectbox("العمود", df.columns.tolist())
        new_type = st.selectbox("النوع الجديد", ["int", "float", "str", "category", "datetime"])

        if st.button("تطبيق التحويل"):
            try:
                if new_type == "datetime":
                    df[col_to_convert] = pd.to_datetime(df[col_to_convert], errors="coerce")
                elif new_type == "category":
                    df[col_to_convert] = df[col_to_convert].astype("category")
                else:
                    df[col_to_convert] = df[col_to_convert].astype(new_type)
                st.session_state.df = df
                st.success(f"✅ تم تحويل {col_to_convert} إلى {new_type}")
                add_result("Data Transform", "Type Conversion", {
                    "column": col_to_convert,
                    "new_type": new_type,
                })
            except Exception as e:
                st.error(f"خطأ في التحويل: {e}")

        st.markdown("---")
        cat_cols = df.select_dtypes(exclude=np.number).columns.tolist()
        if cat_cols:
            col_enc = st.selectbox("عمود فئوي للترميز", cat_cols)
            enc_type = st.radio("نوع الترميز", ["Label Encoding", "One-Hot Encoding"])
            if st.button("تطبيق الترميز"):
                if enc_type == "Label Encoding":
                    df[col_enc] = df[col_enc].astype("category").cat.codes
                else:
                    df = pd.get_dummies(df, columns=[col_enc])
                st.session_state.df = df
                st.success("✅ تم تطبيق الترميز")
                add_result("Data Transform", "Categorical Encoding", {
                    "column": col_enc,
                    "method": enc_type,
                })
        else:
            st.info("لا توجد أعمدة فئوية حالياً")

        st.markdown("---")
        st.subheader("⬇️ تنزيل البيانات الحالية")
        csv_bytes = st.session_state.df.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            "تنزيل البيانات المنظفة CSV",
            data=csv_bytes,
            file_name=f"cleaned_{st.session_state.filename or 'dataset'}.csv",
            mime="text/csv",
        )
