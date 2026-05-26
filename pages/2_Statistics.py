"""
Page 2 — Advanced Statistics & Regression
Comprehensive descriptive statistics, tests, and regression diagnostics.
"""
import os
import sys
import json

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.theme import apply_theme, render_header
from utils.session import init_session, add_result
from utils.stats_utils import (
    numeric_columns,
    categorical_columns,
    descriptive_table,
    confidence_interval_mean,
    normality_test,
    pairwise_correlation,
    independent_t_test,
    paired_t_test,
    one_way_anova,
    chi_square_test,
    outlier_summary,
    regression_analysis,
    polynomial_regression_analysis,
)

st.set_page_config(page_title="Advanced Statistics", page_icon="📈", layout="wide")
init_session()
apply_theme()
render_header()

st.markdown("## 📈 Statistics & Regression Center — مركز الإحصاء والانحدار")
st.caption("إحصاء وصفي، اختبارات فرضيات، ارتباط، قيم شاذة، وانحدار تشخيصي متقدم")

df = st.session_state.df
if df is None:
    st.info("⚠️ حمّل بياناتك أولاً من صفحة Data Lab")
    st.stop()

num_cols = numeric_columns(df)
cat_cols = categorical_columns(df)
all_cols = df.columns.tolist()

if not num_cols:
    st.warning("لا توجد أعمدة رقمية كافية لإجراء التحليل الإحصائي.")
    st.stop()

m1, m2, m3, m4 = st.columns(4)
m1.metric("الأعمدة الرقمية", len(num_cols))
m2.metric("الأعمدة الفئوية", len(cat_cols))
m3.metric("إجمالي الصفوف", df.shape[0])
m4.metric("القيم المفقودة", int(df.isnull().sum().sum()))

main_tabs = st.tabs([
    "📊 الإحصاء الوصفي",
    "📏 التوزيع وفترات الثقة",
    "🔗 الارتباط",
    "🧪 اختبارات الفرضيات",
    "🚨 القيم الشاذة",
    "📈 الانحدار",
])

with main_tabs[0]:
    st.subheader("الإحصاء الوصفي المتقدم")
    selected_desc = st.multiselect(
        "الأعمدة المراد تحليلها",
        num_cols,
        default=num_cols[: min(6, len(num_cols))],
    )

    if selected_desc:
        desc_df = descriptive_table(df, selected_desc).round(4)
        st.dataframe(desc_df, use_container_width=True)

        st.download_button(
            "⬇️ تنزيل الجدول الوصفي CSV",
            desc_df.to_csv(index=False).encode("utf-8-sig"),
            file_name="descriptive_statistics.csv",
            mime="text/csv",
        )

        add_preview = desc_df[["variable", "mean", "std", "skewness", "kurtosis"]].fillna(0)
        fig = px.bar(
            add_preview,
            x="variable",
            y="mean",
            error_y="std",
            title="Mean ± Std",
            template="plotly_white",
        )
        st.plotly_chart(fig, use_container_width=True)

        if st.button("💾 حفظ النتيجة الوصفية في السجل"):
            add_result(
                "Statistics",
                "Descriptive Statistics",
                {
                    "variables": ", ".join(selected_desc),
                    "records": int(len(desc_df)),
                    "avg_mean": round(float(desc_df["mean"].mean()), 4),
                    "avg_std": round(float(desc_df["std"].mean()), 4),
                },
            )
            st.success("✅ تم حفظ الملخص في سجل النتائج")

with main_tabs[1]:
    st.subheader("طبيعية التوزيع وفترات الثقة")
    col1, col2 = st.columns(2)

    with col1:
        normality_col = st.selectbox("عمود فحص الطبيعية", num_cols)
        if st.button("تشغيل اختبار الطبيعية"):
            try:
                result = normality_test(df[normality_col])
                st.json(result)
                hist = px.histogram(df, x=normality_col, marginal="box", nbins=30, template="plotly_white")
                st.plotly_chart(hist, use_container_width=True)
                add_result("Statistics", "Normality Test", {"column": normality_col, **result})
            except Exception as e:
                st.error(f"خطأ: {e}")

    with col2:
        ci_col = st.selectbox("عمود فترة الثقة", num_cols, key="ci_col")
        confidence = st.slider("مستوى الثقة", 0.80, 0.99, 0.95, 0.01)
        if st.button("احسب فترة الثقة"):
            try:
                ci = confidence_interval_mean(df[ci_col], confidence)
                st.json(ci)
                add_result("Statistics", "Confidence Interval", {"column": ci_col, **ci})
            except Exception as e:
                st.error(f"خطأ: {e}")

with main_tabs[2]:
    st.subheader("تحليل الارتباط")
    corr_tabs = st.tabs(["مصفوفة الارتباط", "علاقة بين متغيرين"])

    with corr_tabs[0]:
        method = st.radio("طريقة الارتباط", ["pearson", "spearman", "kendall"], horizontal=True)
        corr = df[num_cols].corr(method=method)
        heatmap = px.imshow(
            corr.round(2),
            text_auto=True,
            color_continuous_scale="RdBu_r",
            zmin=-1,
            zmax=1,
            title=f"{method.capitalize()} Correlation Matrix",
        )
        st.plotly_chart(heatmap, use_container_width=True)
        st.dataframe(corr.round(4), use_container_width=True)

    with corr_tabs[1]:
        x = st.selectbox("X", num_cols, key="corr_x")
        y = st.selectbox("Y", num_cols, key="corr_y", index=1 if len(num_cols) > 1 else 0)
        method_pair = st.selectbox("طريقة التحليل", ["pearson", "spearman", "kendall"], key="corr_method")
        if st.button("تحليل العلاقة"):
            try:
                result = pairwise_correlation(df, x, y, method_pair)
                st.json(result)
                fig = px.scatter(df, x=x, y=y, trendline="ols", template="plotly_white")
                st.plotly_chart(fig, use_container_width=True)
                add_result("Statistics", "Correlation", {"x": x, "y": y, **result})
            except Exception as e:
                st.error(f"خطأ: {e}")

with main_tabs[3]:
    st.subheader("اختبارات الفرضيات")
    test_tabs = st.tabs(["Independent T-Test", "Paired T-Test", "ANOVA", "Chi-Square"])

    with test_tabs[0]:
        if not cat_cols:
            st.info("نحتاج عموداً فئوياً لإجراء Independent T-Test.")
        else:
            group_col = st.selectbox("عمود المجموعات", cat_cols, key="ind_group")
            value_col = st.selectbox("العمود الرقمي", num_cols, key="ind_value")
            groups = df[group_col].dropna().astype(str).unique().tolist()
            if len(groups) >= 2:
                g1 = st.selectbox("المجموعة الأولى", groups, key="g1")
                g2 = st.selectbox("المجموعة الثانية", groups, index=1, key="g2")
                equal_var = st.checkbox("افتراض تساوي التباين", value=False)
                if st.button("تشغيل Independent T-Test"):
                    try:
                        res = independent_t_test(df, value_col, group_col, g1, g2, equal_var)
                        st.json(res)
                        fig = px.box(df[df[group_col].astype(str).isin([g1, g2])], x=group_col, y=value_col, color=group_col, template="plotly_white")
                        st.plotly_chart(fig, use_container_width=True)
                        add_result("Hypothesis Test", "Independent T-Test", {"value_col": value_col, "group_col": group_col, **res})
                    except Exception as e:
                        st.error(f"خطأ: {e}")
            else:
                st.warning("يجب أن يحتوي العمود الفئوي على مجموعتين على الأقل.")

    with test_tabs[1]:
        before_col = st.selectbox("القياس الأول", num_cols, key="paired_before")
        after_col = st.selectbox("القياس الثاني", num_cols, key="paired_after", index=1 if len(num_cols) > 1 else 0)
        if st.button("تشغيل Paired T-Test"):
            try:
                res = paired_t_test(df, before_col, after_col)
                st.json(res)
                paired_df = df[[before_col, after_col]].dropna().melt(var_name="Measure", value_name="Value")
                fig = px.box(paired_df, x="Measure", y="Value", color="Measure", template="plotly_white")
                st.plotly_chart(fig, use_container_width=True)
                add_result("Hypothesis Test", "Paired T-Test", {"before": before_col, "after": after_col, **res})
            except Exception as e:
                st.error(f"خطأ: {e}")

    with test_tabs[2]:
        if not cat_cols:
            st.info("نحتاج عموداً فئوياً لإجراء ANOVA.")
        else:
            anova_value = st.selectbox("المتغير الرقمي", num_cols, key="anova_value")
            anova_group = st.selectbox("المتغير الفئوي", cat_cols, key="anova_group")
            if st.button("تشغيل One-Way ANOVA"):
                try:
                    res, tukey_df = one_way_anova(df, anova_value, anova_group)
                    st.json(res)
                    fig = px.box(df, x=anova_group, y=anova_value, color=anova_group, template="plotly_white")
                    st.plotly_chart(fig, use_container_width=True)
                    if tukey_df is not None and not tukey_df.empty:
                        st.markdown("### Tukey Post-hoc")
                        st.dataframe(tukey_df, use_container_width=True)
                    add_result("Hypothesis Test", "One-Way ANOVA", {"value": anova_value, "group": anova_group, **res})
                except Exception as e:
                    st.error(f"خطأ: {e}")

    with test_tabs[3]:
        if len(cat_cols) < 2:
            st.info("نحتاج عمودين فئويين لإجراء Chi-Square.")
        else:
            chi_1 = st.selectbox("المتغير الفئوي الأول", cat_cols, key="chi1")
            chi_2 = st.selectbox("المتغير الفئوي الثاني", cat_cols, index=1, key="chi2")
            if st.button("تشغيل Chi-Square"):
                try:
                    res, expected_df = chi_square_test(df, chi_1, chi_2)
                    contingency = pd.crosstab(df[chi_1], df[chi_2])
                    st.json(res)
                    st.markdown("### Contingency Table")
                    st.dataframe(contingency, use_container_width=True)
                    st.markdown("### Expected Frequencies")
                    st.dataframe(expected_df.round(3), use_container_width=True)
                    fig = px.imshow(contingency, text_auto=True, color_continuous_scale="Blues")
                    st.plotly_chart(fig, use_container_width=True)
                    add_result("Hypothesis Test", "Chi-Square", {"col1": chi_1, "col2": chi_2, **res})
                except Exception as e:
                    st.error(f"خطأ: {e}")

with main_tabs[4]:
    st.subheader("كشف القيم الشاذة")
    selected_outliers = st.multiselect(
        "أعمدة الفحص",
        num_cols,
        default=num_cols[: min(5, len(num_cols))],
        key="outlier_cols",
    )
    if selected_outliers:
        out_df = outlier_summary(df, selected_outliers)
        st.dataframe(out_df, use_container_width=True)
        st.download_button(
            "⬇️ تنزيل تقرير القيم الشاذة CSV",
            out_df.to_csv(index=False).encode("utf-8-sig"),
            file_name="outlier_summary.csv",
            mime="text/csv",
        )
        chosen = st.selectbox("رسم عمود", selected_outliers, key="outlier_plot_col")
        fig = px.box(df, y=chosen, points="outliers", template="plotly_white", title=f"Outlier View — {chosen}")
        st.plotly_chart(fig, use_container_width=True)

        if st.button("💾 حفظ تقرير القيم الشاذة"):
            add_result(
                "Statistics",
                "Outlier Summary",
                {"variables": ", ".join(selected_outliers), "rows": int(len(out_df))},
            )
            st.success("✅ تم الحفظ")

with main_tabs[5]:
    st.subheader("تحليل الانحدار")
    reg_tabs = st.tabs(["انحدار خطي متعدد", "انحدار متعدد الحدود"])

    with reg_tabs[0]:
        if len(num_cols) < 2:
            st.warning("نحتاج عمودين رقميين على الأقل")
        else:
            features = st.multiselect(
                "المتغيرات المستقلة X",
                num_cols,
                default=num_cols[:-1] if len(num_cols) > 1 else num_cols,
                key="reg_features",
            )
            target = st.selectbox(
                "المتغير التابع y",
                [c for c in num_cols if c not in features] or num_cols,
                key="reg_target",
            )
            test_size = st.slider("نسبة الاختبار", 0.1, 0.4, 0.2, 0.05, key="reg_test_size")

            if st.button("تشغيل الانحدار الخطي"):
                if not features:
                    st.warning("اختر متغيراً مستقلاً واحداً على الأقل")
                elif target in features:
                    st.warning("المتغير التابع يجب ألا يكون ضمن X")
                else:
                    try:
                        result = regression_analysis(df, features, target, test_size)
                        c1, c2, c3, c4 = st.columns(4)
                        c1.metric("R² Test", f"{result['r2_test']:.4f}")
                        c2.metric("Adjusted R²", f"{result['r2_adjusted']:.4f}")
                        c3.metric("RMSE", f"{result['rmse_test']:.4f}")
                        c4.metric("MAE", f"{result['mae_test']:.4f}")

                        st.markdown("### معاملات النموذج واختبار الدلالة")
                        st.dataframe(result["coefficients"].round(6), use_container_width=True)

                        if not result["vif"].empty:
                            st.markdown("### VIF — فحص التعدد الخطي")
                            st.dataframe(result["vif"].round(4), use_container_width=True)

                        pred_fig = px.scatter(
                            result["pred_actual"],
                            x="actual",
                            y="predicted",
                            trendline="ols",
                            template="plotly_white",
                            title="Actual vs Predicted",
                        )
                        min_val = result["pred_actual"]["actual"].min()
                        max_val = result["pred_actual"]["actual"].max()
                        pred_fig.add_trace(go.Scatter(x=[min_val, max_val], y=[min_val, max_val], mode="lines", name="Ideal", line=dict(color="red", dash="dash")))
                        st.plotly_chart(pred_fig, use_container_width=True)

                        resid_fig = px.scatter(
                            result["residuals"],
                            x="fitted",
                            y="residual",
                            template="plotly_white",
                            title="Residuals vs Fitted",
                        )
                        resid_fig.add_hline(y=0, line_dash="dash", line_color="red")
                        st.plotly_chart(resid_fig, use_container_width=True)

                        st.markdown("### ملخص OLS الكامل")
                        st.code(result["summary_text"], language="text")

                        export_json = {
                            "features": features,
                            "target": target,
                            "n": result["n"],
                            "r2_test": result["r2_test"],
                            "r2_adjusted": result["r2_adjusted"],
                            "rmse_test": result["rmse_test"],
                            "mae_test": result["mae_test"],
                            "f_statistic": result["f_statistic"],
                            "f_p_value": result["f_p_value"],
                        }
                        st.download_button(
                            "⬇️ تنزيل ملخص الانحدار JSON",
                            json.dumps(export_json, ensure_ascii=False, indent=2),
                            file_name="linear_regression_summary.json",
                            mime="application/json",
                        )

                        add_result("Regression", "Multiple Linear Regression", export_json)
                    except Exception as e:
                        st.error(f"خطأ: {e}")

    with reg_tabs[1]:
        x_poly = st.selectbox("المتغير المستقل", num_cols, key="poly_x")
        y_poly_candidates = [c for c in num_cols if c != x_poly] or num_cols
        y_poly = st.selectbox("المتغير التابع", y_poly_candidates, key="poly_y")
        degree = st.slider("درجة متعدد الحدود", 2, 5, 2)
        poly_test_size = st.slider("نسبة الاختبار", 0.1, 0.4, 0.2, 0.05, key="poly_test")

        if st.button("تشغيل Polynomial Regression"):
            try:
                result = polynomial_regression_analysis(df, x_poly, y_poly, degree, poly_test_size)
                c1, c2, c3 = st.columns(3)
                c1.metric("R² Test", f"{result['r2_test']:.4f}")
                c2.metric("RMSE", f"{result['rmse_test']:.4f}")
                c3.metric("MAE", f"{result['mae_test']:.4f}")

                fig = px.scatter(result["raw"], x=x_poly, y=y_poly, template="plotly_white", title="Polynomial Regression")
                fig.add_trace(go.Scatter(x=result["grid"][x_poly], y=result["grid"]["prediction"], mode="lines", name=f"Degree {degree}", line=dict(color="#4f46e5", width=3)))
                st.plotly_chart(fig, use_container_width=True)

                poly_summary = {
                    "feature": x_poly,
                    "target": y_poly,
                    "degree": degree,
                    "n": result["n"],
                    "r2_test": result["r2_test"],
                    "rmse_test": result["rmse_test"],
                    "mae_test": result["mae_test"],
                }
                add_result("Regression", "Polynomial Regression", poly_summary)
                st.download_button(
                    "⬇️ تنزيل بيانات المنحنى CSV",
                    result["grid"].to_csv(index=False).encode("utf-8-sig"),
                    file_name="polynomial_curve.csv",
                    mime="text/csv",
                )
            except Exception as e:
                st.error(f"خطأ: {e}")


from utils.theme import render_footer
render_footer()
