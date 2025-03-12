import streamlit as st
import requests
import pandas as pd



def analytics_month_ui(API_URL):
    st.subheader("Expense Breakdown By Category")
    
    response = requests.get(f"{API_URL}/month/expenses")
    
    if response.status_code == 200:    
        data = response.json()
        df = pd.DataFrame(data)
    else:
        st.error("Could not fetch analytics!")
        df = pd.DataFrame({
                "month": [],
                "total": [],
            })
    
    st.bar_chart(
        data=df[["month", "total"]].set_index("month"),
        x_label="Month",
        y_label="Expenses (INR)",
    )
    
    
    st.table(df.style.format({"total": "{:.2f}"}))