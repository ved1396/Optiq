import streamlit as st

from frontend.components.theme import apply_theme, render_hero

st.set_page_config(page_title="Optiq Dashboard", page_icon="OP", layout="wide", initial_sidebar_state="expanded")
apply_theme()

with st.sidebar:
    st.markdown("## Optiq Console")
    st.caption("AI routing analytics and system visibility")
    st.markdown("---")
    st.markdown("Navigate between the query router, analytics, cost, energy, and monitoring pages.")

render_hero(
    "Optiq Control Center",
    "A recruiter-friendly operational dashboard for intelligent query routing, model usage, and optimization impact.",
)

left, right = st.columns([1.2, 1])
with left:
    st.markdown(
        """
        <div class="optiq-card">
            <h3 style="margin-top:0;">What This Dashboard Shows</h3>
            <p class="optiq-section">
                Optiq routes each query to the most efficient engine available, balancing response quality with latency,
                estimated cost, and energy use. Use the pages in the sidebar to test live routing behavior and review
                operational analytics across the stack.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right:
    st.markdown(
        """
        <div class="optiq-card">
            <h3 style="margin-top:0;">Recommended Demo Flow</h3>
            <p class="optiq-section">1. Open Query Router and submit a few varied prompts.</p>
            <p class="optiq-section">2. Review route distribution and latency trends on Analytics.</p>
            <p class="optiq-section">3. Use Cost and Energy pages to show efficiency wins.</p>
            <p class="optiq-section">4. Finish with System Monitoring for health and usage visibility.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
