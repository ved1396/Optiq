import pandas as pd
import streamlit as st

from frontend.components.cards import metric_card
from frontend.components.charts import bar_chart, line_chart, pie_chart
from frontend.components.formatters import latency
from frontend.components.theme import apply_theme, render_hero
from frontend.utils.api import get_analytics

st.set_page_config(page_title="Analytics Dashboard", page_icon="OP", layout="wide")
apply_theme()
render_hero("Analytics Dashboard", "Track query volume, route distribution, routing quality, and latency behavior in real time.")

payload = get_analytics(limit=1000)
summary = payload.get("summary", {})
route_distribution = pd.DataFrame(payload.get("route_distribution", []))
latency_trend = pd.DataFrame(payload.get("latency_trend", []))
recent_queries = pd.DataFrame(payload.get("recent_queries", []))

metric_cols = st.columns(4)
with metric_cols[0]:
    metric_card("Total Queries", f"{summary.get('total_queries', 0):,}")
with metric_cols[1]:
    metric_card("Routing Accuracy", f"{summary.get('routing_accuracy', 0.0):.1f}%")
with metric_cols[2]:
    metric_card("Average Latency", latency(summary.get("average_latency_ms", 0.0)))
with metric_cols[3]:
    metric_card("Last Updated", summary.get("last_updated", "N/A"))

if route_distribution.empty:
    st.info("No analytics data yet. Route a few queries first.")
else:
    charts_top = st.columns(2)
    with charts_top[0]:
        st.plotly_chart(pie_chart(route_distribution, "route", "count", "Route Distribution"), use_container_width=True)
    with charts_top[1]:
        st.plotly_chart(bar_chart(route_distribution, "route", "count", "Query Count by Route"), use_container_width=True)

    if not latency_trend.empty:
        latency_trend["created_at"] = pd.to_datetime(latency_trend["created_at"])
        st.plotly_chart(
            line_chart(latency_trend, "created_at", "latency_ms", "Latency Trend Over Time"),
            use_container_width=True,
        )

    st.markdown("### Recent Queries")
    st.dataframe(recent_queries, use_container_width=True, hide_index=True)
