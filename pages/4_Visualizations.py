"""
Page 4 — Interactive Visualizations using Plotly
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.theme import apply_theme, render_header
from utils.session import init_session

st.set_page_config(page_title="Visualizations", page_icon="icon.png", layout="wide")
init_session()
apply_theme()
render_header()

st.markdown("## 📊 Interactive Visualizations — الرسوم التفاعلية")

df = st.session_state.df
if df is None:
    st.info("⚠️ حمّل بيانات من Data Lab أولاً")
    st.stop()

num_cols = df.select_dtypes(include=np.number).columns.tolist()
cat_cols = df.select_dtypes(exclude=np.number).columns.tolist()
all_cols = df.columns.tolist()

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Histogram", "📦 Box Plot", "🔵 Scatter",
    "🔥 Heatmap", "📈 Line", "🌐 3D",
])

# ===== HISTOGRAM =====
with tab1:
    st.subheader("📊 Histogram")
    if num_cols:
        col = st.selectbox("العمود", num_cols, key="hist_c")
        bins = st.slider("عدد الفئات", 5, 100, 30)
        color = st.selectbox("تلوين حسب (اختياري)",
                             ["—"] + cat_cols, key="hist_color")
        fig = px.histogram(df, x=col, nbins=bins,
                           color=None if color == "—" else color,
                           marginal="box", template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

# ===== BOX PLOT =====
with tab2:
    st.subheader("📦 Box Plot")
    if num_cols:
        col_y = st.selectbox("Y (رقمي)", num_cols, key="box_y")
        col_x = st.selectbox("X (فئوي - اختياري)",
                             ["—"] + cat_cols, key="box_x")
        fig = px.box(df, y=col_y,
                     x=None if col_x == "—" else col_x,
                     color=None if col_x == "—" else col_x,
                     template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

# ===== SCATTER =====
with tab3:
    st.subheader("🔵 Scatter Plot")
    if len(num_cols) >= 2:
        x = st.selectbox("X", num_cols, key="sc_x")
        y = st.selectbox("Y", num_cols, key="sc_y",
                         index=1 if len(num_cols) > 1 else 0)
        color = st.selectbox("Color", ["—"] + all_cols, key="sc_c")
        size = st.selectbox("Size", ["—"] + num_cols, key="sc_s")
        trendline = st.checkbox("أضف خط اتجاه (OLS)")
        fig = px.scatter(df, x=x, y=y,
                         color=None if color == "—" else color,
                         size=None if size == "—" else size,
                         trendline="ols" if trendline else None,
                         template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

# ===== HEATMAP =====
with tab4:
    st.subheader("🔥 Correlation Heatmap")
    if len(num_cols) >= 2:
        method = st.radio("الطريقة", ["pearson", "spearman", "kendall"],
                          horizontal=True)
        corr = df[num_cols].corr(method=method)
        fig = px.imshow(corr, text_auto=".2f",
                        color_continuous_scale="RdBu_r",
                        zmin=-1, zmax=1, aspect="auto",
                        title=f"{method.capitalize()} Correlation")
        st.plotly_chart(fig, use_container_width=True)

# ===== LINE =====
with tab5:
    st.subheader("📈 Line Chart")
    if num_cols:
        cols_sel = st.multiselect("الأعمدة", num_cols,
                                  default=num_cols[:2] if len(num_cols) >= 2 else num_cols)
        if cols_sel:
            fig = px.line(df[cols_sel], template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)

# ===== 3D =====
with tab6:
    st.subheader("🌐 3D Scatter")
    if len(num_cols) >= 3:
        x = st.selectbox("X", num_cols, key="3d_x")
        y = st.selectbox("Y", num_cols, key="3d_y",
                         index=1 if len(num_cols) > 1 else 0)
        z = st.selectbox("Z", num_cols, key="3d_z",
                         index=2 if len(num_cols) > 2 else 0)
        color = st.selectbox("Color", ["—"] + all_cols, key="3d_c")
        fig = px.scatter_3d(df, x=x, y=y, z=z,
                            color=None if color == "—" else color,
                            template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("نحتاج 3 أعمدة رقمية على الأقل")


from utils.theme import render_footer
render_footer()
