# =============================================================================
# app.py — AI Readiness Evaluation App  |  Main entry point
# =============================================================================
# Run locally:  streamlit run app.py
# Deploy:       Upload this folder as a Databricks App
# =============================================================================

import streamlit as st

# ---------------------------------------------------------------------------
# Page config — must be the first Streamlit call
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title = "AI Readiness Evaluator",
    page_icon  = "🤖",
    layout     = "wide",
    initial_sidebar_state = "expanded",
)

# ---------------------------------------------------------------------------
# Navigation — define all pages
# ---------------------------------------------------------------------------
dashboard       = st.Page("pages/dashboard.py",       title="Dashboard",       icon="🏠")
new_assessment  = st.Page("pages/new_assessment.py",  title="New Assessment",  icon="📋")
results         = st.Page("pages/results.py",         title="Results",         icon="📊")
history         = st.Page("pages/history.py",         title="History",         icon="📁")

nav = st.navigation([dashboard, new_assessment, results, history])

# ---------------------------------------------------------------------------
# Sidebar branding
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🤖 AI Readiness")
    st.markdown("*AI Agents Enterprise*")
    st.divider()

# ---------------------------------------------------------------------------
# Run selected page
# ---------------------------------------------------------------------------
nav.run()
