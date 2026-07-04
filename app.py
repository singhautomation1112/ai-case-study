import streamlit as st
import uuid
import datetime

# ✅ Initialize session state repository
if "TEST_DATA_REPO" not in st.session_state:
    st.session_state.TEST_DATA_REPO = {
        "patients": [],
        "insurance": [],
        "lab_results": []
    }

# Utility: generate synthetic patient record
def generate_patient_record(name, dob, tenant_id):
    return {
        "patient_id": str(uuid.uuid4()),
        "name": name,
        "dob": dob,
        "tenant_id": tenant_id,
        "created_at": datetime.datetime.utcnow().isoformat()
    }

st.title("Healthcare Test Automation Dashboard")

# --- Provision Patient Data ---
st.subheader("Provision Synthetic Patient Data")
name = st.text_input("Patient Name", "Test Patient")
dob = st.text_input("DOB (YYYY-MM-DD)", "1990-01-01")
tenant_id = st.text_input("Tenant ID", "default")

if st.button("Provision Patient Data"):
    record = generate_patient_record(name, dob, tenant_id)
    st.session_state.TEST_DATA_REPO["patients"].append(record)
    st.success(f"Provisioned patient record for tenant {tenant_id}")
    st.json(record)
    st.info(f"Total patient records: {len(st.session_state.TEST_DATA_REPO['patients'])}")

# --- Update Patient Record ---
st.subheader("Update Patient Record")
update_patient_id = st.text_input("Patient ID to Update", "")
new_name = st.text_input("New Name", "")
new_tenant_id = st.text_input("New Tenant ID", "")

if st.button("Update Patient"):
    patients = st.session_state.TEST_DATA_REPO["patients"]
    found = False
    for p in patients:
        if p["patient_id"] == update_patient_id:
            if new_name:
                p["name"] = new_name
            if new_tenant_id:
                p["tenant_id"] = new_tenant_id
            p["updated_at"] = datetime.datetime.utcnow().isoformat()
            st.success(f"Patient {update_patient_id} updated successfully")
            st.json(p)
            found = True
            break
    if not found:
        st.error("Patient ID not found")

# --- Integration Contract Validation ---
st.subheader("Integration Contract Validation")
insurance_id = st.text_input("Insurance ID", "")
claim_amount = st.number_input("Claim Amount", min_value=0.0, step=100.0)

if st.button("Validate Integration Contract"):
    if not insurance_id or claim_amount <= 0:
        st.error("Integration contract validation failed: Missing required fields")
    else:
        st.success("Integration contract validated successfully")

# --- Smoke Test ---
st.subheader("Smoke Test: Patient Registration Workflow")
expected_tenant = st.text_input("Expected Tenant ID for Smoke Test", "default")

if st.button("Run Smoke Test"):
    patients = st.session_state.TEST_DATA_REPO["patients"]
    if len(patients) == 0:
        st.error("Smoke test failed: No patient records available. Please provision data first.")
    elif not any(p["tenant_id"] == expected_tenant for p in patients):
        st.error("Smoke test failed: Patient record mismatch or updated incorrectly")
    else:
        st.success(f"Smoke test passed ✅. Patients count: {len(patients)}")

# --- Health Check ---
st.subheader("System Health Check")
if st.button("Check Health"):
    st.json({"status": "healthy", "timestamp": datetime.datetime.utcnow().isoformat()})
