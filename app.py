"""
Stat Suite Pro
Main landing page for the Streamlit multipage app.
"""
import streamlit as st
from utils.session import init_session
from utils.theme import render_footer

st.set_page_config(
    page_title="Stat Suite Pro | AI Statistical & Research Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

init_session()

# Custom CSS for the landing page exclusively
st.markdown(
    """
    <style>
    [data-testid="collapsedControl"] { display: none; }
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .landing-hero {
        text-align: center;
        padding: 5rem 1rem;
        background: linear-gradient(180deg, #f8fbff 0%, #f3f6fb 100%);
        border-radius: 24px;
        margin-bottom: 3rem;
        border: 1px solid #dbe4f0;
        box-shadow: 0 20px 40px rgba(15,23,42,0.03);
    }
    .landing-hero h1 {
        font-size: 3.5rem;
        font-weight: 900;
        color: #0f172a;
        margin-bottom: 1.5rem;
        line-height: 1.2;
    }
    .landing-hero p {
        font-size: 1.25rem;
        color: #475569;
        max-width: 700px;
        margin: 0 auto 2.5rem auto;
        line-height: 1.6;
    }
    .hero-btn-primary {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        color: white !important;
        padding: 14px 32px;
        border-radius: 30px;
        text-decoration: none;
        font-weight: 800;
        font-size: 1.2rem;
        box-shadow: 0 10px 20px rgba(79,70,229,0.3);
        margin: 0 10px;
        transition: transform 0.2s;
        display: inline-block;
    }
    .hero-btn-secondary {
        background: white;
        color: #4f46e5 !important;
        border: 2px solid #4f46e5;
        padding: 12px 30px;
        border-radius: 30px;
        text-decoration: none;
        font-weight: 800;
        font-size: 1.2rem;
        margin: 0 10px;
        transition: transform 0.2s;
        display: inline-block;
    }
    .hero-btn-primary:hover, .hero-btn-secondary:hover {
        transform: translateY(-2px);
    }
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
        margin-bottom: 3rem;
    }
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid #dbe4f0;
        box-shadow: 0 10px 25px rgba(15,23,42,0.04);
        text-align: right;
    }
    .feature-card h3 {
        color: #0f172a;
        margin-top: 0;
        margin-bottom: 1rem;
        font-size: 1.4rem;
    }
    .feature-card p {
        color: #475569;
        line-height: 1.7;
    }
    .section-title {
        text-align: center;
        font-size: 2.2rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="landing-hero rtl-app">
        <h1>AI Statistical & Research Assistant</h1>
        <p>Analyze data, generate insights, and create research-ready reports using intelligent statistical workflows. Without writing a single line of code.</p>
        <div>
            <a href="Data_Lab" target="_self" class="hero-btn-primary">🚀 Start Analysis</a>
            <a href="Data_Lab" target="_self" class="hero-btn-secondary">▶️ Try Demo</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<h2 class='section-title rtl-app'>⚙️ Why Stat Suite Pro?</h2>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="feature-grid rtl-app">
        <div class="feature-card">
            <h3>🤖 AI Insights Generator</h3>
            <p>Don't just calculate P-values. Our Rule-Based AI automatically interprets the results of your T-tests, ANOVA, and Regression models, generating human-readable insights instantly.</p>
        </div>
        <div class="feature-card">
            <h3>🧹 Smart Data Cleaning</h3>
            <p>Upload any messy CSV or Excel file. Handle missing values, drop duplicates, and encode categorical variables with a single click in the Data Lab.</p>
        </div>
        <div class="feature-card">
            <h3>📄 Research-Ready Reports</h3>
            <p>Export your entire session—including tables, descriptive stats, charts, and AI explanations—into a professionally formatted PDF Report ready for academic submission.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<h2 class='section-title rtl-app'>🔄 The Research Workflow</h2>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.info("**1. Upload & Clean**\n\nDrag and drop your dataset into the Data Lab. Clean it instantly.")
with col2:
    st.success("**2. Analyze & Test**\n\nRun correlations, hypothesis tests, and view descriptive stats.")
with col3:
    st.warning("**3. Build Models**\n\nRun multiple linear and polynomial regression with full diagnostics.")
with col4:
    st.error("**4. Export Report**\n\nGenerate a PDF report covering your entire analytical session.")

st.markdown("---")
render_footer()
