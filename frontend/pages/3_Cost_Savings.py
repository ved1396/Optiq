import streamlit as st
import pandas as pd
import plotly.express as px
from frontend.utils.api import get_cost_summary

st.set_page_config(page_title="Cost Savings", page_icon="💰", layout="wide")
st.title("💰 Cost Savings Dashboard")

data = get_cost_summary()

if not data:
    st.info("No cost data available.")
else:
    df = pd.DataFrame(data)
    
    # Calculate savings
    LARGE_LLM_COST = 0.0300
    df['simulated_large_llm_cost'] = df['query_count'] * LARGE_LLM_COST
    
    actual_total_cost = df['total_cost'].sum()
    baseline_total_cost = df['simulated_large_llm_cost'].sum()
    savings = baseline_total_cost - actual_total_cost
    savings_percentage = (savings / baseline_total_cost * 100) if baseline_total_cost > 0 else 0
    
    st.subheader("Financial Impact")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Actual Cost", f"${actual_total_cost:.4f}")
    col2.metric("Estimated Cost Saved", f"${savings:.4f}")
    col3.metric("Savings Percentage", f"{savings_percentage:.1f}%")
    
    st.markdown("---")
    
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.subheader("Cost by Route")
        fig1 = px.bar(df, x='route', y='total_cost', color='route', title="Actual Cost Incurred")
        st.plotly_chart(fig1, use_container_width=True)
        
    with col_chart2:
        st.subheader("Cost Comparison")
        comp_df = pd.DataFrame({
            "Scenario": ["If everything used Large LLM", "With Optiq Routing"],
            "Cost": [baseline_total_cost, actual_total_cost]
        })
        fig2 = px.bar(comp_df, x='Scenario', y='Cost', color='Scenario', text_auto='.4f')
        st.plotly_chart(fig2, use_container_width=True)
