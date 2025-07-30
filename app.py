import streamlit as st
import pandas as pd
import joblib
from PIL import Image


# Configure page settings
st.set_page_config(
    page_title="Salary Estimation Tool",
    layout="centered",
    initial_sidebar_state="auto"
)


# Custom CSS styles for theming and layout
st.markdown("""
<style>
/* Background and text colors */
.main {
    background-color: #22272B;
    color: #F0F0F0;
}

/* Primary heading */
.heading {
    color: #82AAFF;
    font-size: 28px;
    font-weight: 700;
    text-align: center;
    margin-bottom: 25px;
}

/* Secondary heading */
.subheading {
    color: #B0B9C1;
    font-size: 20px;
    font-weight: 600;
    margin-top: 35px;
    margin-bottom: 15px;
}

/* Information panel */
.info-panel {
    background-color: #2E3B4E;
    border-left: 5px solid #4A90E2;
    padding: 18px;
    border-radius: 8px;
    font-size: 15px;
    line-height: 1.5;
    color: #D9DCDC;
    margin-bottom: 28px;
}

/* Inputs styling */
.stNumberInput input, .stSelectbox div[data-baseweb="select"] {
    background-color: #374151;
    color: #ECEFF4;
    border-radius: 5px;
    border: 1px solid #475569;
}
.stSelectbox div[data-baseweb="select"] > div {
    color: #ECEFF4;
}

/* Button container */
.button-center {
    display: flex;
    justify-content: center;
    margin-top: 22px;
}
.stButton>button {
    background-color: #4A90E2;
    color: #FFFFFF;
    padding: 11px 28px;
    border-radius: 9px;
    font-weight: 600;
    font-size: 16px;
    border: none;
}
.stButton>button:hover {
    background-color: #6BA3F2;
}

/* Output box */
.output-box {
    background-color: #357ABD;
    color: white;
    padding: 28px;
    font-size: 20px;
    font-weight: 700;
    text-align: center;
    border-radius: 10px;
    margin-top: 28px;
    line-height: 1.5;
}
.output-box small {
    color: #C4D2E0;
    font-size: 13px;
    text-align: left;
    display: block;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)


# Load the trained model and utilities
saved_data = joblib.load("salary_predictor.pkl")
regressor_model = saved_data["model"]
encoders = saved_data["label_encoders"]
data_scaler = saved_data["scaler"]
features = saved_data["feature_names"]


# Load model evaluation image asset
evaluation_image = Image.open("plot.png")


# Display main app title
st.markdown('<div class="heading">💼 Salary Estimation Tool</div>', unsafe_allow_html=True)


# Display info panel about the model
st.markdown(f"""
<div class="info-panel">
    <strong>⚙️ Model Used:</strong> XGBoost Regression <br>
    <strong>📊 Performance Metric (R²):</strong> 94.58% <br>
    <strong>📈 Overview:</strong> Visualises predicted vs actual salaries.
</div>
""", unsafe_allow_html=True)


# Section for user input
st.markdown('<div class="subheading">📝 Provide Employee Details</div>', unsafe_allow_html=True)


# Form for collecting inputs
with st.form("income_form"):
    employee_age = st.number_input("Age (years)", min_value=18, max_value=80, value=30)
    employee_gender = st.selectbox("Gender", options=encoders["Gender"].classes_)
    employee_education = st.selectbox("Education Level", options=encoders["Education Level"].classes_)
    employee_job = st.selectbox("Job Role", options=encoders["Job Title"].classes_)
    experience_years = st.number_input("Years of Work Experience", min_value=0, max_value=40, value=5)

    st.markdown('<div class="button-center">', unsafe_allow_html=True)
    submit_clicked = st.form_submit_button("Calculate Salary")
    st.markdown('</div>', unsafe_allow_html=True)


# Process prediction on form submit
if submit_clicked:
    user_input = pd.DataFrame({
        "Age": [employee_age],
        "Gender": [employee_gender],
        "Education Level": [employee_education],
        "Job Title": [employee_job],
        "Years of Experience": [experience_years]
    })

    for category in ["Gender", "Education Level", "Job Title"]:
        user_input[category] = encoders[category].transform(user_input[category])

    scaled_input = data_scaler.transform(user_input)
    projected_salary = regressor_model.predict(scaled_input)[0]

    # Display salary output
    st.markdown(f"""
    <div class="output-box">
        💰 <strong>Projected Annual Salary:</strong><br>
        USD ${projected_salary:,.2f}<br>
        <small>⚠️ Based on inputs and model training data.<br>📉 Actual pay may differ due to market factors.</small>
    </div>
    """, unsafe_allow_html=True)


# Display model evaluation section
st.markdown('<div class="subheading">📉 Model Evaluation Chart</div>', unsafe_allow_html=True)
st.image(evaluation_image, caption="Predicted vs Actual Salary Comparison", use_container_width=True)
