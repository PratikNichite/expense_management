import streamlit as st
import requests
import pandas as pd
import plotly.express as px

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

    df['date'] = pd.to_datetime(df['date'], format='%Y-%m')
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.strftime('%B')

    # Interactive Line Chart
    fig_line = px.line(
        df,
        x="date",
        y="total",
        title="Monthly Expense Trend",
        labels={"date": "Month", "total": "Expenses (INR)"}
    )
    st.plotly_chart(fig_line)  # Use st.plotly_chart for Plotly charts


    # Interactive Bar Chart
    fig_bar = px.bar(
        df,
        x="month",
        y="total",
        title="Monthly Expenses",
        labels={"month": "Month", "total": "Expenses (INR)"}
    )
    st.plotly_chart(fig_bar)

    st.table(df[["month", "year", "total"]].style.format({"total": "{:.2f}"}))
