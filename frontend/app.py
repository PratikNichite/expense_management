import streamlit as st
from add_epense_tab import add_expense_ui
from update_expenses_tab import update_expenses_ui
from analytics_tab import analytics_ui

API_URL = "http://localhost:8000"

st.title("Expense Tracking System")

tab1, tab2, tab3, tab4 = st.tabs(["Add Expense", "Update Expenses", "Analytics (Category)", "Analytics (Month)"])
categories = ["Rent", "Food", "Shopping", "Entertainment", "Other"]

with tab1:
    add_expense_ui(API_URL, categories)

with tab2:
    update_expenses_ui(API_URL, categories)

with tab3:
    analytics_ui()

with tab4:
    analytics_month_ui()