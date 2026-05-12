# =============================================================================
# pages/dashboard.py — Home / Dashboard
# =============================================================================
# Shows: latest automation ceiling, most recent scores, quick-start CTA.
# Full chart implementation comes in Step 4.
# =============================================================================

import streamlit as st
from utils.db import get_summary

st.title("🏠 Dashboard")
st.caption("Your latest AI readiness snapshot")

# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------
with st.spinner("Loading assessments…"):
    df = get_summary()

# ---------------------------------------------------------------------------
# Empty state
# ---------------------------------------------------------------------------
if df.empty:
    st.info(
        "No assessments found. Run your first evaluation to see results here.",
        icon="📋",
    )
    if st.button("Start a New Assessment", type="primary"):
        st.switch_page("pages/new_assessment.py")
    st.stop()

# ---------------------------------------------------------------------------
# Latest assessment summary (top KPI cards)
# ---------------------------------------------------------------------------
latest = df.iloc[0]

st.subheader(f"{latest['product_name']} — {latest['organization_name']}")
st.caption(f"Last assessed: {latest['assessed_at']}  ·  by {latest['assessed_by']}")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Automation Ceiling",   f"L{latest['automation_ceiling']}")
col2.metric("Avg Current Level",    f"{latest['avg_current_level']:.1f}")
col3.metric("Avg Target Level",     f"{latest['avg_target_level']:.1f}")
col4.metric("Biggest Gap Activity", latest["highest_gap_activity"])

st.divider()

# ---------------------------------------------------------------------------
# All assessments table
# ---------------------------------------------------------------------------
st.subheader("All Assessments")
st.dataframe(
    df[[
        "organization_name", "product_name", "assessed_at",
        "automation_ceiling", "avg_current_level", "avg_target_level", "avg_gap"
    ]].rename(columns={
        "organization_name":  "Organisation",
        "product_name":       "Product",
        "assessed_at":        "Date",
        "automation_ceiling": "Ceiling",
        "avg_current_level":  "Avg Current",
        "avg_target_level":   "Avg Target",
        "avg_gap":            "Avg Gap",
    }),
    use_container_width=True,
    hide_index=True,
)

# ---------------------------------------------------------------------------
# CTA
# ---------------------------------------------------------------------------
st.divider()
if st.button("＋ New Assessment", type="primary"):
    st.switch_page("pages/new_assessment.py")
