import streamlit as st
from datetime import datetime
import requests

API_URL = "http://localhost:8000"

st.title("Expense Tracking System")

tab1, tab2, tab3 = st.tabs(["Add Expense", "Update Expenses", "Analytics"])
categories = ["Rent", "Food", "Shopping", "Entertainment", "Other"]

with tab1:
    selected_date = st.date_input("Date", datetime.now(), key="add-expense")
    with st.form(key="add-expense-form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("Amount")
            amount_input = st.number_input(
                    label="Amount", 
                    min_value=0.0, 
                    step=1.0, 
                    value=0.0, 
                    key="amount",
                    label_visibility="collapsed"
                )
        with col2:
            st.subheader("Category")
            category_input = st.selectbox(
                    label="Category", 
                    options=categories, 
                    key="category", 
                    label_visibility="collapsed",
                )
        with col3:
            st.subheader("Notes")
            notes_input = st.text_input(
                    label="Note", 
                    value="", 
                    key="notes", 
                    label_visibility="collapsed"
                )    
        
        expense = {
            "amount": amount_input,
            "category": category_input,
            "notes": notes_input
        }
        
        submit_button = st.form_submit_button()
        
        if submit_button:
            response = requests.post(f"{API_URL}/expenses/{selected_date}", json=expense)
                
            if response.status_code == 200:
                st.success("Expense added Successfully!")
            else:
                st.error("Failed to add expense!")

with tab2:
    selected_date = st.date_input("Date", datetime.now(), key="update-expense")
    response = requests.get(f"{API_URL}/expenses/{selected_date}")
    if response.status_code == 200:
        existing_expenses = response.json()
        # st.write(existing_expenses)
    else:
        st.error("Failed to retrieve expenses")
        existing_expenses = []
        
    with st.form(key="update-expenses-form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("Amount")
        with col2:
            st.subheader("Category")
        with col3:
            st.subheader("Notes")

        expenses = []
        for i in range(len(existing_expenses)):
            col1, col2, col3 = st.columns(3)
            
            id = existing_expenses[i]["id"] if existing_expenses[i]["id"] else None
            amount = existing_expenses[i]["amount"] if existing_expenses[i]["amount"] else 0.0
            category = categories.index(existing_expenses[i]["category"]) if existing_expenses[i]["category"] else 1
            notes = existing_expenses[i]["notes"] if existing_expenses[i]["notes"] else ""
            
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
                "id": id if id else None,
                "amount": amount_input,
                "category": category_input,
                "notes": notes_input
            })

        submit_button = st.form_submit_button()
        
        if submit_button:
            requests.patch(f"{API_URL}/expenses/{selected_date}", json=expenses)
            
            if response.status_code == 200:
                st.success("Expenses updated Successfully!")
            else:
                st.error("Failed to update expenses!")

with tab2:
    pass