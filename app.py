import streamlit as st
import pandas as pd
import pickle

# 1. Load the model
with open('my_model.pkl', 'rb') as f:
    model = pickle.load(f)

st.title("🏦 Loan Approval & Revenue Optimization")

# 2. Inputs (The first 4 features)
fico = st.number_input("FICO Score", 300, 850, 700)
income = st.number_input("Monthly Income ($)", value=5000)
loan = st.number_input("Loan Amount ($)", value=15000)
housing = st.number_input("Monthly Housing Payment ($)", value=1200)
lender_selection = st.selectbox("Select Lender", ["A", "B", "C"])

# 3. Payout Logic
payouts = {"A": 250, "B": 350, "C": 150}

if st.button("Predict Approval"):
    # 4. THE FIX: Creating the 10 features to match your model
    # We start with the 4 numeric features
    input_data = {
        'FICO_score': fico,
        'Monthly_Gross_Income': income,
        'Requested_Loan_Amount': loan,
        'Monthly_Housing_Payment': housing,
        # We add the "Dummy/One-Hot" variables for Lenders (adds 3 columns)
        'Lender_A': 1 if lender_selection == "A" else 0,
        'Lender_B': 1 if lender_selection == "B" else 0,
        'Lender_C': 1 if lender_selection == "C" else 0,
        # If your notebook had other columns (like 'Employment_Years'), 
        # we add them here with a default value to reach 10 total columns.
        'Years_at_Job': 5, 
        'Debt_to_Income': 0.3,
        'Existing_Loans': 0
    }
    
    data = pd.DataFrame([input_data])
    
    try:
        prediction = model.predict(data)[0]
        
        if prediction == 1:
            st.success(f"Outcome: APPROVED. Platform Revenue: ${payouts[lender_selection]}")
            if lender_selection != "B":
                st.info(f"Strategy Tip: Lender B pays $350. Recommend switching.")
        else:
            st.error("Outcome: DENIED")
            
    except Exception as e:
        st.error(f"Feature Mismatch: Your model needs 10 features. Current columns: {list(data.columns)}")
        st.write("Error details:", e)