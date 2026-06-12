import streamlit as st
from supabase import create_client, Client
import json

@st.cache_resource
def init_supabase() -> Client:
    """Initialize and return the Supabase client."""
    try:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"Failed to initialize Supabase: {e}")
        return None

def save_analysis(user_id: str, project_name: str, analysis_type: str, result_data: dict):
    """Save an analysis result to Supabase Database."""
    supabase = init_supabase()
    if not supabase:
        return False
        
    try:
        data = {
            "user_id": user_id,
            "project_name": project_name,
            "analysis_type": analysis_type,
            "result_data": json.dumps(result_data)
        }
        # Assuming a table named 'analyses' exists. If not, this will silently fail or throw an error.
        # We wrap in try-except to prevent breaking the UI.
        supabase.table("analyses").insert(data).execute()
        return True
    except Exception as e:
        print(f"Database error: {e}")
        return False
