"""
Page 3 — Machine Learning
Linear/Logistic Regression, K-Means, Decision Tree, Random Forest.
"""
import streamlit as st
import pandas as pd
import numpy as np
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.cluster import KMeans
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import (
    mean_squared_error, r2_score, mean_absolute_error,
    accuracy_score, classification_report, confusion_matrix,
    silhouette_score,
)
import plotly.express as px
import plotly.graph_objects as go

from utils.theme import apply_theme, render_header
from utils.session import init_session, add_result

st.set_page_config(page_title="Machine Learning", page_icon="🤖",
                   layout="wide")
init_session()
apply_theme()
render_header()

st.markdown("## 🤖 Machine Learning — تعلم الآلة")

df = st.session_state.df
if df is None:
    st.info("⚠️ حمّل بيانات من Data Lab أولاً")
    st.stop()

num_cols = df.select_dtypes(include=np.number).columns.tolist()
all_cols = df.columns.tolist()

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Linear Regression",
    "🎯 Logistic Regression",
    "🧩 K-Means",
    "🌳 Decision Tree",
    "🌲 Random Forest",
])

# ============================================================
# 1. LINEAR REGRESSION
# ============================================================
with tab1:
    st.subheader("📈 Linear Regression — الانحدار الخطي")
    if len(num_cols) < 2:
        st.warning("نحتاج عمودين رقميين على الأقل")
    else:
        features = st.multiselect("المتغيرات المستقلة (X)", num_cols,
                                  default=num_cols[:-1])
        target = st.selectbox("المتغير التابع (y)", num_cols,
                              index=len(num_cols)-1)
        test_size = st.slider("نسبة الاختبار", 0.1, 0.5, 0.2, 0.05)

        if st.button("🚀 درّب النموذج", key="train_lr"):
            X = df[features].dropna()
            y = df[target].loc[X.index]
            mask = y.notna()
            X, y = X[mask], y[mask]

            X_tr, X_te, y_tr, y_te = train_test_split(
                X, y, test_size=test_size, random_state=42)
            model = LinearRegression()
            model.fit(X_tr, y_tr)
            preds = model.predict(X_te)

            r2 = r2_score(y_te, preds)
            mse = mean_squared_error(y_te, preds)
            mae = mean_absolute_error(y_te, preds)

            c1, c2, c3 = st.columns(3)
            c1.metric("R²", f"{r2:.4f}")
            c2.metric("MSE", f"{mse:.4f}")
            c3.metric("MAE", f"{mae:.4f}")

            st.markdown("**معاملات النموذج**")
            coef_df = pd.DataFrame({
                "Feature": features,
                "Coefficient": model.coef_,
            })
            st.dataframe(coef_df, use_container_width=True)
            st.write(f"**Intercept:** {model.intercept_:.4f}")

            fig = px.scatter(x=y_te, y=preds,
                             labels={"x": "Actual", "y": "Predicted"},
                             title="Actual vs Predicted")
            fig.add_trace(go.Scatter(x=[y_te.min(), y_te.max()],
                                     y=[y_te.min(), y_te.max()],
                                     mode="lines", name="Ideal",
                                     line=dict(dash="dash", color="red")))
            st.plotly_chart(fig, use_container_width=True)

            st.session_state.ml_models["Linear Regression"] = model
            add_result("ML — Regression", f"Linear: {target} ~ {features}", {
                "R²": round(r2, 4), "MSE": round(mse, 4),
                "MAE": round(mae, 4),
            })

# ============================================================
# 2. LOGISTIC REGRESSION
# ============================================================
with tab2:
    st.subheader("🎯 Logistic Regression — الانحدار اللوجستي")
    features = st.multiselect("المتغيرات المستقلة (X)", num_cols,
                              default=num_cols[:-1] if len(num_cols) > 1 else num_cols,
                              key="logit_x")
    target = st.selectbox("المتغير التابع (تصنيف)", all_cols,
                          index=len(all_cols)-1, key="logit_y")
    test_size = st.slider("نسبة الاختبار", 0.1, 0.5, 0.2, 0.05,
                          key="logit_ts")

    if st.button("🚀 درّب النموذج", key="train_logit"):
        try:
            X = df[features].dropna()
            y_raw = df[target].loc[X.index]

            if not pd.api.types.is_numeric_dtype(y_raw):
                y = y_raw.astype("category").cat.codes
            else:
                y = y_raw

            mask = y.notna()
            X, y = X[mask], y[mask]

            scaler = StandardScaler()
            X_sc = scaler.fit_transform(X)

            X_tr, X_te, y_tr, y_te = train_test_split(
                X_sc, y, test_size=test_size, random_state=42, stratify=y)
            model = LogisticRegression(max_iter=1000)
            model.fit(X_tr, y_tr)
            preds = model.predict(X_te)
            acc = accuracy_score(y_te, preds)

            c1, c2 = st.columns(2)
            c1.metric("Accuracy", f"{acc:.4f}")
            c2.metric("الفئات", len(np.unique(y)))

            st.markdown("**Confusion Matrix**")
            cm = confusion_matrix(y_te, preds)
            fig = px.imshow(cm, text_auto=True, color_continuous_scale="Blues",
                            labels=dict(x="Predicted", y="Actual"))
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("**Classification Report**")
            report = classification_report(y_te, preds, output_dict=True)
            st.dataframe(pd.DataFrame(report).T, use_container_width=True)

            st.session_state.ml_models["Logistic Regression"] = model
            add_result("ML — Classification", f"Logistic: {target}", {
                "Accuracy": round(acc, 4),
                "n_features": len(features),
                "n_classes": int(len(np.unique(y))),
            })
        except Exception as e:
            st.error(f"خطأ: {e}")

# ============================================================
# 3. K-MEANS
# ============================================================
with tab3:
    st.subheader("🧩 K-Means Clustering — التجميع")
    features = st.multiselect("المتغيرات للتجميع", num_cols,
                              default=num_cols[:2] if len(num_cols) >= 2 else num_cols,
                              key="km_x")
    k = st.slider("عدد المجموعات (K)", 2, 10, 3)
    use_elbow = st.checkbox("اعرض Elbow Method", value=True)

    if st.button("🚀 شغّل K-Means", key="train_km"):
        if len(features) < 2:
            st.warning("اختر عمودين على الأقل")
        else:
            X = df[features].dropna()
            scaler = StandardScaler()
            X_sc = scaler.fit_transform(X)

            if use_elbow:
                inertias = []
                Ks = list(range(2, 11))
                for kk in Ks:
                    m = KMeans(n_clusters=kk, random_state=42, n_init=10)
                    m.fit(X_sc)
                    inertias.append(m.inertia_)
                fig_e = px.line(x=Ks, y=inertias, markers=True,
                                title="Elbow Method",
                                labels={"x": "K", "y": "Inertia"})
                st.plotly_chart(fig_e, use_container_width=True)

            model = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = model.fit_predict(X_sc)
            sil = silhouette_score(X_sc, labels)

            c1, c2 = st.columns(2)
            c1.metric("Silhouette Score", f"{sil:.4f}")
            c2.metric("Inertia", f"{model.inertia_:.2f}")

            X_plot = X.copy()
            X_plot["Cluster"] = labels.astype(str)
            if len(features) >= 2:
                fig = px.scatter(X_plot, x=features[0], y=features[1],
                                 color="Cluster", title="Clusters")
                st.plotly_chart(fig, use_container_width=True)

            st.session_state.ml_models["K-Means"] = model
            add_result("ML — Clustering", "K-Means", {
                "K": k, "Silhouette": round(sil, 4),
                "Inertia": round(model.inertia_, 2),
            })

# ============================================================
# 4. DECISION TREE
# ============================================================
with tab4:
    st.subheader("🌳 Decision Tree")
    task_type = st.radio("نوع المهمة", ["Classification", "Regression"],
                         horizontal=True, key="dt_task")
    features = st.multiselect("المتغيرات المستقلة", num_cols,
                              default=num_cols[:-1] if len(num_cols) > 1 else num_cols,
                              key="dt_x")
    target = st.selectbox("المتغير التابع", all_cols,
                          index=len(all_cols)-1, key="dt_y")
    max_depth = st.slider("Max Depth", 2, 20, 5, key="dt_d")

    if st.button("🚀 درّب", key="train_dt"):
        try:
            X = df[features].dropna()
            y_raw = df[target].loc[X.index]
            if task_type == "Classification" and not pd.api.types.is_numeric_dtype(y_raw):
                y = y_raw.astype("category").cat.codes
            else:
                y = y_raw
            mask = y.notna()
            X, y = X[mask], y[mask]

            X_tr, X_te, y_tr, y_te = train_test_split(
                X, y, test_size=0.2, random_state=42)

            if task_type == "Classification":
                model = DecisionTreeClassifier(max_depth=max_depth,
                                               random_state=42)
            else:
                model = DecisionTreeRegressor(max_depth=max_depth,
                                              random_state=42)
            model.fit(X_tr, y_tr)
            preds = model.predict(X_te)

            if task_type == "Classification":
                score = accuracy_score(y_te, preds)
                st.metric("Accuracy", f"{score:.4f}")
            else:
                score = r2_score(y_te, preds)
                st.metric("R²", f"{score:.4f}")

            imp = pd.DataFrame({
                "Feature": features,
                "Importance": model.feature_importances_,
            }).sort_values("Importance", ascending=False)
            fig = px.bar(imp, x="Importance", y="Feature", orientation="h",
                         title="Feature Importance")
            st.plotly_chart(fig, use_container_width=True)

            st.session_state.ml_models["Decision Tree"] = model
            add_result("ML — Decision Tree", f"{task_type}: {target}", {
                "score": round(score, 4),
                "max_depth": max_depth,
                "n_features": len(features),
            })
        except Exception as e:
            st.error(f"خطأ: {e}")

# ============================================================
# 5. RANDOM FOREST
# ============================================================
with tab5:
    st.subheader("🌲 Random Forest")
    task_type = st.radio("نوع المهمة", ["Classification", "Regression"],
                         horizontal=True, key="rf_task")
    features = st.multiselect("المتغيرات المستقلة", num_cols,
                              default=num_cols[:-1] if len(num_cols) > 1 else num_cols,
                              key="rf_x")
    target = st.selectbox("المتغير التابع", all_cols,
                          index=len(all_cols)-1, key="rf_y")
    n_estimators = st.slider("عدد الأشجار", 10, 500, 100, 10, key="rf_n")
    max_depth = st.slider("Max Depth", 2, 30, 10, key="rf_d")

    if st.button("🚀 درّب", key="train_rf"):
        try:
            X = df[features].dropna()
            y_raw = df[target].loc[X.index]
            if task_type == "Classification" and not pd.api.types.is_numeric_dtype(y_raw):
                y = y_raw.astype("category").cat.codes
            else:
                y = y_raw
            mask = y.notna()
            X, y = X[mask], y[mask]

            X_tr, X_te, y_tr, y_te = train_test_split(
                X, y, test_size=0.2, random_state=42)

            if task_type == "Classification":
                model = RandomForestClassifier(n_estimators=n_estimators,
                                               max_depth=max_depth,
                                               random_state=42, n_jobs=-1)
            else:
                model = RandomForestRegressor(n_estimators=n_estimators,
                                              max_depth=max_depth,
                                              random_state=42, n_jobs=-1)
            model.fit(X_tr, y_tr)
            preds = model.predict(X_te)

            if task_type == "Classification":
                score = accuracy_score(y_te, preds)
                st.metric("Accuracy", f"{score:.4f}")
                cm = confusion_matrix(y_te, preds)
                fig_cm = px.imshow(cm, text_auto=True,
                                   color_continuous_scale="Blues",
                                   labels=dict(x="Predicted", y="Actual"))
                st.plotly_chart(fig_cm, use_container_width=True)
            else:
                score = r2_score(y_te, preds)
                st.metric("R²", f"{score:.4f}")

            imp = pd.DataFrame({
                "Feature": features,
                "Importance": model.feature_importances_,
            }).sort_values("Importance", ascending=False)
            fig = px.bar(imp, x="Importance", y="Feature", orientation="h",
                         title="Feature Importance")
            st.plotly_chart(fig, use_container_width=True)

            st.session_state.ml_models["Random Forest"] = model
            add_result("ML — Random Forest", f"{task_type}: {target}", {
                "score": round(score, 4),
                "n_estimators": n_estimators,
                "max_depth": max_depth,
            })
        except Exception as e:
            st.error(f"خطأ: {e}")


from utils.theme import render_footer
render_footer()
