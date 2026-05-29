import streamlit as st
from frontend.utils.api import check_health, get_analytics
import pandas as pd

st.set_page_config(page_title="System Monitoring", page_icon="🖥️", layout="wide")
st.title("🖥️ System Monitoring")

st.subheader("API Status")
is_healthy = check_health()

if is_healthy:
    st.success("✅ Backend API is Online and Healthy")
else:
    st.error("❌ Backend API is Offline or Unreachable")

st.markdown("---")

st.subheader("Database Statistics")
data = get_analytics(limit=10000)

if data:
    df = pd.DataFrame(data)
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Database Records (Queries)", len(df))
    with col2:
        st.metric("Latest Query Timestamp", str(df['timestamp'].max()) if not df.empty else "N/A")
else:
    st.info("No database records found.")
