import streamlit as st
import requests
from datetime import datetime

def update_expenses_ui(API_URL, categories):
    selected_date = st.date_input("📅 Date", datetime.now(), key="update-expense")
    try:
        response = requests.get(f"{API_URL}/expenses/{selected_date}")
        response.raise_for_status()
        existing_expenses = response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Failed to retrieve expenses: {e}")
        existing_expenses = []
        return

    with st.form(key="update-expenses-form"):
        for i, expense in enumerate(existing_expenses):
            st.subheader(f"Expense {i+1}")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # st.subheader(f"Expense {i+1}")
                amount_input = st.number_input(
                    "Amount",
                    min_value=0.0,
                    step=1.0,
                    value=expense.get("amount", 0.0),
                    key=f"amount_{expense.get('id', i)}",
                    # label_visibility="collapsed"
                )

            with col2:
                # st.subheader("Category")
                category_input = st.selectbox(
                    "Category",
                    options=categories,
                    key=f"category_{expense.get('id', i)}",
                    # label_visibility="collapsed",
                    index=categories.index(expense["category"]) if expense["category"] in categories else 0
                )
            
            with col3:
                notes_input = st.text_input(
                    "Note",
                    value=expense.get("notes", ""),
                    key=f"notes_{expense.get('id', i)}",
                    # label_visibility="collapsed"
                )

            expense["amount"] = amount_input
            expense["notes"] = notes_input
            expense["category"] = category_input

        submit_button = st.form_submit_button("Update Expenses")

        if submit_button:
            try:
                response = requests.patch(f"{API_URL}/expenses/{selected_date}", json=existing_expenses)
                response.raise_for_status()
                st.success("✅ Expenses updated Successfully!")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Failed to update expenses: {e}")

