"""
Theme & UI utilities — Arabic-friendly RTL support with modern responsive styling.
"""
import streamlit as st


def apply_theme():
    """Apply professional theme with Arabic RTL support and mobile responsiveness."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800;900&display=swap');

        :root {
            --primary: #4f46e5;
            --primary-2: #7c3aed;
            --accent: #06b6d4;
            --bg: #f3f6fb;
            --surface: rgba(255,255,255,0.92);
            --text: #0f172a;
            --muted: #475569;
            --border: #dbe4f0;
            --success: #10b981;
        }

        html, body, [class*="css"], [data-testid="stMarkdownContainer"] * {
            font-family: 'Cairo', sans-serif !important;
        }

        .stApp {
            background:
                radial-gradient(circle at top right, rgba(99,102,241,0.14), transparent 28%),
                radial-gradient(circle at top left, rgba(6,182,212,0.14), transparent 24%),
                linear-gradient(180deg, #f8fbff 0%, var(--bg) 100%);
            color: var(--text);
        }

        .main .block-container {
            padding-top: 1.2rem;
            padding-bottom: 2rem;
            max-width: 1280px;
        }

        .rtl-app {
            direction: rtl;
            text-align: right;
        }

        .app-header {
            background: linear-gradient(135deg, rgba(79,70,229,0.95), rgba(124,58,237,0.92));
            color: white;
            padding: 1.25rem 1.4rem;
            border-radius: 22px;
            margin-bottom: 1rem;
            box-shadow: 0 18px 45px rgba(79,70,229,0.22);
            border: 1px solid rgba(255,255,255,0.18);
        }

        .app-header h1 {
            margin: 0;
            font-size: 1.7rem;
            font-weight: 800;
            line-height: 1.4;
        }

        .app-header p {
            margin: 0.45rem 0 0 0;
            opacity: 0.94;
            font-size: 0.98rem;
        }

        .hero-card, .feature-card, .mini-card, .footer-card {
            background: var(--surface);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(219,228,240,0.95);
            border-radius: 22px;
            box-shadow: 0 12px 35px rgba(15,23,42,0.08);
        }

        .hero-card {
            padding: 1.6rem;
            margin: 0.5rem 0 1.2rem 0;
            background: linear-gradient(135deg, rgba(255,255,255,0.97), rgba(241,245,255,0.96));
        }

        .hero-card h1 {
            color: var(--text);
            margin: 0.2rem 0 0.75rem 0;
            font-size: 2rem;
            line-height: 1.45;
        }

        .hero-card p {
            color: var(--muted);
            margin: 0;
            font-size: 1rem;
            line-height: 1.9;
        }

        .hero-badge {
            display: inline-block;
            background: rgba(79,70,229,0.12);
            color: var(--primary);
            border: 1px solid rgba(79,70,229,0.18);
            border-radius: 999px;
            padding: 0.35rem 0.85rem;
            font-size: 0.85rem;
            font-weight: 700;
            margin-bottom: 0.8rem;
        }

        .feature-card, .mini-card, .footer-card {
            padding: 1.15rem 1.2rem;
            height: 100%;
        }

        .feature-card h2, .feature-card h3, .mini-card h4 {
            color: var(--text);
            margin-top: 0;
            margin-bottom: 0.55rem;
            font-weight: 800;
        }

        .feature-card p, .mini-card p, .footer-card {
            color: var(--muted);
            line-height: 1.8;
            margin-bottom: 0.35rem;
        }

        .stButton > button,
        [data-testid="baseButton-secondary"],
        [data-testid="baseButton-primary"] {
            border: none !important;
            border-radius: 14px !important;
            background: linear-gradient(135deg, var(--primary), var(--primary-2)) !important;
            color: white !important;
            font-weight: 800 !important;
            padding: 0.55rem 1rem !important;
            box-shadow: 0 10px 24px rgba(79,70,229,0.25);
        }

        .stDownloadButton > button {
            width: 100%;
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 16px 28px rgba(79,70,229,0.26);
        }

        [data-testid="stMetric"] {
            background: rgba(255,255,255,0.9);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 0.8rem 1rem;
            box-shadow: 0 6px 20px rgba(15,23,42,0.05);
        }

        [data-testid="stMetricLabel"], [data-testid="stMetricValue"] {
            color: var(--text) !important;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
            border-left: 1px solid rgba(255,255,255,0.08);
        }

        [data-testid="stSidebar"] * {
            color: #f8fafc !important;
        }

        .stDataFrame, .dataframe, [data-testid="stTable"] {
            border-radius: 18px;
            overflow: hidden;
            border: 1px solid var(--border);
            box-shadow: 0 6px 20px rgba(15,23,42,0.05);
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            flex-wrap: wrap;
        }

        .stTabs [data-baseweb="tab"] {
            background: rgba(255,255,255,0.85);
            border-radius: 12px 12px 0 0;
            padding: 0.55rem 0.9rem;
            font-weight: 700;
            border: 1px solid var(--border);
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, var(--primary), var(--primary-2));
            color: white !important;
        }

        .stAlert {
            border-radius: 16px;
            border: 1px solid var(--border);
        }

        div[data-testid="stHorizontalBlock"] {
            gap: 0.8rem;
        }

        @media (max-width: 992px) {
            .main .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }
            .hero-card h1 {
                font-size: 1.6rem;
            }
        }

        @media (max-width: 768px) {
            .app-header {
                padding: 1rem;
                border-radius: 18px;
            }
            .app-header h1 {
                font-size: 1.35rem;
            }
            .hero-card, .feature-card, .mini-card, .footer-card {
                padding: 0.95rem;
                border-radius: 18px;
            }
            .main .block-container {
                padding-top: 0.65rem;
                padding-left: 0.75rem;
                padding-right: 0.75rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header():
    """Render the top application header."""
    st.markdown(
        """
        <div class="app-header rtl-app">
            <h1>📊 Stat Suite Pro — منصة التحليل الإحصائي والانحدار</h1>
            <p>تحليل البيانات · الاختبارات الإحصائية · الانحدار · التعلم الآلي · التقارير</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
