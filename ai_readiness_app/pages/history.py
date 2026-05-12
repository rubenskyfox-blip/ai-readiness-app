# =============================================================================
# pages/history.py — Historical assessments & trend view
# =============================================================================
# Shows all past assessments in a table with ceiling trend over time.
# Trend chart and filtering expanded in later steps.
# =============================================================================

import streamlit as st
from utils.db import get_summary

st.title("📁 History")
st.caption("All past assessments — track how readiness changes over time")

# ---------------------------------------------------------------------------
# Filters
# ---------------------------------------------------------------------------
with st.spinner("Loading history…"):
    df = get_summary()

if df.empty:
    st.info("No assessments yet. Start one from the New Assessment page.", icon="📋")
    st.stop()

col1, col2 = st.columns(2)
with col1:
    orgs = ["All"] + sorted(df["organization_name"].unique().tolist())
    selected_org = st.selectbox("Filter by organisation", orgs)
with col2:
    products = ["All"] + sorted(df["product_name"].unique().tolist())
    selected_product = st.selectbox("Filter by product", products)

filtered = df.copy()
if selected_org     != "All": filtered = filtered[filtered["organization_name"] == selected_org]
if selected_product != "All": filtered = filtered[filtered["product_name"]      == selected_product]

# ---------------------------------------------------------------------------
# Results table
# ---------------------------------------------------------------------------
st.subheader(f"{len(filtered)} assessment(s)")

st.dataframe(
    filtered[[
        "organization_name", "product_name", "team_name",
        "assessed_at", "assessed_by",
        "data_maturity", "tooling_infrastructure", "team_ai_capability",
        "governance_controls", "stakeholder_trust", "automation_ceiling",
        "avg_gap", "highest_gap_activity",
    ]].rename(columns={
        "organization_name":     "Organisation",
        "product_name":          "Product",
        "team_name":             "Team",
        "assessed_at":           "Date",
        "assessed_by":           "Assessed by",
        "data_maturity":         "Data",
        "tooling_infrastructure":"Tooling",
        "team_ai_capability":    "Capability",
        "governance_controls":   "Governance",
        "stakeholder_trust":     "Trust",
        "automation_ceiling":    "Ceiling",
        "avg_gap":               "Avg Gap",
        "highest_gap_activity":  "Biggest Gap",
    }),
    use_container_width=True,
    hide_index=True,
)

# Trend chart placeholder — implemented in a later step
st.info("📈 Ceiling trend chart over time coming in Step 4", icon="🔧")
