import streamlit as st
from datetime import datetime
import requests

def add_expense_ui(API_URL, categories):
    selected_date = st.date_input("📅 Date", datetime.now(), key="add-expense")

    with st.form(key="add-expense-form"):
        col1, col2 = st.columns(2)  # Reduce to 2 columns

        with col1:
            st.subheader("💰 Amount")
            amount_input = st.number_input(
                label="Amount",
                min_value=0.0,
                step=1.0,
                value=0.0,
                key="amount",
                label_visibility="collapsed"
            )

            st.subheader("📝 Notes")  # Move Notes to the same column
            notes_input = st.text_input(
                label="Note",
                value="",
                key="notes",
                label_visibility="collapsed"
            )

        with col2:
            st.subheader("🗂️ Category")
            category_input = st.selectbox(
                label="Category",
                options=categories,
                key="category",
                label_visibility="collapsed",
            )

        expense = {
            "amount": amount_input,
            "category": category_input,
            "notes": notes_input
        }

        submit_button = st.form_submit_button("Add Expense")

        if submit_button:
            try:
                response = requests.post(f"{API_URL}/expenses/{selected_date}", json=expense)
                response.raise_for_status()
                st.success("✅ Expense added Successfully!")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Failed to add expense: {e}")

