import streamlit as st
import pandas as pd
import pickle

# 1. Load the model
with open('my_model.pkl', 'rb') as f:
    model = pickle.load(f)

st.title("🏦 Loan Approval & Revenue Optimization")

# 2. Inputs
fico = st.number_input("FICO Score", 300, 850, 700)
income = st.number_input("Monthly Income ($)", value=5000)
loan = st.number_input("Loan Amount ($)", value=15000)
housing = st.number_input("Monthly Housing Payment ($)", value=1200)
lender_name = st.selectbox("Select Lender", ["A", "B", "C"])

# 3. THE FIX: Map names to numbers (Standard encoding: A=0, B=1, C=2)
# Change these numbers if your notebook used a different order!
lender_map = {"A": 0, "B": 1, "C": 2}
lender_numeric = lender_map[lender_name]

# 4. Payout Logic
payouts = {"A": 250, "B": 350, "C": 150}

if st.button("Predict Approval"):
    # 5. Create Dataframe using the NUMERIC lender value
    data = pd.DataFrame([[fico, income, loan, housing, lender_numeric]], 
                        columns=['FICO_score', 'Monthly_Gross_Income', 'Requested_Loan_Amount', 'Monthly_Housing_Payment', 'Lender'])
    
    try:
        prediction = model.predict(data)[0]
        
        if prediction == 1:
            st.success(f"Outcome: APPROVED. Platform Revenue: ${payouts[lender_name]}")
            if lender_name != "B":
                st.info(f"Strategy Tip: Switching to Lender B would increase payout to $350.")
        else:
            st.error("Outcome: DENIED")
    except Exception as e:
        st.error(f"Model Error: {e}. Check if your input columns match your training data exactly.")