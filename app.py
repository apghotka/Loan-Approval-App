import streamlit as st
import pandas as pd
import pickle

# Load your model (ensure this filename matches your .pkl file exactly)
with open('my_model.pkl', 'rb') as f:
    model = pickle.load(f)

st.title("Final Project: Loan Approval Revenue Tool")

# Input sliders and boxes
fico = st.number_input("FICO Score", 300, 850, 700)
income = st.number_input("Monthly Income ($)", value=5000)
loan = st.number_input("Loan Amount ($)", value=15000)
lender = st.selectbox("Select Lender", ["A", "B", "C"])

# Payout logic for the Business Insight requirement
payouts = {"A": 250, "B": 350, "C": 150}

if st.button("Predict"):
    # Note: Ensure these columns match your training data names exactly
    data = pd.DataFrame([[fico, income, loan, lender]], 
                        columns=['FICO_score', 'Monthly_Gross_Income', 'Requested_Loan_Amount', 'Lender'])
    
    prediction = model.predict(data)[0]
    
    if prediction == 1:
        st.success(f"Outcome: APPROVED. Platform Revenue: ${payouts[lender]}")
        # The A+ Insight:
        if lender != "B":
            st.warning("Strategy Tip: Lender B pays $350. Match with B to maximize revenue.")
    else:
        st.error("Outcome: DENIED.")