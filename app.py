import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from faker import Faker
import importlib.util
import sys

# --- App Title ---
st.title("AI-Driven Test Automation Prototype")

# Step 1: Environment Setup
st.header("Step 1: Environment Setup")
libs = ["playwright", "sklearn", "faker", "matplotlib", "pandas", "selenium"]
status = []
for lib in libs:
    installed = importlib.util.find_spec(lib) is not None
    status.append({"Library": lib, "Installed": "✅ Yes" if installed else "❌ No"})
st.subheader("Dependency Check")
st.table(status)
st.write("Python Version:", sys.version)
if all(s["Installed"] == "✅ Yes" for s in status):
    st.success("✅ Environment ready. Proceed to Step 2.")
else:
    st.warning("⚠️ Some dependencies missing. Please install before continuing.")

# Step 2: Upload User Story → Generate Scenarios + RTM
st.header("Step 2: User Story → Test Scenarios & RTM")
uploaded_file = st.file_uploader("Upload a user story (txt, docx, pdf)", type=["txt","docx","pdf"])
if uploaded_file:
    text = uploaded_file.read().decode("utf-8", errors="ignore")
    st.subheader("Extracted User Story Text")
    st.write(text[:500] + "...")

    scenarios = [
        {"Requirement":"Patient Intake","Scenario":"Patient provides symptoms → doctor records complaint"},
        {"Requirement":"Diagnosis","Scenario":"Doctor checks stomach pain → suggests tests"},
        {"Requirement":"Negative Case","Scenario":"Patient provides incomplete info → system prompts for details"},
        {"Requirement":"Edge Case","Scenario":"Patient age not provided → validation error"},
    ]
    st.subheader("Generated Test Scenarios")
    st.table(scenarios)

    rtm = [{"Requirement": s["Requirement"], "TestCase": f"TC_{s['Requirement'].replace(' ','_')}_{i+1}"} for i, s in enumerate(scenarios)]
    st.subheader("Requirements Traceability Matrix (RTM)")
    st.table(rtm)

# Step 3: Adaptive Regression Selector
st.header("Step 3: Adaptive Regression Selector")
data = pd.DataFrame({
    "files_changed": [3, 10, 2, 5, 8, 1],
    "lines_added":   [50, 200, 20, 120, 300, 10],
    "past_defects":  [1, 4, 0, 2, 5, 0],
    "test_case_priority": ["High", "High", "Low", "Medium", "High", "Low"]
})
X = data[['files_changed','lines_added','past_defects']]
y = data['test_case_priority']
model = RandomForestClassifier(random_state=42).fit(X, y)

files = st.number_input("Files Changed", 1, 20, 5)
lines = st.number_input("Lines Added", 10, 500, 120)
defects = st.number_input("Past Defects", 0, 10, 2)
if st.button("Predict Regression Priority"):
    new_commit = pd.DataFrame([[files, lines, defects]],
                               columns=['files_changed','lines_added','past_defects'])
    priority = model.predict(new_commit)[0]
    st.success(f"Predicted Regression Priority: {priority}")

    test_suite = {
        "High": ["TC_Patient_Intake_1", "TC_Diagnosis_2", "TC_Negative_Case_3", "TC_Edge_Case_4"],
        "Medium": ["TC_Patient_Intake_1", "TC_Diagnosis_2"],
        "Low": ["TC_Patient_Intake_1"]
    }
    st.subheader("Recommended Test Cases to Run")
    st.table(pd.DataFrame(test_suite[priority], columns=["Test Case ID"]))

# Step 4: Self-Healing Automation (Selenium sample)
st.header("Step 4: Self-Healing Automation")
if st.button("Run Selenium Test"):
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get("https://the-internet.herokuapp.com/login")  # ✅ real demo site

        try:
            driver.find_element(By.ID, "username").send_keys("tomsmith")
            driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
            driver.find_element(By.CSS_SELECTOR, "button.radius").click()
            st.success("Login successful using primary locator")
        except Exception as e:
            st.warning(f"Primary locator failed: {e}")
            driver.find_element(By.XPATH, "//button[contains(text(),'Login')]").click()
            st.success("Login successful using fallback locator")

        driver.quit()
    except Exception as e:
        st.error(f"Selenium test failed: {e}")

# Step 5: AI-Generated Synthetic Test Data
st.header("Step 5: Synthetic Test Data")
fake = Faker()
if st.button("Generate Patient Data"):
    patient = {
        "patient_id": fake.uuid4(),
        "name": fake.name(),
        "dob": str(fake.date_of_birth(minimum_age=18, maximum_age=90)),
        "insurance_id": fake.bothify(text="INS####"),
        "lab_result": fake.random_element(elements=["Pending","Completed","Failed"])
    }
    st.table(pd.DataFrame([patient]))

# Step 6: Integration Anomaly Detection
st.header("Step 6: Integration Anomaly Detection")
logs = ["API timeout", "Invalid response", "Success", "Success", "Unexpected null"]
if st.button("Detect Anomalies"):
    anomalies = [log for log in logs if log not in ["Success"]]
    st.write("Anomalies found:", anomalies)

# Step 7: Quality Metrics & Continuous Learning
st.header("Step 7: Quality Metrics & Continuous Learning")
coverage = {"Platform API": 90, "Custom Modules": 70, "Integrations": 80}
defect_leakage = [5, 3, 2, 4]
reliability = [95, 97, 93, 98]

fig, ax = plt.subplots()
ax.bar(coverage.keys(), coverage.values(), color=['blue','green','orange'])
ax.set_title("Automation Coverage %")
st.pyplot(fig)

st.subheader("Defect Leakage Trend")
st.line_chart(defect_leakage, height=200, width="stretch")

st.subheader("Integration Reliability")
st.line_chart(reliability, height=200, width="stretch")

if st.button("Retrain Model (Continuous Learning)"):
    st.info("Retraining regression selector with new commit history... (simulated)")
    st.success("Model retrained successfully")
