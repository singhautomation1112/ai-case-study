import streamlit as st
import pandas as pd
import datetime

# Import reusable functions from tools.py
from tools import (
    generate_patient_record,
    update_patient_record,
    validate_integration_contract,
    run_smoke_test,
    system_health_check,
)

# Import AI Agent
from ai_agent import ask_agent

# -----------------------------
# Initialize Session State
# -----------------------------
if "TEST_DATA_REPO" not in st.session_state:
    st.session_state.TEST_DATA_REPO = {
        "patients": [],
        "insurance": [],
        "lab_results": []
    }

# -----------------------------
# Page Title
# -----------------------------
st.set_page_config(page_title="Healthcare Test Automation Dashboard", layout="wide")

st.title("🏥 Healthcare Test Automation Dashboard")

# ======================================================
# Provision Synthetic Patient Data
# ======================================================

st.header("Provision Synthetic Patient Data")

name = st.text_input("Patient Name", "Test Patient")
dob = st.text_input("DOB (YYYY-MM-DD)", "1990-01-01")
tenant_id = st.text_input("Tenant ID", "default")

if st.button("Provision Patient Data"):

    record = generate_patient_record(
        name,
        dob,
        tenant_id
    )

    st.session_state.TEST_DATA_REPO["patients"].append(record)

    st.success("Patient record created successfully.")

    st.json(record)

    st.info(
        f"Total Patients: {len(st.session_state.TEST_DATA_REPO['patients'])}"
    )

# ======================================================
# Update Patient Record
# ======================================================

st.header("Update Patient Record")

update_patient_id = st.text_input("Patient ID")

new_name = st.text_input("New Name")

new_tenant_id = st.text_input("New Tenant ID")

if st.button("Update Patient"):

    updated = update_patient_record(
        st.session_state.TEST_DATA_REPO["patients"],
        update_patient_id,
        new_name,
        new_tenant_id
    )

    if updated:

        st.success("Patient updated successfully.")

        st.json(updated)

    else:

        st.error("Patient ID not found.")

# ======================================================
# Validate Integration Contract
# ======================================================

st.header("Integration Contract Validation")

insurance_id = st.text_input("Insurance ID")

claim_amount = st.number_input(
    "Claim Amount",
    min_value=0.0,
    step=100.0
)

if st.button("Validate Integration Contract"):

    result = validate_integration_contract(
        insurance_id,
        claim_amount
    )

    if result["status"] == "success":

        st.success(result["message"])

    else:

        st.error(result["message"])

# ======================================================
# Smoke Test
# ======================================================

st.header("Smoke Test")

expected_tenant = st.text_input(
    "Expected Tenant ID",
    "default"
)

if st.button("Run Smoke Test"):

    result = run_smoke_test(
        st.session_state.TEST_DATA_REPO["patients"],
        expected_tenant
    )

    if result["status"] == "success":

        st.success(result["message"])

    else:

        st.error(result["message"])

# ======================================================
# System Health Check
# ======================================================

st.header("System Health Check")

if st.button("Check System Health"):

    health = system_health_check()

    st.success("System Health Retrieved")

    st.json(health)

# ======================================================
# Display Current Repository
# ======================================================

st.header("Current Test Data Repository")

if len(st.session_state.TEST_DATA_REPO["patients"]) > 0:

    df = pd.DataFrame(
        st.session_state.TEST_DATA_REPO["patients"]
    )

    st.dataframe(df)

else:

    st.info("No patient records available.")

# ======================================================
# AI Assistant
# ======================================================

st.header("AI Assistant")

st.write("Ask the AI to perform healthcare QA operations.")

query = st.text_input(
    "Enter your request",
    placeholder="Example: Generate a patient record"
)

if st.button("Ask AI"):

    if query.strip() == "":

        st.warning("Please enter a request.")

    else:

        response = ask_agent(query)

        st.success("AI Response")

        st.json(response)