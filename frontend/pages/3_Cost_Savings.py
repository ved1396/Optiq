import pandas as pd
import streamlit as st

from frontend.components.cards import metric_card
from frontend.components.charts import bar_chart, line_chart
from frontend.components.formatters import currency
from frontend.components.theme import apply_theme, render_hero
from frontend.utils.api import get_cost_summary

st.set_page_config(page_title="Cost Savings Dashboard", page_icon="OP", layout="wide")
apply_theme()
render_hero("Cost Savings Dashboard", "Show how intelligent routing reduces spend compared with sending every request to a large hosted model.")

payload = get_cost_summary()
summary = payload.get("summary", {})
cost_per_route = pd.DataFrame(payload.get("cost_per_route", []))
historical_trends = pd.DataFrame(payload.get("historical_trends", []))

metric_cols = st.columns(3)
with metric_cols[0]:
    metric_card("Total Cost", currency(summary.get("total_cost", 0.0)))
with metric_cols[1]:
    metric_card("Estimated Cost Saved", currency(summary.get("estimated_cost_saved", 0.0)))
with metric_cols[2]:
    metric_card("Baseline Large LLM Cost", currency(summary.get("baseline_large_llm_cost", 0.0)))

if cost_per_route.empty:
    st.info("No cost data yet. Route a few queries first.")
else:
    charts = st.columns(2)
    with charts[0]:
        st.plotly_chart(bar_chart(cost_per_route, "route", "estimated_cost", "Cost Per Route"), use_container_width=True)
    with charts[1]:
        st.plotly_chart(bar_chart(cost_per_route, "route", "estimated_saved", "Estimated Savings Per Route"), use_container_width=True)

    if not historical_trends.empty:
        historical_trends["created_at"] = pd.to_datetime(historical_trends["created_at"])
        st.plotly_chart(
            line_chart(historical_trends, "created_at", "cumulative_cost", "Historical Cost Trend"),
            use_container_width=True,
        )
        st.dataframe(historical_trends, use_container_width=True, hide_index=True)
