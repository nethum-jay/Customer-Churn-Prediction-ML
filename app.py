import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Model eka load karaganna (Meka repository ekata upload karala thiyenna ona)
try:
    model = pickle.load(open('churn_model.pkl', 'rb'))
except FileNotFoundError:
    st.error("Model file (churn_model.pkl) not found. Please upload it to GitHub.")

st.title("📉 Customer Churn Prediction App")
st.write("Predict if a customer will leave the service based on their profile.")

# Input Form
with st.form("prediction_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        gender = st.selectbox("Gender", ["Male", "Female"])
        senior = st.selectbox("Senior Citizen", ["No", "Yes"])
        tenure = st.number_input("Tenure (Months)", min_value=0, max_value=100, value=1)
        
    with col2:
        internet = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
        contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
        monthly = st.number_input("Monthly Charges ($)", min_value=0.0, value=50.0)
        total = st.number_input("Total Charges ($)", min_value=0.0, value=50.0)

    submit = st.form_submit_button("Predict Churn")

if submit:
    # Input data transform karaganna (Obage notebook eke thiyena encoding walata anuwa)
    # Gender: Male=1, Female=0 | Senior: Yes=1, No=0
    input_df = pd.DataFrame([{
        'gender': 1 if gender == "Male" else 0,
        'SeniorCitizen': 1 if senior == "Yes" else 0,
        'tenure': tenure,
        'InternetService': 1 if internet == "Fiber optic" else (0 if internet == "DSL" else 2),
        'Contract': 0 if contract == "Month-to-month" else (1 if contract == "One year" else 2),
        'MonthlyCharges': monthly,
        'TotalCharges': total
    }])

    prediction = model.predict(input_df)
    
    if prediction[0] == 1:
        st.error("⚠️ The customer is likely to CHURN.")
    else:
        st.success("✅ The customer is likely to STAY.")
