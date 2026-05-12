# =============================================================================
# utils/db.py — Databricks SQL connection & query helpers
# =============================================================================
# When running inside a Databricks App, authentication is handled automatically
# via the app's built-in service principal. No credentials needed in code.
#
# Required environment variables (set in the Databricks App config):
#   DATABRICKS_HOST        — your workspace URL  e.g. https://adb-xxx.azuredatabricks.net
#   DATABRICKS_HTTP_PATH   — SQL Warehouse HTTP path  e.g. /sql/1.0/warehouses/abc123
#
# The catalog and schema are hardcoded here since they are fixed for this app.
# =============================================================================

import os
import pandas as pd
import streamlit as st
from databricks import sql

# ---------------------------------------------------------------------------
# Config — update SCHEMA to match the schema you used when running the SQL
# ---------------------------------------------------------------------------
CATALOG = "cdgebe_dev"
SCHEMA  = "ai_readiness"   # update if you used a different schema name


def _get_connection():
    """
    Returns a Databricks SQL connection.
    Uses Streamlit's cache_resource so the connection is reused across reruns.
    """
    host      = os.environ.get("DATABRICKS_HOST", "").replace("https://", "")
    http_path = os.environ.get("DATABRICKS_HTTP_PATH", "")

    if not host or not http_path:
        st.error(
            "Missing environment variables: DATABRICKS_HOST and DATABRICKS_HTTP_PATH "
            "must be set in the Databricks App configuration."
        )
        st.stop()

    return sql.connect(
        server_hostname = host,
        http_path       = http_path,
        # When inside a Databricks App, auth is automatic.
        # For local dev, set DATABRICKS_TOKEN env var instead.
        access_token    = os.environ.get("DATABRICKS_TOKEN", None),
    )


@st.cache_resource(show_spinner=False)
def get_connection():
    """Cached connection — shared across all pages and reruns."""
    return _get_connection()


def run_query(sql_text: str, params: list = None) -> pd.DataFrame:
    """
    Execute a SQL query and return results as a DataFrame.
    Uses a fresh cursor each call (connections are reused via cache_resource).
    """
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute(sql_text, params or [])
        rows    = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
    return pd.DataFrame(rows, columns=columns)


def run_write(sql_text: str, params: list = None) -> None:
    """Execute a write statement (INSERT / UPDATE / DELETE). No return value."""
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute(sql_text, params or [])


# ---------------------------------------------------------------------------
# Convenience query functions used across pages
# ---------------------------------------------------------------------------

def get_all_assessments() -> pd.DataFrame:
    """All assessments, newest first. Used by Dashboard and History pages."""
    return run_query(f"""
        SELECT
            assessment_id,
            organization_name,
            product_name,
            team_name,
            assessed_by,
            assessed_at,
            data_maturity,
            tooling_infrastructure,
            team_ai_capability,
            governance_controls,
            stakeholder_trust,
            automation_ceiling
        FROM {CATALOG}.{SCHEMA}.assessments
        ORDER BY assessed_at DESC
    """)


def get_assessment_by_id(assessment_id: str) -> pd.DataFrame:
    """Single assessment row. Used by Results page."""
    return run_query(f"""
        SELECT *
        FROM {CATALOG}.{SCHEMA}.assessments
        WHERE assessment_id = ?
    """, [assessment_id])


def get_activity_levels_by_id(assessment_id: str) -> pd.DataFrame:
    """All activity rows for one assessment. Used by Results page."""
    return run_query(f"""
        SELECT activity_name, current_level, target_level, gap, notes
        FROM {CATALOG}.{SCHEMA}.activity_levels
        WHERE assessment_id = ?
        ORDER BY activity_name
    """, [assessment_id])


def get_summary() -> pd.DataFrame:
    """Summary view — one row per assessment with aggregated gap stats."""
    return run_query(f"""
        SELECT *
        FROM {CATALOG}.{SCHEMA}.assessment_summary
        ORDER BY assessed_at DESC
    """)
