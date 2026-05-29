import pandas as pd
import streamlit as st

from frontend.components.cards import metric_card
from frontend.components.charts import bar_chart
from frontend.components.theme import apply_theme, render_hero
from frontend.utils.api import get_health

st.set_page_config(page_title="System Monitoring Dashboard", page_icon="OP", layout="wide")
apply_theme()
render_hero("System Monitoring", "Monitor API health, route usage, active models, and database activity from one operational view.")

health = get_health()
route_usage = pd.DataFrame(health.get("route_usage", []))
models = health.get("models", {})

metric_cols = st.columns(4)
with metric_cols[0]:
    metric_card("API Health", health.get("status", "offline").upper())
with metric_cols[1]:
    metric_card("Database", health.get("database", "unknown").title())
with metric_cols[2]:
    metric_card("Queries Logged", f"{health.get('total_queries', 0):,}")
with metric_cols[3]:
    metric_card("Classifier Threshold", f"{models.get('classifier_threshold', 0.0):.2f}")

details = st.columns(2)
with details[0]:
    st.markdown(
        f"""
        <div class="optiq-card">
            <h3 style="margin-top:0;">Model Usage</h3>
            <p><strong>Local Model:</strong> {models.get('local_llm', 'N/A')}</p>
            <p><strong>Large Model:</strong> {models.get('large_llm', 'N/A')}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with details[1]:
    st.markdown(
        """
        <div class="optiq-card">
            <h3 style="margin-top:0;">Database Statistics</h3>
            <p>SQLite is used for query logging and analytics snapshots.</p>
            <p>Indexes are created for timestamps, routes, and query joins to keep dashboard reads fast.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

if not route_usage.empty:
    st.plotly_chart(bar_chart(route_usage, "route", "count", "Route Usage"), use_container_width=True)
