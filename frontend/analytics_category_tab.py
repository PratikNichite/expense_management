import streamlit as st
from datetime import datetime, date
import pandas as pd
import requests
import plotly.express as px

def analytics_category_ui(API_URL):
    st.subheader("📊 Expense Breakdown By Category")

    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input("📅 Start date", value=date(2024, 8, 1))

    with col2:
        end_date = st.date_input("📅 End date", value=date.today())

    button = st.button("Get Analytics")

    if button:

        user_inputs = {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        }

        try:
            response = requests.post(f"{API_URL}/category/expenses/", json=user_inputs)
            response.raise_for_status()
            data = response.json()
            df = pd.DataFrame(data)
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Could not fetch analytics! Error: {e}")
            return

        if df.empty:
            st.warning("No category data available for the selected period.")
            return

        # Calculate Total Expenses
        total_expenses = df['total'].sum()
        st.metric("Total Expenses", f"₹{total_expenses:.2f}")

        # Pie Chart
        fig_pie = px.pie(
            df,
            values="percentage",
            names="category",
            title="Expense Distribution by Category",
        )
        st.plotly_chart(fig_pie, use_container_width=True)

        # Bar Chart
        fig_bar = px.bar(
            df,
            x="percentage",
            y="category",
            orientation='h',
            title="Expenses by Category",
            labels={"percentage": "Total Expenses (%)", "category": "Expense Category"}
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        st.dataframe(df.style.format({"total": "{:.2f}", "percentage": "{:.2f}"}))
