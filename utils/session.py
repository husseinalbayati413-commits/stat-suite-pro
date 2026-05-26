"""
Session state management — handles persistence across pages
"""
import streamlit as st
import json
import pickle
import base64
from datetime import datetime


def init_session():
    """Initialize all session state variables."""
    defaults = {
        "df": None,                # main DataFrame
        "df_original": None,       # original (untouched) copy
        "filename": None,
        "results_log": [],         # list of dicts of analysis results
        "ml_models": {},           # trained ML models
        "figures": [],             # plot figures for PDF
        "project_name": "Untitled Project",
        "created_at": datetime.now().isoformat(),
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def add_result(category: str, title: str, content: dict):
    """Append an analysis result to the results log (for PDF report)."""
    st.session_state.results_log.append({
        "category": category,
        "title": title,
        "content": content,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })


def add_figure(name: str, fig):
    """Track a matplotlib figure for inclusion in the PDF report."""
    st.session_state.figures.append({"name": name, "fig": fig})


def reset_session():
    """Reset all session data."""
    keys = list(st.session_state.keys())
    for k in keys:
        del st.session_state[k]
    init_session()


def export_session() -> str:
    """Export session as base64 string for download."""
    data = {
        "results_log": st.session_state.results_log,
        "project_name": st.session_state.project_name,
        "filename": st.session_state.filename,
        "created_at": st.session_state.created_at,
    }
    if st.session_state.df is not None:
        data["df_csv"] = st.session_state.df.to_csv(index=False)
    raw = pickle.dumps(data)
    return base64.b64encode(raw).decode()


def import_session(b64_str: str):
    """Restore session from a base64 string."""
    import pandas as pd
    from io import StringIO
    raw = base64.b64decode(b64_str.encode())
    data = pickle.loads(raw)
    st.session_state.results_log = data.get("results_log", [])
    st.session_state.project_name = data.get("project_name", "Untitled")
    st.session_state.filename = data.get("filename")
    st.session_state.created_at = data.get("created_at")
    if "df_csv" in data:
        st.session_state.df = pd.read_csv(StringIO(data["df_csv"]))
        st.session_state.df_original = st.session_state.df.copy()
