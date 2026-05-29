import streamlit as st

from frontend.components.cards import metric_card
from frontend.components.formatters import currency, energy, latency
from frontend.components.theme import apply_theme, render_hero
from frontend.utils.api import route_query, submit_feedback

st.set_page_config(page_title="Query Router", page_icon="OP", layout="wide")
apply_theme()
render_hero("Query Router", "Send a live query to the FastAPI backend and inspect the route, response, cost, and energy footprint.")

query = st.text_area(
    "Enter a query",
    height=140,
    placeholder="Try: What is 84 / 3? | Summarize this project update... | Design a resilient API architecture...",
)

if st.button("Route Query", use_container_width=False):
    if not query.strip():
        st.warning("Enter a query before routing.")
    else:
        with st.spinner("Routing query through Optiq..."):
            result = route_query(query)
        if result:
            st.session_state["last_route_result"] = result

result = st.session_state.get("last_route_result")
if result:
    card_cols = st.columns(5)
    with card_cols[0]:
        metric_card("Selected Route", result["route"].replace("_", " ").title())
    with card_cols[1]:
        metric_card("Classifier", result["classifier_label"].replace("_", " ").title(), f"Confidence {result['confidence_score']:.2f}")
    with card_cols[2]:
        metric_card("Latency", latency(result["latency_ms"]))
    with card_cols[3]:
        metric_card("Estimated Cost", currency(result["estimated_cost"]))
    with card_cols[4]:
        metric_card("Estimated Energy", energy(result["estimated_energy"]))

    response_col, meta_col = st.columns([1.5, 1])
    with response_col:
        st.markdown("### Response")
        st.markdown(f'<div class="optiq-card">{result["response"]}</div>', unsafe_allow_html=True)
    with meta_col:
        st.markdown("### Routing Details")
        heuristic = result.get("heuristic_route") or "Classifier-driven"
        st.markdown(
            f"""
            <div class="optiq-card">
                <p><strong>Query ID:</strong> {result['query_id']}</p>
                <p><strong>Heuristic Match:</strong> {heuristic}</p>
                <p><strong>Confidence Score:</strong> {result['confidence_score']:.4f}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### Feedback")
    feedback_cols = st.columns([1, 1.2, 1])
    with feedback_cols[0]:
        rating = st.slider("Rating", min_value=1, max_value=5, value=4)
    with feedback_cols[1]:
        correct_route = st.selectbox(
            "Correct route if different",
            options=["", "calculator", "rule_engine", "search", "local_llm", "large_llm"],
            index=0,
        )
    with feedback_cols[2]:
        comments = st.text_input("Comments", placeholder="Optional notes about routing quality")

    if st.button("Submit Feedback"):
        feedback = submit_feedback(result["query_id"], rating, comments or None, correct_route or None)
        if feedback:
            st.success(feedback["message"])
