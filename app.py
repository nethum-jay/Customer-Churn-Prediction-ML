import streamlit as st
import pandas as pd
import pickle

# 1. Model eka load karaganna
model = pickle.load(open('trained_model.pkl', 'rb'))

st.title("📊 Customer Churn Prediction App")
st.write("Enter customer details to predict if they will stay or leave.")

# 2. Input fields (Obage dataset eke thiyena columns anuwa mewa wenas wenna ona)
age = st.number_input("Age", min_value=18, max_value=100)
tenure = st.number_input("Tenure (Months)", min_value=0)
usage = st.number_input("Monthly Usage")

# 3. Predict Button
if st.button("Predict"):
    # Input data dataframe ekakata harawa ganna
    input_data = pd.DataFrame([[age, tenure, usage]], columns=['Age', 'Tenure', 'Usage'])
    
    prediction = model.predict(input_data)
    
    if prediction[0] == 1:
        st.error("⚠️ This customer is likely to CHURN (Leave).")
    else:
        st.success("✅ This customer is likely to STAY.")
