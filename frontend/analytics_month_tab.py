import streamlit as st
import requests
import pandas as pd
import plotly.express as px

def analytics_month_ui(API_URL):
    st.subheader("🗓️ Monthly Expense Breakdown")

    try:
        response = requests.get(f"{API_URL}/month/expenses")
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data)
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Could not fetch analytics! Error: {e}")
        return

    if df.empty:
        st.warning("No monthly expense data available.")
        return

    df['date'] = pd.to_datetime(df['date'], format='%Y-%m')
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.strftime('%B')

    # Summary Metric
    total_last_month = df['total'].iloc[-1] if not df.empty else 0  # Get last month's total
    st.metric("Last Month's Expenses", f"₹{total_last_month:.2f}")

    # Interactive Line Chart
    fig_line = px.line(
        df,
        x="date",
        y="total",
        title="Monthly Expense Trend",
        labels={"date": "Month", "total": "Expenses (INR)"}
    )
    st.plotly_chart(fig_line, use_container_width=True)

    # Interactive Bar Chart
    fig_bar = px.bar(
        df,
        x="month",
        y="total",
        title="Monthly Expenses",
        labels={"month": "Month", "total": "Expenses (INR)"}
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # Compact Table Display
    st.write("Monthly Expense Details:")
    st.dataframe(df[["month", "year", "total"]].style.format({"total": "{:.2f}"}))
