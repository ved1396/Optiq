import pandas as pd
import streamlit as st

from frontend.components.cards import metric_card
from frontend.components.charts import bar_chart, line_chart
from frontend.components.formatters import energy
from frontend.components.theme import apply_theme, render_hero
from frontend.utils.api import get_energy_summary

st.set_page_config(page_title="Energy Savings Dashboard", page_icon="OP", layout="wide")
apply_theme()
render_hero("Energy Savings Dashboard", "Quantify how much energy Optiq saves by reserving expensive model calls for only the hardest tasks.")

payload = get_energy_summary()
summary = payload.get("summary", {})
energy_per_route = pd.DataFrame(payload.get("energy_per_route", []))
historical_trends = pd.DataFrame(payload.get("historical_trends", []))

metric_cols = st.columns(3)
with metric_cols[0]:
    metric_card("Total Energy", energy(summary.get("total_energy", 0.0)))
with metric_cols[1]:
    metric_card("Estimated Energy Saved", energy(summary.get("estimated_energy_saved", 0.0)))
with metric_cols[2]:
    metric_card("Baseline Large LLM Energy", energy(summary.get("baseline_large_llm_energy", 0.0)))

if energy_per_route.empty:
    st.info("No energy data yet. Route a few queries first.")
else:
    charts = st.columns(2)
    with charts[0]:
        st.plotly_chart(bar_chart(energy_per_route, "route", "estimated_energy", "Energy Per Route"), use_container_width=True)
    with charts[1]:
        st.plotly_chart(bar_chart(energy_per_route, "route", "estimated_saved", "Estimated Energy Saved Per Route"), use_container_width=True)

    if not historical_trends.empty:
        historical_trends["created_at"] = pd.to_datetime(historical_trends["created_at"])
        st.plotly_chart(
            line_chart(historical_trends, "created_at", "cumulative_energy", "Historical Energy Trend"),
            use_container_width=True,
        )
        st.dataframe(historical_trends, use_container_width=True, hide_index=True)
