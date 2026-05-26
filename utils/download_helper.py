
import streamlit as st

def auto_download(file_data, filename):
    st.download_button(
        label="Download Report",
        data=file_data,
        file_name=filename,
        mime="application/octet-stream"
    )
