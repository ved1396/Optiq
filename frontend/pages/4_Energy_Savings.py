import streamlit as st
import pandas as pd
import plotly.express as px
from frontend.utils.api import get_energy_summary

st.set_page_config(page_title="Energy Savings", page_icon="🌱", layout="wide")
st.title("🌱 Energy Savings Dashboard")

data = get_energy_summary()

if not data:
    st.info("No energy data available.")
else:
    df = pd.DataFrame(data)
    
    # Calculate savings (assume Large LLM = 100 units)
    LARGE_LLM_ENERGY = 100.0
    df['simulated_large_llm_energy'] = df['query_count'] * LARGE_LLM_ENERGY
    
    actual_total_energy = df['total_energy'].sum()
    baseline_total_energy = df['simulated_large_llm_energy'].sum()
    savings = baseline_total_energy - actual_total_energy
    savings_percentage = (savings / baseline_total_energy * 100) if baseline_total_energy > 0 else 0
    
    st.subheader("Environmental Impact")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Actual Energy", f"{actual_total_energy:,.0f} units")
    col2.metric("Estimated Energy Saved", f"{savings:,.0f} units")
    col3.metric("Savings Percentage", f"{savings_percentage:.1f}%")
    
    st.markdown("---")
    
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.subheader("Energy by Route")
        fig1 = px.bar(df, x='route', y='total_energy', color='route', title="Actual Energy Consumed")
        st.plotly_chart(fig1, use_container_width=True)
        
    with col_chart2:
        st.subheader("Energy Comparison")
        comp_df = pd.DataFrame({
            "Scenario": ["If everything used Large LLM", "With Optiq Routing"],
            "Energy": [baseline_total_energy, actual_total_energy]
        })
        fig2 = px.bar(comp_df, x='Scenario', y='Energy', color='Scenario', text_auto='.0f')
        st.plotly_chart(fig2, use_container_width=True)
