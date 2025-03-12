import streamlit as st
import requests
import pandas as pd

def analytics_month_ui(API_URL):
    st.subheader("🗓️ Monthly Expense Breakdown")

    response = requests.get(f"{API_URL}/month/expenses")

    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
    else:
        st.error("❌ Could not fetch analytics!")
        df = pd.DataFrame({
            "date": [],
            "year": [],
            "month": [],
            "total": [],
        })

    st.bar_chart(
        data=df[["date", "total"]].set_index("date"),
        x_label="Month",
        y_label="Expenses (INR)",
    )

    df['date'] = pd.to_datetime(df['date'], format='%Y-%m')
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.strftime('%B')

    st.table(df[["month", "year", "total"]].style.format({"total": "{:.2f}"}))
