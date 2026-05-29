import streamlit as st

st.set_page_config(
    page_title="Optiq Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("⚡ Optiq – Intelligent AI Router")
st.markdown("""
Welcome to the **Optiq Administration Dashboard**.

Optiq minimizes compute waste, cost, and energy consumption by intelligently routing queries to the most efficient processing engine.

### Explore the Dashboard
👈 **Use the sidebar** to navigate through the different modules:

*   **Query Router**: Test queries in real-time and observe the routing decision, latency, cost, and energy metrics.
*   **Analytics**: View aggregate system metrics, route distributions, and performance trends.
*   **Cost Savings**: Analyze how much money Optiq has saved by avoiding unnecessary Large LLM calls.
*   **Energy Savings**: Track your carbon footprint reduction and energy efficiency.
*   **System Monitoring**: Check the health and status of your database and backend engines.
""")

st.info("Ensure the FastAPI backend is running on `http://localhost:8000` to fetch live data.")
