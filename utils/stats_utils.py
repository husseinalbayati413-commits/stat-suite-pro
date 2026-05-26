"""
Statistical helper utilities for descriptive analysis, hypothesis testing,
and regression workflows used across the Streamlit app.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.multicomp import pairwise_tukeyhsd



def numeric_columns(df: pd.DataFrame) -> list[str]:
    return df.select_dtypes(include=np.number).columns.tolist()



def categorical_columns(df: pd.DataFrame) -> list[str]:
    return df.select_dtypes(exclude=np.number).columns.tolist()



def descriptive_table(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    subset = df[columns].copy().dropna(how="all")
    records = []
    for col in columns:
        s = pd.to_numeric(subset[col], errors="coerce").dropna()
        if s.empty:
            continue
        mean_val = s.mean()
        std_val = s.std(ddof=1)
        records.append({
            "variable": col,
            "count": int(s.count()),
            "missing": int(df[col].isna().sum()),
            "mean": float(mean_val),
            "median": float(s.median()),
            "std": float(std_val),
            "variance": float(s.var(ddof=1)),
            "min": float(s.min()),
            "q1": float(s.quantile(0.25)),
            "q3": float(s.quantile(0.75)),
            "max": float(s.max()),
            "range": float(s.max() - s.min()),
            "iqr": float(s.quantile(0.75) - s.quantile(0.25)),
            "cv_%": float((std_val / mean_val) * 100) if mean_val not in (0, np.nan) else np.nan,
            "skewness": float(stats.skew(s, bias=False)) if len(s) > 2 else np.nan,
            "kurtosis": float(stats.kurtosis(s, fisher=True, bias=False)) if len(s) > 3 else np.nan,
        })
    return pd.DataFrame(records)



def confidence_interval_mean(series: pd.Series, confidence: float = 0.95) -> dict:
    s = pd.to_numeric(series, errors="coerce").dropna()
    n = len(s)
    if n < 2:
        raise ValueError("At least two valid observations are required.")
    mean_val = s.mean()
    sem = stats.sem(s, nan_policy="omit")
    alpha = 1 - confidence
    t_crit = stats.t.ppf(1 - alpha / 2, df=n - 1)
    margin = sem * t_crit
    return {
        "n": n,
        "mean": float(mean_val),
        "std": float(s.std(ddof=1)),
        "standard_error": float(sem),
        "confidence": confidence,
        "ci_lower": float(mean_val - margin),
        "ci_upper": float(mean_val + margin),
        "margin_of_error": float(margin),
    }



def normality_test(series: pd.Series) -> dict:
    s = pd.to_numeric(series, errors="coerce").dropna()
    n = len(s)
    if n < 3:
        raise ValueError("At least 3 valid observations are required.")
    if n <= 5000:
        stat, p = stats.shapiro(s)
        method = "Shapiro-Wilk"
    else:
        stat, p = stats.normaltest(s)
        method = "D'Agostino K²"
    return {
        "method": method,
        "n": n,
        "statistic": float(stat),
        "p_value": float(p),
        "is_normal_at_0.05": bool(p >= 0.05),
    }



def pairwise_correlation(df: pd.DataFrame, x: str, y: str, method: str = "pearson") -> dict:
    data = df[[x, y]].dropna()
    if len(data) < 3:
        raise ValueError("Need at least 3 complete rows for correlation.")
    if method == "pearson":
        r, p = stats.pearsonr(data[x], data[y])
    elif method == "spearman":
        r, p = stats.spearmanr(data[x], data[y])
    elif method == "kendall":
        r, p = stats.kendalltau(data[x], data[y])
    else:
        raise ValueError("Unsupported correlation method.")
    return {
        "method": method,
        "n": int(len(data)),
        "coefficient": float(r),
        "p_value": float(p),
        "strength": interpret_correlation(abs(r)),
    }



def interpret_correlation(value: float) -> str:
    if value < 0.2:
        return "Very weak"
    if value < 0.4:
        return "Weak"
    if value < 0.6:
        return "Moderate"
    if value < 0.8:
        return "Strong"
    return "Very strong"



def cohens_d_independent(group1, group2) -> float:
    g1 = np.asarray(group1, dtype=float)
    g2 = np.asarray(group2, dtype=float)
    n1, n2 = len(g1), len(g2)
    if n1 < 2 or n2 < 2:
        return np.nan
    pooled_sd = np.sqrt(((n1 - 1) * g1.var(ddof=1) + (n2 - 1) * g2.var(ddof=1)) / (n1 + n2 - 2))
    if pooled_sd == 0:
        return np.nan
    return float((g1.mean() - g2.mean()) / pooled_sd)



def cohens_d_paired(before, after) -> float:
    diff = np.asarray(after, dtype=float) - np.asarray(before, dtype=float)
    if len(diff) < 2 or diff.std(ddof=1) == 0:
        return np.nan
    return float(diff.mean() / diff.std(ddof=1))



def independent_t_test(df: pd.DataFrame, value_col: str, group_col: str, group_a, group_b, equal_var: bool = False) -> dict:
    data = df[[value_col, group_col]].dropna()
    g1 = pd.to_numeric(data.loc[data[group_col] == group_a, value_col], errors="coerce").dropna()
    g2 = pd.to_numeric(data.loc[data[group_col] == group_b, value_col], errors="coerce").dropna()
    if len(g1) < 2 or len(g2) < 2:
        raise ValueError("Each group must contain at least 2 valid values.")
    stat, p = stats.ttest_ind(g1, g2, equal_var=equal_var)
    return {
        "group_a": str(group_a),
        "group_b": str(group_b),
        "n_group_a": int(len(g1)),
        "n_group_b": int(len(g2)),
        "mean_group_a": float(g1.mean()),
        "mean_group_b": float(g2.mean()),
        "t_statistic": float(stat),
        "p_value": float(p),
        "cohens_d": cohens_d_independent(g1, g2),
    }



def paired_t_test(df: pd.DataFrame, before_col: str, after_col: str) -> dict:
    data = df[[before_col, after_col]].dropna()
    if len(data) < 2:
        raise ValueError("Need at least 2 paired observations.")
    stat, p = stats.ttest_rel(data[before_col], data[after_col])
    return {
        "n": int(len(data)),
        "mean_before": float(data[before_col].mean()),
        "mean_after": float(data[after_col].mean()),
        "mean_difference": float((data[after_col] - data[before_col]).mean()),
        "t_statistic": float(stat),
        "p_value": float(p),
        "cohens_d": cohens_d_paired(data[before_col], data[after_col]),
    }



def one_way_anova(df: pd.DataFrame, value_col: str, group_col: str) -> tuple[dict, pd.DataFrame | None]:
    data = df[[value_col, group_col]].dropna()
    groups = [pd.to_numeric(g[value_col], errors="coerce").dropna().values for _, g in data.groupby(group_col)]
    labels = list(data[group_col].dropna().unique())
    if len(groups) < 2:
        raise ValueError("At least two groups are required.")
    if any(len(g) < 2 for g in groups):
        raise ValueError("Each group should have at least 2 observations.")
    stat, p = stats.f_oneway(*groups)
    grand_mean = pd.to_numeric(data[value_col], errors="coerce").mean()
    ss_between = sum(len(g) * (np.mean(g) - grand_mean) ** 2 for g in groups)
    ss_total = sum(((g - grand_mean) ** 2).sum() for g in groups)
    eta_sq = ss_between / ss_total if ss_total != 0 else np.nan
    result = {
        "groups": len(groups),
        "f_statistic": float(stat),
        "p_value": float(p),
        "eta_squared": float(eta_sq) if eta_sq == eta_sq else np.nan,
    }
    tukey_df = None
    if len(labels) >= 3:
        tukey = pairwise_tukeyhsd(endog=data[value_col], groups=data[group_col], alpha=0.05)
        tukey_df = pd.DataFrame(tukey._results_table.data[1:], columns=tukey._results_table.data[0])
    return result, tukey_df



def chi_square_test(df: pd.DataFrame, col1: str, col2: str) -> tuple[dict, pd.DataFrame]:
    contingency = pd.crosstab(df[col1], df[col2])
    if contingency.empty:
        raise ValueError("Contingency table is empty.")
    chi2, p, dof, expected = stats.chi2_contingency(contingency)
    n = contingency.to_numpy().sum()
    phi2 = chi2 / n if n else np.nan
    r, k = contingency.shape
    cramers_v = np.sqrt(phi2 / max(min(k - 1, r - 1), 1)) if n else np.nan
    result = {
        "rows": int(r),
        "cols": int(k),
        "chi2": float(chi2),
        "p_value": float(p),
        "dof": int(dof),
        "cramers_v": float(cramers_v) if cramers_v == cramers_v else np.nan,
    }
    expected_df = pd.DataFrame(expected, index=contingency.index, columns=contingency.columns)
    return result, expected_df



def outlier_summary(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    records = []
    for col in columns:
        s = pd.to_numeric(df[col], errors="coerce").dropna()
        if len(s) < 3:
            continue
        z_scores = np.abs(stats.zscore(s, nan_policy="omit"))
        q1, q3 = s.quantile(0.25), s.quantile(0.75)
        iqr = q3 - q1
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        records.append({
            "variable": col,
            "n": int(len(s)),
            "zscore_outliers": int((z_scores > 3).sum()),
            "iqr_outliers": int(((s < lower) | (s > upper)).sum()),
            "lower_bound": float(lower),
            "upper_bound": float(upper),
        })
    return pd.DataFrame(records)



def vif_table(df: pd.DataFrame, features: list[str]) -> pd.DataFrame:
    X = df[features].dropna().copy()
    if X.empty or len(X) < 3:
        return pd.DataFrame()
    X_const = sm.add_constant(X)
    vif_values = []
    for i, col in enumerate(X_const.columns):
        if col == "const":
            continue
        vif_values.append({
            "feature": col,
            "VIF": float(variance_inflation_factor(X_const.values, i))
        })
    return pd.DataFrame(vif_values)



def regression_analysis(df: pd.DataFrame, features: list[str], target: str, test_size: float = 0.2) -> dict:
    data = df[features + [target]].dropna()
    if len(data) < 8:
        raise ValueError("Regression requires at least 8 complete rows.")
    X = data[features]
    y = data[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )
    model = LinearRegression()
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    X_sm = sm.add_constant(X)
    ols_model = sm.OLS(y, X_sm).fit()
    coef_df = pd.DataFrame({
        "feature": ["Intercept"] + features,
        "coefficient": [ols_model.params.iloc[0]] + ols_model.params.iloc[1:].tolist(),
        "p_value": [ols_model.pvalues.iloc[0]] + ols_model.pvalues.iloc[1:].tolist(),
        "ci_lower": [ols_model.conf_int().iloc[0, 0]] + ols_model.conf_int().iloc[1:, 0].tolist(),
        "ci_upper": [ols_model.conf_int().iloc[0, 1]] + ols_model.conf_int().iloc[1:, 1].tolist(),
    })

    fitted_all = model.predict(X)
    residuals = y - fitted_all

    return {
        "n": int(len(data)),
        "train_rows": int(len(X_train)),
        "test_rows": int(len(X_test)),
        "r2_test": float(r2_score(y_test, preds)),
        "rmse_test": float(np.sqrt(mean_squared_error(y_test, preds))),
        "mae_test": float(mean_absolute_error(y_test, preds)),
        "r2_adjusted": float(ols_model.rsquared_adj),
        "f_statistic": float(ols_model.fvalue) if ols_model.fvalue is not None else np.nan,
        "f_p_value": float(ols_model.f_pvalue) if ols_model.f_pvalue is not None else np.nan,
        "coefficients": coef_df,
        "pred_actual": pd.DataFrame({"actual": y_test.values, "predicted": preds}),
        "residuals": pd.DataFrame({"fitted": fitted_all, "residual": residuals}),
        "summary_text": ols_model.summary().as_text(),
        "vif": vif_table(data, features),
    }



def polynomial_regression_analysis(df: pd.DataFrame, feature: str, target: str, degree: int = 2, test_size: float = 0.2) -> dict:
    data = df[[feature, target]].dropna()
    if len(data) < 8:
        raise ValueError("Polynomial regression requires at least 8 complete rows.")
    X = data[[feature]]
    y = data[target]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )
    model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    grid = pd.DataFrame({feature: np.linspace(X[feature].min(), X[feature].max(), 200)})
    grid["prediction"] = model.predict(grid[[feature]])

    return {
        "n": int(len(data)),
        "degree": int(degree),
        "r2_test": float(r2_score(y_test, preds)),
        "rmse_test": float(np.sqrt(mean_squared_error(y_test, preds))),
        "mae_test": float(mean_absolute_error(y_test, preds)),
        "grid": grid,
        "raw": data,
    }
