import streamlit as st
import numpy as np 
import pandas as pd

st.title("BRRR Valuation Calculator")
st.subheader("Assumptions/notes:")
st.write("- This does not account for any bridging loan repayments")
st.write("- There is no deposit for the mortgage post renovation due to ownership")
st.write("- Assumes mortgage post renovation is always 75% LTV")
st.write("- There is no stamp duty due to sole purchase of uninhabitable properties")
st.write("- Additional solicitor/miscellaneous fees may apply")

# Does not account for Birdging Loan repayments

# inputs:
# Property Price
# Initial Investment 
# Bridging Loan
# Renovation Cost
# Value After Renovation  

# 1. Initial Phases:
st.subheader("Please enter the relevant details:")

Property_Price = st.number_input("Property Price (£):", min_value = 0, value = 300000, step= 1000)
Initial_Investment = st.number_input("Initial Investment (£):", min_value = 0, value = 75000, step = 1000)
Bridging_Loan = st.number_input("Bridging Loan Amount (£)", min_value =0, value = 225000, step = 1000)
Renovation_Cost = st.number_input("Renovation Cost (£):", min_value = 0, value = 30000, step = 1000)
Value_After_Renovation =  st.number_input("Property Value after Renovation (£)", min_value = 0, value = 400000, step =1000)

# Mortgage repayments & note to compare to rental income 
# Note Mortgage has 0% deposit

st.title("Post Renovation")

st.subheader("Capital Position")

loan_amount = Value_After_Renovation * 0.75
cash_released = loan_amount - Bridging_Loan
cash_left_in = Initial_Investment - cash_released
equity = Value_After_Renovation - loan_amount
costs = Property_Price + Renovation_Cost
deal_profit = Value_After_Renovation - (Property_Price + Renovation_Cost)
true_gain = equity + cash_released - Initial_Investment
ROI = true_gain / Initial_Investment * 100
net_position = cash_released + equity
cash_position = cash_released - Initial_Investment
st.metric("Value created in the asset (Deal uplift)", f"£{deal_profit:,.2f}") # Value created in asset
st.metric("Cash pulled out from refinancing",f"£{cash_released:,.2f}") # Money recovered from refinancing
st.metric("Your ROI:", f"{ROI:.2f}%")
st.metric("Total position (cash + equity)", f"£{net_position:,.2f}")
st.metric("Cash left in deal", f"£{cash_position:,.2f}")

st.title("Mortgage Repayments")

st.subheader("Inputs")
rent = st.number_input("Rental Income after Renovation (£)", min_value = 0, value = 2000, step = 100)
interest_rate = st.number_input("Annual interest rate (%):", min_value=0.1, value=5.0, step=0.1)
loan_term = st.number_input("Loan term (years):", min_value=1, value=25, step=1)

# Calculations
n = loan_term * 12 # Yearly -> Monthly
i_p = interest_rate/100 # 5% -> 0.05
i = i_p / 12 # Monthly rate 
Discount_factor = 1/(1+i) # Get v
annuity = (1-Discount_factor**n)/i #a_n
premium = loan_amount / annuity # C/a_n

def amount_outstanding(m):
   amount_outstanding = loan_amount-(premium * ((1-Discount_factor**m)/i))
   return amount_outstanding

def interest_paid(m):
    interest_paid = amount_outstanding(m-1)*(i)
    return interest_paid

st.subheader("Results Montly")
st.metric("Monthly payment", f"£{premium:,.2f}")
net_cashflow = rent - premium
st.metric("Monthly Cashflow",f"£{net_cashflow:,.2f}")

st.subheader("Results full term")
# Build full loan schedule 
months = list(range(1, int(n)+1))
outstanding = [amount_outstanding(m) for m in months]
interest = [interest_paid(m) for m in months]
principal = [premium - interest_paid(m) for m in months]

total_interest = sum(interest)
total_repaid = loan_amount + total_interest

st.metric("Total Mortgage Repaid", f"£{total_repaid:,.2f}")
st.metric("Total interest paid", f"£{total_interest:,.2f}")

st.title("Full Schedule of Payments")
schedule = pd.DataFrame({
   "Month": months,
   "Amount Outstanding (£)": [f"{x:,.2f}" for x in outstanding],
   "Interest Paid (£)": [f"{x:,.2f}" for x in interest],
   "Principal Repaid (£)": [f"{x:,.2f}" for x in principal]
})

st.dataframe(schedule) 