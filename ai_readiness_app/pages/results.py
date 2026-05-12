# =============================================================================
# pages/results.py — Assessment results view
# =============================================================================
# Full radar chart and gap analysis implemented in Step 4.
# This skeleton loads data and renders a summary table.
# =============================================================================

import streamlit as st
from utils.db import get_all_assessments, get_assessment_by_id, get_activity_levels_by_id

st.title("📊 Results")
st.caption("Select an assessment to view its full results")

# ---------------------------------------------------------------------------
# Assessment picker
# ---------------------------------------------------------------------------
with st.spinner("Loading assessments…"):
    df = get_all_assessments()

if df.empty:
    st.info("No assessments yet. Run one from the New Assessment page.", icon="📋")
    st.stop()

options = {
    f"{row['product_name']} — {row['organization_name']} ({str(row['assessed_at'])[:10]})": row["assessment_id"]
    for _, row in df.iterrows()
}

selected_label = st.selectbox("Choose assessment", list(options.keys()))
selected_id    = options[selected_label]

# ---------------------------------------------------------------------------
# Load selected assessment
# ---------------------------------------------------------------------------
assessment = get_assessment_by_id(selected_id)
activities = get_activity_levels_by_id(selected_id)

if assessment.empty:
    st.error("Assessment not found.")
    st.stop()

a = assessment.iloc[0]

# ---------------------------------------------------------------------------
# Readiness scores
# ---------------------------------------------------------------------------
st.subheader("AI Readiness Scorecard")

DIMS = [
    ("Data Maturity",          "data_maturity"),
    ("Tooling & Infrastructure","tooling_infrastructure"),
    ("Team AI Capability",     "team_ai_capability"),
    ("Governance & Controls",  "governance_controls"),
    ("Stakeholder Trust",      "stakeholder_trust"),
]

cols = st.columns(5)
for col, (label, field) in zip(cols, DIMS):
    col.metric(label, f"{a[field]} / 5")

st.success(f"**Automation Ceiling: L{a['automation_ceiling']}**", icon="🎯")

# Radar chart placeholder — implemented in Step 4
st.info("📈 Radar chart coming in Step 4", icon="🔧")

st.divider()

# ---------------------------------------------------------------------------
# Activity levels
# ---------------------------------------------------------------------------
st.subheader("Activity Automation Matrix")

if not activities.empty:
    st.dataframe(
        activities.rename(columns={
            "activity_name":  "Activity",
            "current_level":  "Current",
            "target_level":   "Target",
            "gap":            "Gap",
            "notes":          "Notes",
        }),
        use_container_width=True,
        hide_index=True,
    )
else:
    st.info("No activity levels recorded for this assessment.")
