import streamlit as st
from frontend.utils.api import route_query

st.set_page_config(page_title="Query Router", page_icon="🧭", layout="wide")
st.title("🧭 Query Router")

st.markdown("Test the Optiq router by submitting a query. The system will automatically classify and route it to the optimal engine.")

query = st.text_area("Enter your query:", height=100, placeholder="e.g. What is 520 * 4? or Summarize the history of AI.")

if st.button("Route Query", type="primary"):
    if not query.strip():
        st.warning("Please enter a query first.")
    else:
        with st.spinner("Analyzing and routing..."):
            result = route_query(query)
            
            if result:
                st.success("Query processed successfully!")
                
                # Display Results
                st.subheader("Response")
                st.info(result.get("response", "No response returned."))
                
                # Display Metadata in Columns
                st.subheader("Routing Metadata")
                col1, col2, col3, col4 = st.columns(4)
                
                col1.metric("Selected Route", result.get("route", "Unknown"))
                col2.metric("Confidence", f"{result.get('confidence_score', 0.0):.2f}")
                col3.metric("Cost", f"${result.get('estimated_cost', 0.0):.5f}")
                col4.metric("Energy", f"{result.get('estimated_energy', 0.0):.2f} units")
                
                st.caption(f"Latency: {result.get('latency_ms', 0.0):.2f} ms")
