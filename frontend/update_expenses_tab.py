import streamlit as st
import requests
from datetime import datetime

def update_expenses_ui(API_URL, categories):
    selected_date = st.date_input("📅 Date", datetime.now(), key="update-expense")
    response = requests.get(f"{API_URL}/expenses/{selected_date}")

    if response.status_code == 200:
        existing_expenses = response.json()
    else:
        st.error("❌ Failed to retrieve expenses")
        existing_expenses = []

    with st.form(key="update-expenses-form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("💰 Amount")
        with col2:
            st.subheader("🗂️ Category")
        with col3:
            st.subheader("📝 Notes")

        expenses = []
        for i in range(len(existing_expenses)):
            col1, col2, col3 = st.columns(3)

            id_val = existing_expenses[i].get("id")
            id = id_val if id_val is not None else None

            amount_val = existing_expenses[i].get("amount")
            amount = amount_val if amount_val is not None else 0.0

            category_val = existing_expenses[i].get("category")
            category = categories.index(category_val) if category_val in categories else 0

            notes_val = existing_expenses[i].get("notes")
            notes = notes_val if notes_val is not None else ""

            with col1:
                amount_input = st.number_input(
                    label="Amount",
                    min_value=0.0,
                    step=1.0,
                    value=amount,
                    key=f"amount_{id if id else i}",
                    label_visibility="collapsed"
                )
            with col2:
                category_input = st.selectbox(
                    label="Category",
                    options=categories,
                    key=f"category_{id if id else i}",
                    label_visibility="collapsed",
                    index=category
                )
            with col3:
                notes_input = st.text_input(
                    label="Note",
                    value=notes,
                    key=f"notes_{id if id else i}",
                    label_visibility="collapsed"
                )

            expenses.append({
                "id": id,
                "amount": amount_input,
                "category": category_input,
                "notes": notes_input
            })

        submit_button = st.form_submit_button("Update Expenses")

        if submit_button:
            response = requests.patch(f"{API_URL}/expenses/{selected_date}", json=expenses)

            if response.status_code == 200:
                st.success("✅ Expenses updated Successfully!")
            else:
                st.error("❌ Failed to update expenses!")
