"""
Data loading & preprocessing utilities
"""
import pandas as pd
import numpy as np


def load_file(uploaded_file):
    """Read CSV or Excel uploaded file into a DataFrame."""
    name = uploaded_file.name.lower()
    if name.endswith(".csv"):
        try:
            return pd.read_csv(uploaded_file)
        except UnicodeDecodeError:
            uploaded_file.seek(0)
            return pd.read_csv(uploaded_file, encoding="latin-1")
    elif name.endswith((".xls", ".xlsx")):
        return pd.read_excel(uploaded_file)
    else:
        raise ValueError("نوع الملف غير مدعوم. CSV أو Excel فقط.")


def summary_dict(df: pd.DataFrame) -> dict:
    """Return a small summary dict used by the PDF generator."""
    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    cat_cols = df.select_dtypes(exclude=np.number).columns.tolist()
    return {
        "rows": df.shape[0],
        "cols": df.shape[1],
        "numeric_cols": len(num_cols),
        "categorical_cols": len(cat_cols),
        "missing": int(df.isnull().sum().sum()),
        "describe": df.describe().round(3) if num_cols else pd.DataFrame(),
    }


def fill_missing(df: pd.DataFrame, strategy: str = "mean") -> pd.DataFrame:
    """Fill missing values with the chosen strategy."""
    df = df.copy()
    num_cols = df.select_dtypes(include=np.number).columns
    cat_cols = df.select_dtypes(exclude=np.number).columns

    if strategy == "mean":
        df[num_cols] = df[num_cols].fillna(df[num_cols].mean())
    elif strategy == "median":
        df[num_cols] = df[num_cols].fillna(df[num_cols].median())
    elif strategy == "zero":
        df[num_cols] = df[num_cols].fillna(0)
    elif strategy == "drop":
        df = df.dropna()

    # Categorical → fill with mode
    for c in cat_cols:
        if df[c].isnull().any() and len(df[c].mode()) > 0:
            df[c] = df[c].fillna(df[c].mode()[0])
    return df


def parse_numbers(text: str):
    """Parse comma-separated numbers from a textarea."""
    return [float(x.strip()) for x in text.replace("\n", ",").split(",")
            if x.strip()]
