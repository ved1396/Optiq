import streamlit as st
import pandas as pd
import plotly.express as px
from frontend.utils.api import get_analytics

st.set_page_config(page_title="Analytics Dashboard", page_icon="📊", layout="wide")
st.title("📊 Analytics Dashboard")

data = get_analytics(limit=1000)

if not data:
    st.info("No data available yet. Please submit some queries through the Router.")
else:
    df = pd.DataFrame(data)
    
    # Top-level metrics
    st.subheader("System Overview")
    col1, col2, col3 = st.columns(3)
    
    total_queries = len(df)
    avg_latency = df['latency_ms'].mean()
    most_common_route = df['route'].mode()[0] if not df.empty else "N/A"
    
    col1.metric("Total Queries", total_queries)
    col2.metric("Average Latency (ms)", f"{avg_latency:.2f}")
    col3.metric("Top Route", most_common_route)
    
    st.markdown("---")
    
    # Visualizations
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("Route Distribution")
        route_counts = df['route'].value_counts().reset_index()
        route_counts.columns = ['Route', 'Count']
        fig = px.pie(route_counts, values='Count', names='Route', hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
        
    with col_chart2:
        st.subheader("Latency by Route")
        fig2 = px.box(df, x='route', y='latency_ms', color='route')
        st.plotly_chart(fig2, use_container_width=True)
        
    st.subheader("Recent Queries")
    st.dataframe(df[['timestamp', 'query', 'route', 'latency_ms']].head(10), use_container_width=True)
