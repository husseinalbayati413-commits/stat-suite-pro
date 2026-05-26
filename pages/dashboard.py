import os
import sys
import streamlit as st
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.theme import apply_theme, render_header
from utils.session import init_session

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
init_session()
apply_theme()
render_header()

st.markdown("## 📊 Quick Dashboard — لوحة سريعة")

df = st.session_state.get("df")
if df is None:
    st.info("حمّل البيانات أولاً لعرض مؤشرات اللوحة السريعة.")
else:
    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Numeric Columns", len(num_cols))
    col4.metric("Missing Values", int(df.isnull().sum().sum()))

    st.dataframe(df.head(10), use_container_width=True)
