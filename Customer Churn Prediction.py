import streamlit as st
import pickle
import numpy as np

st.set_page_config(page_title="Customer Churn Predictor", page_icon="📊", layout="wide")

st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_resource
def load_model():
    with open("trained_model.pkl", "rb") as f:
        return pickle.load(f)

model = load_model()

gender_map = {'Female': 0, 'Male': 1}
location_map = {"Illinois": 0, "California": 1, "Florida": 2, "New York": 3, "Texas": 4}
sub_type_map = {"Basic": 0, "Premium": 1, "Enterprise": 2}
last_interaction_map = {"Neutral": 0, "Negative": 1, "Positive": 2}

st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3121/3121800.png", width=100)
st.sidebar.title("About Project")

st.title("📊 Customer Churn Prediction System")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("👤 Personal Details")
    age = st.slider("Age", 18, 80, 30)
    gender = st.radio("Gender", list(gender_map.keys()), horizontal=True)
    location = st.selectbox("Location", list(location_map.keys()))
    satisfaction_score = st.select_slider("Satisfaction Score", options=range(1, 11), value=5)

with col2:
    st.subheader("💳 Subscription Details")
    subscription_type = st.selectbox("Subscription Type", list(sub_type_map.keys()))
    monthly_spending = st.number_input("Monthly Spending ($)", 10.0, 200.0, 50.0)
    account_age_months = st.number_input("Account Age (Months)", 1, 60, 12)
    promo_opted_in = st.checkbox("Promo Opted In")

st.markdown("---")
st.subheader("📈 Usage & Interaction")
c1, c2, c3 = st.columns(3)

with c1:
    total_usage_hours = st.number_input("Total Usage Hours", 10, 500, 100)
    support_calls = st.number_input("Support Calls", 0, 10, 1)
with c2:
    late_payments = st.number_input("Late Payments", 0, 5, 0)
    streaming_usage = st.number_input("Streaming Usage (%)", 0, 100, 20)
with c3:
    last_interaction_type = st.selectbox("Last Interaction", list(last_interaction_map.keys()))
    complaint_tickets = st.number_input("Complaint Tickets", 0, 5, 0)

st.markdown("<br>", unsafe_allow_html=True)
if st.button("🚀 Analyze Customer Churn"):
    input_row = [
        age, gender_map[gender], location_map[location], sub_type_map[subscription_type],
        account_age_months, monthly_spending, total_usage_hours, support_calls,
        late_payments, streaming_usage, 0, satisfaction_score,
        last_interaction_map[last_interaction_type], complaint_tickets, int(promo_opted_in)
    ]

    pred = model.predict(np.array([input_row]))[0]

    st.markdown("### Result:")
    if pred == 1:
        st.error("⚠️ **Prediction: High Risk!** The customer is likely to **Churn**.")
    else:
        st.success("✅ **Prediction: Safe!** The customer is likely to **Stay**.")

# streamlit run "C:\My Data\ICBT - TOP-UP\Repete - 2\CIS 6005 - Computational Intelligence\Assignment\BSc_SE_CIS_6005_20242847\Chunrn_UI\Customer Churn Prediction.py"