# =============================================================================
# pages/new_assessment.py — Guided scoring form
# =============================================================================
# Step 3 will flesh out the full scoring logic and submission.
# This skeleton renders the form structure and wires the submit button.
# =============================================================================

import uuid
import streamlit as st
from datetime import datetime, timezone

st.title("📋 New Assessment")
st.caption("Score your product across the five readiness dimensions and nine activities")

# ---------------------------------------------------------------------------
# Section 1 — Session metadata
# ---------------------------------------------------------------------------
st.subheader("1. About this assessment")

col1, col2 = st.columns(2)
with col1:
    org_name     = st.text_input("Organisation name *", placeholder="e.g. Acme Corp")
    product_name = st.text_input("Product / platform name *", placeholder="e.g. Customer Portal")
with col2:
    team_name    = st.text_input("Team name", placeholder="e.g. Delivery Team")
    assessed_by  = st.text_input("Your name or email *", placeholder="e.g. jane.smith@acme.com")

session_notes = st.text_area("Session notes", placeholder="Optional — capture context, attendees, caveats…")

st.divider()

# ---------------------------------------------------------------------------
# Section 2 — AI Readiness Scorecard (5 dimensions)
# ---------------------------------------------------------------------------
st.subheader("2. AI Readiness Scorecard")
st.info(
    "Score each dimension 1–5. "
    "**Your automation ceiling is your lowest score** — not your average.",
    icon="ℹ️",
)

DIMENSION_HELP = {
    "Data Maturity": (
        "**1** – Siloed, inconsistent, manual extraction required\n"
        "**2** – Core data available but quality inconsistent\n"
        "**3** – Clean data for most processes, reliable pipelines\n"
        "**4** – Real-time APIs across all key processes\n"
        "**5** – Comprehensive governed ecosystem; AI can act autonomously"
    ),
    "Tooling & Infrastructure": (
        "**1** – No AI-specific infrastructure\n"
        "**2** – Some tools adopted, not integrated\n"
        "**3** – Tools integrated into key workflows\n"
        "**4** – Robust AI platform with orchestration & monitoring\n"
        "**5** – Full multi-agent orchestration, self-healing pipelines"
    ),
    "Team AI Capability": (
        "**1** – AI used reactively, limited ability to build\n"
        "**2** – Some members skilled; knowledge patchy\n"
        "**3** – Most can work with AI; some can build workflows\n"
        "**4** – Team can design, build, and operate AI agents\n"
        "**5** – AI-native team; multi-agent architecture capability"
    ),
    "Governance & Controls": (
        "**1** – No governance, no audit trails\n"
        "**2** – Basic ad hoc quality checks\n"
        "**3** – Defined review workflows, basic audit trails\n"
        "**4** – Comprehensive framework with escalation paths\n"
        "**5** – Automated governance, real-time anomaly detection"
    ),
    "Stakeholder Trust": (
        "**1** – Sceptical; AI outputs routinely overridden\n"
        "**2** – Accept low-risk items; extra scrutiny when AI involved\n"
        "**3** – Trust the human-reviewed process; no extra scrutiny\n"
        "**4** – Delegate decisions to AI within defined scopes\n"
        "**5** – Set direction only; operations fully delegated to AI"
    ),
}

dim_scores = {}
for dim_name, help_text in DIMENSION_HELP.items():
    col_label, col_slider = st.columns([2, 3])
    with col_label:
        st.markdown(f"**{dim_name}**")
        with st.expander("Score descriptions"):
            st.markdown(help_text)
    with col_slider:
        dim_scores[dim_name] = st.slider(
            label     = dim_name,
            min_value = 1,
            max_value = 5,
            value     = 3,
            key       = f"dim_{dim_name}",
            label_visibility = "collapsed",
        )

automation_ceiling = min(dim_scores.values())
st.success(f"**Automation ceiling: L{automation_ceiling}** (lowest dimension score)", icon="🎯")

st.divider()

# ---------------------------------------------------------------------------
# Section 3 — Activity Automation Matrix (9 activities)
# ---------------------------------------------------------------------------
st.subheader("3. Activity Automation Matrix")
st.info(
    "For each activity, score where your team is today and where you want to reach.",
    icon="ℹ️",
)

ACTIVITIES = [
    "Requirements Capture",
    "Requirements Preparation",
    "Architecture",
    "Code Development",
    "Design",
    "Wireframe / Prototype",
    "Data Supply Chain",
    "CI/CD Process",
    "UAT",
]

LEVEL_LABELS = {
    1: "L1 — AI as tool",
    2: "L2 — AI assistant",
    3: "L3 — AI does it, human reviews",
    4: "L4 — Autonomous + approval gate",
    5: "L5 — Fully autonomous agents",
}

activity_scores = {}

header_cols = st.columns([2, 2, 2, 3])
header_cols[0].markdown("**Activity**")
header_cols[1].markdown("**Current Level**")
header_cols[2].markdown("**Target Level**")
header_cols[3].markdown("**Notes**")

for activity in ACTIVITIES:
    cols = st.columns([2, 2, 2, 3])
    with cols[0]:
        st.markdown(f"{activity}")
    with cols[1]:
        current = st.selectbox(
            label   = f"current_{activity}",
            options = list(LEVEL_LABELS.keys()),
            format_func = lambda x: LEVEL_LABELS[x],
            index   = 1,   # default L2
            key     = f"current_{activity}",
            label_visibility = "collapsed",
        )
    with cols[2]:
        target = st.selectbox(
            label   = f"target_{activity}",
            options = list(LEVEL_LABELS.keys()),
            format_func = lambda x: LEVEL_LABELS[x],
            index   = 2,   # default L3
            key     = f"target_{activity}",
            label_visibility = "collapsed",
        )
    with cols[3]:
        note = st.text_input(
            label = f"note_{activity}",
            placeholder = "Optional note…",
            key   = f"note_{activity}",
            label_visibility = "collapsed",
        )
    activity_scores[activity] = {"current": current, "target": target, "note": note}

st.divider()

# ---------------------------------------------------------------------------
# Submit
# ---------------------------------------------------------------------------
st.subheader("4. Submit")

required_filled = all([org_name, product_name, assessed_by])
if not required_filled:
    st.warning("Please fill in Organisation, Product, and Your name/email before submitting.", icon="⚠️")

if st.button("Submit Assessment", type="primary", disabled=not required_filled):
    # Full write logic wired in Step 3
    st.session_state["pending_assessment"] = {
        "assessment_id":        str(uuid.uuid4()),
        "organization_name":    org_name,
        "product_name":         product_name,
        "team_name":            team_name,
        "assessed_by":          assessed_by,
        "assessed_at":          datetime.now(timezone.utc),
        "notes":                session_notes,
        "dim_scores":           dim_scores,
        "automation_ceiling":   automation_ceiling,
        "activity_scores":      activity_scores,
    }
    st.success("Assessment ready — saving to Databricks (Step 3 will wire this up).")
    st.json(st.session_state["pending_assessment"], expanded=False)
